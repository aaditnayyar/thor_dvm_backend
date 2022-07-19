from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm):
	body = forms.CharField(
		label = '',
		widget = forms.Textarea(attrs={
			'rows':3,
			'placeholder': 'Body...',
			}))
	class Meta:
		model = Post
		fields = ['body']

class CommentForm(forms.ModelForm):
	body = forms.CharField(
		label = '',
		widget = forms.Textarea(attrs={
			'rows':1,
			'placeholder': 'Add a Comment...',
			}))

	class Meta:
		model = Comment
		fields = ['body']