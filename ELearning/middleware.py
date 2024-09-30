from django_tenants.middleware.main import TenantMainMiddleware

class TanantMiddleware(TenantMainMiddleware):
    def get_tenant(self, domain_model, hostname):
        tenant = super().get_tenant(domain_model, hostname)
        if not tenant.is_active:
            raise self.TENANT_NOT_FOUND_EXCEPTION('Tenant is invalid')
        return tenant
    
class AuthenticationMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
     # One-time configuration and initialization on start-up

    def __call__(self, request):
        # Logic executed on a request before the view (and other middleware) is called.
        # get_response call triggers next phase
        response = self.get_response(request)
        # Logic executed on response after the view is called.
        # Return response to finish middleware sequence
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
    # Logic executed before a call to view
    # Gives access to the view itself & arguments
        pass

    def process_exception(self,request, exception):
    # Logic executed if an exception/error occurs in the view
        pass

    def process_template_response(self,request, response):
    # Logic executed after the view is called,
    # ONLY IF view response is TemplateResponse,
        pass