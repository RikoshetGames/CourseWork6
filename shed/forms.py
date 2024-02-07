from django import forms
from django.forms import DateTimeInput

from shed.models import Mail, Message, Client


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailForm(StyleFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        user = self.request.user
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(user=user)
        self.fields['message'].queryset = Message.objects.filter(user=user)

    class Meta:
        model = Mail
        exclude = ('next_date', 'user', 'is_active',)

        widgets = {
            'start_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
            'end_date': DateTimeInput(attrs={'placeholder': 'ДД.ММ.ГГГГ ЧЧ:ММ:СС', 'type': 'datetime-local'}),
        }


class MailModeratorForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Mail
        fields = ('is_active',)


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('user',)


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        exclude = ('user',)