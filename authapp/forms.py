from django import forms
from django.contrib.auth.forms import UserCreationForm, \
    AuthenticationForm, UserChangeForm

from authapp.models import ShopUser


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = (
            "username", "first_name", "email", "age",
            "password1", "password2",
        )

    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}))
    age = forms.IntegerField(
        label="Возраст",
        widget=forms.NumberInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(
        label="Повтор пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_age(self):
        data = self.cleaned_data["age"]
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")
        return data

# class ShopUserEditForm(forms.ModelForm):
#     class Meta:
#         model = ShopUser
#         fields = (
#             "username", "first_name", "last_name", "email"
#         )

class ShopUserEditForm(forms.ModelForm):
    class Meta:
        model = ShopUser
        fields = (
            "username", "first_name", "last_name", "email",
        )

    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(
        label="Фамилия",
        widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}))


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ("username", "password")

    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
