from django import forms


class PreOrderForm(forms.Form):
    name = forms.CharField(
        max_length=150,
        label="Full Name"
    )

    phone = forms.CharField(
        max_length=20,
        label="Phone Number"
    )

    payment_option = forms.ChoiceField(
        choices=[
            ("deposit", "80% Deposit"),
            ("full", "100% Full Payment"),
        ],
        label="Payment Option",
        widget=forms.RadioSelect
    )