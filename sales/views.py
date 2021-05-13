from django.shortcuts import render, HttpResponse
from mainsite.models import Customers
from sales.models import Cart, Orders, ActiveProjects,\
    PayId
from sales.forms import OrderTailing
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
import random
from sales.functions import options_to_db, db_to_options,\
    mail_invoice
#import weasyprint

def invoice(request):
    try:                                                        # If customer did enter his email and ordered some
        customer_id = request.session['customer']               #some service in 'register_order' form
        cart_id = request.session['cart']
        customer = Customers.objects.get(id=customer_id)
        cart = Cart.objects.get(id=cart_id)
        options = request.session['options']
        mail_invoice(customer, options)
        
        return render(request, 'invoice.html',
                      {'customer': customer,
                       'cart': cart,
                       'options': options})
    except ObjectDoesNotExist or KeyError:   # If customer hasn't ordered something yet or deleted his order
        return render(request, 'waiting.html')


def result_invoice(request):   # After customer paid for the invoice FOR THE FIRST TIME
    customer = Customers.objects.get(id=request.session['customer'])
    cart = customer.cart
    options = request.session['options']
    
    options_price_list = options_to_db(options) # it returns a 2_element list
    
    # Create order object for the customer in db
    order = Orders.objects.create(customer=customer,
                                  price=request.session['amount'],
                                  paid=int(float(request.session['pay'])),
                                  discount = request.session['discount'],
                                  paid_method = request.session['paid_method'],
                                  domain=customer.domain,
                                  options_name=options_price_list[0],
                                  options_price=options_price_list[1],
                                  order_id=str(random.randint(10001, 99999)))
    pay_id = request.session['pay_id']      # for registering the payment into db
    pay_obj = PayId.objects.create(order=order,
                                   pay_amount=int(float(request.session['pay'])),
                                   pay_id=pay_id)
    # Create activeproject object for customer in db
    ActiveProjects.objects.create(
                                  customer=customer,
                                  order=order,
                                  )
    customer.hasOrder = True
    customer.save()
    cart.delete()   # empty customer cart
    # delete all the unneeded sessions
    del request.session['amount'], request.session['pay'],\
    request.session['discount'], request.session['paid_method'],\
    request.session['pay_id']
    # Now the paid invoice should been shown to customer
    return render(request, 'result_invoice.html',
                  {'customer': customer,
                   'order': order,
                   'pay': pay_obj,
                   'options': options})


def update_invoice(request):
    customer_id = request.session['customer']
    customer = Customers.objects.get(id=customer_id)
    order = customer.orders.last()
    order.paid = int(order.paid) + int(float(request.session['pay'])) # order object just needs to get updated
    order.save()

    pay_obj = PayId.objects.create(order=order,   # create PayId model for each payment
                         pay_amount=int(float(request.session['pay'])),
                         pay_id=request.session['pay_id'])
    del request.session['customer'], request.session['pay'],\
        request.session['pay_id']

    return render(request, 'result_invoice.html',
                  {'customer': customer,
                   'order': order,
                   'pay': pay_obj,
                   'options': request.session['options']})


def tail_order(request):
    if request.method == 'POST':
        form = OrderTailing(data=request.POST)

        if form.is_valid():
            email_received = form.cleaned_data['email']
            try:        # if there is no customer registered before or customer has no active project
                customer = Customers.objects.get(email=email_received)
                order = customer.orders.last()
                customer.active_projects.last()
            except ObjectDoesNotExist:
                return render(request, 'waiting.html')

            #order = customer.orders
            # options is a dictionary that returns options and respective price
            options = db_to_options(order.options_name, order.options_price)
            return render(request, 'tailing_order.html',
                          {'customer': customer,
                           'order': order,
                           'options': options})
    else:
        form = OrderTailing
    return render(request, 'tailing_order_email.html',
                  {'form': form})

"""
inactive yet
"""
def invoice_pdf(request):   # Creating invoice as a pdf file
    customer = Customers.objects.get(id=request.session['customer'])
    order = Orders.objects.get(id=request.session['order_id'])
    html = render_to_string('result_invoice.html',
                            {'customer': customer,
                             'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=invoice.pdf'
    #weasyprint.HTML(string=html).write_pdf(response)
    return response

