import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django import forms
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import FormMixin, ModelFormMixin
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, ButtonHolder, Column, Div, Layout, Row, Submit

# User = get_user_model()



class ReadOnlyModelFormMixin(ModelFormMixin):
    def get_form(self, form_class=None):
        form = super(ReadOnlyModelFormMixin, self).get_form()

        for field in form.fields:
            # Set html attributes as needed for all fields
            form.fields[field].widget.attrs["readonly"] = "readonly"
            form.fields[field].widget.attrs["disabled"] = "disabled"

        return form

    def form_valid(self, form):
        """
        Called when form is submitted and form.is_valid()
        """
        return self.form_valid(form)