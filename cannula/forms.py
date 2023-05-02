from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from .models import IFASBottleneck,gbvTool,GbvQaTool_Choices, gbvTool2
from .enums import Where_Identified_CHOICES

from . import models

class SourceDocumentForm(ModelForm):
	class Meta:
		model = models.SourceDocument
		fields = ['file1',]


class DataElementAliasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DataElementAliasForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['readonly'] = True

    class Meta:
        model = models.DataElement
        fields = ['name', 'alias']

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class BottleneckInventory(forms.ModelForm):
    bottleneck = forms.CharField(label='Bottleneck')
    level = forms.CharField(label='Level')
    when_identified = forms.DateField(label='When Identified',input_formats=['%d/%m/%Y'],required=True)
    where_identified=forms.ChoiceField(choices = Where_Identified_CHOICES, label="Where Identified", initial='', widget=forms.Select(), required=True)
    potential_solutions = forms.CharField(label='Potential Solutions')
    efforts_to_address_bottleneck=forms.CharField(label="Efforts to address the bottleneck")
    next_steps=forms.CharField(label='Next steps')
    additional_bottleneck_identified=forms.CharField(label='Additional bottleneck identified during efforts')
    comments=forms.CharField(label='Comments if any')


    class Meta:
        model=IFASBottleneck
        fields=['bottleneck','when_identified','level','where_identified','potential_solutions','efforts_to_address_bottleneck','next_steps','additional_bottleneck_identified','comments']

    def clean_bottleneck(self):
        data=self.cleaned_data['bottleneck']
        #some ifs to do some cleaning
        return data
    
GbvQaTool_Form_Choices=[
    ("None","None"),
    ("No","No"),
    ("Yes","Yes"),
]

Year_Form_Choices=[
    ("None","None"),
    ("No","No"),
    ("Yes","Yes"),
]

class GBVQaForm(forms.ModelForm):
    reporting_period = forms.DateField(label='Reporting Period',input_formats=['%d/%m/%Y'],required=True)
    
    class Meta:
        model=gbvTool
        exclude = ('roid','doid','hfoid', )
        fields=['reporting_period','fd1_1','fd1_2','fd1_3','fd1_4',
                'fd1_5','fd1_6','fd1_7','fd1_8','fd1_9','fd1_10','fd1_11','fd1_12','fd1_13','fd1_14',
                'fd1_15','fd1_16','fd1_17','fd1_18','fd1_19','fd1_20','fd1_21','fd1_22','fd1_23','fd1_24','fd1_25',]
       
        widgets={
             'reporting_period':forms.DateInput(attrs={'type':'date', 'placeholder':'yyyy-mm-dd (DOB)','class':'form-control'}),
             #'fd1_2':forms.CharField(choices=GbvQaTool_Form_Choices,required=True),
             #'fd1_4':forms.CharField(attrs={'class','form-control'})
            
             
        }

    def clean_GBVQaTool(self):
        data=self.cleaned_data['gbvTool']
        
        #some ifs to do some cleaning
        return data

class GBVQaForm2(forms.ModelForm):
    reporting_period2 = forms.DateField(label='Reporting Period',input_formats=['%d/%m/%Y'],required=True)
    
    class Meta:
        model=gbvTool2
        fields=['reporting_period2',]
       
        widgets={
             'reporting_period2':forms.DateInput(attrs={'type':'date', 'placeholder':'yyyy-mm-dd (DOB)','class':'form-control'}),
        }

    def clean_GBVQaTool(self):
        data=self.cleaned_data['gbvTool']
        
        #some ifs to do some cleaning
        return data
    
   