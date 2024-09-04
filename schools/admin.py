from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from schools.models import Department, Subject, SchoolLevel, StudentClass, CourseSubject

# from .models import School, Domain

# # class SchoolAdmin(TenantAdminMixin, admin.ModelAdmin):
# #         list_display = ('__all__')
        

# admin.site.register(School)
# admin.site.register(Domain)

admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(SchoolLevel)
admin.site.register(StudentClass)
admin.site.register(CourseSubject)
