from django import forms

from catalog.models import Product


FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "image",
            "category",
            "price",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({"class": "form-check-input"})
            else:
                field.widget.attrs.update({"class": "form-control"})

    def clean_name(self):
        name = self.cleaned_data.get("name")
        self._validate_forbidden_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        self._validate_forbidden_words(description)
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")

        if price is not None and price < 0:
            raise forms.ValidationError(
                "Цена продукта не может быть отрицательной."
            )

        return price

    @staticmethod
    def _validate_forbidden_words(value):
        if not value:
            return

        value_lower = value.lower()

        for word in FORBIDDEN_WORDS:
            if word in value_lower:
                raise forms.ValidationError(
                    f"Нельзя использовать запрещённое слово: {word}."
                )
