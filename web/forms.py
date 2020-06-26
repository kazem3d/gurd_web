from django import forms

class CommentForm(forms.Form):
    content=forms.CharField(label='متن', widget=forms.Textarea(attrs={"rows":5, "cols":100}))
    