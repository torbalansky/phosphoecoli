from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import PhosphoProtein

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

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(label="E-mail", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="First name", max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="Last name", max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    username = forms.CharField(label="Username", max_length=50,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}), required=False)
    institution_name = forms.CharField(label="Institution Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Institution Name'}))
    country = forms.CharField(label="Country", max_length=60, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'country', 'institution_name', )
    
    def clean(self):
        cleaned_data = super(UserUpdateForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("The passwords do not match.")
        
        return cleaned_data

class ContactForm(forms.Form):
    name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}))
    email = forms.EmailField(label="Email", max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}))
    content = forms.CharField(label="Message", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message', 'rows': 3})) 

class ProteinSearchForm(forms.Form):
    
    MODIFICATION_CHOICES = (
        ('', 'Any'),  
        ('Y', 'Y'),
        ('H', 'H'),
        ('S', 'S'),
        ('T', 'T'),
        ('D', 'D'),
        ('K', 'K'),
        ('R', 'R'),
        ('C', 'C'),
    )

    uniprot_code = forms.CharField(required=False, max_length=20, label="UniprotID", widget=forms.TextInput(attrs={"class": "form-item", "placeholder": "Enter Uniprot ID"}))
    gene_name = forms.CharField(required=False, max_length=50, label="Gene Name", widget=forms.TextInput(attrs={"class": "form-item", "placeholder": "Enter Gene Name"}))
    protein_name = forms.CharField(required=False, max_length=100, label="Protein Name", widget=forms.TextInput(attrs={"class": "form-item", "placeholder": "Enter Protein Name"}))
    modification_type = forms.ChoiceField(required=False, label="Modification", choices=MODIFICATION_CHOICES, widget=forms.Select(attrs={"class": "form-item"}))
    peptide_sequence = forms.CharField(required=False, max_length=20, label="Peptide Sequence", widget=forms.TextInput(attrs={"class": "form-item", "placeholder": "Enter Peptide Sequence"}))

    def clean(self):
        cleaned_data = super().clean()
        uniprot_code = cleaned_data.get("uniprot_code")
        gene_name = cleaned_data.get("gene_name")
        protein_name = cleaned_data.get("protein_name")
        modification_type = cleaned_data.get("modification_type")
        peptide_sequence = cleaned_data.get('peptide_sequence')

        if not (uniprot_code or gene_name or protein_name or modification_type or peptide_sequence):
            raise forms.ValidationError(
                "Please provide at least one search criteria."
            )
        return cleaned_data

class PhosphoProteinForm(forms.ModelForm):
    class Meta:
        model = PhosphoProtein
        fields = ['uniprot_code', 'uniprot_url', 'gene_name', 'protein_name', 'position', 'window_5_aa',
                  'modification_type', 'method', 'sequence', 'pdb_code', 'pdb_url', 'submitted_by', 'reference',
                  'approved']
        widgets = {
            'uniprot_code': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'uniprot_url': forms.URLInput(attrs={'class': 'form-control'}),
            'gene_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'protein_name': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'position': forms.NumberInput(attrs={'class': 'form-control', 'required': True}),
            'window_5_aa': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'modification_type': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'method': forms.TextInput(attrs={'class': 'form-control', 'required': True}),
            'sequence': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'pdb_code': forms.TextInput(attrs={'class': 'form-control'}),
            'pdb_url': forms.URLInput(attrs={'class': 'form-control'}),
            'submitted_by': forms.Select(attrs={'class': 'form-control'}),
            'reference': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'required': True}),
            'approved': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }