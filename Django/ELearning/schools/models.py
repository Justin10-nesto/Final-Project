from django.db import models
# from django_tenants.models import TenantMixin, DomainMixin

# class School(TenantMixin):
#     school_name = models.CharField(max_length=100)
#     schoo_logo =  models.CharField(max_length=100)
#     school_level = models.CharField(max_length=100)
#     school_adress = models.CharField(max_length=100)
#     head_of_school = models.TextField()
#     is_active = models.BooleanField(default=True)
#     created_on = models.DateField(auto_now_add=True)

#     # default true, schema will be automatically created and synced when it is saved
#     auto_create_schema = True
#     auto_drop_schema = True
    
# class Domain(DomainMixin):
#     pass


class Department(models.Model):
    name = models.CharField(max_length=100)
    department_Hod = models.CharField(max_length=100)
    start_date= models.DateField()

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name

class Subject(models.Model):
    subject_code = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.subject_code

class SchoolLevel(models.Model):
    name = models.CharField(max_length=100)

class StudentClass(models.Model):
    name = models.CharField(max_length=100)
    level = models.ForeignKey(SchoolLevel, on_delete= models.CASCADE)