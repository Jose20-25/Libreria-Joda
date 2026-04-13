from django import forms
from .models import Cliente


class ClienteRegistroForm(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre completo',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ej: María García López',
            'autofocus': True,
        })
    )
    telefono = forms.CharField(
        label='Teléfono / WhatsApp',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ej: 5512345678',
            'type': 'tel',
        })
    )

    class Meta:
        model = Cliente
        fields = ('nombre', 'telefono')

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        # Solo permitir dígitos, espacios, +, - y paréntesis
        import re
        if not re.match(r'^[\d\s\+\-\(\)]{7,20}$', telefono):
            raise forms.ValidationError('Ingresa un número de teléfono válido.')
        return telefono
