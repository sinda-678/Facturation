from django.shortcuts import render
from django.views import View
from .models import * 
from django.contrib import messages

from django.http import HttpResponse

import pdfkit

import datetime
from .decorators import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from django.template.loader import get_template

from django.db import transaction

from .utils import pagination, get_invoice


from django.utils.translation import gettext as _


from django.template.loader import get_template

# Vue pour la page d'accueil
class HomeView(View):
    template_name = 'index.html'
    
    # Récupère toutes les factures avec les relations nécessaires
    invoices = Invoice.objects.select_related('customer', 'save_by').all().order_by('-invoice_date_time')

    context = {
        'invoices': invoices
    }

    def get(self, request, *args, **kwargs):
          items = pagination(request, self.invoices)

          self.context['invoices'] = items

          return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwagrs):

        # modify an invoice

        if request.POST.get('id_modified'):

            paid = request.POST.get('modified')

            try: 

                obj = Invoice.objects.get(id=request.POST.get('id_modified'))

                if paid == 'True':

                    obj.paid = True

                else:

                    obj.paid = False 

                obj.save() 

                messages.success(request,  _("Change made successfully.")) 

            except Exception as e:   

                messages.error(request, f"Sorry, the following error has occured {e}.")      

        # deleting an invoice    

        if request.POST.get('id_supprimer'):

            try:

                obj = Invoice.objects.get(pk=request.POST.get('id_supprimer'))

                obj.delete()

                messages.success(request, _("The deletion was successful."))   

            except Exception as e:

                messages.error(request, f"Sorry, the following error has occured {e}.")      

        items = pagination(request, self.invoices)

        self.context['invoices'] = items

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
    



class InvoiceVisualizationView(View):
    """ This view helps to visualize the invoice """

    template_name = 'invoice.html'

    def get(self, request, *args, **kwargs):

        pk = kwargs.get('pk')

        obj = Invoice.objects.get(pk=pk)

        articles = obj.article_set.all()


        context = {
            'obj': obj,
            'articles' : articles
        }

        return render(request, self.template_name, context)
    



@superuser_required
def get_invoice_pdf(request, *args, **kwargs):
    """ generate pdf file from html file """

    pk = kwargs.get('pk')

    context = get_invoice(pk)

    context['date'] = datetime.datetime.today()

    # get html file
    template = get_template('invoice-pdf.html')

    # render html with context variables

    html = template.render(context)

    # options of pdf format 

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }

    # generate pdf 

    pdf = pdfkit.from_string(html, False, options)

    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = "attachement"

    return response
