from django import forms
from .models import ContactSubmission,RoomBooking


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
            "start_date",
            "return_date",
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
            "start_date": forms.DateInput(attrs={
                "class": "form-control", "type": "date", "required": True,
            }),
            "return_date": forms.DateInput(attrs={
                "class": "form-control", "type": "date", "required": True,
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
            "start_date": "Travel Start Date",
            "return_date": "Travel Return Date",
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

        start_date = cleaned_data.get("start_date")
        return_date = cleaned_data.get("return_date")
        if start_date and return_date and return_date < start_date:
            self.add_error("return_date", "Return date cannot be before the start date.")

        return cleaned_data
    
    from .models import RoomBooking

class RoomBookingForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = RoomBooking
        fields = ["name", "phone", "email", "location", "check_in_date", "check_out_date",
                  "room_type", "number_of_rooms", "number_of_guests", "special_requests"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your Name", "required": True}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "10-digit Mobile Number", "required": True, "inputmode": "numeric", "maxlength": "10"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email (optional)"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Munnar, Ooty", "required": True}),
            "check_in_date": forms.DateInput(attrs={"class": "form-control", "type": "date", "required": True}),
            "check_out_date": forms.DateInput(attrs={"class": "form-control", "type": "date", "required": True}),
            "room_type": forms.Select(attrs={"class": "form-select"}),
            "number_of_rooms": forms.NumberInput(attrs={"class": "form-control", "min": "1", "max": "20"}),
            "number_of_guests": forms.NumberInput(attrs={"class": "form-control", "min": "1", "max": "50"}),
            "special_requests": forms.Textarea(attrs={"class": "form-control", "rows": "3"}),
        }
        labels = {"location": "Preferred Stay Location", "check_in_date": "Check-in Date", "check_out_date": "Check-out Date"}

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return self.cleaned_data.get("website")

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()
        if not phone.isdigit() or len(phone) != 10 or phone[0] not in "6789":
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in_date")
        check_out = cleaned_data.get("check_out_date")
        if check_in and check_out and check_out <= check_in:
            self.add_error("check_out_date", "Check-out must be after check-in.")
        return cleaned_data