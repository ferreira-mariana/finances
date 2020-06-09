from django import forms

class AddNewEntry(forms.Form):
    EntryType = (
        ('in', 'income'),
        ('out', 'expense')
    )
    name = forms.CharField(help_text='Describe your expense or your income.', max_length=100)
    amount = forms.FloatField(min_value=0.01)
    category = forms.CharField(max_length=100)
    date = forms.DateField(help_text='Use this date format 2020-01-01.')
    entry_type = forms.ChoiceField(widget=forms.RadioSelect, choices=EntryType)

    def clean(self):
        super(AddNewEntry, self).clean() # data from the form is fetched using super function 
        name = self.cleaned_data.get('name')
        amount = self.cleaned_data.get('amount')
        category = self.cleaned_data.get('category')
        date = self.cleaned_data.get('date')
        entry_type = self.cleaned_data.get('entry_type')

        if len( str(amount).split('.')[-1] ) > 2 : #if has more than 2 decimals
            self._errors['amount'] = self.error_class(['Maximum of 2 decimals places'])

        return self.cleaned_data
