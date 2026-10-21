from django.contrib import admin

from .models import Competence, ContactMessage, Experience, Mission


class MissionInline(admin.TabularInline):
    model = Mission
    extra = 1


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("titre", "role", "theme", "ordre")
    inlines = [MissionInline]


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ("titre", "ordre")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("nom", "sujet", "email", "cree_le", "lu")
    list_filter = ("lu",)
    readonly_fields = ("nom", "email", "sujet", "message", "cree_le")
