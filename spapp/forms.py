from django import forms
from .models import Theme, Question, Report

    
class New_theme_form(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['title', 'image']
        widgets = {            
            'title': forms.TextInput(attrs={"class": "form-control", 
                                            "placeholder":"New Theme Title"}),
            'image':  forms.FileInput(attrs={"class": "form-control"}),}


class New_question_form(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title']
        widgets = {            
            'title': forms.Textarea(attrs={'rows':2, "class": 
                "form-control", "placeholder":"New Question Title"}),}


class Edit_question_form(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title']
        widgets = {            
            'title': forms.Textarea(attrs={'rows':2, "class": 
                "form-control", "placeholder":"Edited Question Title"}),}
        

class Edit_theme_form(forms.ModelForm):
    class Meta:
        model = Theme
        fields = ['title', 'image']
        widgets = {            
            'title': forms.TextInput(attrs={"class": "form-control", 
                                            "placeholder":"Edit Theme Title"}),
            'image':  forms.FileInput(attrs={"class": "form-control"}),}


class Flag_question_form(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']
        widgets = {            
            'reason': forms.Textarea(attrs={'rows':4, "class": 
                "form-control", "placeholder":"What do you think about this question?"}),}


class Flag_theme_form(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']
        widgets = {            
            'reason': forms.Textarea(attrs={'rows':4, "class": 
                "form-control", "placeholder":"Why do you think this theme is bad?"}),}