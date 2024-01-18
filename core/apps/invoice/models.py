from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist

from apps.user.models import UserAccount
from apps.item.models import Item

states = (('pending','Pendiente'),('done','Abonada'),('expired','Expirado'),('error','Error'))

class Invoice(models.Model):

    uuid = models.CharField(_("Codigo"), max_length=128, null=False, blank=False)
    client = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    state = models.CharField(_("Estado de la Factura"), default='pending', choices=states, max_length=128, null=False, blank=False)
    date_sold = models.DateField(_("Fecha"), default=timezone.now)
    total = models.FloatField(_("Total"), null=False, blank=False,
        help_text="$Costo Total (COP)")


    def save(self, *args, **kwargs):
        try:
            last_id = Invoice.objects.latest('id').id
        except ObjectDoesNotExist:
            last_id = 0

        if not self.uuid:
            self.uuid = "F0" + str(100 + last_id)
        super(Invoice, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = _("Factura")
        verbose_name_plural = _("Facturas")



class ItemList(models.Model):

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    price = models.FloatField(_("Precio"), null=False, blank=False,
        help_text="$Costo del Producto (COP)")

    ammount = models.PositiveBigIntegerField(_("Cantidad"), default=1000, null=False, blank=False,
        help_text="#Numero de Productos en Comprados")


    def __str__(self):
        return f"{self.item}"

    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")