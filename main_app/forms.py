
from django.forms import ModelForm
from .models import Item, Comment

class ItemForm(ModelForm):
  class Meta:
    model = Item
    fields = '__all__'

class CommentForm(ModelForm):
  class Meta:
    model = Comment
    fields = ['text']

