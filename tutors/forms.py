from django import forms
from .models import TutorProfile, Subject

class TutorProfileForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Subjects You Teach"
    )

    class Meta:
        model = TutorProfile
        fields = ['bio', 'hourly_rate', 'profile_pic', 'subjects']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell students about yourself...'}),
            'hourly_rate': forms.NumberInput(attrs={'placeholder': 'e.g. 10'}),
        }
        
class TutorSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search')
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        empty_label='All Subjects'
    )
    max_rate = forms.DecimalField(required=False, label='Max Hourly Rate')