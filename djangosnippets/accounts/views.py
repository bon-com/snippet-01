from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignupForm
from django.contrib.auth import login, authenticate

# Create your views here.
class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('top')

    # 会員登録後、自動ログインするために必要
    def form_valid(self, form):
      res = super().form_valid(form)
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=password)
      login(self.request, user)
      return res