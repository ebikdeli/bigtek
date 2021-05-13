from django import forms
from mainsite.models import Customers
import validators   # pip install validators : simple pkg for validating common things like email and domain and ...
import re   # using regular expression to filter domain & phone & cdomain & cphone
from whois import whois  # pip install python-whois


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customers
        fields = ['name', 'company', 'domain',
                  'email', 'phone', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'id': 'validationCustom01'}),
            'company': forms.TextInput(attrs={'class': 'form-control', 'id': 'validationCustom02'}),
            'domain': forms.TextInput(attrs={'class': 'form-control', 'id': 'validationCustom03', 'placeholder': 'example.com or .ir'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'colFormLabel'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'validatedCustomFile'}),
        }

    def clean_domain(self):
        user_domain = self.cleaned_data['domain']
        regexed = validators.domain(user_domain)
        if not regexed:
            raise forms.ValidationError('دامنه وارد شده صحیح نیست')
        domain = whois(user_domain)
        if domain['emails']:
            raise forms.ValidationError('این نام دامنه قبلا ثبت شده است')
        return user_domain

    def clean_phone(self):
        phone_number = self.cleaned_data['phone']
        regexed_mobile = re.search(r'^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$', phone_number)
        regexed_phone = re.search(r'^0[0-9]{2,}[0-9]{7,}$', phone_number)
        if not regexed_mobile and not regexed_phone:
            if phone_number.startswith('09') or phone_number.startswith('9'):
                raise forms.ValidationError('شماره موبایل وارد شده صحیح نیست')
            else:
                raise forms.ValidationError('شماره تلفن وارد شده صیح نیست')
        return phone_number


class CustomerChangeForm(forms.Form):
    cname = forms.CharField(required=False, label='نام و نام خانوادگی', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'validationCustom01'}))
    ccompany = forms.CharField(required=False, label='نام شرکت', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'validationCustom02'}))
    cdomain = forms.CharField(required=False, label='دامنه', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'validationCustom03'}))
    cphone = forms.CharField(required=False, label='شماره تماس', widget=forms.TextInput(attrs={'class': 'form-control'}))
    clogo = forms.ImageField(required=False, label='لوگوی موردنظر خود را ارسال کنید', widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'validatedCustomFile'}))

    def clean_cdomain(self):
        user_domain = self.cleaned_data['cdomain']
        regexed = validators.domain(user_domain)
        if not regexed:
            raise forms.ValidationError('دامنه وارد شده صحیح نیست')
        domain = whois(user_domain)
        if domain['emails']:
            raise forms.ValidationError('این نام دامنه قبلا ثبت شده است')
        return user_domain

    def clean_cphone(self):
        phone_number = self.changed_data['cphone']
        regexed_mobile = re.search(r'^(?:0|98|\+98|\+980|0098|098|00980)?(9\d{9})$', phone_number)
        regexed_phone = re.search(r'^0[0-9]{2,}[0-9]{7,}$', phone_number)
        if not regexed_mobile and not regexed_phone:
            if phone_number.startswith('09') or phone_number.startswith('9'):
                raise forms.ValidationError('شماره موبایل وارد شده صحیح نیست')
            else:
                raise forms.ValidationError('شماره تلفن وارد شده صیح نیست')
        return phone_number


class HasRegistered(forms.Form):
    email = forms.EmailField(required=False, label='آیا ایمیل مورد نظر ثبت شده؟')
