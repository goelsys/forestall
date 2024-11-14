from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserView, name='user'),
    path('profile/', views.profile, name='profile'),
    path('create_company/', views.CreateCompanyView.as_view(), name='create_company'),
    path('companies/<int:pk>/edit/', views.EditCompanyView.as_view(), name='edit_company'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:pk>/edit/', views.EditProjectView.as_view(), name='edit_project'),
    path('projects/<int:project_id>/', views.Risklog, name='log'),
    path('projects/<int:project_id>/add_risk/', views.add_risk, name='add_risk'),
    path('risks/<int:pk>/edit/', views.EditRiskView.as_view(), name='edit_risk'),
    path('risks/<int:project_id>/<int:risk_id>/', views.RiskView, name='risk'),
    path('risks/<int:project_id>/<int:risk_id>/delete/', views.delete_risk, name='delete_risk'),
    path('risks/<int:project_id>/<int:risk_id>/print', views.export_pdf, name='export_pdf'),
    
]
