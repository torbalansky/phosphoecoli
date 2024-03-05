from django.db import models
from django.contrib.auth.models import User

class PhosphoProtein(models.Model):
    uniprot_code = models.CharField(max_length=255)
    uniprot_url = models.URLField(null=True, blank=True)
    gene_name = models.CharField(max_length=255)
    protein_name = models.TextField()
    synonyms = models.TextField(null=True, blank=True)
    protein_description = models.TextField(null=True, blank=True)
    molecular_function = models.TextField(null=True, blank=True)
    biological_process = models.TextField(null=True, blank=True)
    cellular_component = models.TextField(null=True, blank=True)
    molecular_weight = models.IntegerField(null=True, blank=True)
    protein_type = models.TextField(null=True, blank=True)
    sequence = models.TextField(default='')
    alphafold_structure = models.URLField(null=True, blank=True)
    pdb_code = models.CharField(max_length=20, null=True, blank=True)
    pdb_url = models.URLField(null=True, blank=True)
    ecocyc_url = models.URLField(null=True, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    reference = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.gene_name

class PhosphoSite(models.Model):
    protein = models.ForeignKey(PhosphoProtein, on_delete=models.CASCADE)
    position = models.IntegerField()
    window_5_aa = models.TextField()
    modification_type = models.CharField(max_length=50)
    method = models.CharField(max_length=50, default='')
    reference = models.TextField(default='')
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.protein.gene_name} - {self.position}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=100)
    country = models.CharField(max_length=60)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username