from django.shortcuts import render
from systemConfig.models import SystemConfig
from hardwareProject.models import Project, ProjectImage


config = SystemConfig.objects.latest('id') if SystemConfig.objects.exists() else None

def home(request):
    # Obtiene el último registro de SystemConfig (name y logo)
    return render(request, 'home.html', {'config': config})

def projects_view(request):
    projects = Project.objects.filter(state=1)

    # Agregar la primera imagen como atributo `main_image` a cada proyecto
    for project in projects:
        project.main_image = ProjectImage.objects.filter(project=project).first()

    return render(request, 'projects.html', {'config': config, 'projects': projects})