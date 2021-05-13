from django.shortcuts import render, redirect
from mainsite.models import Customers
from mainsite.forms import CustomerForm, CustomerChangeForm
from sales.forms import OptionsForm
from sales.models import Cart
from django.contrib import messages
from sales.count import counting   # Returns two_element dictionary: first elem is 'total_price' and second is 'options'


def index(request):
    return render(request, 'index.html')


def register_order(request):
    if request.GET:     # If customer wants to change-delete its order
        invoice_request = request.GET
        for req, v in invoice_request.items():

            if req == 'change_invoice':
                return redirect('mainsite:change_order')

            if req == 'delete_invoice':
                Cart.objects.filter(id=request.session['cart']).delete()  # Delete cart for customer
                messages.add_message(request, messages.INFO, 'فاکتور شما پاک گردید')
                return redirect('mainsite:register_order')

    if request.method == 'POST':
        form_option = OptionsForm(data=request.POST)
        form_customer = CustomerForm(data=request.POST, files=request.FILES)
        if form_option.is_valid() and form_customer.is_valid():
            price_options = counting(request, form_option)  # price_options = ['total_price':<int>, 'options':<dict>]
            customer_obj = form_customer.cleaned_data  # 'options' = {'option_name': 'option_price'}

            if not Customers.objects.filter(email=customer_obj['email']):  # If customer NOT registered before
                customer = form_customer.save()  # Add customer to db
                cart = Cart.objects.create(  # Create cart for customer
                    customer=customer,
                    total_price=price_options['total_price'],
                    options=price_options['options']
                )
                messages.add_message(request, messages.INFO, 'مشخصات شما ثبت گردید')

            else:  # If customer HAS registered before
                customer = Customers.objects.get(email=customer_obj['email'])
                customer_changed = form_customer.save(False)
                customer.name = customer_changed.name
                customer.company = customer_changed.company
                customer.phone = customer_changed.phone
                if customer.domain != customer_changed.domain:
                    customer.domain = customer_changed.domain
                customer.logo = customer_changed.logo
                customer.save()  # Save changed models
                try:
                    cart = customer.cart  # Change cart for customer
                    cart.customer = customer
                    cart.total_price = price_options['total_price']
                    cart.options = price_options['options']
                except Cart.DoesNotExist:  # If 'cart' object does not exist
                    cart = Cart(
                        customer = customer,
                        total_price=price_options['total_price'],
                        options=price_options['options']
                    )
                cart.save()
                messages.add_message(request, messages.INFO, 'ایمیل شما قبلا ثبت شده')

            if customer.email and cart.options:  # If everything is good direct customer to invoice page
                request.session['customer'] = customer.id  # We define 'customer' and 'cart' and 'options' in
                request.session['cart'] = cart.id  # session to use them in another views
                request.session['options'] = price_options['options']
                return redirect('sales:invoice')

            messages.add_message(request, messages.INFO, 'مشکلی پیش آمده. سفارش خود را دوباره ثبت کنید')
            redirect('mainsite:register_order')

    else:   # GET or any other methods
        form_customer = CustomerForm()
        form_option = OptionsForm()

    return render(request, 'register_order.html',
                        {'form_option': form_option,
                         'form_customer': form_customer})


def change_order(request):
    customer = Customers.objects.get(id=request.session['customer'])
    cart = customer.cart
    data = {
        'cname': customer.name,
        'ccompany': customer.company,
        'cdomain': customer.domain,
        'cphone': customer.phone,
        'clogo': customer.logo
    }   # for Form initialization

    if request.method == 'POST':
        form_option = OptionsForm(data=request.POST)
        form_change = CustomerChangeForm(data=request.POST, files=request.FILES)

        if form_option.is_valid() and form_change.is_valid():
            price_options = counting(request, form_option)
            changed = form_change.cleaned_data
            # Now we assign form value to 'customer' object
            if customer.name != changed['cname']:
                customer.name = changed['cname']
            if customer.company != changed['ccompany']:
                customer.company = changed['ccompany']
            if customer.domain != changed['cdomain']:
                customer.domain = changed['cdomain']
            if customer.phone != changed['cphone']:
                customer.phone = changed['cphone']
            if changed['clogo']:
                customer.logo = changed['clogo']
            customer.save()
            cart.customer = customer
            cart.total_price = price_options['total_price']
            cart.options = price_options['options']
            cart.save()
            messages.add_message(request, messages.INFO, 'تغییرات اعمال گردید')

            if customer.email and cart.options:     # At last we update sessions attributes
                request.session['customer'] = customer.id
                request.session['cart'] = cart.id
                request.session['options'] = price_options['options']
                return redirect('sales:invoice')

    else:   # GET method
        form_option = OptionsForm()
        form_change = CustomerChangeForm(initial=data)

    return render(request, 'register_order.html',
                  {'form_option': form_option,
                   'form_change': form_change,
                   'customer': customer})

"""
def has_registered(request):

    if request.method == 'POST':
        has_registered = HasRegistered(request.POST)
        if has_registered.is_valid():
            customer = Customers.objects.filter(email=has_registered.cleaned_data['email'])
            try:
                options = request.session['options']
            except KeyError:
                options = ''
            if customer:    # If email has registered before
                return render(request, 'has_registered.html', {'customer': customer[0],
                                                               'options': options})
            return HttpResponse("این کاربر مشخصاتی ندارد")
    else:
        return HttpResponse('این صفحه وجود ندارد')
"""