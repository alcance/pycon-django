from __future__ import absolute_import

import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.timezone import utc

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit

from .models import TalkList, Talk


class TalkListForm(forms.ModelForm):
    class Meta:
        fields = ('name',)
        model = TalkList

    def __init__(self, *args, **kwargs):
        super(TalkListForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            ButtonHolder(
                Submit('create', 'Create')
            )
        )


class TalkForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'host', 'when', 'room',)
        model = Talk

    """docstring for TalkForm"""
    def __init__(self, *args, **kwargs):
        super(TalkForm, self).__init__(*args, **kwargs)
        self.args = args

        self.helper = FormHelper()
        self.helper.layout = Layout(
            'name',
            'host',
            'when',
            'room',
            ButtonHolder(
                Submit('add', 'Add')
            )

        )

    def clean_when(self):
        when = self.cleaned_data.get('when')
        pycon_start = datetime.datetime(2014, 4, 11).replace(tzinfo=utc)
        pycon_end = datetime.datetime(2014, 4, 13, 17).replace(tzinfo=utc)
        if not pycon_start < when < pycon_end:
            raise ValidationError("'when' is outside of python")
        return when
