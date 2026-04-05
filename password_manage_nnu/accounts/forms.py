from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.Form):
    """User registration form including passkey."""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-400 dark:focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Choose a username',
            'id': 'id_username',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-400 dark:focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Enter your email',
            'id': 'id_email',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-400 dark:focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Create a strong password',
            'id': 'id_password',
        })
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-400 dark:focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Confirm your password',
            'id': 'id_password_confirm',
        })
    )
    passkey = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-400 dark:focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Create a passkey for vault operations',
            'id': 'id_passkey',
        }),
        help_text='This passkey will be required to edit or delete vault entries.'
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get('password')
        pw2 = cleaned.get('password_confirm')
        if pw and pw2 and pw != pw2:
            self.add_error('password_confirm', 'Passwords do not match.')
        return cleaned


class LoginForm(AuthenticationForm):
    """Styled login form."""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-400 dark:focus:ring-purple-500 focus:border-transparent transition-all duration-200',
        'placeholder': 'Username',
        'id': 'id_login_username',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-400 dark:focus:ring-purple-500 focus:border-transparent transition-all duration-200',
        'placeholder': 'Password',
        'id': 'id_login_password',
    }))


class PasskeyVerifyForm(forms.Form):
    """Form requesting the user's passkey before sensitive operations."""
    passkey = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-400 dark:focus:ring-purple-500 focus:border-transparent transition-all duration-200',
            'placeholder': 'Enter your passkey',
            'id': 'id_verify_passkey',
        })
    )
