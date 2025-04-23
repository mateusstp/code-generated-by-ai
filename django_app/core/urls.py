from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('rules/', views.rule_list_view, name='rule_list'),
    path('rules/search/', views.rule_search_view, name='rule_search'),
    path('rules/<int:pk>/', views.rule_detail_view, name='rule_detail'),
    path('rules/create/', views.rule_create_view, name='rule_create'),
    path('rules/<int:pk>/update/', views.rule_update_view, name='rule_update'),
    path('rules/<int:pk>/delete/', views.rule_delete_view, name='rule_delete'),
    path('rules/<int:pk>/restore/', views.rule_restore_view, name='rule_restore'),
    
    # ProjectGCP CRUD
    path('projects/', views.project_list_view, name='project_list'),
    path('projects/create/', views.project_create_view, name='project_create'),
    path('projects/<int:pk>/', views.project_detail_view, name='project_detail'),
    path('projects/<int:pk>/update/', views.project_update_view, name='project_update'),
    path('projects/<int:pk>/delete/', views.project_delete_view, name='project_delete'),
    path('projects/<int:pk>/restore/', views.project_restore_view, name='project_restore'),
    
    # ComponentGCP CRUD
    path('components/', views.component_list_view, name='component_list'),
    path('components/create/', views.component_create_view, name='component_create'),
    path('components/<int:pk>/', views.component_detail_view, name='component_detail'),
    path('components/<int:pk>/update/', views.component_update_view, name='component_update'),
    path('components/<int:pk>/delete/', views.component_delete_view, name='component_delete'),
    path('components/<int:pk>/restore/', views.component_restore_view, name='component_restore'),
    
    # BusinessUnit CRUD
    path('business-units/', views.business_unit_list_view, name='business_unit_list'),
    path('business-units/create/', views.business_unit_create_view, name='business_unit_create'),
    path('business-units/<int:pk>/', views.business_unit_detail_view, name='business_unit_detail'),
    path('business-units/<int:pk>/update/', views.business_unit_update_view, name='business_unit_update'),
    path('business-units/<int:pk>/delete/', views.business_unit_delete_view, name='business_unit_delete'),
    path('business-units/<int:pk>/restore/', views.business_unit_restore_view, name='business_unit_restore'),
    
    path('preferences/', views.preferences_view, name='preferences'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]
