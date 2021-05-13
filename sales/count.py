"""
Takes the form and returns a dictionary
contains 1-total price as integer and
2- all selected options and their respective price as a dictionary
"""
def counting(request, form_recv):
    price = 0
    options = {}
    for key, value in form_recv.cleaned_data.items():
            if key == 'api_simple' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 200000
                options[''.join(request.POST.getlist(key))] = 200000

            if key == 'api_intermediary' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 400000
                options[''.join(request.POST.getlist(key))] = 400000

            if key == 'api_advanced' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 600000
                options[''.join(request.POST.getlist(key))] = 600000

            if key == 'search_simple' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 0
                options[''.join(request.POST.getlist(key))] = 'رایگان'

            if key == 'search_advanced' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 300000
                options[''.join(request.POST.getlist(key))] = 300000

            if key == 'filtering_simple' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 100000
                options[''.join(request.POST.getlist(key))] = 100000

            if key == 'filtering_advanced' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 300000
                options[''.join(request.POST.getlist(key))] = 300000

            if key == 'responsive' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 400000
                options[''.join(request.POST.getlist(key))] = 400000

            if key == 'login' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 100000
                options[''.join(request.POST.getlist(key))] = 100000

            if key == 'login_social' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 250000
                options[''.join(request.POST.getlist(key))] = 250000

            if key == 'pgi' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 100000
                options[''.join(request.POST.getlist(key))] = 100000

            if key == 'users_add_content' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 400000
                options[''.join(request.POST.getlist(key))] = 400000

            if key == 'comments' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 100000
                options[''.join(request.POST.getlist(key))] = 'رایگان'

            if key == 'comments_advanced' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 300000
                options[''.join(request.POST.getlist(key))] = 300000

            if key == 'security' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 0
                options[''.join(request.POST.getlist(key))] = 'رایگان'

            if key == 'security_advanced' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 100000
                options[''.join(request.POST.getlist(key))] = 100000

            if key == 'language_add' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 400000
                options[''.join(request.POST.getlist(key))] = 400000

            if key == 'cache' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 300000
                options[''.join(request.POST.getlist(key))] = 300000

            if key == 'seo_simple' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 100000
                options[''.join(request.POST.getlist(key))] = 100000

            if key == 'seo_advanced' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 300000
                options[''.join(request.POST.getlist(key))] = 300000

            if key == 'auth_change' and value == 'True':
                #temp_options.append(''.join(request.POST.getlist(key)))
                price += 400000
                options[''.join(request.POST.getlist(key))] = 400000

    try:
        del(options[''])
    except KeyError:
        pass
    return {'total_price': price, 'options': options}