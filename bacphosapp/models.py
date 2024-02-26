from django.db import models
from django.contrib.auth.models import User

class PhosphoProtein(models.Model):
    uniprot_code = models.CharField(max_length=255)
    url = models.URLField()
    gene_name = models.CharField(max_length=255)
    protein_name = models.TextField()
    modification_type = models.CharField(max_length=50)
    position = models.IntegerField()
    window_5_aa = models.TextField()
    sequence = models.TextField()
    method = models.CharField(max_length=50)
    reference = models.IntegerField()
    alphafold_link = models.URLField()

    def __str__(self):
        return self.protein_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=100)
    country = models.CharField(max_length=60)

    def __str__(self):
        return self.user.username