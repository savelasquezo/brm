from django.contrib import admin
from django.conf.locale.es import formats as es_formats

import apps.item.models as models

class ItemAdmin(admin.ModelAdmin):

    list_display = (
        'uuid',
        'lot_number',
        'name',
        'price',
        'ammount',
        'date_joined',
        'is_active'
        )
    
    fieldsets = (
        ("", {"fields": 
            (('uuid'),
             ('lot_number','name'))
            }
        ),
        ("Detalles", {"fields": 
            (('price','ammount','is_active'),
             ('banner','date_joined'),)
            }
        ),
    )
    
    list_filter=['is_active']
    es_formats.DATETIME_FORMAT = "d M Y"

    readonly_fields=['uuid','date_joined',]

admin.site.register(models.Item, ItemAdmin)