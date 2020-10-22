from django import forms

class BloodForm(forms.Form):
	a1c = forms.DecimalField(max_digits = 20,decimal_places = 5)
	recorded_at = forms.DateTimeField(required = False)
class mediForm(forms.Form):
	typee = forms.CharField(max_length = 20,required = False)
	hospitalname = forms.CharField(max_length = 20,required = False)
	recorded_at = forms.DateTimeField(required = False)
class diabeteForm(forms.Form):
	diabetes_type = forms.CharField(max_length = 20,required = False)
	oad = forms.CharField(max_length = 20,required = False)
	insulin = forms.CharField(max_length = 20,required = False)
	anti_hypertensives = forms.CharField(max_length = 20,required = False)