from django.db import models

class Resume(models.Model):
    # pdf = models.FileField(upload_to='pdfs', null=True)
    photos = models.ImageField(upload_to='photos')


class Csv(models.Model):
    csv = models.FileField(upload_to='csvs')