import re
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import Usuario


# ─────────────────────────────────────────────
# Mixin reutilizable: trim + validación de solo espacios
# ─────────────────────────────────────────────

class TrimMixin:
    """
    Elimina espacios al inicio y al final de todos los campos CharField/EmailField.
    Rechaza campos que queden vacíos tras el trim.
    """
    def clean(self):
        cleaned = super().clean()
        for field_name, value in cleaned.items():
            if isinstance(value, str):
                stripped = value.strip()
                if stripped != value:
                    cleaned[field_name] = stripped
                # Si tras el trim queda vacío y el campo es requerido, error
                if not stripped and self.fields.get(field_name) and self.fields[field_name].required:
                    self.add_error(field_name, 'Este campo no puede contener solo espacios.')
        return cleaned


# ─────────────────────────────────────────────
# Registro
# ─────────────────────────────────────────────

class RegistroUsuarioForm(TrimMixin, UserCreationForm):
    """Formulario de registro con validaciones estrictas."""

    email = forms.EmailField(
        required=True,
        label='Correo electrónico',
        max_length=150,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com',
            'maxlength': '150',
        }),
    )
    first_name = forms.CharField(
        required=True,
        label='Nombre',
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre',
            'maxlength': '50',
        }),
    )
    last_name = forms.CharField(
        required=True,
        label='Apellido',
        min_length=2,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido',
            'maxlength': '50',
        }),
    )

    class Meta:
        model = Usuario
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario',
                'maxlength': '50',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].max_length = 50
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_first_name(self):
        value = self.cleaned_data.get('first_name', '').strip()
        if not value:
            raise ValidationError('El nombre no puede estar vacío ni contener solo espacios.')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]+$', value):
            raise ValidationError('El nombre solo puede contener letras, espacios y guiones.')
        return value

    def clean_last_name(self):
        value = self.cleaned_data.get('last_name', '').strip()
        if not value:
            raise ValidationError('El apellido no puede estar vacío ni contener solo espacios.')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]+$', value):
            raise ValidationError('El apellido solo puede contener letras, espacios y guiones.')
        return value

    def clean_username(self):
        value = self.cleaned_data.get('username', '').strip()
        if not value:
            raise ValidationError('El nombre de usuario no puede estar vacío.')
        if ' ' in value:
            raise ValidationError('El nombre de usuario no puede contener espacios.')
        if not re.match(r'^[\w\-]+$', value):
            raise ValidationError('El usuario solo puede contener letras, números, guiones y guiones bajos.')
        return value

    def clean_email(self):
        value = self.cleaned_data.get('email', '').strip().lower()
        if not value:
            raise ValidationError('El correo no puede estar vacío.')
        if Usuario.objects.filter(email=value).exists():
            raise ValidationError('Ya existe una cuenta con este correo electrónico.')
        return value

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.rol = Usuario.ROL_OPERADOR
        if commit:
            user.save()
        return user


# ─────────────────────────────────────────────
# Login
# ─────────────────────────────────────────────

class LoginForm(TrimMixin, AuthenticationForm):
    """Formulario de login con estilos Bootstrap y trim automático."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre de usuario',
            'maxlength': '50',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña',
        })

    def clean_username(self):
        value = self.cleaned_data.get('username', '').strip()
        if not value:
            raise ValidationError('Ingresa tu nombre de usuario.')
        return value


# ─────────────────────────────────────────────
# Perfil
# ─────────────────────────────────────────────

class PerfilUsuarioForm(TrimMixin, forms.ModelForm):
    """Formulario para editar el perfil del usuario con validaciones."""

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '50'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'maxlength': '150'}),
        }
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
        }

    def clean_first_name(self):
        value = self.cleaned_data.get('first_name', '').strip()
        if not value:
            raise ValidationError('El nombre no puede estar vacío.')
        if len(value) < 2:
            raise ValidationError('El nombre debe tener al menos 2 caracteres.')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]+$', value):
            raise ValidationError('El nombre solo puede contener letras, espacios y guiones.')
        return value

    def clean_last_name(self):
        value = self.cleaned_data.get('last_name', '').strip()
        if not value:
            raise ValidationError('El apellido no puede estar vacío.')
        if len(value) < 2:
            raise ValidationError('El apellido debe tener al menos 2 caracteres.')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s\-]+$', value):
            raise ValidationError('El apellido solo puede contener letras, espacios y guiones.')
        return value

    def clean_email(self):
        value = self.cleaned_data.get('email', '').strip().lower()
        if not value:
            raise ValidationError('El correo no puede estar vacío.')
        # Verificar que el email no lo use otro usuario
        qs = Usuario.objects.filter(email=value).exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Este correo ya está en uso por otra cuenta.')
        return value
