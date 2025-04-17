from django import forms 


class SearchForm(forms.Form):
    query = forms.CharField(label='поиск', max_length=100)