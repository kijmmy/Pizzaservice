from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django import forms
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
class RegisterVisitor(CreateView):
    form_class=UserCreationForm
    template_name='register.html'
    success_url=reverse_lazy('order:menu')

from order.models import Meal, Order, Topping

class ShowRecipie(PermissionRequiredMixin, DetailView):
    model=Meal
    permission_required='order.view_recipie'
    raise_exception=True
    slug_field='pk'
    template_name='order/meal_recipie.html'

class MyOrder(object):
    model=Order

    def get_queryset(self):
        return self.request.user.order_set

class ShowOrders(MyOrder, ListView):
    pass

class ShowOrder(MyOrder, DetailView):
    slug_field='pk'

class ListMenu(ListView):
    model=Meal

class ShowMeal(DetailView):
    model=Meal
    slug_field='pk'

class OrderMealForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OrderMealForm, self).__init__(*args, **kwargs)
        for meal in Meal.objects.all():
            self.fields['price[%i]'%(meal.pk)] = forms.ModelChoiceField(queryset=meal.price_set.all(), label=meal.name+' size (price)', required=False)
            self.fields['topping[%i]'%(meal.pk)]=forms.ChoiceField(choices=Topping.TOPPINGS, label="with topping: ", required=False)

    def order_meals(self):
        self.instance.save()
        for i in Meal.objects.all().values_list('pk'):
            price_pk = self.cleaned_data['price[%i]'%i]
            topping = self.cleaned_data['topping[%i]'%i]
            if price_pk and topping:
                Topping.objects.get_or_create(order=self.instance, meal=price_pk, topping=topping)

    class Meta:
        model=Order
        fields=('address',)

class OrderMeal(LoginRequiredMixin, CreateView):
    form_class = OrderMealForm
    template_name='order/order_form.html'

    def get_context_data(self, **kwargs):
        context = super(OrderMeal, self).get_context_data(**kwargs)
        context['meals'] = Meal.objects.all()
        return context

    def form_valid(self, form):
        #form.user = self.request.user
        form.instance.user = self.request.user
        form.order_meals()
        return super(OrderMeal, self).form_valid(form)

class ListRecievedOrders(PermissionRequiredMixin, ListView):
    model=Order
    permission_required='order.change_state'
    raise_exception=True

class ChangeOrderState(PermissionRequiredMixin, UpdateView):
    model=Order
    slug_field='pk'
    fields=('state',)