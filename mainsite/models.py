from django.db import models


def customer_directory_path(instance, filename):    # To save users' logo in custom path
    if not instance.email:
        return 'customer_{0}/{1}/{2}'.format(instance.email, instance.domain, filename)
    return '{0}/{1}'.format(instance.domain, filename)
"""
 In fact every customer identified by 'email' and 'domain' fields
"""
class Customers(models.Model):   # Specification & characteristics of customer
    name = models.CharField(max_length=20, verbose_name='نام و نام خانوادگی')
    company = models.CharField(max_length=30, verbose_name='نام شرکت', blank=True)
    phone = models.CharField(max_length=11, verbose_name='شماره تماس')
    email = models.EmailField(verbose_name='ایمیل') # به عنوان مشخصه اضلی شناسایی هر کاربر تعیین می شود
    website_name = models.URLField(blank=True)
    domain = models.CharField(max_length=50, verbose_name='دامنه', unique=True, error_messages={'unique': 'این دامنه قبلا ثبت شده و قابل انتخاب نیست'})
    logo = models.ImageField(upload_to=customer_directory_path, verbose_name='لوگوی موردنظر خود را ارسال کنید')
    isSSL = models.BooleanField(default=False)
    hasOrder = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Customer_db'
        ordering = ['created', 'updated']

    def __str__(self):
        return self.domain

    def save(self, *args, **kwargs):
        if isinstance(self.domain, tuple):
            self.domain = self.domain[0]
        if not self.isSSL:
            self.website_name = "http://www." + str(self.domain)
        else:
            self.website_name = "https://www." + str(self.domain)
        super().save(*args, **kwargs)
