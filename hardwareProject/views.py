from django.shortcuts import render, redirect, get_object_or_404
from systemConfig.models import SystemConfig
from hardwareProject.models import Project, ProjectImage
from django.http import JsonResponse
from .models import Project, ProjectImage, ProjectComponent, Component
from .forms import RegisterProjectForm, ProjectImageFormSet, ComponentForm
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
import json
from urllib.parse import urlparse, parse_qs
from django.contrib import messages



# Obtiene el último registro de SystemConfig (name y logo)
try:
    config = SystemConfig.objects.latest('id')
except SystemConfig.DoesNotExist:
    config = None

def home(request):
    imgDestacadas = ProjectImage.objects.filter(project__favorite = True)
    return render(request, 'home.html', {'config': config, 'ProjectImage': imgDestacadas})

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
    components = ProjectComponent.objects.filter(project=project)
    project_images = ProjectImage.objects.filter(project=project)

    # Convertir URL de YouTube a formato embed
    video_url = None
    if project.urlVideo:
        url_data = urlparse(project.urlVideo)
        query = parse_qs(url_data.query)
        video_id = query.get("v")
        if video_id:
            video_url = f"https://www.youtube.com/embed/{video_id[0]}"

    return render(request, 'project_detail.html', {
        'config': config,
        'project': project,
        'components': components,
        'project_images': project_images,
        'video_url': video_url,
    })

def register(request):
    component_form = ComponentForm()
    components = Component.objects.all()

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
        project_components = request.POST.get('components_data')

        if form.is_valid() and formset.is_valid():
            project = form.save()  # Guardar el proyecto
            formset.instance = project
            formset.save()  # Guardar imágenes relacionadas al proyecto

            # Procesar componentes dinámicos
            project_components = request.POST.get('components_data')  # Obtener la cadena JSON
            if project_components:
                try:
                    # Convertir la cadena JSON a una lista de diccionarios
                    project_components = json.loads(project_components)
                    for component_data in project_components:
                        existing_relation = ProjectComponent.objects.filter(
                            project=project,
                            component_id=component_data['component_id']
                        ).exists()
                        if not existing_relation:
                            # Crear solo si no existe
                            ProjectComponent.objects.create(
                                project=project,
                                component_id=component_data['component_id'],
                                amount=component_data['amount'],
                                description=component_data['description']
                            )
                except json.JSONDecodeError:
                    # Manejo de errores en caso de JSON inválido
                    return JsonResponse({'error': 'Invalid component data'}, status=400)
                
                messages.success(request, '¡El proyecto se ha guardado exitosamente!')

            return redirect('projects_view')
    else:
        form = RegisterProjectForm()
        formset = ProjectImageFormSet()

    return render(
        request,
        'register.html',
        {
            'config': config,
            'form': form,
            'formset': formset,
            'component_form': component_form,
            'components': components,
        }
    )