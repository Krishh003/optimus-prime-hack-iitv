from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Sponsor, College, SponsorEvent, CollegeEvent, EventRequest, SponsorHistory, CollegeSponsorshipHistory

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_college', 'contact_no', 'state', 'created_at')
    list_filter = ('is_college', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'state')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'contact_no', 'address', 'state')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_college', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_college'),
        }),
    )

@admin.register(SponsorEvent)
class SponsorEventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'sponsor', 'amount', 'location', 'created_at')
    list_filter = ('sponsor', 'created_at')
    search_fields = ('event_name', 'description', 'keywords')

@admin.register(CollegeEvent)
class CollegeEventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'college', 'amount', 'created_at')
    list_filter = ('college', 'created_at')
    search_fields = ('event_name', 'description', 'basic_deliverables')

@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = ('sponsor', 'college', 'event', 'status', 'created_at')
    list_filter = ('status', 'event_type', 'created_at')
    search_fields = ('sponsor__username', 'college__username', 'event__event_name')

@admin.register(SponsorHistory)
class SponsorHistoryAdmin(admin.ModelAdmin):
    list_display = ('sponsor', 'college', 'event', 'amount', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('sponsor__username', 'college__username', 'event__event_name')

@admin.register(CollegeSponsorshipHistory)
class CollegeSponsorshipHistoryAdmin(admin.ModelAdmin):
    list_display = ('college', 'sponsor', 'event', 'amount', 'created_at')
    list_filter = ('event_type', 'created_at')
    search_fields = ('college__username', 'sponsor__username', 'event__event_name')

# Register the Sponsor model with the custom admin
admin.site.register(Sponsor, CustomUserAdmin)