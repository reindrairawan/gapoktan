from django import forms

class NIKForm(forms.Form):
    nik = forms.CharField(label='NIK', max_length=16)


class OTPForm(forms.Form):
    otp = forms.CharField(label='Kode OTP', max_length=6)