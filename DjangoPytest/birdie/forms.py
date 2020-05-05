from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    """Form definition for Post."""

    class Meta:
        """Meta definition for Postform."""

        model = Post
        fields  = ('body',)
    
    def clean_body(self):
        body = self.cleaned_data.get('body')
        
        if len(body)<=5:
               raise forms.ValidationError('Message too short')
         # TODO Validation
    
        return body
