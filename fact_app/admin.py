from django.contrib import admin
from .models import Customer, Invoice, Article

# Register your models here.
class AdminCustomer(admin.ModelAdmin):  # Correction du nom de la classe
    list_display = ('name', 'email', 'phone', 'address', 'sex', 'age', 'city', 'zip_code')

class AdminInvoice(admin.ModelAdmin):
    list_display = ('customer', 'save_by', 'invoice_date_time', 'total', 'last_update_date', 'paid', 'invoice_type')

# Enregistrement des modèles dans l'administration avec la méthode correcte
admin.site.register(Customer, AdminCustomer)
admin.site.register(Invoice, AdminInvoice)
admin.site.register(Article)
