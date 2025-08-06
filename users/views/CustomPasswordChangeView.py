from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from ..forms import CustomPasswordChangeForm

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'user/change_password.html'  
    success_url = reverse_lazy('profile')  
