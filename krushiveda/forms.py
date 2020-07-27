from django import forms
from .models import FarmerQueries


class QueryForm(forms.ModelForm):
    id = forms.IntegerField()
    query = forms.CharField(disabled=True)
    answer = forms.CharField(max_length=10000, required=True)
    isQuestionAnswered = forms.BooleanField()

    class Meta:
        model = FarmerQueries
        fields = ('id', 'query', 'answer', 'isQueryAnswered',)
