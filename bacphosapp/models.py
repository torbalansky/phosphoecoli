from django.db import models
from django.contrib.auth.models import User

class PhosphoProtein(models.Model):
    uniprot_code = models.CharField(max_length=255)
    uniprot_url = models.URLField(null=True, blank=True)
    gene_name = models.CharField(max_length=255)
    protein_name = models.TextField()
    sequence = models.TextField(default='')
    alphafold_structure = models.URLField(null=True, blank=True)
    pdb_code = models.CharField(max_length=20, null=True, blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gene_name

class PhosphoSite(models.Model):
    protein = models.ForeignKey(PhosphoProtein, on_delete=models.CASCADE)
    position = models.IntegerField()
    window_5_aa = models.TextField()
    modification_type = models.CharField(max_length=50)
    method = models.CharField(max_length=50, default='')
    reference = models.CharField(max_length=100, default='')
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.protein.gene_name} - {self.position}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=100)
    country = models.CharField(max_length=60)

    def __str__(self):
        return self.user.username