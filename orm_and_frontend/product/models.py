from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product_Table(models.Model):
    name = models.CharField(max_length = 50)
    price = models.FloatField()
    details = models.CharField(max_length = 100)

    CATEGORIES = (
        (1,'Mobile'),
        (2,'Clothes'),
        (3,'Shoes')
    )
    category = models.IntegerField(choices = CATEGORIES)

    is_active = models.BooleanField()
    rating = models.FloatField()
    image = models.ImageField(upload_to='image')

    def __str__(self):
        msg = "Product "+self.name+" added successfully!"
        return msg
    

class Cart_Table(models.Model):
    uid = models.ForeignKey(User, on_delete = models.CASCADE, db_column="uid")
    pid = models.ForeignKey(Product_Table, on_delete = models.CASCADE, db_column="pid")
    quantity = models.IntegerField(default=1)
    
class OrderTable(models.Model):
    order_id=models.CharField(max_length=50)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Product_Table,on_delete=models.CASCADE,db_column='pid')
    quantity=models.IntegerField()

class CustomerDetails(models.Model):
    Address_type=(('home','Home'),("office",'Office'),('other','Other'))
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=30)
    email=models.EmailField( max_length=25)
    address_type=models.CharField(max_length=10,choices=Address_type)
    full_address=models.CharField(max_length=200)
    pincode=models.CharField(max_length=30)
    
