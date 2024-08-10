from django.shortcuts import render
from django.views import View
from .models import Customer, Invoice,Article
from django.contrib import messages
from django.db import transaction

# Vue pour la page d'accueil
class HomeView(View):
    template_name = 'index.html'
    
    # Récupère toutes les factures avec les relations nécessaires
    invoices = Invoice.objects.select_related('customer', 'save_by').all()

    context = {
        'invoices': invoices
    }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

# Vue pour ajouter un client
class AddCustomerView(View):
    template_name = 'add_customer.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'sex': request.POST.get('sex'),
            'age': request.POST.get('age'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('zip'),
            'save_by': request.user
        }

        try:
            # Création du nouveau client
            created = Customer.objects.create(**data)
            if created:
                messages.success(request, "Customer registered successfully")
            else:
                messages.error(request, "Sorry, please try again. The sent data is corrupt.")
        except Exception as e:
            messages.error(request, f"Sorry, our system is detecting the following issues: {e}")

        return render(request, self.template_name)
    
class AddInvoiceView(View):
    template_name = 'add_invoice.html'

    def get(self, request, *args, **kwargs):
        customers = Customer.objects.select_related('save_by').all()
        context = {
            'customers': customers
        }
        return render(request, self.template_name, context)
    
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        customers = Customer.objects.select_related('save_by').all()
        context = {
            'customers': customers
        }
        
        items = []

        try: 
            customer = Customer.objects.get(id=request.POST.get('customer'))
            type = request.POST.get('invoice_type')
            articles = request.POST.getlist('article')
            qties = request.POST.getlist('qty')
            units = request.POST.getlist('unit')
            total_a = request.POST.getlist('total-a')
            total = request.POST.get('total')
            comment = request.POST.get('comment')

            invoice_object = {
                'customer': customer,
                'save_by': request.user,
                'total': total,
                'invoice_type': type,
                'comments': comment
            }

            invoice = Invoice.objects.create(**invoice_object)

            for index, article in enumerate(articles):
                data = Article(
                    invoice=invoice,
                    name=article,
                    quantity=qties[index],
                    unit_price=units[index],
                    total=total_a[index],
                )
                items.append(data)

            created = Article.objects.bulk_create(items)   

            if created:
                messages.success(request, "Data saved successfully.") 
            else:
                messages.error(request, "Sorry, please try again, the sent data is corrupt.")    

        except Exception as e:
            messages.error(request, f"Sorry, the following error has occurred: {e}.")   
        
        return render(request, self.template_name, context)