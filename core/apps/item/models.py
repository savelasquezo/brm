from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist

def ImageUploadTo(instance, filename):
    return f"uploads/products/{filename}"

class Item(models.Model):

    uuid = models.CharField(_("Codigo"),max_length=8)

    lot_number = models.CharField(_("#Lote"), max_length=128, unique=False, null=False, blank=False)
    name = models.CharField(_("Nombre"), max_length=128, unique=False, null=False, blank=False)
    
    price = models.FloatField(_("Precio"), null=False, blank=False,
        help_text="$Costo del Producto (COP)")

    ammount = models.PositiveBigIntegerField(_("Cantidad Disponible"), default=1000, null=False, blank=False,
        help_text="#Numero de Productos en Inventario")

    banner = models.ImageField(_("Imagen"), upload_to=ImageUploadTo, max_length=32, null=False, blank=False, 
                help_text="Dimenciones: width:1250px height:385px")

    date_joined = models.DateField(_("Fecha de Listado"), default=timezone.now)

    is_active = models.BooleanField(_("¿Activo?"),default=True)

    def save(self, *args, **kwargs):
        try:
            last_id = Item.objects.latest('id').id
        except ObjectDoesNotExist:
            last_id = 0

        if not self.uuid:
            self.uuid = "I0" + str(100 + last_id)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")
