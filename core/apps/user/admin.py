from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

import apps.user.models as models

class MyAdminSite(admin.AdminSite):
    index_title = 'Consola Administrativa'
    verbose_name = "BRM"


admin_site = MyAdminSite()
admin.site = admin_site
admin_site.site_header = "BRM"


class UserAccountAdmin(BaseUserAdmin):
    list_display = ('username', 'email','phone')
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': (('email','is_active','is_staff'), 'password')}),
            ('Información', {'fields': (
            ('username','date_joined'),
            ('first_name','last_name'),
            ('phone'),
        )}),
    )

    fieldsets = (
        ("", {"fields": 
            (('email','is_active','is_staff'), 'password')
            }
        ),
        ("", {"fields": 
            (('username','date_joined'),)
            }   
        ),
        ("Detalles", {"fields": 
            (('country','postal_code'),
             ('city','street'),)
            }
        ),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2','phone'),
        }),
    )

    list_filter=[]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        self.inlines = []
        return fieldsets

    # def get_readonly_fields(self, request, obj=None):
    #    return ['username','email','date_joined']


admin.site.register(models.UserAccount, UserAccountAdmin)
