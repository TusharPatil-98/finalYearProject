from django.db import models


# Create your models here.
class Diseases(models.Model):
    disease_name = models.CharField(max_length=200)
    plant_name = models.CharField(max_length=200)
    disease_description_en = models.CharField(max_length=10000)
    treatment_en = models.CharField(max_length=10000, default='')

    def get_description(self):
        return self.disease_description_en

    def get_disease_name(self):
        return self.disease_name

    def get_plant_name(self):
        return self.plant_name

    def get_english_treatment(self):
        return self.treatment_en


class FarmerQueries(models.Model):
    app_id = models.BigIntegerField()
    location = models.CharField(max_length=200)
    query = models.CharField(max_length=10000)
    answer = models.CharField(max_length=10000, default='')
    isQueryAnswered = models.BooleanField(default=False)
    query_date = models.DateTimeField(auto_now=True)
    isQueryViewed = models.BooleanField(default=False)

    def get_isQueryAnswered(self):
        return self.isQueryAnswered

    def get_isQueryViewed(self):
        return self.isQueryViewed

    def get_answer(self):
        return self.answer

    def get_query(self):
        return self.query


class DiseaseTrackRecord(models.Model):
    app_id = models.BigIntegerField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    disease = models.CharField(max_length=200)
    notified = models.BooleanField(default=False)
    dateTime = models.DateTimeField(auto_now=False)