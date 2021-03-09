from django.db import models


# Create your models here.


class ClassModel(models.Model):
    class_number = models.IntegerField()  # This is the 5 digit unique class ID. Ex: 15927
    class_mnemonic = models.CharField(max_length=200)
    course_number = models.IntegerField()  # This is the 4 digit course number, but is not specific to section Ex: 3240
    class_section = models.IntegerField()
    class_type = models.CharField(max_length=200)
    class_units = models.FloatField()
    class_instructor = models.CharField(max_length=200)
    class_days = models.CharField(max_length=100)  # TODO: This will need to be more complicated to store up to 3 durations
    class_room = models.CharField(max_length=200)
    class_title = models.CharField(max_length=200)
    class_topic = models.CharField(max_length=200)
    class_status = models.CharField(max_length=200)
    class_enrollment = models.IntegerField()
    class_enrollment_limit = models.IntegerField()
    class_waitlist = models.IntegerField()
    # TODO: Make this refer to an instance of ClassModel
    # class_combined_with = models.ForeignKey(object.__class__)
    class_description = models.CharField(max_length=2000)

    def __str__(self):
        return str(self.class_number)

