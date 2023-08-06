import json

from django.forms import Widget
from django.template.loader import render_to_string


class JsonPairInputs(Widget):
    """
    A widget to display JsonField as a list of select field pairs that represent two models.

    Usage:
    class ArticleAdminForm(forms.ModelForm):
        class Meta:
            widgets = {
                'authors': JsonPairInputs(User, Role)
            }

    """

    def __init__(self, model1, model2, sort_field_model1: str = None, sort_field_model2: str = None, *args, **kwargs):
        """
        A widget to display JsonField as a list of select field pairs that represent two models.

        kwargs:
        key_attrs -- html attributes applied to the 1st input box pairs
        val_attrs -- html attributes applied to the 2nd input box pairs

        """
        self.key_attrs = {}
        self.val_attrs = {}
        if "key_attrs" in kwargs:
            self.key_attrs = kwargs.pop("key_attrs")
        if "val_attrs" in kwargs:
            self.val_attrs = kwargs.pop("val_attrs")
        Widget.__init__(self, *args, **kwargs)

        self.col1 = model1.objects.all()
        self.col2 = model2.objects.all()

        if sort_field_model1 is not None:
            self.col1 = model1.objects.order_by(sort_field_model1).all()
        if sort_field_model2 is not None:
            self.col2 = model2.objects.order_by(sort_field_model2).all()

    def render(self, name, value, attrs=None, renderer=None) -> str:
        """

        Renders widget into an html string

        :param name: field name
        :param value: json string of a two-tuple list automatically passed in by django
        :param attrs: automatically passed in by django (unused)
        :param renderer: automatically passed in by django (unused)
        :return: rendered string
        """
        if value is None or value.strip() is '':
            value = '{}'

        context = {
            "col1": self.col1,
            "col2": self.col2,
            "json": json.loads(value),
            "name": name
        }

        return render_to_string('json_model_widget/json_model_widget.html', context=context)

    def value_from_datadict(self, data, files, name) -> str:
        """
        Returns the json representation of the key-value pairs
        sent in the POST parameters

        :param data: request.POST or request.GET parameters
        :param files: request.FILES
        :param name: the name of the field associated with this widget
        :return: stringified json
        """
        res = {}

        if f'jsonkey{name}' in data and f'jsonvalue{name}' in data:
            keys = data.getlist(f'jsonkey{name}')
            values = list(map(int, data.getlist(f'jsonvalue{name}')))
            res = dict(zip(keys, values))
        return json.dumps(res)
