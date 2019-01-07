from django.db import models


class Certificate(models.Model):
    name = models.CharField(max_length=1000, default="Ivan Pupkin")
    course = models.CharField(max_length=1000, default="Python for Data Science")
    date = models.DateField(default="2019-01-01")
    mark = models.CharField(max_length=1000, default="Excellent")
    permanent_link = models.CharField(max_length=1000, default="AUTO")

    def __str__(self):
        return self.name + " " + self.course
