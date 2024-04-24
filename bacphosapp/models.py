from django.db import models
from django.contrib.auth.models import User

class PhosphoProtein(models.Model):
    uniprot_code = models.CharField(max_length=255)
    uniprot_url = models.URLField(null=True, blank=True)
    gene_name = models.CharField(max_length=255)
    protein_name = models.TextField()
    position = models.IntegerField(default=0)
    window_5_aa = models.TextField(default='')
    modification_type = models.CharField(max_length=50, default='')
    method = models.CharField(max_length=50, default='')
    sequence = models.TextField(null=True, blank=True, default='')
    pdb_code = models.CharField(max_length=50, null=True, blank=True)
    pdb_url = models.URLField(null=True, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    reference = models.TextField(null=True, blank=True)
    alphafold_url = models.URLField(null=True, blank=True)
    coli_strain = models.TextField(null=True, blank=True, default='')

    def __str__(self):
        return self.gene_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=100)
    country = models.CharField(max_length=60)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
