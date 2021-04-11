from map.models import ClassModel
from django.dispatch import receiver
from django.db.backends.signals import connection_created
import csv
from sys import argv


@receiver(connection_created)
def add_classes(sender, **kwargs):
    """
    Called when the database is first connected. Moves all the data in the
    csv into the database if it isn't there already
    """
    # Only update the database if we are running the server
    if argv[1].__eq__("makemigrations") or argv[1].__eq__("migrate") or argv[1].__eq__("test"):
        print("Database not updated")
        return

    print("Updating SIS data")
    # If there isn't any data in the table we need to update it
    # TODO: Change this to if the table is not as long as the .csv file, but make it efficient...
    if not ClassModel.objects.all().exists():
        # Value to count how many were updated
        # So there is more to log
        num_updated = 0
        # Read in the csv.
        with open(file='map/static/map/searchData.csv', newline='') as sis_data:
            reader = csv.reader(sis_data, delimiter=',')
            reader.__next__()  # Move past the header line
            rows = list(reader)

            # First pass adds all the classes
            for row in rows:
                # TODO: Change these if it means something important
                # For some reason graduate studies seem to have dates coded instead of units
                # So just make them 0 units?
                units = row[5]
                if str(units).__contains__('/') or str(units).__contains__('-'):
                    units = 0

                # Similarly, some sections are labeled "ROS" or "CHO"
                # No idea what it means, but messes up our table >:(
                section = row[3]
                try:
                    section = int(section)
                except ValueError:
                    section = -1

                # create the database entry
                entry = ClassModel(
                    class_number=row[0],  # This is the 5 digit unique class ID. Ex: 15927
                    class_mnemonic=row[1],
                    course_number=row[2],  # This is the 4 digit course number, but is not specific to section Ex: 3240
                    class_section=section,
                    class_type=row[4],
                    class_units=units,
                    class_instructor=row[6],
                    class_days=row[7],
                    class_room=row[8],
                    class_title=row[9],
                    class_topic=row[10],
                    class_status=row[11],
                    class_enrollment=row[12],
                    class_enrollment_limit=row[13],
                    class_waitlist=row[14],
                    # class_combined_with=ClassModel(None),
                    class_description=row[16],
                )
                # Add the row to the database
                entry.save()
                num_updated += 1

            '''
            # Second pass updates the combined with field
            for row in rows:
                combined_with = row[15]
                current_class = ClassModel.objects.get(class_number=row[0])

                if len(combined_with) > 0:
                    for thing in combined_with.split(','):
                        components = thing.split("^ [a-zA-Z]+ [0-9]+-[0-9]+$")  # split on space and dash
                        dept = components[0]
                        course = components[1]
                        section = components[2]
                        # Makes this consistent with what would be in the table
                        try:
                            section = int(section)
                        except ValueError:
                            section = -1

                        model = ClassModel.objects.get(class_mnemonic=dept, course_number=course, class_section=section)
                        # add that model to the row
                        current_class.class_combined_with.add(model)
                        current_class.save()
            '''
            print("Updated %i entries" % num_updated)
    # The data is already in the database
    else:
        print("SIS data up to date")
