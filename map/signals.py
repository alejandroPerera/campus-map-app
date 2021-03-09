from map.models import ClassModel
from django.dispatch import receiver
from django.db.backends.signals import connection_created
import csv


@receiver(connection_created)
def update_classes(sender, **kwargs):
    """ Called when the database is first connected. Moves all the data in the
    csv into the database if it isn't there already
    """

    print("Updating SIS data")
    # If there isn't any data in the table we need to update it
    if not ClassModel.objects.all().exists():
        # Read in the csv.
        with open(file='map/static/map/searchData.csv', newline='') as sis_data:
            reader = csv.reader(sis_data, delimiter=',')
            reader.__next__()  # Move past the header line
            for row in reader:
                # create the database entry
                entry = ClassModel(
                    class_number=row[0],  # This is the 5 digit unique class ID. Ex: 15927
                    class_mnemonic=row[1],
                    course_number=row[2],  # This is the 4 digit course number, but is not specific to section Ex: 3240
                    class_section=row[3],
                    class_type=row[4],
                    class_units=row[5],
                    class_instructor=row[6],
                    class_days=row[7],
                    class_room=row[8],
                    class_title=row[9],
                    class_topic=row[10],
                    class_status=row[11],
                    class_enrollment=row[12],
                    class_enrollment_limit=row[13],
                    class_waitlist=row[14],
                    # class_combined_with=row[15],
                    class_description=row[16],
                )
                # Add the row to the database
                entry.save()
    # The data is already in the database
    else:
        print("SIS data up to date")
