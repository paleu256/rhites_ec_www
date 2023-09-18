from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms
from .models import IFASBottleneck,gbvTool,GbvQaTool_Choices, gbvToolB, gbvToolC, gbvToolD
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
    reporting_period = forms.DateField(label='Reporting Period',input_formats=['%d/%m/%Y'],required=False)
    
    
    class Meta:
        model=gbvTool
        #exclude = ('roid','doid','hfoid', )
        fields=['reporting_period','fd1_1','fd1_2','fd1_3','fd1_4',
                'fd1_5','fd1_6','fd1_7','fd1_8','fd1_9','fd1_10','fd1_11','fd1_12','fd1_13','fd1_14',
                'fd1_15','fd1_16','fd1_17','fd1_18','fd1_19','fd1_20','fd1_21','fd1_22','fd1_23','fd1_24','fd1_25',]
       
        widgets={
             'reporting_period':forms.DateInput(attrs={'type':'date', 'placeholder':'yyyy-mm-dd (DOB)','class':'form-control'}),
             #'fd1_2':forms.RadioSelect(choices=GbvQaTool_Form_Choices),
             #'fd1_4':forms.CharField(attrs={'class','form-control'})     
        }

    def clean_GBVQaTool(self):
        data=self.cleaned_data['gbvTool']
        
        #some ifs to do some cleaning
        return data

class GBVQaFormB(forms.ModelForm):
    
    class Meta:
        model=gbvToolB
        exclude = ('rgbv_oid', )
        fields=['fd1_26','fd1_27','fd1_28','fd1_29','fd1_30','fd1_31','fd1_32','fd1_33','fd1_34',
                'fd1_35','fd1_36','fd1_37','fd1_38','fd1_39','fd1_40','fd1_41','fd1_42','fd1_43',
                'fd1_44','fd1_45','fd1_46','fd1_47','fd1_48','fd1_49','fd1_50','fd1_51','fd1_52',
                'fd1_53','fd1_54','fd1_55','fd1_56','fd1_57','fd1_58','fd1_59','fd1_60','fd1_61',
                'fd1_62','fd1_63','fd1_64',]
       
        widgets={
             
        }

    def clean_GBVQaTool(self):
        data=self.cleaned_data['gbvToolB']
        
        #some ifs to do some cleaning
        return data
    
class GBVQaFormC(forms.ModelForm):
    
    class Meta:
        model=gbvToolC
        exclude = ('rgbv_oid', )
        fields=['fd1_65','fd1_66','fd1_67','fd1_68','fd1_69','fd1_70','fd1_71','fd1_72','fd1_73',
                'fd1_74','fd1_75','fd1_76','fd1_77','fd1_78','fd1_79','fd1_80','fd1_81','fd1_82',
                'fd1_83','fd1_84','fd1_85','fd1_86','fd1_87','fd1_88','fd1_89','fd1_90','fd1_91',
                'fd1_92','fd1_93','fd1_94','fd1_95','fd1_96','fd1_97','fd1_98','fd1_99','fd1_100',
                'fd1_101','fd1_102','fd1_103','fd1_104','fd1_105','fd1_106',]
       
        widgets={
                 
        }

    def clean_GBVQaTool(self):
        data=self.cleaned_data['gbvToolC']
        
        #some ifs to do some cleaning
        return data
    
class GBVQaFormD(forms.ModelForm):
    
    class Meta:
        model=gbvToolD
        exclude = ('rgbv_oid', )
        fields=['fd1_107','fd1_108','fd1_109','fd1_110','fd1_111','fd1_112','fd1_113','fd1_114','fd1_115',
                'fd1_116','fd1_117','fd1_118','fd1_119','fd1_120','fd1_121','fd1_122','fd1_123','fd1_124',
                'fd1_125','fd1_126','fd1_127','fd1_128','fd1_129',]
       
        widgets={
               
        }

    def clean_GBVQaTool(self):
        data=self.cleaned_data['gbvToolD']
        
        #some ifs to do some cleaning
        return data  