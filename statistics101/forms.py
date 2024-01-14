from django import forms

# ----------------------------------------------------------------------------
# Classes in this module define forms that are displayed in templates
# ----------------------------------------------------------------------------


# Displayed in login template
class Login(forms.Form):
    username = forms.CharField(
        max_length=50,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Username",
                "label": "",
            }
        ),
    )
    password = forms.CharField(
        max_length=50,
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Password",
                "label": "",
            }
        ),
    )


# Displayed in register template
class Register(forms.Form):
    username = forms.CharField(
        max_length=50,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Username",
                "label": "",
            }
        ),
    )
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Email",
            }
        ),
    )
    password = forms.CharField(
        max_length=50,
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Password",
                "label": "",
            }
        ),
    )
    confirmation = forms.CharField(
        max_length=50,
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
                "placeholder": "Confirm Password",
                "label": "",
            }
        ),
    )
