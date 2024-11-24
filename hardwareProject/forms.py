from django import forms
from .models import Project, ProjectImage, Component, ProjectComponent
from django.forms import inlineformset_factory


class RegisterProjectForm(forms.ModelForm):
    """
    Formulario para registrar o editar proyectos, excluyendo la relación directa con Component.
    """
    class Meta:
        model = Project
        fields = ['title', 'description', 'imgDiagram', 'code', 'urlVideo']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el título del proyecto',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describa el proyecto',
                'rows': 4,
            }),
            'imgDiagram': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'code': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el código fuente',
                'rows': 10,
            }),
            'urlVideo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el link del video',
            }),
        }


class ProjectImageForm(forms.ModelForm):
    """
    Formulario para gestionar las imágenes asociadas a un proyecto.
    """
    class Meta:
        model = ProjectImage
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# FormSet para manejar múltiples imágenes relacionadas con un proyecto
ProjectImageFormSet = inlineformset_factory(
    Project,
    ProjectImage,
    form=ProjectImageForm,
    extra=1,
    can_delete=True,  # Permitir eliminar imágenes en el formulario
)


class ProjectComponentForm(forms.ModelForm):
    """
    Formulario para gestionar la relación entre proyectos y componentes, incluyendo cantidad y descripción.
    """
    class Meta:
        model = ProjectComponent
        fields = ['component', 'amount', 'description']
        widgets = {
            'component': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cantidad requerida',
                'min': 1,
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción del uso del componente en el proyecto',
            }),
        }


class ComponentForm(forms.ModelForm):
    """
    Formulario para gestionar la creación y edición de componentes.
    """
    class Meta:
        model = Component
        fields = ['name', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre del componente',
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
