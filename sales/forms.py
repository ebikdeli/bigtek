from django import forms


class OptionsForm(forms.Form):
    api_simple = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'رابط برنامه نویسی ساده،', 'class': 'uk-checkbox'}), label='API ساده')
    api_intermediary = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'رابط برنامه نویسی متوسط،', 'class': 'uk-checkbox'}), label='API متوسط')
    api_advanced = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'رابط برنامه نویسی پیشرفته،', 'class': 'uk-checkbox'}), label='API پیشرفته')
    search_simple = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': '،سرچ ساده،', 'class': 'uk-checkbox'}), label='سرچ ساده')
    search_advanced = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'سرچ پیشرفته،', 'class': 'uk-checkbox'}), label='سرچ پیشرفته')
    filtering_simple = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'فیلترینگ ساده،', 'class': 'uk-checkbox'}), label='فیلترینگ ساده')
    filtering_advanced = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'فیلترینگ پیشرفته،', 'class': 'uk-checkbox'}), label='فیلترینگ پیشرفته')
    responsive = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'ریسپانسیوسازی کامل،', 'class': 'uk-checkbox'}), label='ریسپانسیوسازی کامل')
    login = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'قابلیت ثبت نام کاربران،', 'class': 'uk-checkbox'}), label='قابلیت ثبت نام کاربران')
    login_social = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'قابلیت لاگین کاربران با استفاده از جی میل گوگل،', 'class': 'uk-checkbox'}), label='قابلیت لاگین کاربران با استفاده از جی میل گوگل')
    pgi = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'درگاه پرداخت(زرین پال)،', 'class': 'uk-checkbox'}), label='درگاه پرداخت(زرین پال)')
    users_add_content = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'امکان پست محتوا توسط کاربران،', 'class': 'uk-checkbox'}), label='امکان پست آنلاین توسط کاربران')
    comments = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'امکان نظرگذاشتن کاربران،', 'class': 'uk-checkbox'}), label='امکان نظرگذاشتن کاربران')
    comments_advanced = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'کامنت گذاری پیشرفته،', 'class': 'uk-checkbox'}), label='کامنت گذاری پیشرفته')
    security = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'امنیت،', 'class': 'uk-checkbox'}), label='امنیت')
    security_advanced = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'امنیت پیشرفته', 'class': 'uk-checkbox'}), label='امنیت پیشرفته')
    language_add = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'اضافه کردن زبان انگلیسی،', 'class': 'uk-checkbox'}), label='اضافه کردن زبان انگلیسی')
    cache = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'قابلیت کش کردن محتوا،', 'class': 'uk-checkbox'}), label='قابلیت کش کردن محتوا')
    seo_simple = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'سئو ساده،', 'class': 'uk-checkbox'}), label='سئو ساده')
    seo_advanced = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'سئو پیشرفته،', 'class': 'uk-checkbox'}), label='سئو پیشرفته')
    auth_change = forms.CharField(required=False, widget=forms.CheckboxInput(attrs={'value': 'تغییر شیوه احراز هویت،', 'class': 'uk-checkbox'}), label='تغییر شیوه احراز هویت')


class OrderTailing(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "example@gmail.com", }), required=True)
