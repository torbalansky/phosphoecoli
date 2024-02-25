from django.db import models

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

