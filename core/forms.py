from django import forms
from .models import ContactSubmission


class ContactForm(forms.ModelForm):
    # Honeypot field for spam protection — must stay empty
    website = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = ContactSubmission
        fields = [
            "name",
            "phone",
            "destination",
            "pickup_location",
            "travel_days",
            "members",
            "room_booking",
            "location_place",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Your Name", "required": True, "autocomplete": "name",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "10-digit Mobile Number", "required": True,
                "autocomplete": "tel", "inputmode": "numeric", "maxlength": "10",
            }),
            "destination": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Where do you want to go?", "required": True,
            }),
            "pickup_location": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Pickup Location", "required": True,
            }),
            "travel_days": forms.NumberInput(attrs={
                "class": "form-control", "min": "1", "max": "60", "required": True,
            }),
            "members": forms.NumberInput(attrs={
                "class": "form-control", "min": "1", "max": "50", "required": True,
            }),
            "room_booking": forms.Select(attrs={
                "class": "form-select",
            }),
            "location_place": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Room booking location",
            }),
        }

        labels = {
            "pickup_location": "Pickup Location",
            "travel_days": "Number of Travel Days",
            "members": "Number of Members",
        }

    def clean_website(self):
        # Honeypot: if this hidden field is filled, it's a bot
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not phone.isdigit() or len(phone) != 10 or phone[0] not in "6789":
            raise forms.ValidationError("Enter a valid 10-digit Indian mobile number.")
        return phone

    def clean(self):
        cleaned_data = super().clean()

        room_booking = cleaned_data.get("room_booking")
        location_place = cleaned_data.get("location_place")

        if room_booking == "Yes" and not location_place:
            self.add_error(
                "location_place",
                "Please enter the booking location."
            )

        return cleaned_data