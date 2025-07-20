from dataclasses import field
from django import forms
from post.models import Post, post_save

class NewPostForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Caption'}), required=True)
    tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tags | Seperate with comma'}), required=True)

    class Meta:
        model = Post
        fields = ['picture', 'caption', 'tag']
