from django import forms

class NameForm(forms.Form):
    reltag = forms.CharField

class MyForm(forms.Form):
    next10 = forms.CharField

class NameForm2(forms.Form):
    inputtag = forms.CharField(label='inputtag', max_length=20)