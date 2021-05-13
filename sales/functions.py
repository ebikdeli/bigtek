from django.core.mail import send_mail

"""
this func returns a 2_element list:
first element is a string consist of all options(only) seprated by ' '
second element is a string consist of all price(only) seprated by ' '
note that this two elements are respective to each other
"""
def options_to_db(options):    # get options from session
    option_price_list = []
    keys = ''
    values = ''
    print(options)

    for k, v in options.items():
        print(k)
        print(v)
        keys += str(k) + ' '
        values += str(v) + ' '

    option_price_list.append(keys.strip())
    option_price_list.append(values.strip())

    return option_price_list

"""
this func returns a dictionary
keys are the options
values are respective prices to oprions
"""
def db_to_options(options_name, options_price):
    options_price_dict = {}
    names = options_name.split('،')    # in register_order, checkboxes are valued by '،' as separator
    prices = options_price.split(' ')

    # this 4 lines clean data
    if '' in names:
        names.remove('')
    if ' ' in names:
        names.remove(' ')
    if '' or ' ' in prices:
        prices.remove('')
    i = 0
    while i < len(names):
        options_price_dict[names[i]] = prices[i]
        i += 1
    return options_price_dict

"""
this func is for sending email to customers after
selecting their services put still haven't paid for
it
"""
def mail_invoice(customer, options):
    # we should build our 'message' as a long string that contains all the data we want send to our customer
    msg = 'مشخصات سفارش دهنده'
    msg += '\n' + ' <= نام سفارش دهنده' + customer.name
    if customer.company:
        msg += '\n' + ' <= نام شرکت' + customer.company
    msg += '\n' + ' <= نام دامنه' + customer.domain
    msg += '\n' + ' <= ایمیل' + customer.email
    msg += '\n' + ' <= شماره تماس' + customer.phone
    msg = '\nلییت خدمات انتخاب شده:'
    for k, v in options.items():
        if str(v) == 'رایگان':
            msg += '\n' + k + ' => ' + str(v)
            continue
        msg += '\n' + k + ' => ' + str(v) + ' تومان'
    msg += '\nقیمت کل: ' + str(customer.cart.total_price)
    subject = 'لیست خدمات انتخاب شده'
    message = msg
    from_email = 'ebikdeli@gmail.com'
    to_email = ['ebikdeli@yahoo.com']
    send_mail(subject, message, from_email, to_email)
    return 1
