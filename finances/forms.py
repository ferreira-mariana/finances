from django import forms

class AddNewEntry(forms.Form):
    EntryType = (
        ('in', 'income'),
        ('out', 'expense')
    )
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-input'}), help_text='Describe your expense or your income.', max_length=100)
    amount = forms.FloatField(widget=forms.NumberInput(attrs={'class' : 'form-input'}), min_value=0.01)
    category = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-input'}), max_length=100)
    date = forms.DateField(widget=forms.DateInput(attrs={'class' : 'form-input'}), help_text='Use this date format YYYY-MM-DD.')
    entry_type = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class' : 'radio-input'}), choices=EntryType)

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
