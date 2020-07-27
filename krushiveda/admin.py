from django.contrib import admin
from .models import Diseases, FarmerQueries, DiseaseTrackRecord

# Register your models here.
admin.site.register(Diseases)
admin.site.register(FarmerQueries)
admin.site.register(DiseaseTrackRecord)