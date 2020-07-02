from django import forms

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    next = forms.CharField()

class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    
