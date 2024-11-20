from django import forms
from .models import Project, ProjectImage, Component
from django_select2.forms import Select2MultipleWidget
from django.forms import inlineformset_factory


class RegisterProject(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'imgDiagram', 'code', 'components']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título del proyecto'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Describa el proyecto', 'rows': 4}),
            'imgDiagram': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'code': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese el código fuente', 'rows': 6}),
            'components': Select2MultipleWidget(attrs={'class': 'form-control'}),
        }


class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


ProjectImageFormSet = inlineformset_factory(Project, ProjectImage, form=ProjectImageForm, extra=1)


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        fields = ['name', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
