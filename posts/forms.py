from django import forms
from .models import Post
class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)
    content.widget.attrs.update({'class' : 'form-control'})
    class Meta:
        model = Post
        fields = ['content', 'user', 'politician',]
