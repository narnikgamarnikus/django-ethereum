from django.views.generic import DetailView, ListView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django import http


from .models import Ethereum

try:
    _messages = 'django.contrib.messages' in settings.INSTALLED_APPS

except AttributeError:  # pragma: no cover
    _messages = False

if _messages:  # pragma: no cover
    from django.contrib import messages


class EthereumListView(LoginRequiredMixin, ListView):

    model = Ethereum

    def get_queryset(self):
        queryset = super(EthereumListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class EthereumCreateView(LoginRequiredMixin, RedirectView):

    model = Ethereum

    def get(self, request, *args, **kwargs):
        ethereum = Ethereum.objects.create(user=self.request.user)
        url = ethereum.get_absolute_url()
        if url:
            if _messages:
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


class EthereumDetailView(LoginRequiredMixin, DetailView):

    model = Ethereum

    def get_context_data(self, **kwargs):
        context = super(EthereumDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def get_form(self):
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
        tx_hash = self.object.spend(to_address=address, gas=gas, value=value)
        if tx_hash:
            message = _('''%(value)s ETH was successfully sent to %(address)s.
                 Transaction: %(tx_hash)s''' % {
                'value': value,
                'address': address,
                'tx_hash': tx_hash
            })
            messages.success(
                self.request,
                message
            )
