from django.db import models


# Create your models here.


class ClassModel(models.Model):
    class_number = models.IntegerField()  # This is the 5 digit unique class ID. Ex: 15927
    class_mnemonic = models.CharField()
    course_number = models.IntegerField()  # This is the 4 digit course number, but is not specific to section Ex: 3240
    class_section = models.IntegerField()
    class_type = models.CharField()
    class_units = models.IntegerField()
    class_instructor = models.CharField()
    class_days = models.DateTimeField()
    class_room = models.CharField()
    class_title = models.CharField()
    class_topic = models.CharField()
    class_status = models.CharField()
    class_enrollment = models.IntegerField()
    class_enrollment_limit = models.IntegerField()
    class_waitlist = models.IntegerField()
    # TODO: Make this refer to an instance of ClassModel
    # class_combined_with = models.ForeignKey(object.__class__)
    class_description = models.CharField()

    def __str__(self):
        return str(self.class_number)

