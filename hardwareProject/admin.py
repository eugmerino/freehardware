from django.contrib import admin
from .models import Project, Component, ProjectImage, ProjectComponent
from django.forms import BaseInlineFormSet
from django import forms
from django.urls import reverse
from django.utils.html import format_html


class ProjectImageInlineFormSet(BaseInlineFormSet):
    def clean(self):
        # Verificar que se suban imágenes correctamente si es necesario
        if not any([form.cleaned_data.get('image') for form in self.forms if not form.cleaned_data.get('DELETE')]):
            raise forms.ValidationError("Debe haber al menos una imagen.")
        return super().clean()


class ImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1  # Cuántas filas vacías mostrar para agregar imágenes
    formset = ProjectImageInlineFormSet
    fields = ('image',)
    show_change_link = True


class ProjectComponentInlineFormSet(BaseInlineFormSet):
    def clean(self):
        # Verificar que haya al menos un componente
        components = [
            form.cleaned_data.get('component') for form in self.forms
            if form.cleaned_data.get('component') and not form.cleaned_data.get('DELETE')
        ]
        if not components:
            raise forms.ValidationError("Debe haber al menos un componente asociado al proyecto.")
        return super().clean()


class ProjectComponentInline(admin.TabularInline):
    model = ProjectComponent
    extra = 1  # Fila adicional para agregar nuevos componentes
    formset = ProjectComponentInlineFormSet
    fields = ('component', 'amount', 'description')
    show_change_link = True
    verbose_name_plural = "Componentes"


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectComponentInline, ImageInline]  # Añadimos ProjectComponentInline aquí
    list_display = ('title', 'state', 'description', 'view_link')
    list_editable = ('state',)
    search_fields = ('title', 'description')
    list_per_page = 10
    ordering = ['state']

    @admin.display(description='Detalles del Proyecto')  # Nombre de la columna
    def view_link(self, obj):
        # Construimos la URL hacia la vista `project_detail`
        url = reverse('project_detail', args=[obj.id])  # Utilizamos el nombre de la ruta configurada
        return format_html('<a href="{}" target="_blank">Ver Detalles</a>', url)


# Registro de modelos en el admin
admin.site.register(Project, ProjectAdmin)
admin.site.register(Component)
admin.site.register(ProjectImage)
