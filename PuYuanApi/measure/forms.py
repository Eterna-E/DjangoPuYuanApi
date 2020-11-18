from django import forms

from .forms import *

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

class DietForm(forms.ModelForm):
    uid = forms.CharField(max_length = 100,required = False)
    description = forms.CharField(max_length=10, required = False)
    meal = forms.CharField(max_length = 100, required = False)
    tag = forms.CharField(max_length = 100,required = False)
    image_count = forms.CharField(max_length = 100, required = False)
    lat = forms.CharField(max_length = 100, required = False)
    lng = forms.CharField(max_length = 100, required = False)
    recorded_at = forms.DateTimeField(required = False)
    created_at = forms.DateTimeField(required = False)
    date = forms.DateField(required = False)
    def clean(self):
    	if "meal" in self.cleaned_data:
    		self.cleaned_data["meal"] = int(self.cleaned_data["meal"])
    		print(self.cleaned_data["meal"])
    	if "image_count" in self.cleaned_data:
    		self.cleaned_data["image_count"] = int(self.cleaned_data["image_count"])
    		print(self.cleaned_data["image_count"])
    	if "lat" in self.cleaned_data:
    		self.cleaned_data["lat"] = int(self.cleaned_data["lat"])
    		print(self.cleaned_data["lat"])
    	if "lng" in self.cleaned_data:
    		self.cleaned_data["lng"] = int(self.cleaned_data["lng"])
    		print(self.cleaned_data["lng"])
		return self.cleaned_data