from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Rule, ProjectGCP, ComponentGCP, BusinessUnit
from .forms import RuleForm
from django import forms
import json

# Form classes for the other models
class ProjectGCPForm(forms.ModelForm):
    class Meta:
        model = ProjectGCP
        fields = ['name', 'description']

class ComponentGCPForm(forms.ModelForm):
    class Meta:
        model = ComponentGCP
        fields = ['name', 'description']

class BusinessUnitForm(forms.ModelForm):
    class Meta:
        model = BusinessUnit
        fields = ['name', 'description']

# Create your views here.

@csrf_exempt
def rule_list(request):
    if request.method == 'GET':
        rules = Rule.objects.filter(archived=False)
        data = [{"id": rule.id, "name": rule.name, "description": rule.description} for rule in rules]
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        rule = Rule.objects.create(name=data['name'], description=data['description'])
        return JsonResponse({"id": rule.id, "name": rule.name, "description": rule.description})

@csrf_exempt
def rule_detail(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    if request.method == 'GET':
        data = {"id": rule.id, "name": rule.name, "description": rule.description}
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        rule.name = data['name']
        rule.description = data['description']
        rule.save()
        return JsonResponse({"id": rule.id, "name": rule.name, "description": rule.description})
    elif request.method == 'DELETE':
        rule.archived = True
        rule.save()
        return JsonResponse({"deleted": True})

@login_required
def rule_list_view(request):
    if request.user.is_superuser:
        rules = Rule.objects.all()
    else:
        rules = Rule.objects.filter(archived=False)
    return render(request, 'core/rule_list.html', {'rules': rules})

@login_required
def rule_detail_view(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    return render(request, 'core/rule_detail.html', {'rule': rule})

@login_required
def rule_create_view(request):
    if request.method == 'POST':
        form = RuleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rule_list')
    else:
        form = RuleForm()
    return render(request, 'core/rule_form.html', {'form': form})

@login_required
def rule_update_view(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    if request.method == 'POST':
        form = RuleForm(request.POST, instance=rule)
        if form.is_valid():
            form.save()
            return redirect('rule_list')
    else:
        form = RuleForm(instance=rule)
    return render(request, 'core/rule_form.html', {'form': form, 'rule': rule})

@login_required
def rule_delete_view(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    if request.method == 'POST':
        rule.archived = True
        rule.save()
        return redirect('rule_list')
    return render(request, 'core/rule_confirm_delete.html', {'rule': rule})

@login_required
def rule_restore_view(request, pk):
    rule = get_object_or_404(Rule, pk=pk)
    rule.archived = False
    rule.save()
    return redirect('rule_list')

@login_required
def rule_search_view(request):
    query = request.GET.get('q', '')
    if query:
        rules = Rule.objects.filter(name__icontains=query, archived=False)
    else:
        rules = Rule.objects.filter(archived=False)
    return render(request, 'core/rule_list.html', {'rules': rules, 'query': query})

@csrf_exempt
def project_gcp_list(request):
    if request.method == 'GET':
        projects_gcp = ProjectGCP.objects.filter(archived=False)
        data = [{"id": project_gcp.id, "name": project_gcp.name, "description": project_gcp.description} for project_gcp in projects_gcp]
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        project_gcp = ProjectGCP.objects.create(name=data['name'], description=data['description'])
        return JsonResponse({"id": project_gcp.id, "name": project_gcp.name, "description": project_gcp.description})

@csrf_exempt
def project_gcp_detail(request, pk):
    project_gcp = get_object_or_404(ProjectGCP, pk=pk)
    if request.method == 'GET':
        data = {"id": project_gcp.id, "name": project_gcp.name, "description": project_gcp.description}
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        project_gcp.name = data['name']
        project_gcp.description = data['description']
        project_gcp.save()
        return JsonResponse({"id": project_gcp.id, "name": project_gcp.name, "description": project_gcp.description})
    elif request.method == 'DELETE':
        project_gcp.archived = True
        project_gcp.save()
        return JsonResponse({"deleted": True})

@csrf_exempt
def component_gcp_list(request):
    if request.method == 'GET':
        components_gcp = ComponentGCP.objects.filter(archived=False)
        data = [{"id": component_gcp.id, "name": component_gcp.name, "description": component_gcp.description} for component_gcp in components_gcp]
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        component_gcp = ComponentGCP.objects.create(name=data['name'], description=data['description'])
        return JsonResponse({"id": component_gcp.id, "name": component_gcp.name, "description": component_gcp.description})

@csrf_exempt
def component_gcp_detail(request, pk):
    component_gcp = get_object_or_404(ComponentGCP, pk=pk)
    if request.method == 'GET':
        data = {"id": component_gcp.id, "name": component_gcp.name, "description": component_gcp.description}
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        component_gcp.name = data['name']
        component_gcp.description = data['description']
        component_gcp.save()
        return JsonResponse({"id": component_gcp.id, "name": component_gcp.name, "description": component_gcp.description})
    elif request.method == 'DELETE':
        component_gcp.archived = True
        component_gcp.save()
        return JsonResponse({"deleted": True})

@csrf_exempt
def business_unit_list(request):
    if request.method == 'GET':
        business_units = BusinessUnit.objects.filter(archived=False)
        data = [{"id": business_unit.id, "name": business_unit.name, "description": business_unit.description} for business_unit in business_units]
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = json.loads(request.body)
        business_unit = BusinessUnit.objects.create(name=data['name'], description=data['description'])
        return JsonResponse({"id": business_unit.id, "name": business_unit.name, "description": business_unit.description})

@csrf_exempt
def business_unit_detail(request, pk):
    business_unit = get_object_or_404(BusinessUnit, pk=pk)
    if request.method == 'GET':
        data = {"id": business_unit.id, "name": business_unit.name, "description": business_unit.description}
        return JsonResponse(data)
    elif request.method == 'PUT':
        data = json.loads(request.body)
        business_unit.name = data['name']
        business_unit.description = data['description']
        business_unit.save()
        return JsonResponse({"id": business_unit.id, "name": business_unit.name, "description": business_unit.description})
    elif request.method == 'DELETE':
        business_unit.archived = True
        business_unit.save()
        return JsonResponse({"deleted": True})

@login_required
def index_view(request):
    return render(request, 'core/index.html')

@login_required
def project_list_view(request):
    query = request.GET.get('q', '')
    if request.user.is_superuser:
        if query:
            projects = ProjectGCP.objects.filter(name__icontains=query)
        else:
            projects = ProjectGCP.objects.all()
    else:
        if query:
            projects = ProjectGCP.objects.filter(name__icontains=query, archived=False)
        else:
            projects = ProjectGCP.objects.filter(archived=False)
    return render(request, 'core/project_list.html', {'projects': projects, 'query': query})

@login_required
def component_list_view(request):
    query = request.GET.get('q', '')
    if request.user.is_superuser:
        if query:
            components = ComponentGCP.objects.filter(name__icontains=query)
        else:
            components = ComponentGCP.objects.all()
    else:
        if query:
            components = ComponentGCP.objects.filter(name__icontains=query, archived=False)
        else:
            components = ComponentGCP.objects.filter(archived=False)
    return render(request, 'core/component_list.html', {'components': components, 'query': query})

@login_required
def business_unit_list_view(request):
    query = request.GET.get('q', '')
    if request.user.is_superuser:
        if query:
            business_units = BusinessUnit.objects.filter(name__icontains=query)
        else:
            business_units = BusinessUnit.objects.all()
    else:
        if query:
            business_units = BusinessUnit.objects.filter(name__icontains=query, archived=False)
        else:
            business_units = BusinessUnit.objects.filter(archived=False)
    return render(request, 'core/business_unit_list.html', {'business_units': business_units, 'query': query})

# Project CRUD views
@login_required
def project_detail_view(request, pk):
    project = get_object_or_404(ProjectGCP, pk=pk)
    return render(request, 'core/project_detail.html', {'object': project})

@login_required
def project_create_view(request):
    if request.method == 'POST':
        form = ProjectGCPForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectGCPForm()
    return render(request, 'core/project_form.html', {'form': form})

@login_required
def project_update_view(request, pk):
    project = get_object_or_404(ProjectGCP, pk=pk)
    if request.method == 'POST':
        form = ProjectGCPForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ProjectGCPForm(instance=project)
    return render(request, 'core/project_form.html', {'form': form, 'object': project})

@login_required
def project_delete_view(request, pk):
    project = get_object_or_404(ProjectGCP, pk=pk)
    if request.method == 'POST':
        project.archived = True
        project.save()
        return redirect('project_list')
    return render(request, 'core/project_confirm_delete.html', {'object': project})

# Component CRUD views
@login_required
def component_detail_view(request, pk):
    component = get_object_or_404(ComponentGCP, pk=pk)
    return render(request, 'core/component_detail.html', {'object': component})

@login_required
def component_create_view(request):
    if request.method == 'POST':
        form = ComponentGCPForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('component_list')
    else:
        form = ComponentGCPForm()
    return render(request, 'core/component_form.html', {'form': form})

@login_required
def component_update_view(request, pk):
    component = get_object_or_404(ComponentGCP, pk=pk)
    if request.method == 'POST':
        form = ComponentGCPForm(request.POST, instance=component)
        if form.is_valid():
            form.save()
            return redirect('component_list')
    else:
        form = ComponentGCPForm(instance=component)
    return render(request, 'core/component_form.html', {'form': form, 'object': component})

@login_required
def component_delete_view(request, pk):
    component = get_object_or_404(ComponentGCP, pk=pk)
    if request.method == 'POST':
        component.archived = True
        component.save()
        return redirect('component_list')
    return render(request, 'core/component_confirm_delete.html', {'object': component})

# BusinessUnit CRUD views
@login_required
def business_unit_detail_view(request, pk):
    business_unit = get_object_or_404(BusinessUnit, pk=pk)
    return render(request, 'core/business_unit_detail.html', {'object': business_unit})

@login_required
def business_unit_create_view(request):
    if request.method == 'POST':
        form = BusinessUnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('business_unit_list')
    else:
        form = BusinessUnitForm()
    return render(request, 'core/business_unit_form.html', {'form': form})

@login_required
def business_unit_update_view(request, pk):
    business_unit = get_object_or_404(BusinessUnit, pk=pk)
    if request.method == 'POST':
        form = BusinessUnitForm(request.POST, instance=business_unit)
        if form.is_valid():
            form.save()
            return redirect('business_unit_list')
    else:
        form = BusinessUnitForm(instance=business_unit)
    return render(request, 'core/business_unit_form.html', {'form': form, 'object': business_unit})

@login_required
def business_unit_delete_view(request, pk):
    business_unit = get_object_or_404(BusinessUnit, pk=pk)
    if request.method == 'POST':
        business_unit.archived = True
        business_unit.save()
        return redirect('business_unit_list')
    return render(request, 'core/business_unit_confirm_delete.html', {'object': business_unit})

@login_required
def project_restore_view(request, pk):
    project = get_object_or_404(ProjectGCP, pk=pk)
    project.archived = False
    project.save()
    return redirect('project_list')

@login_required
def component_restore_view(request, pk):
    component = get_object_or_404(ComponentGCP, pk=pk)
    component.archived = False
    component.save()
    return redirect('component_list')

@login_required
def business_unit_restore_view(request, pk):
    business_unit = get_object_or_404(BusinessUnit, pk=pk)
    business_unit.archived = False
    business_unit.save()
    return redirect('business_unit_list')

@login_required
def preferences_view(request):
    if request.method == 'POST':
        # Process form data here
        pass
    return render(request, 'core/preferences.html')
