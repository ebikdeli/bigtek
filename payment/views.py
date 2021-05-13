from django.shortcuts import redirect, HttpResponse
from mainsite.models import Customers
from sales.models import Cart
from bigtek.settings import MERCHANT_ID_ZARRIN
from zeep import Client

# PGI_URL = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'
PGI_URL = 'https://sandbox.zarinpal.com/pg/services/WebGate/wsdl'
# CallbackURL = 'http://www.bigtek.ir/payment/verify/'  # for deployment
CallbackURL = 'http://127.0.0.1:8000/payment/verify/'  # for production
client = Client(PGI_URL)

amount = 0
payment_factor = 0
another_pay = None

SESSION_VARIABLES = {}


def payment_request(request):
    global amount
    global payment_factor
    global another_pay
    description = ''
    email = ''
    pay = 0

    if request.method == 'GET':

        if request.GET.get('order') == 'begin':  # for the first time customer pay
            cart = Cart.objects.get(id=request.session['cart'])
            amount = cart.total_price
            email = cart.customer.email
            discount_value = request.GET['discount']
            discount = 100 - int(float(discount_value) * 100)
            pay = int(float(discount_value) * amount)
            amount = pay
            request.session['amount'] = amount
            request.session['pay'] = pay
            request.session['discount'] = discount

            if discount == 7:
                request.session['paid_method'] = 'once'
                payment_factor = 1.0
                description = 'سفارش وبسایت ( 7 درصد تخفیف)'

            elif discount == 3:
                request.session['paid_method'] = 'twice'
                payment_factor = 0.5
                description = 'سفارش وب سایت ( 3 درصد تخفیف) - پرداخت اول'

            elif discount == 0:
                request.session['paid_method'] = 'third'
                payment_factor = 0.4
                description = 'سفارش وب سایت - پرداخت اول'

    elif request.method == 'POST':
        # for POST method this is wrong: some_val = request.POST.get(...) or request.POST['....']
        data = {}
        for k, v in request.POST.items():  # POST method sends its data to server as a QueryDict
            data[k] = v  # so we can iterate over it like a ordinary dictionary
        customer = Customers.objects.get(email=data['customer_email'])
        request.session['customer'] = customer.id
        order = customer.orders.last()

        email = customer.email
        pay = order.price

        another_pay = data['another_pay']

        if data['order'] == 'twice':
            description = 'پرداخت پایانی'
            payment_factor = 0.5

        elif data['order'] == 'third_first':
            description = 'پرداخت دوم'
            payment_factor = 0.4

        else:
            description = 'پرداخت پایانی'
            payment_factor = 0.2
    request.session['pay'] = pay = str(payment_factor * pay)
    result = client.service.PaymentRequest(MERCHANT_ID_ZARRIN,
                                           pay,
                                           description,
                                           email,
                                           CallbackURL=CallbackURL,
                                           )
    for k, v in request.session.items():
        SESSION_VARIABLES[k] = v
    print(result)
    if result.Status == 100:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
        # return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    elif result.Status == -1:
        return HttpResponse('اطلاعات ارسال شده ناقص است')
    elif result.Status == -10:
        return HttpResponse('شناسه پذیرنده صحیح نیست')
    else:
        return HttpResponse("درخواست شما ممکن نیست")


def verify(request):
    global another_pay
    print(request.GET)
    for k, v in SESSION_VARIABLES.items():
        request.session[k] = v

    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT_ID_ZARRIN,
                                                    request.GET['Authority'],
                                                    request.session['pay']
                                                    )
        print(result.Status)
        if result.Status == 100:
            request.session['pay_id'] = str(result.RefID)
            print(result.RefID)
            if another_pay:
                another_pay = None
                return redirect('sales:update_invoice')
            return redirect('sales:result_invoice')

        elif result.Status == 101:
            request.session['pay_id'] = result.RefID
            if another_pay:
                another_pay = None
                return redirect('sales:update_invoice')
            return redirect('sales:result_invoice')

        elif result.Status == -1:
            return HttpResponse('اطلاعات ارسال شده ناقص است')
        elif result.Status == -3:
            return HttpResponse('بدلیل محدودیت های شاپرک امکان تارکنش وجود ندارد')
        elif result.Status == -22:
            return HttpResponse('تراکنش ناموفق')
        elif result.Status == -33:
            return HttpResponse('رقم تراکنش با رقم پرداخت شده مطابقت ندارد')
        elif result.Status == -34:
            return HttpResponse('رقم وارد شده از حداکثر مجاز عبور کرده')
        else:
            return HttpResponse('پرداخت موفقیت آمیز نبود. وضعیت پرداخت: ' + str(result.Status))
    else:
        return HttpResponse('مشکلی پیش آمده')


