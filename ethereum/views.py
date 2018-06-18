from django.views.generic import DetailView, ListView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.urls import reverse
from django.conf import settings
from django import http


from .models import Ethereum
from .forms import EthereumPayForm

try:
    _messages = 'django.contrib.messages' in settings.INSTALLED_APPS

except AttributeError:  # pragma: no cover
    _messages = False

if _messages:  # pragma: no cover
    from django.contrib import messages


class EthereumListView(LoginRequiredMixin, ListView):

    model = Ethereum
    paginate_by = 10

    def get_queryset(self):
        queryset = super(EthereumListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class EthereumCreateView(LoginRequiredMixin, RedirectView):

    model = Ethereum

    def get(self, request, *args, **kwargs):
        ethereum = Ethereum.objects.create(user=self.request.user)
        url = ethereum.get_absolute_url()
        if url:
            if _messages:  # pragma: no cover
                messages.success(
                    self.request,
                    _('New address %(address)self successfully created' % {
                        'address': ethereum.address
                    })
                )
        if self.permanent:
            return http.HttpResponsePermanentRedirect(url)
        else:
            return http.HttpResponseRedirect(url)
        return super(EthereumCreateView, self).get(request, *args, **kwargs)


class EthereumDetailView(LoginRequiredMixin,
                         FormMixin, DetailView):

    model = Ethereum
    form_class = EthereumPayForm

    def get_object(self):
        obj = get_object_or_404(Ethereum, pk=self.kwargs['pk'])
        if obj.user == self.request.user:
            return obj
        raise PermissionDenied()

    def get_context_data(self, **kwargs):
        context = super(EthereumDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_form(self):
        if self.request.POST:
            return self.form_class(data=self.request.POST)
        return self.form_class()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        address = form.cleaned_data['address']
        gas = form.cleaned_data['gas']
        value = form.cleaned_data['value']
        message = None
        try:
            tx_hash = self.object.spend(to_address=address, gas=gas,
                                        value=value)
        except Exception as e:
            if 'message' in e.args[0]:
                message = e.args[0]['message'].capitalize()
            tx_hash = None

        if tx_hash:
            if _messages:  # pragma: no cover
                message = _('''%(value)s ETH was successfully
                     sent to %(address)s. Transaction: %(tx_hash)s''' % {
                    'value': value,
                    'address': address,
                    'tx_hash': tx_hash
                })
                messages.success(
                    self.request,
                    message
                )
        else:
            if _messages:  # pragma: no cover
                if not message:
                    message = _('''Something wrong, try again later''')
                messages.error(
                    self.request,
                    message
                )
        self.success_url = reverse(
            'ethereum_detail', kwargs={'pk': self.object.pk}
        )
        return redirect(self.success_url)
