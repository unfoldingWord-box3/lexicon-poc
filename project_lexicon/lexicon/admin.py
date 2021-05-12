from django.contrib import admin
from django.apps import apps

from lexicon.models import Notes

#  https://medium.com/hackernoon/automatically-register-all-models-in-django-admin-django-tips-481382cf75e5


class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields]
        super(ListAdminMixin, self).__init__(model, admin_site)


class NotesAdmin(ListAdminMixin, admin.ModelAdmin):
    list_filter = 'supportreference'.split()
admin.site.register(Notes, NotesAdmin)


models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass