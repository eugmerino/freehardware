from django.shortcuts import render, redirect, get_object_or_404
from systemConfig.models import SystemConfig
from hardwareProject.models import Project, ProjectImage
from django.http import JsonResponse
from .models import Project, ProjectImage, ProjectComponent, Component
from .forms import RegisterProjectForm, ProjectImageFormSet, ComponentForm
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory



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
    # Filtramos el proyecto según el estado y si el usuario está autenticado
    if request.user.is_authenticated:
        # Usuarios autenticados pueden ver cualquier proyecto
        project = get_object_or_404(Project, id=project_id)
    else:
        # Usuarios no autenticados solo pueden ver proyectos activos
        project = get_object_or_404(Project, id=project_id, state=1)

    # Obtenemos los componentes y las imágenes relacionados
    components = project.components.all()
    project_images = ProjectImage.objects.filter(project=project)

    return render(request, 'project_detail.html', {
        'config': config,
        'project': project,
        'components': components,
        'project_images': project_images
    })

def register(request):
    component_form = ComponentForm()
    components = Component.objects.all()  # Cargar componentes existentes para el select

    if request.method == 'POST':
        # Verificar si es una solicitud AJAX para agregar un nuevo componente
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
        form = RegisterProjectForm(request.POST, request.FILES)
        formset = ProjectImageFormSet(request.POST, request.FILES, instance=form.instance)
        project_components = request.POST.getlist('components_data')

        if form.is_valid() and formset.is_valid():
            project = form.save()  # Guardar el proyecto
            formset.instance = project
            formset.save()  # Guardar imágenes relacionadas al proyecto

            # Guardar relaciones de componentes con el proyecto
            for component_data in project_components:
                data = eval(component_data)  # Convertir la string JSON-like en un diccionario
                ProjectComponent.objects.create(
                    project=project,
                    component_id=data['component_id'],
                    amount=data['amount'],
                    description=data['description']
                )

            return redirect('projects_view')
    else:
        form = RegisterProjectForm()
        formset = ProjectImageFormSet()

    return render(
        request,
        'register.html',
        {
            'form': form,
            'formset': formset,
            'component_form': component_form,
            'components': components,
        }
    )