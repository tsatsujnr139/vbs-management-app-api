from admin_export_action.admin import export_selected_objects
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email", "first_name", "last_name"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            "None",
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


@admin.register(models.Participant)
class ParticipantAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "modified",
    )
    list_display = (
        "first_name",
        "last_name",
        "age",
        "gender",
        "grade",
        "church",
        "parent_name",
    )
    list_filter = (
        "grade",
        "gender",
        "age",
    )
    search_fields = ("first_name", "last_name", "parent_name", "church")
    list_max_show_all = 1200
    actions = [
        export_selected_objects,
    ]


@admin.register(models.Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "modified",
    )
    list_display = (
        "first_name",
        "last_name",
        "preferred_role",
        "email",
        "previous_volunteer",
        "church",
    )
    list_filter = (
        "preferred_role",
        "preferred_class",
        "previous_volunteer",
        "previous_site",
    )
    search_fields = ("first_name", "last_name")
    list_max_show_all = 1200

    actions = [
        export_selected_objects,
    ]


@admin.register(models.Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.AttendanceType)
class AttendanceTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "start_date", "end_date")


@admin.register(models.ParticipantAttendance)
class ParticipantAttendanceAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return models.ParticipantAttendance.objects.all().select_related("participant")

    list_display = (
        "first_name",
        "last_name",
        "grade",
        "day_1",
        "day_2",
        "day_3",
        "day_4",
        "day_5",
    )

    list_filter = ("participant__grade",)
    search_fields = ("participant__first_name", "participant__last_name")
    list_max_show_all = 1200


    @admin.display()
    def first_name(self, obj):
        return obj.participant.first_name

    @admin.display()
    def last_name(self, obj):
        return obj.participant.last_name

    @admin.display()
    def grade(self, obj):
        return obj.participant.grade

    actions = [
        export_selected_objects,
    ]


@admin.register(models.ParticipantPickup)
class ParticipantPickupAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return models.ParticipantPickup.objects.all().select_related("participant")

    list_display = (
        "first_name",
        "last_name",
        "grade",
        "day_1",
        "day_2",
        "day_3",
        "day_4",
        "day_5",
    )

    list_filter = ("participant__grade",)
    search_fields = ("participant__first_name", "participant__last_name")
    list_max_show_all = 1200

    actions = [
        export_selected_objects,
    ]

    @admin.display()
    def first_name(self, obj):
        return obj.participant.first_name

    @admin.display()
    def last_name(self, obj):
        return obj.participant.last_name

    @admin.display()
    def grade(self, obj):
        return obj.participant.grade
