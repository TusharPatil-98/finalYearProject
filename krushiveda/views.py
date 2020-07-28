from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .models import Diseases, FarmerQueries, DiseaseTrackRecord
from .forms import QueryForm
from .codes.LanguageProcessing import LanguageProcessing
import nltk
from datetime import datetime, timedelta
from math import radians, cos, sin, asin, sqrt

from django.conf import settings
from django.utils.timezone import make_aware

naive_datetime = datetime.now()
naive_datetime.tzinfo  # None

settings.TIME_ZONE  # 'UTC'
aware_datetime = make_aware(naive_datetime)
aware_datetime.tzinfo  # <UTC>

nltk.download('stopwords')
lp = LanguageProcessing()
lp.train_model()
#print("Current Accuracy: ", lp.get_model_accuracy(), '%')


@csrf_exempt
def disease_info(request):
    query = request.POST['disease_name'].split()
    plantName = query[0]
    #print(query)
    diseaseName = ' '.join(i for i in query[1:])

    data = dict()
    description = ''
    treatment = ''

    if 'Healthy' not in diseaseName:
        disease = Diseases.objects.get(disease_name=diseaseName, plant_name=plantName)
        description = disease.get_description().split()
        treatment = disease.get_english_treatment().split()
    data['type'] = plantName[0].upper() + ''.join(i.capitalize() for i in diseaseName.split())
    # data['description'] = ' \n '.join(' '.join(j for j in description[i:i+5]) for i in range(0, len(description), 5))
    # data['treatment'] = ' \n '.join(' '.join(j for j in treatment[i:i+5]) for i in range(0, len(treatment), 5))
    data['description'] = ' '.join(description)
    data['treatment'] = ' '.join(treatment)
    #print(data)

    diseaseTrack = DiseaseTrackRecord()
    diseaseTrack.app_id = request.POST['app_id']
    if request.POST['app_longitude'] == "" or request.POST['app_latitude'] == "":
        diseaseTrack.longitude = 0.00
        diseaseTrack.latitude = 0.00
    else:
        diseaseTrack.longitude = request.POST['app_longitude']
        diseaseTrack.latitude = request.POST['app_latitude']
    diseaseTrack.disease = ' '.join(query)
    diseaseTrack.notified = True
    diseaseTrack.dateTime = datetime.now()

    diseaseTrack.save()

    return JsonResponse(data, safe=False)


@csrf_exempt
def index(request):
    global lp
    data = dict()
    #print("Query: ", request.POST['query'])
    output = data['answer'] = lp.predict_text_class(request.POST['query'])
    output = output.split('_')
    #print(' '.join([i.capitalize() for i in output[1:]]))
    #print(output[0].capitalize())
    if len(output) > 3:
        disease = Diseases.objects.get(disease_name=' '.join([i.capitalize() for i in output[1:len(output) - 1]]),
                                       plant_name=output[0].capitalize())
    else:
        disease = Diseases.objects.get(disease_name=' '.join([i.capitalize() for i in output[1:]]),
                                       plant_name=output[0].capitalize())
    try:
        if len(output) > 3:
            data['answer'] = disease.get_description()
        else:
            data['answer'] = disease.get_english_treatment()
    except:
        pass
        #print("Error while querying")
    return JsonResponse(data, safe=False)


def train(request):
    #print('Requesting')
    return HttpResponse(lp.predict_text_class("Tell me something about Potato Early blight ?"))


@csrf_exempt
def helpline(request):
    #print('App ID: ', request.POST['app_id'])
    #print('App Location', request.POST['app_location'])
    #print('App Query: ', request.POST['query'])

    query = FarmerQueries()
    query.app_id = int(request.POST['app_id'])
    query.location = request.POST['app_location']
    query.query = request.POST['query']
    query.save()

    return JsonResponse(data={'answer': "Your Question has been recorded. Wait for Expert's Answer"}, safe=False)


@csrf_exempt
def query_operator(request):
    data = {}
    queries = FarmerQueries.objects.all()
    count = 0
    for query in queries:
        if not query.get_isQueryViewed():
            data[query.id] = {
                'app_id': query.app_id,
                'question': query.get_query(),
                'status': query.get_isQueryAnswered(),
                'date': query.query_date,
            }
    return render(request, 'krushiveda/query_table.html', {'queries': data})


