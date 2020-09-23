from django import forms

from .models import Pressure,Weight,Sugar

class PressureForm(forms.ModelForm):
    class Meta:
        model = Pressure
        fields = '__all__'

class WeightForm(forms.ModelForm):
    class Meta:
        model = Weight
        fields = '__all__'

class SugarForm(forms.ModelForm):
    class Meta:
        model = Sugar
        fields = '__all__'