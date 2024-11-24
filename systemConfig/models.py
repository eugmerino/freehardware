from django.db import models
import os
from django.conf import settings

class SystemConfig(models.Model):
    """
    representa la información del sistema
    """
    name = models.CharField("Nombre", max_length=200)
    acronym = models.CharField("Acrónimo", max_length=10)
    logo = models.ImageField("Logo", upload_to="logo/")

    def save(self, *args, **kwargs):
        # Eliminar la imagen anterior si se está actualizando el logo
        if self.pk:
            old_logo = SystemConfig.objects.get(pk=self.pk).logo
            if old_logo and old_logo != self.logo:
                old_logo_path = os.path.join(settings.MEDIA_ROOT, old_logo.name)
                if os.path.exists(old_logo_path):
                    os.remove(old_logo_path)
        super().save(*args, **kwargs) # Llama al método save original

    def delete(self, *args, **kwargs):
        # Eliminar la imagen del sistema de archivos antes de eliminar el objeto
        if self.logo:
            # Construir la ruta completa de la imagen
            logo_path = os.path.join(settings.MEDIA_ROOT, self.logo.name)
            if os.path.exists(logo_path):
                os.remove(logo_path)
        super().delete(*args, **kwargs)  # Llama al método delete original

    class Meta:
         verbose_name="Configuración del sistema"
         verbose_name_plural="Configuración del sistema"