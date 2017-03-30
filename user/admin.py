from django.contrib import admin
from .models import Profile

class ProfileAdminLayout(admin.ModelAdmin):
    fieldsets = (

        ('Basic Information', {
            'fields': ('user','banned'),
        }),

        ('Avatar', {
            'fields': ('avatar', 'height_field','width_field'),
        }),

        ('Account activation', {
            'fields': ('activation_key', 'key_expires'),
        }),

        ('Forgot password', {
            'fields': ('forgot_pass_key', 'forgot_pass_expires'),
        }),
    )

    list_display = ['__str__','banned','staff','isactive']
    search_fields = ('user__username',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(ProfileAdminLayout, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(user__username=search_term_as_int)
        return queryset, use_distinct

admin.site.register(Profile,ProfileAdminLayout)

# Register your models here.
