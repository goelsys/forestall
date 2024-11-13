from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserCompany(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.company.name}"

class Prj(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[('Planned', 'Planned'), ('Ongoing', 'Ongoing'), ('Closed', 'Closed'), ('OnHold', 'OnHold')], blank=True)
    start_date = models.DateField(blank=True, null=True, help_text="YYYY-MM-DD")
    estimated_finish_date = models.DateField(blank=True, null=True, help_text="YYYY-MM-DD")
    client = models.CharField(max_length=100, blank=True)
    technology_stack = models.TextField(blank=True, null=True)
    total_budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)
    size_bucket = models.CharField(max_length=20, choices=[('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large'), ('Very Large', 'Very Large')], blank=True)
    team_size = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name 

class Risk(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    approach = models.CharField(max_length=10, choices=[('Reduce', 'Reduce'), ('Avoid', 'Avoid'), ('Transfer', 'Transfer'), ('Accept', 'Accept'), ('Share', 'Share')], blank=True)
    status = models.CharField(max_length=20, choices=[('New', 'New'), ('Open', 'Open'), ('Mitigation', 'Mitigation'), ('Contingency', 'Contingency'), ('Closed', 'Closed'), ('Reopen', 'Reopen')], blank=True)
    impact = models.IntegerField(blank=True, null=True, default=0)
    likelihood = models.IntegerField(blank=True, null=True, default=0)
    owner = models.CharField(max_length=40, blank=True, null=True)
    escalated = models.BooleanField(blank=True, null=True, default=False)
    date_identified = models.DateField(blank=True, null=True, default=timezone.now)
    mitigation_plan = models.TextField(blank=True, null=True)
    first_indicator = models.TextField(blank=True, null=True)
    contingency_plan = models.TextField(blank=True, null=True)
    date_closed = models.DateField(blank=True, null=True, help_text="YYYY-MM-DD")
    final_report = models.TextField(blank=True, null=True)
    date_last_updated = models.DateField(blank=True, null=True, auto_now=True, help_text="YYYY-MM-DD")
    date_reopened = models.DateField(blank=True, null=True, help_text="YYYY-MM-DD")
    reason_and_action = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Prj,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

