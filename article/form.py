from django import forms

from article.models import Tags

class PressForm(forms.Form):
    press = forms.CharField()
    category = forms.CharField()

class TagsForm(forms.Form):
	
	class Meta:
		model = Tags
		fields = ('aid','atitle','asentence','asubject','aobject', 'averb', 'acomplement','aetc') 
	"""
	aid = forms.CharField(required = False)
	atitle = forms.CharField(required = False)
	asentence = forms.CharField(required=False)
	asubject = forms.CharField(required=False)
	aobject = forms.CharField(required=False)
	averb = forms.CharField(required=False)
	acomplement = forms.CharField(required=False)
	aetc = forms.CharField(required=False)
	"""
