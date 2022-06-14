from django import forms
from . import models

class QForm(forms.ModelForm):
    class Meta:
        model = models.Question_DB
        fields = '__all__'
        exclude = ['qno', 'professor']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'optionA': forms.TextInput(attrs={'class': 'form-control'}),
            'optionB': forms.TextInput(attrs={'class': 'form-control'}),
            'optionC': forms.TextInput(attrs={'class': 'form-control'}),
            'optionD': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.TextInput(attrs={'class': 'form-control'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class QPForm(forms.ModelForm):
    def __init__(self,professor,*args,**kwargs):
        super (QPForm,self ).__init__(*args,**kwargs) 
        self.fields['questions'].queryset = models.Question_DB.objects.filter(professor=professor)

    class Meta:
        model = models.Question_Paper
        fields = '__all__'
        exclude = ['professor','marks']
        widgets = {
            'qPaperTitle': forms.TextInput(attrs = {'class':'form-control'})
        }

class ExamForm(forms.ModelForm):
    def __init__(self,professor,*args,**kwargs):
        super (ExamForm,self ).__init__(*args,**kwargs) 
        self.fields['question_paper'].queryset = models.Question_Paper.objects.filter(professor=professor)

    class Meta:
        model = models.Exam_Model
        fields = '__all__'
        exclude = ['professor','marks']
        widgets = {
            'name': forms.TextInput(attrs = {'class':'form-control'}),
            'start_time': forms.DateTimeInput(attrs = {'class':'form-control'}),
            'end_time': forms.DateTimeInput(attrs = {'class':'form-control'})
        }