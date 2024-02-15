from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class RegisterForm(forms.ModelForm):
    # email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    con_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'username']
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Bunday foydalanuvchi mavjud! Foydalanuvchi nomini o'zgartiring!")
        if len(username) < 4:
            raise forms.ValidationError(" Foydalanuvchi nomi 4 ta belgidan kam bo'lmasligi kerak!")
        if username.isdigit():  # Faqat sonlardan tashkil topganligini tekshirish
            raise forms.ValidationError("Foydalanuvchi nomi raqamlardan tashkil topishi munkin emas!")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name.isdigit():  # Faqat sonlardan tashkil topganligini tekshirish
            raise forms.ValidationError("Ismingiz raqamlardan tashkil topishi munkin emas!")
        if len(first_name) < 4:
            raise forms.ValidationError("Iltimos! Ismingiz 4 ta belgidan kam kiritmang!")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name.isdigit():  # Faqat sonlardan tashkil topganligini tekshirish
            raise forms.ValidationError("Familyangiz raqamlardan tashkil topishi munkin emas!")
        if len(last_name) < 4:
            raise forms.ValidationError("Iltimos! Familiyangizni 4 ta belgidan kam kiritmang!")
        return last_name

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 4 or len(password) > 8:
            raise forms.ValidationError(" Parolingiz 4 ta va 8 ta belgi oralig'ida bo'lishi kerak!")
        return password

    def clean_con_password(self):
        password = self.cleaned_data.get('password')  # get() ni ishlatamiz
        con_password = self.cleaned_data.get('con_password')
        if password and con_password and password != con_password:
            raise forms.ValidationError("Parollaringiz bir xil emas!")
        return con_password

    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if User.objects.filter(email__iexact=email).exists():
    #         self.add_error("email", _("Bunday email egasi mavjud! Emailni o'zgartiring!"))
    #     return email

    # def save(self, commit=True):
    #     user = super(RegisterForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     user.username = self.cleaned_data['email']
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #     user.password = self.cleaned_data['password']
    #
    #     if commit:
    #         user.save()
    #
    #     return user
    #