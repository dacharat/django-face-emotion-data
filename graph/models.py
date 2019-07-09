from django.contrib.postgres.fields import ArrayField
from django.db import models

class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    face = models.CharField(max_length=200)
    emotion_detail = ArrayField(models.TextField())

    def __str__(self):
        return self.face

class TestPerson(models.Model):
    face = models.CharField(max_length=200)
    emotion_detail = ArrayField(models.TextField())
    face_image = ArrayField(models.TextField())

    class Meta:
        managed = True
        db_table = 'test_person'
