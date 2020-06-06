from django.db import models
from enum import Enum

import datetime

class AccountEntry(models.Model):
    EntryType = (
        ('in', 'income'),
        ('out', 'expense')
    )
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    category = models.CharField(max_length=100, default='other')
    date = models.DateField()
    entry_type = models.CharField(choices=EntryType, max_length=10)

    def __str__(self):
        return self.name

    def was_spent_recently(self):
        return self.date >= datetime.date.today() - datetime.timedelta(days=7)

# django gerou como account entrys em vez de account entries 