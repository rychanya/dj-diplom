from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    next = forms.CharField()


class SigInUpForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField()
    next = forms.CharField()


class AddToCartForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())


class OderForm(forms.Form):
    cart_id = forms.IntegerField(widget=forms.HiddenInput())


class ReviewForm(forms.Form):
    rating_choices = [(n, n) for n in range(1, 6)]

    product = forms.IntegerField(widget=forms.HiddenInput())
    user = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea())
    rating = forms.IntegerField(widget=forms.RadioSelect(choices=rating_choices))
