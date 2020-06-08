from django import forms

class AddNewEntry(forms.Form):
    EntryType = (
        ('in', 'income'),
        ('out', 'expense')
    )
    name = forms.CharField(help_text='Describe your expense or your income.', max_length=100)
    amount = forms.FloatField(min_value=0.01)
    category = forms.CharField(max_length=100)
    date = forms.DateField()
    entry_type = forms.ChoiceField(widget=forms.RadioSelect, choices=EntryType)
