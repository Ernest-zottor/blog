from dataclasses import field
import imp
from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


# This is how to build forms from models
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('name','email', 'body') # This specifies what fields on the model that we want to use "exclude filed will exclude some fileds"
