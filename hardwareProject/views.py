from django.shortcuts import render, redirect, get_object_or_404
from systemConfig.models import SystemConfig
from hardwareProject.models import Project, ProjectImage
from django.http import JsonResponse
from .models import Project, ProjectImage, Component
from .forms import RegisterProject, ProjectImageFormSet, ComponentForm



# Obtiene el último registro de SystemConfig (name y logo)
config = SystemConfig.objects.latest('id') if SystemConfig.objects.exists() else None

def home(request):
    return render(request, 'home.html', {'config': config})

def projects_view(request):
    projects = Project.objects.filter(state=1)

    # Agregar la primera imagen como atributo `main_image` a cada proyecto
    for project in projects:
        project.main_image = ProjectImage.objects.filter(project=project).first()

    return render(request, 'projects.html', {'config': config, 'projects': projects})

def project_detail(request, project_id):
    # Recuperar el proyecto por su id o devolver 404 si no existe
    project = get_object_or_404(Project, id=project_id)
    components = project.components.all()
    project_images = ProjectImage.objects.filter(project=project)

    return render(request, 'project_detail.html', {'config': config, 'project': project, 'components': components, 'project_images': project_images})

def register(request):
    component_form = ComponentForm()

    if request.method == 'POST':
        # Verificar si es una solicitud AJAX para agregar un componente
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'name' in request.POST:
            component_form = ComponentForm(request.POST, request.FILES)
            if component_form.is_valid():
                component = component_form.save()
                return JsonResponse({
                    'success': True,
                    'component_id': component.id,
                    'component_name': component.name
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': component_form.errors
                })

        # Procesamiento del formulario de proyecto
        form = RegisterProject(request.POST, request.FILES)
        formset = ProjectImageFormSet(request.POST, request.FILES, instance=form.instance)
        
        if form.is_valid() and formset.is_valid():
            project = form.save()  # Guarda el proyecto
            formset.instance = project
            formset.save()  # Guarda las imágenes relacionadas con el proyecto
            return redirect('projects_view')
    else:
        form = RegisterProject()
        formset = ProjectImageFormSet()

    return render(request, 'register.html', {'config': config, 'form': form, 'formset': formset, 'component_form': component_form})
