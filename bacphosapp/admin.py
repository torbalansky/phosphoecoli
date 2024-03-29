from django.contrib import admin
from .models import PhosphoProtein, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

class PhosphoProteinAdmin(admin.ModelAdmin):
    search_fields = ['uniprot_code', 'gene_name', 'protein_name']

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(PhosphoProtein, PhosphoProteinAdmin)
admin.site.register(Profile)
