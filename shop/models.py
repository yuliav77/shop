from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	phone = models.CharField(max_length=13)
	pass
	
	def serialize(self):
		return {
			"id": self.id,
			"phone": self.phone,
			"email": self.email,
			"username": self.username,
			"first_name": self.first_name,
			"staff": self.is_staff
		}

	
class Product(models.Model):
	name = models.CharField(max_length=100,blank=False)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	unit = models.CharField(max_length=12)
	photo = models.ImageField(upload_to = 'pic_folder', default = 'pic_folder/None/no-img.jpg')
	top = models.BooleanField(default = False)
	
	def serialize(self):
		return {
           "id": self.id,
           "name": self.name,
           "description": self.description,
			"price": self.price,
			"unit": self.unit,
			"photo": self.photo,
			"top": self.top
		}


class Item(models.Model):
	product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="items")
	amount = models.IntegerField()
	
	
class Order(models.Model):
	items = models.ManyToManyField("Item", related_name="orders_with_items")
	customer = models.ForeignKey("User", on_delete=models.CASCADE, related_name="ordered")
	sum = models.DecimalField(max_digits=12, decimal_places=2)
	timestamp = models.DateTimeField(auto_now_add=True)
	comment = models.TextField(blank=True)
	
	def serialize(self):
		return {
           "id": self.id,
           "items": [[item.product.name, item.amount] for item in self.items.all()],
           "customer":[self.customer.username, self.customer.first_name, self.customer.phone],
		   "sum": self.sum,
		   "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
			"comment": self.comment
		}
