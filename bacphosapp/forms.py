from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    username = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'User Name'}))
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    password1 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))
    password2 = forms.CharField(label="", widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}))
    first_name = forms.CharField(label="", max_length=90, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=90, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    institution_name = forms.CharField(label="", max_length=90, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Institution name'}))
    country = forms.CharField(label="", max_length=90, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'institution_name', 'country')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].label = ''
        self.fields['username'].help_text = ''
        
        self.fields['email'].label = ''
        self.fields['email'].help_text = ''

        self.fields['password1'].label = ''
        self.fields['password1'].help_text = ''

        self.fields['password2'].label = ''
        self.fields['password2'].help_text = ''

class ContactForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}))
    email = forms.EmailField(label="Email", max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}))
    content = forms.CharField(label="Message", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message'}))

class ProteinSearchForm(forms.Form):
    
    MODIFICATION_CHOICES = (
        ('', 'Any'),  
        ('Y', 'Y'),
        ('H', 'H'),
        ('S', 'S'),
        ('T', 'T'),
    )

    uniprot_code = forms.CharField(required=False, max_length=20, label="UniprotID", widget=forms.TextInput(attrs={"class": "form-item", "placeholder": "Enter Uniprot ID"}))
    gene_name = forms.CharField(required=False, max_length=50, label="Gene Name", widget=forms.TextInput(attrs={"class": "form-item", "placeholder": "Enter Gene Name"}))
    protein_name = forms.CharField(required=False, max_length=100, label="Protein Name", widget=forms.TextInput(attrs={"class": "form-item", "placeholder": "Enter Protein Name"}))
    modification_type = forms.ChoiceField(required=False, label="Modification", choices=MODIFICATION_CHOICES, widget=forms.Select(attrs={"class": "form-item"}))
    
    def clean(self):
        cleaned_data = super().clean()
        uniprot_code = cleaned_data.get("uniprot_code")
        gene_name = cleaned_data.get("gene_name")
        protein_name = cleaned_data.get("protein_name")
        modification_type = cleaned_data.get("modification_type")

        if not (uniprot_code or gene_name or protein_name or modification_type):
            raise forms.ValidationError(
                "Please provide at least one search criteria."
            )
        return cleaned_data
