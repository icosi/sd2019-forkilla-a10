from django import forms

from .models import Reservation, Review

class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ["day", "time_slot", "num_people"]


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["rate", "message"]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        limited_choices = ["0","1","2"]
        self.fields["rate"].choices = limited_choices

 