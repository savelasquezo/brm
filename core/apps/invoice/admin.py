from django.contrib import admin
from django.conf.locale.es import formats as es_formats

import apps.invoice.models as models


class ItemListInline(admin.StackedInline):
    
    model = models.ItemList
    extra = 0

    fieldsets = (
        (" ", {"fields": (
            ('item','ammount'),
                )
            }
        ),
    )

    # def get_readonly_fields(self, request, obj=None):
    #    return ['item','ammount']

    # def has_add_permission(self, request, obj=None):
    #    return False

class InvoiceAdmin(admin.ModelAdmin):

    list_display = (
        'uuid',
        'client',
        'date_sold',
        'total',
        'state'
        )
    
    fieldsets = (
        ("", {"fields": 
            (('uuid','client'),)
            }
        ),
        ("Detalles", {"fields": 
            (('total','date_sold','state'),)
            }
        ),
    )
    
    list_filter=['state']

    es_formats.DATETIME_FORMAT = "d M Y"

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('client', 'total','date_sold','state'),
        }),
    )


    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        self.inlines = [ItemListInline]
        if not obj:
            self.inlines = []
        return fieldsets

    #readonly_fields=['uuid','client','total','date_sold']

    # def has_add_permission(self, request):
    #     return False

admin.site.register(models.Invoice, InvoiceAdmin)