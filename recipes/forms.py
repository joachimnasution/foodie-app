from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search for recipes...", "class": "form-control mr-sm-2"},
            ),
    )
