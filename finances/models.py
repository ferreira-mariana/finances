from django.db import models
import datetime

class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    category = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.name

    def was_spent_recently(self):
        return self.date >= datetime.date.today() - datetime.timedelta(days=7)

class Income(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    category = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.name