# THIS CODE HAS SESSION PROBLEM IN DEPLOYMENT
"""
from django.shortcuts import redirect, HttpResponse
from mainsite.models import Customers
from sales.models import Cart, Orders
from bigtek.settings import MERCHANT_ID_ZARRIN
from zeep import Client
from django.views.decorators.cache import cache_control


# PGI_URL = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'
PGI_URL = 'https://sandbox.zarinpal.com/pg/services/WebGate/wsdl'
CallbackURL = 'http://127.0.0.1:8000/payment/verify/'
client = Client(PGI_URL)

amount = 0
payment_factor = 0
another_pay = None

@cache_control(private=True)
def payment_request(request):
    global amount
    global payment_factor
    global another_pay
    pay = 0.0
    description = ''
    email = ''

    if request.method == 'GET':

        if request.GET.get('order') == 'begin':     # for the first time customer pay
            cart = Cart.objects.get(id=request.session['cart'])
            amount = cart.total_price
            email = cart.customer.email
            discount_value = request.GET['discount']
            discount = 100 - int(float(discount_value) * 100)
            pay = int(float(discount_value) * amount)
            amount = pay
            request.session['amount'] = amount
            request.session['pay'] = pay
            request.session['discount'] = discount

            if discount == 7:
                request.session['paid_method'] = 'once'
                payment_factor = 1.0
                description = 'سفارش وبسایت ( 7 درصد تخفیف)'

            elif discount == 3:
                request.session['paid_method'] = 'twice'
                payment_factor = 0.5
                description = 'سفارش وب سایت ( 3 درصد تخفیف) - پرداخت اول'

            elif discount == 0:
                request.session['paid_method'] = 'third'
                payment_factor = 0.4
                description = 'سفارش وب سایت - پرداخت اول'

    elif request.method == 'POST':
        # for POST method this is wrong: some_val = request.POST.get(...) or request.POST['....']
        data = {}
        for k, v in request.POST.items():   # POST method sends its data to server as a QueryDict
            data[k] = v                     # so we can iterate over it like a ordinary dictionary
        customer = Customers.objects.get(email=data['customer_email'])
        request.session['customer'] = customer.id
        order = customer.orders.last()

        email = customer.email
        pay = order.price

        another_pay = data['another_pay']

        if data['order'] == 'twice':
            description = 'پرداخت پایانی'
            payment_factor = 0.5

        elif data['order'] == 'third_first':
            description = 'پرداخت دوم'
            payment_factor = 0.4

        else:
            description = 'پرداخت پایانی'
            payment_factor = 0.2

    request.session['pay'] = pay = str(payment_factor * pay)
    result = client.service.PaymentRequest(MERCHANT_ID_ZARRIN,
                                            pay,
                                            description,
                                            email,
                                            CallbackURL=CallbackURL,
                                            )
    print(result)
    if result.Status == 100:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/' + str(result.Authority))
        #return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    elif result.Status == -1:
        return HttpResponse('اطلاعات ارسال شده ناقص است')
    elif result.Status == -10:
        return HttpResponse('شناسه پذیرنده صحیح نیست')
    else:
        return HttpResponse("درخواست شما ممکن نیست")

@cache_control(private=True)
def verify(request):
    global another_pay
    print(request.GET)
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT_ID_ZARRIN,
                                                    request.GET['Authority'],
                                                    request.session['pay'],
                                                    )
        print(result.Status)
        if result.Status == 100:
            request.session['pay_id'] = str(result.RefID)
            print(result.RefID)
            if another_pay:
                another_pay = None
                return redirect('sales:update_invoice')
            return redirect('sales:result_invoice')

        elif result.Status == 101:
            request.session['pay_id'] = result.RefID
            if another_pay:
                another_pay = None
                return redirect('sales:update_invoice')
            return redirect('sales:result_invoice')

        elif result.Status == -1:
            return HttpResponse('اطلاعات ارسال شده ناقص است')
        elif result.Status == -3:
            return HttpResponse('بدلیل محدودیت های شاپرک امکان تارکنش وجود ندارد')
        elif result.Status == -22:
            return HttpResponse('تراکنش ناموفق')
        elif result.Status == -33:
            return HttpResponse('رقم تراکنش با رقم پرداخت شده مطابقت ندارد')
        elif result.Status == -34:
            return HttpResponse('رقم وارد شده از حداکثر مجاز عبور کرده')
        else:
            return HttpResponse('پرداخت موفقیت آمیز نبود. وضعیت پرداخت: ' + str(result.Status))
    else:
        return HttpResponse('مشکلی پیش آمده')
"""
