from django.db import models

# Create your models here.

class Meal(models.Model):
    name = models.CharField(max_length=255)
    recipie = models.TextField()
    description = models.TextField()

    class Meta:
        permissions=(
            ("view_recipie", "Can see everything we put in our 'food'."),
        )

class Price(models.Model):
    SIZES=(
        ('s', 'XSMALL'),
        ('S', 'SMALL'),
        ('M', 'MEDIUM'),
        ('L', 'LARGE'),
        ('X', 'XLARGE')
    )
    meal = models.ForeignKey(Meal)
    size = models.CharField(max_length=1, choices=SIZES)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "%s - %d"%(self.size, self.value)

class Order(models.Model):
    STATES = (
        ('R', 'RECIEVED'),
        ('B', 'BAKING'),
        ('T', 'TRAVEL'),
        ('D', 'DONE'),
        ('E', 'ABBORTED')
    )
    meals = models.ManyToManyField(Price, through='Topping')
    address = models.CharField(max_length=1023)
    state = models.CharField(max_length=1, choices=STATES, default='R')

    def __str__(self):
        return self.address

    class Meta():
        permissions=(
            ('change_state', "Can change what's happening with the food!"),
        )

class Topping(models.Model):
    TOPPINGS=(
        ('MU', 'MUSHROOMS'),
        ('CE', 'CHEESE'),
        ('HM', 'HAM'),
        ('PP', 'PEPPERONI'),
        ('BL', 'BELLPEPPER'),
        ('PA', 'PINAPPLE'),
        ('MZ', 'MOZARELLA'),
        ('TN', 'TUNA'),
        ('ON', 'ONIONS'),
        ('SC', 'SAUCE'),
        ('MT', 'MEAT'),
        ('TO', 'TOMATOES'),
    )
    meal=models.ForeignKey(Price, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    topping=models.CharField(max_length=2, choices=TOPPINGS)