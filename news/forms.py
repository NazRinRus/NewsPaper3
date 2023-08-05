from django.core.exceptions import NON_FIELD_ERRORS
from django import forms
from .models import Post
class PostForm(forms.ModelForm):
   class Meta:
       error_messages = {
           NON_FIELD_ERRORS: {
               'unique_together': "%(model_name)s's %(field_labels)s are not unique.",
           }
       }
       model = Post
       fields = [
           'author',
           'category',
           'header',
           'text_post',
       ]