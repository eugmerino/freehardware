from django.contrib import admin
from .models import Project, Component, ProjectImage
from django.forms import BaseInlineFormSet
from django import forms


class ProjectImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        # Verificar que se suban imágenes correctamente si es necesario
        if not any([form.cleaned_data.get('image') for form in self.forms]):
            raise forms.ValidationError("Debe haber al menos una imagen.")
        return super().clean()

class ImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1  # Cuántas filas vacías mostrar para agregar imágenes
    formset = ProjectImageInlineFormSet
    fields = ('image',)
    show_change_link = True

class ComponentInlineFormSet(BaseInlineFormSet):
    def clean(self):
        # Verificar que haya al menos un componente
        components = [form.cleaned_data.get('component') for form in self.forms if form.cleaned_data.get('component')]
        if not components:
            raise forms.ValidationError("Debe haber al menos un componente.")
        return super().clean()

# Inline para los componentes, que permite agregar nuevos componentes o seleccionar existentes
class ComponentInline(admin.TabularInline):
    model = Project.components.through  # Relación ManyToMany
    extra = 1  # Fila adicional para agregar nuevos componentes
    formset = ComponentInlineFormSet
    fields = ('component',)
    show_change_link = True
    verbose_name_plural = "Componentes"

class ProjectAdmin(admin.ModelAdmin):
    inlines = [ComponentInline, ImageInline, ]  # Añadimos ComponentInline aquí
    list_display = ('title', 'state', 'description', 'imgDiagram')
    search_fields = ('title', 'description')
    exclude = ('components',)

# Registro de modelos en el admin
admin.site.register(Project, ProjectAdmin)
admin.site.register(Component)
admin.site.register(ProjectImage)
