from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import *
from .models import SiteUser
from datetime import datetime
from dateutil.relativedelta import relativedelta

class AgeFilter(admin.SimpleListFilter):
    title = 'Age'
    parameter_name = 'age'

    def lookups(self, request, model_admin):
        return [
            ('youth', 'Youth'),
            ('adult', 'Adult'),
        ]

    def queryset(self, request, queryset):
        checkout_date = datetime.now() - relativedelta(years=18)
        if self.value() == 'youth':
            return queryset.filter(date_of_birth__gte=checkout_date)
        elif self.value() == 'adult':
            return queryset.filter(date_of_birth__lt=checkout_date)

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'date_of_birth', 'get_ages', 'is_admin')
    list_filter = ('is_admin', AgeFilter)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    def get_ages(self, obj):
        return obj.age()

    get_ages.short_description = 'Age'

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'date_of_birth', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(SiteUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
