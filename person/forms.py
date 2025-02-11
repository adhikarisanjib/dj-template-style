from django import forms

from .models import Person, Address, Contact


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        # fields = '__all__'
        fields = ['name', 'birth_date', 'age', 'bio', 'photo']

        widgets = {
            "name": forms.TextInput(attrs={'class': 'px-4 py-2 border bg-gray-50 dark:bg-gray-800 rounded'}),
            "age": forms.NumberInput(attrs={'class': 'px-4 py-2 border bg-gray-50 dark:bg-gray-800 rounded'}),
            "birth_date": forms.DateInput(attrs={'class': 'px-4 py-2 border bg-gray-50 dark:bg-gray-800 rounded', 'type': 'date'}),
            "bio": forms.Textarea(attrs={'class': 'px-4 py-2 border bg-gray-50 dark:bg-gray-800 rounded'}),
            "photo": forms.FileInput(attrs={'class': 'px-4 py-2 border bg-gray-50 dark:bg-gray-800 rounded'}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        # fields = '__all__'
        fields = ['street', 'city', 'state']

        widgets = {
            "street": forms.TextInput(attrs={'class': 'px-4 py-2 border bg-gray-50 dark:bg-gray-800 rounded'}),
            "city": forms.TextInput(attrs={'class': 'px-4 py-2 border bg-gray-50 dark:bg-gray-800 rounded'}),
            "state": forms.TextInput(attrs={'class': 'px-4 py-2 border bg-gray-50 dark:bg-gray-800 rounded'}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        # fields = '__all__'
        fields = ['kind', 'value']

        widgets = {
            "kind": forms.Select(attrs={'class': 'px-4 py-2 border bg-gray-50 dark:bg-gray-800 rounded'}),
            "value": forms.TextInput(attrs={'class': 'px-4 py-2 border bg-gray-50 dark:bg-gray-800 rounded'}),
        }
