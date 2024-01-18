from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

import apps.user.models as models

class MyAdminSite(admin.AdminSite):
    index_title = 'Consola Administrativa'
    verbose_name = "BRM"


admin_site = MyAdminSite()
admin.site = admin_site
admin_site.site_header = "BRM"


class CartItemInline(admin.StackedInline):
    model = models.CartItem
    extra = 0

    fieldsets = (
        (" ", {"fields": 
            (('item','price','ammount'),)
            }
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        return ['item','price','ammount']

    def has_add_permission(self, request, obj=None):
        return False


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user','last_updated','total')

    fieldsets = (
        ("", {"fields": 
            (('user','last_updated','total'),)
            }
        ),
    )

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        self.inlines = [CartItemInline]
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
       return ['user','last_updated','total']

class UserAccountAdmin(BaseUserAdmin):
    list_display = ('username', 'email','city')
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': (('email','is_active','is_staff'), 'password')}),
            ('Información', {'fields': (
            ('username','date_joined'),
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
            (('city','street'),)
            }
        ),
    )


    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    list_filter=[]

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        self.inlines = []
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        return ['username','email','date_joined']


admin.site.register(models.UserAccount, UserAccountAdmin)
admin.site.register(models.ShoppingCart, ShoppingCartAdmin)