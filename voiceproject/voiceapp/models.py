from django.db import models


class AudioRecord(models.Model):
    phonenumber = models.CharField(max_length=15)
    audio = models.FileField(upload_to='audio/')

    class Meta:
        db_table='mytable'


