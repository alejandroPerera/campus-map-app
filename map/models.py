from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class ClassModel(models.Model):
    class_number = models.IntegerField()  # This is the 5 digit unique class ID. Ex: 15927
    class_mnemonic = models.CharField(max_length=200)
    course_number = models.IntegerField()  # This is the 4 digit course number, but is not specific to section Ex: 3240
    #somehow concatenate mnemonic and number
    class_section = models.IntegerField()
    class_type = models.CharField(max_length=200)
    class_units = models.FloatField()
    class_instructor = models.CharField(max_length=200)
    class_days = models.CharField(max_length=100)  # This just stores this as a string
    class_room = models.CharField(max_length=200)
    class_title = models.CharField(max_length=200)
    class_topic = models.CharField(max_length=200)
    class_status = models.CharField(max_length=200)
    class_enrollment = models.IntegerField()
    class_enrollment_limit = models.IntegerField()
    class_waitlist = models.IntegerField()

    # TODO: Make this refer to an instance of ClassModel
    # class_combined_with = models.ForeignKey("ClassModel", on_delete=models.PROTECT, blank=True, null=True)
    class_description = models.CharField(max_length=2000)
    # Has-many relationship
    user = models.ManyToManyField(User, related_name='schedule')

    def __str__(self):
        return str(self.class_mnemonic) + " " + str(self.course_number) + "-" + str(self.class_section)

    def __eq__(self, other):
        return self.class_number == other.class_number

    def __ne__(self, other):
        return not self.__eq__(other)


class EventModel(models.Model):
    title = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    location = models.CharField(max_length=200)
    date = models.DateTimeField(help_text='In the form MM/DD/YY hh:mm')
    # startTime = models.TimeField()
    # endTime = models.TimeField(default=)
    description = models.CharField(max_length=200, blank=True)
    host = models.ForeignKey(User, on_delete=models.PROTECT, related_name='host', null=True, default=None)
    attendees = models.ManyToManyField(User, related_name='attendees', default=None)
    numberOfAttendees = models.PositiveIntegerField(default=0)


