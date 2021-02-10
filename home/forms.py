from django import forms
from django.forms import modelformset_factory
from .models import Organization, App, List, ListField


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control form-control-solid'}),
        }


class AppForm(forms.ModelForm): #(Workspaces)

    class Meta:
        model = App
        fields = ('name',)

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control form-control-solid'}),
        }


class ListForm(forms.ModelForm): #(Workspaces)

    class Meta:
        model = List
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(attrs={
                'class':'form-control form-control-solid p-3',
                'placeholder': 'Enter a name for this list',
                }
            )
        }


ListFieldFormset = modelformset_factory(
    ListField,
    fields = ('field_label', 'field_type', 'required', 'visible', 'select_list'),
    extra=1,
    can_order=True,
    can_delete=True,
    widgets = {
        'field_label': forms.TextInput(attrs={
            'class': 'form-control form-control-solid py-1',
            'placeholder': 'Enter a label for this field',
            'required': '',
            }
        ),
        'field_type': forms.Select(attrs={
            'class': 'form-control form-control-solid py-1 field-type-custom'
            }
        ),
        'select_list': forms.Select(attrs={
            'class': 'form-control form-control-solid py-1 select-type-custom',
            'style': 'display:none;'
            }
        ),
        'required': forms.CheckboxInput(attrs={
            'class': 'form-check-input'
            }
        ),
        'visible': forms.CheckboxInput(attrs={
            'class': 'form-check-input'
            }
        )
    }
)
