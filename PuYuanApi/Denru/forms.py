from django import forms
from Denru.models import patient

class PatientForm(forms.Form):
	account = forms.CharField(max_length = 20)
	phone = forms.CharField(max_length = 10)
	email = forms.EmailField(max_length = 50,required = False)
	password = forms.CharField(max_length = 100)

	def clean(self):
		if patient.objects.filter(username = self.cleaned_data['account']):
			raise Exception("username wrong");
		if patient.objects.filter(phone = self.cleaned_data['phone']):
			raise Exception("phone wrong");
		if patient.objects.filter(email = self.cleaned_data['email']):
			raise Exception("email wrong");
		return self.cleaned_data