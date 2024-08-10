from django.contrib import admin
from .models import Tag, GenomeTag, GenomeScore
# Register your models here.

admin.site.register(Tag)
admin.site.register(GenomeScore)
admin.site.register(GenomeTag)
