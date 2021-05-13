from django.db import models
from mainsite.models import Customers


class Cart(models.Model):   # Cart of every registered email
    customer = models.OneToOneField(Customers,
                                    on_delete=models.CASCADE,
                                    related_name='cart')
    total_price = models.PositiveIntegerField(default=0)
    options = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart'
        ordering = ['created', 'updated']

    def __str__(self):
        return self.customer.email + ", total price: " + str(self.total_price)


class Orders(models.Model):
    customer = models.ForeignKey(Customers,
                                 on_delete=models.CASCADE,
                                 related_name='orders')
    price = models.PositiveIntegerField()
    discount = models.FloatField()
    paid = models.PositiveIntegerField()
    remain = models.PositiveIntegerField()
    paid_method = models.CharField(max_length=10)
    domain = models.URLField()
    options_name = models.CharField(max_length=400)
    options_price = models.CharField(max_length=100)
    order_id = models.CharField(max_length=5)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order'
        ordering = ['created']

    def __str__(self):
        return self.customer.email + ': ' + self.order_id

    def save(self, *args, **kwargs):
        self.remain = self.price - self.paid
        super().save(*args, **kwargs)


class ActiveProjects(models.Model):     # List of active project of any customer(Admin only)
    customer = models.ForeignKey(Customers,
                                 related_name='active_projects',
                                 on_delete=models.CASCADE)
    order = models.OneToOneField(Orders,
                                 related_name='order',
                                 on_delete=models.CASCADE
                                 )
    order_number = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'active_projects'
        ordering = ['created']

    def __str__(self):
        return self.customer.email + ': ' + self.order_number

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.order.order_id
        super().save(*args, **kwargs)


class PayId(models.Model):
    order = models.ForeignKey(Orders,
                              on_delete=models.CASCADE,
                              related_name='all_pays')
    pay_amount = models.PositiveIntegerField()
    pay_id = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pay_id'
        ordering = ['-created']

    def __str__(self):
        return self.pay_id
