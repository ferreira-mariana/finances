from django.db import models

import datetime

class AccountEntry(models.Model):
    EntryType = (
        ('in', 'income'),
        ('out', 'expense')
    )
    name = models.CharField(max_length=50)
    amount = models.FloatField()
    category = models.CharField(max_length=20, default='Other')
    date = models.DateField()
    entry_type = models.CharField(choices=EntryType, max_length=10)

    def __str__(self):
        return self.name


# django gerou como account entrys em vez de account entries 