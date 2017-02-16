from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic.base import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from order.models import Meal, Order

class CooksOnlyMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied

        has_permission = request.user.has_perm(self.permission_required)
        if not has_permission:
            raise PermissionDenied
        else:
            return super(CooksOnlyMixin, self).dispatch(request, *args, **kwargs)

class ShowRecipie(CooksOnlyMixin, ListView):
    model=Meal

class ShowOrders(CooksOnlyMixin, ListView):
    model=Order

    def get_queryset(self, *args, **kwargs):
        pass

class ListMenu(ListView):
    model=Meal

class ShowMeal(DetailView):
    model=Meal

class OrderMeal(LoginRequiredMixin, CreateView):
    model=Order
    fields=(
        'meals',
        'address'
    )

    def get_context_data(self, **kwargs):
        context = super(OrderMeal, self).get_context_data(**kwargs)
        context['meals'] = Meal.objects.all()
        return context

from django.views.generic.base import TemplateView
class ViewIng(PermissionRequiredMixin, TemplateView):
    permission_required='order.change_state'
    raise_exception=True
    template_name="test.html"

class ChangeOrderState(PermissionRequiredMixin, UpdateView):
    model=Order
    fields=('state')
    permission_required='order.change_state'
    permission_denied_message="You are none of our cooks!"
    raise_exception=True