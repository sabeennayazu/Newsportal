from django import forms
from newspaper.models import  Comment, Contact, NewsLetter


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post','content']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields ='__all__'

        
class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsLetter
        fields = "__all__"

       