@csrf_exempt
def StartUpQuery(request):
    #print('App ID: ', request.POST['app_id'])
    #print('Longitude', request.POST['app_longitude'])
    #print('Latitude', request.POST['app_latitude'])
    areaToleranceInKm = 10
    # diseaseTrack = DiseaseTrackRecord.objects.filter(app_id=request.POST['app_id'], dateTime__lte= datetime.datetime.today(), dateTime__gt=datetime.datetime.today()-datetime.timedelta(days=30))
    diseaseTrack = DiseaseTrackRecord.objects.filter(app_id=request.POST['app_id'], dateTime__lte=datetime.today(), dateTime__gt=datetime.today()-timedelta(days=30), notified=False)
    disease = CheckDiseaseInRegion(request.POST['app_id'], request.POST['app_longitude'], request.POST['app_latitude'], areaToleranceInKm)

    for data in diseaseTrack:
        pass
        #print(data)

    if diseaseTrack.exists() and not diseaseTrack[0].notified:
        diseaseTrack[0].notified = True
        diseaseTrack[0].save()

    elif not diseaseTrack.exists():

        diseaseTrack = DiseaseTrackRecord()
        diseaseTrack.app_id = request.POST['app_id']
        diseaseTrack.longitude = request.POST['app_longitude']
        diseaseTrack.latitude = request.POST['app_latitude']
        diseaseTrack.notified = True
        diseaseTrack.disease = disease
        diseaseTrack.dateTime = datetime.now()
        diseaseTrack.save()

    return JsonResponse(data={'disease': disease}, safe=False)


@csrf_exempt
def check_pending_queries(request):
    #print("App ID: ", request.POST['app_id'], "App Location: ", request.POST['app_location'])
    data = {'status': 'success'}
    queries = FarmerQueries.objects.filter(app_id=request.POST['app_id'], location=request.POST['app_location'], isQueryAnswered=1, isQueryViewed=0)
    count = 0

    for i in FarmerQueries.objects.all():
        pass
        #print('APP ID: ', i.app_id, 'APP LOC: ', i.location, 'Query: ', i.query)

    for query in queries:
        data['query'] = ' '.join(i.capitalize() for i in query.query.split(' '))
        data['answer'] = query.answer
        query.isQueryViewed = 1
        query.save()
        count += 1
    if count == 0:
        return JsonResponse(data={'status': 'fail'}, safe=False)
    else:
        return JsonResponse(data, safe=False)


def CheckDiseaseInRegion(app_id, long, lat, tolerance):
    #print(datetime.today())
    #print(datetime.today()-timedelta(days=30))
    # diseaseTracks = DiseaseTrackRecord.objects.filter(dateTime__lte=datetime.datetime.today(), dateTime__gt=datetime.datetime.today()-datetime.timedelta(days=30))
    diseaseTracks = DiseaseTrackRecord.objects.filter(dateTime__lte=datetime.today(), dateTime__gt=datetime.today()-timedelta(days=30), notified=False)
    disease = ''
    for diseaseTrack in diseaseTracks:
        if app_id != diseaseTrack.app_id:
            if distance(diseaseTrack.longitude, diseaseTrack.latitude, long, lat) < tolerance:
                disease = diseaseTrack.disease

    return disease


def distance(lon1, lat1, lon2, lat2):
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(float(lon1))
    lon2 = radians(float(lon2))
    lat1 = radians(float(lat1))
    lat2 = radians(float(lat2))

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    # calculate the result
    return c * r


class FarmerQueriePage(TemplateView):
    template_name = 'krushiveda/farmer_query.html'

    def get(self, request):
        #print('Index: ', request.GET.get('index'))
        model = FarmerQueries.objects.get(pk=request.GET.get('index'))
        form = QueryForm(instance=model)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        #print(request.POST)
        if request.POST.get('isQueryAnswered') == 'on':
            query = FarmerQueries.objects.get(pk=request.POST.get('id'))
            query.answer = request.POST.get('answer')
            query.isQueryAnswered = True
            query.save()
        return redirect(query_operator)