from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import FormView, UpdateView
from django.urls import reverse
from django.http import HttpResponse
from .models import Company, UserCompany, Prj, Risk
from .forms import CompanyForm, ProjectForm, RiskForm, UserForm
from .filters import RiskFilter, ProjectFilter

# for export_to_pdf
from django.template.loader import render_to_string
from weasyprint import HTML


# Create your views here.
def UserView(request):
    user = request.user
    
    try:
        user_company = UserCompany.objects.get(user=user)
        company = user_company.company
    except UserCompany.DoesNotExist:
        company=None

    try:
        projects = Prj.objects.filter(user=user)
        project_filter = ProjectFilter(request.GET, queryset=projects)
        projects = project_filter.qs
    except Prj.DoesNotExist:
        projects = None

    context={
        'company': company,
        'projects': projects,
        'project_filter': project_filter,
    }
    return render(request, "user.html", context)

def profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') # Redirect to profile page
    else:
        form = UserForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})


class CreateCompanyView(FormView):
    template_name = 'company_form.html'  # Replace with your template name
    form_class = CompanyForm
    success_url = '/4s/'  # Redirect to company list after success

    def form_valid(self, form):
        # Save the company form after successful validation
        company = form.save()
        UserCompany.objects.create(user=self.request.user, company=company)
        return super().form_valid(form)


class EditCompanyView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company_form.html'  # Use the same template for creating and editing
    success_url = '/4s/'


def create_project(request):
    user = request.user
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            # Check if a project with the same name already exists for the user_company
            if not Prj.objects.filter(user=user, name=form.cleaned_data['name']).exists():
                project = form.save(commit=False)
                project.user = user
                project.save()
                return redirect('user')  # Redirect to a success page or project list
            else:
                # Handle duplicate project name error
                form.add_error('name', 'Project with this name already exists.')
    else:
        form = ProjectForm(initial={'user': user})

    return render(request, 'project_form.html', {'form': form})

class EditProjectView(UpdateView):
    model = Prj
    form_class = ProjectForm
    template_name = 'project_form.html'  # Use the same template for creating and editing
    success_url = '/4s/'


def Risklog(request, project_id):
    user = request.user
    try:
        project = get_object_or_404(Prj, pk=project_id)
        if project.user != user:
            raise PermissionDenied("You don't have permission to access this project.")
        if request.GET.get('clear_filter'):
            return redirect('log', project_id)
        risks = Risk.objects.filter(project=project)
        risk_count = risks.count()
        risk_filter = RiskFilter(request.GET, queryset=risks)
        risks = risk_filter.qs
    except Risk.DoesNotExist:
        risks = None
    context = {
        'risks': risks,
        'risk_count': risk_count,
        'project': project,
        'risk_filter': risk_filter,
    }
    return render(request, "risks.html", context)

def add_risk(request, project_id):
    project = Prj.objects.get(pk=project_id)

    if request.method == 'POST':
        form = RiskForm(request.POST)
        if form.is_valid():
            risk = form.save(commit=False)
            risk.project = project
            risk.save()
            return redirect('log', project_id)  # Redirect to a success page or project list
    else:
        form = RiskForm(initial={'project': project})
    return render(request, 'risk_form.html', {'form': form, 'project': project})

def RiskView(request, project_id, risk_id):
    risk = get_object_or_404(Risk, pk=risk_id)
    context = {
        'risk': risk,
        'project_id': project_id,
    }
    return render(request, 'risk.html', context)

class EditRiskView(UpdateView):
    model = Risk
    form_class = RiskForm
    template_name = 'risk_form.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.object.project
        return context
    
    def get_success_url(self):
        # Redirect to the project detail page after successful edit
        return reverse('log', args=[self.object.project.id])

def export_pdf(request, project_id, risk_id):
    risk = get_object_or_404(Risk, pk=risk_id)
    context = {
        'risk': risk,
        'project_id': project_id,
    }
    html_string = render_to_string('risk_pdf.html', context)

    # Convert HTML to PDF
    pdf = HTML(string=html_string).write_pdf()

    # Create a response with the PDF content
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="risk_report.pdf"'

    return response


def handle_404(request, exception):
    return render(request, '404.html', status=404)