from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)
from .models import User, Event, Registration

class RegistrantAdmin(ModelAdmin):
    model = User
    menu_label = 'Registrants'
    add_to_settings_menu = True
    exclude_from_explorer = True

class EventAdmin(ModelAdmin):
    model = Event
    menu_label = 'Events'
    add_to_settings_menu = True
    exclude_from_explorer = False


class RegistrationAdmin(ModelAdmin):
    model = Registration
    menu_label = 'Event Registrations'
    add_to_settings_menu = True
    exclude_from_explorer = True

modeladmin_register(RegistrantAdmin)
modeladmin_register(EventAdmin)
modeladmin_register(RegistrationAdmin)
