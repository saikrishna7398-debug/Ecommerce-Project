from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)  # optional, Django adds 'id' by default
    product_name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=300)
    published = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="shop/profile", blank=True, null=True)
    category = models.CharField(max_length=100, default="General")

    def __str__(self):
        return self.product_name
class Contact(models.Model):
    msg_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    desc=models.CharField(max_length=500)


    def __str__(self):
        return self.name
    
class Order(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=500)
    amount=models.IntegerField(default=0)
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    address1=models.CharField(max_length=100)
    address2=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    phone=models.CharField(max_length=100)
    

    def __str__(self):
        return self.name
class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=500)
    timstamps=models.DateField(auto_now_add=True)


    def __str__(self):
        return self.update_desc