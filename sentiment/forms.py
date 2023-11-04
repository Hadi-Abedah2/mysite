from django import forms

class SentimentForm(forms.Form):
    text = forms.CharField(
        label="Enter your text here",
        widget=forms.TextInput(attrs={'placeholder': 'I love python programming...'}),
        required=True
    )