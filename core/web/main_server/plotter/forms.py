from django import forms

class HelicopterParametersForm(forms.Form):
    hor_c = forms.IntegerField(min_value=1, max_value=10**9, label='Horizontal sq. count')
    vert_c = forms.IntegerField(min_value=1, max_value=10**9, label='Vertical sq. count')
    side = forms.IntegerField(min_value=1)

    class Meta:
        fields = ['hor_c', 'vert_c', 'side']
