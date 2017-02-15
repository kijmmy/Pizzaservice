from django.db import models

# Create your models here.
class Order(models.Model):
    STATES = (
        ('R', 'RECIEVED'),
        ('B', 'BAKING'),
        ('T', 'TRAVEL'),
        ('D', 'DONE'),
        ('E', 'ABBORTED')
    )
    meals = models.ManyToManyField(Prices, through='Toppings')
    address = mdoels.CharField(max_length=1023)
    state = models.CharField(max_length=1, choices=STATES, default='R')

class Toppings(models.Model):
    TOPPINGS=(
        ('MU', 'MUSHROOMS'),
        ('CE', 'CHEESE'),
        ('HM', 'HAM'),
        ('PP', 'PEPPERONI'),
        ('BL', 'BELLPEPPER');
        ('PA', 'PINAPPLE'),
        ('MZ', 'MOZARELLA'),
        ('TN', 'TUNA'),
        ('ON' 'ONIONS'),
        ('SC', 'SAUCE'),
        ('MT', 'MEAT'),
        ('TO', 'TOMATOES')
    )
    meal=models.ForeignKey(Price, on_delete=models.CASCADE)
    order = model.ForeignKey(Order, on_delete=models.CASCADE)
    topping=models.CharField(max_length=2, choices=TOPPINGS)

class Meals(models.Model):
    name = models.CharField(max_length=255)
    recipie = models.TextField()
    description = models.TextField()

class Prices(mdels.Model):
    meal = models.ForeignKey(Meals)
    value = models.DecimalField(decimal_places=2)