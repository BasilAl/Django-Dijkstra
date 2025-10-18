from django import forms


class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(label="Upload CSV File")


class DijkstraForm(forms.Form):
    source = forms.ChoiceField(label="From")
    destination = forms.ChoiceField(label="To")
    optimise_by = forms.ChoiceField(
        label="Optimise By", choices=[("cost", "Cost"), ("time", "Time")]
    )

    def __init__(self, *args, **kwargs):
        graph_nodes = kwargs.pop("graph_nodes", [])
        sorted_nodes = sorted(graph_nodes)
        super().__init__(*args, **kwargs)
        self.fields["source"].choices = [(node, node) for node in sorted_nodes]
        self.fields["destination"].choices = [(node, node) for node in sorted_nodes]
