from django import forms
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError

class MultiSelectFormField(forms.MultipleChoiceField):
    widget = forms.CheckboxSelectMultiple
    
    def __init__(self, *args, **kwargs):
        self.max_choices = kwargs.pop('max_choices', 0)
        super(MultiSelectFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        if value and self.max_choices and len(value) > self.max_choices:
            raise forms.ValidationError('You must select a maximum of %s choice%s.'
                    % (apnumber(self.max_choices), pluralize(self.max_choices)))
        return value

class MultiSelectField(models.CharField):

    def __init__(self, choices, *args, **kwargs):
        kwargs['max_length']=len(','.join(dict(choices).keys()))
        kwargs['choices'] = choices
        super(MultiSelectField, self).__init__(*args, **kwargs)

    def get_choices_default(self):
        return self.get_choices(include_blank=False)

    def _get_FIELD_display(self, field):
        value = getattr(self, field.attname)
        choicedict = dict(field.choices)

    def formfield(self, **kwargs):
        # don't call super, as that overrides default widget if it has choices
        defaults = {'required': not self.blank, 'label': self.verbose_name.title(), 
                    'help_text': self.help_text, 'choices':self.choices}
        if self.has_default():
            defaults['initial'] = self.get_default()
        defaults.update(kwargs)
        return MultiSelectFormField(**defaults)

    def validate(self, values, instance):
        self.clean(values)

    def clean(self, values):
        if isinstance(values, str):
            values = values.split(',')
        if not isinstance(values, list):
            raise ValidationError("choices has ot be list or coma-sperated string")
        ret=[]
        for value in values:
            if value == '':
                continue
            if value not in dict(self.choices).keys() and value not in dict(self.choices).values():
                raise ValidationError("Not one of the choices")
            else:
                ret.append(dict(self.choices).get(value, value))
        return ret

    def get_db_prep_value(self, value, *args, **kwargs):
        self.validate(value, self)
        if isinstance(value, list):
            return ",".join(value)
        elif isinstance(value, str):
            return value
        else:
            return repr(value)

    def to_python(self, value):
        print("DTHEASDF")
        if isinstance(value, list):
            return value
        return self.clean(value)

    def contribute_to_class(self, cls, name):
        super(MultiSelectField, self).contribute_to_class(cls, name)
        if self.choices:
            func = lambda self, fieldname = name, choicedict = dict(self.choices):",".join([choicedict.get(value,value) for value in getattr(self,fieldname)])
            setattr(cls, 'get_%s_display' % self.name, func)

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
    includes={
        's':0,
        'S':2,
        'M':2,
        'L':3,
        'X':5
    }
    meal = models.ForeignKey(Meal)
    size = models.CharField(max_length=1, choices=SIZES)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "%s - %d"%(self.size, self.value)

    @property
    def included(self):
        if len(self.size) > 1:
            for s, size in self.SIZES:
                if size == self.size:
                    self.size = s
        return self.includes[self.size]

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def get_absolute_url(self):
        return reverse('order:track_order', kwargs={'slug':self.pk})

    def __str__(self):
        return self.address

    class Meta():
        permissions=(
            ('change_state', "Can change what's happening with the food!"),
        )

TOPPING_PRICE=5

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
    toppings = MultiSelectField(choices=TOPPINGS)

    def save(self, *args, **kwargs):
        if self.count > self.meal.included:
            raise ValidationError("TOO MANY TOPPINGS!")
        super(Topping, self).save(*args, **kwargs)

    @property
    def count(self):
        return len(MultiSelectField(choices=self.TOPPINGS).clean(self.toppings))

    @property
    def price(self):
        return TOPPING_PRICE*self.count + self.meal.value
