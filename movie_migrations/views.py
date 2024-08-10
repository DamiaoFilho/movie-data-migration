from django.views.generic import FormView
from .forms import MigrationForm


class MigrationView(FormView):
    template_name = "base.html"
    form_class = MigrationForm
    