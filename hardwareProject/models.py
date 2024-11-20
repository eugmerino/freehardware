from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


class ActiveProjectManager(models.Manager):
    # Filtra solo los proyectos que están activos (estado 1)
    def get_queryset(self):
        return super().get_queryset().filter(state=1)


class Project(models.Model):
    """
    representa un proyecto
    """
    STATE_CHOICES = [
        (0, 'Inactivo'),
        (1, 'Activo'),
        (2, 'En revisión'),
    ]

    title = models.CharField("Título", max_length=200)
    description = models.TextField("Descripción", max_length=400)
    state = models.IntegerField("Estado", choices=STATE_CHOICES, default=2)
    imgDiagram = models.ImageField("Diagrama", upload_to="diagrams/")
    code = models.TextField("Código fuente")

    def save(self, *args, **kwargs):
        # Definir tamaño de redimensionamiento
        max_width = 800  # Ancho máximo deseado
        max_height = 800  # Altura máxima deseada

        # Redimensionar y optimizar la imagen solo si se ha modificado
        if self.imgDiagram:
            # Abrir la imagen usando Pillow
            img = Image.open(self.imgDiagram)
            img = img.convert('RGB')  # Asegurar que la imagen esté en formato RGB

            # Obtener dimensiones originales
            original_width, original_height = img.size

            # Calcular la nueva dimensión manteniendo la relación de aspecto
            if original_width > max_width or original_height > max_height:
                img.thumbnail((max_width, max_height), Image.LANCZOS)

            # Guardar la imagen en un objeto BytesIO para optimización
            temp_image = BytesIO()
            img.save(temp_image, format='JPEG', quality=85, optimize=True)  # Ajuste de calidad para optimización

            # Guardar la imagen optimizada en el campo `image`
            temp_image.seek(0)
            self.imgDiagram.save(self.imgDiagram.name, ContentFile(temp_image.read()), save=False)

        # Llamar al método save() original para guardar los cambios en el modelo
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
         verbose_name="Proyecto"
         verbose_name_plural="Proyectos"
    

class Component(models.Model):
    """
    representa un componente del proyecto
    """
    name = models.CharField("Nombre", max_length=200)
    description = models.TextField("Descripción", max_length=400)
    image = models.ImageField("imagen", upload_to="components/")

    def save(self, *args, **kwargs):
        max_width = 800 
        max_height = 800

        if self.image:
            img = Image.open(self.image)
            img = img.convert('RGB')

            original_width, original_height = img.size

            if original_width > max_width or original_height > max_height:
                img.thumbnail((max_width, max_height), Image.LANCZOS)

            temp_image = BytesIO()
            img.save(temp_image, format='JPEG', quality=85, optimize=True)

            temp_image.seek(0)
            self.image.save(self.image.name, ContentFile(temp_image.read()), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
         verbose_name="Componente"
         verbose_name_plural="Componentes"

    
class ProjectComponent(models.Model):
    """
    Representa la relación entre un proyecto y sus componentes
    """
    amount = models.PositiveIntegerField("Cantidad", default=1)
    description = models.TextField("Descripción", max_length=400, blank=True, null=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name="Proyecto",
        related_name="project_components"
    )
    component = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        verbose_name="Componente",
        related_name="project_components"
    )

    def __str__(self):
        return f"{self.project.title} - {self.component.name}"

    class Meta:
        verbose_name = "Proyecto-Componente"
        verbose_name_plural = "Proyectos-Componentes"
        unique_together = ('project', 'component')
    

class ProjectImage(models.Model):
    """
    representa las imagenes del proyecto terminado
    """
    image = models.ImageField("imagen", upload_to="projects/")
    project= models.ForeignKey(Project,
        on_delete = models.CASCADE,
        null=False,
        blank=False,
        verbose_name="Proyecto",
    )

    def save(self, *args, **kwargs):
        max_width = 800
        max_height = 800

        if self.image:
            img = Image.open(self.image)
            img = img.convert('RGB')

            original_width, original_height = img.size

            if original_width > max_width or original_height > max_height:
                img.thumbnail((max_width, max_height), Image.LANCZOS)

            temp_image = BytesIO()
            img.save(temp_image, format='JPEG', quality=85, optimize=True)

            temp_image.seek(0)
            self.image.save(self.image.name, ContentFile(temp_image.read()), save=False)

        super().save(*args, **kwargs)
    
    class Meta:
         verbose_name="Imagen"
         verbose_name_plural="Imagenes"

