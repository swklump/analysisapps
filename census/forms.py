# from django import forms
# from django.forms import ModelForm
# from .models import DP04, DP05
# fields_list = ['DP04_0001PE', 'DP04_0002PE', 'DP04_0003PE', 'DP04_0004PE', 'DP04_0005PE', 'DP04_0006PE', 'DP04_0007PE', 'DP04_0008PE', 'DP04_0009PE', 'DP04_0010PE', 'DP04_0011PE', 'DP04_0012PE', 'DP04_0013PE', 'DP04_0014PE', 'DP04_0015PE', 'DP04_0016PE', 'DP04_0017PE', 'DP04_0018PE', 'DP04_0019PE', 'DP04_0020PE', 'DP04_0021PE', 'DP04_0022PE', 'DP04_0023PE', 'DP04_0024PE', 'DP04_0025PE', 'DP04_0026PE', 'DP04_0027PE', 'DP04_0028PE', 'DP04_0029PE', 'DP04_0030PE', 'DP04_0031PE', 'DP04_0032PE', 'DP04_0033PE', 'DP04_0034PE', 'DP04_0035PE', 'DP04_0036PE', 'DP04_0037PE', 'DP04_0038PE', 'DP04_0039PE', 'DP04_0040PE', 'DP04_0041PE', 'DP04_0042PE', 'DP04_0043PE', 'DP04_0044PE', 'DP04_0045PE', 'DP04_0046PE', 'DP04_0047PE', 'DP04_0048PE', 'DP04_0049PE', 'DP04_0050PE', 'DP04_0051PE', 'DP04_0052PE', 'DP04_0053PE', 'DP04_0054PE', 'DP04_0055PE', 'DP04_0056PE', 'DP04_0057PE', 'DP04_0058PE', 'DP04_0059PE', 'DP04_0060PE', 'DP04_0061PE', 'DP04_0062PE', 'DP04_0063PE', 'DP04_0064PE', 'DP04_0065PE', 'DP04_0066PE', 'DP04_0067PE', 'DP04_0068PE', 'DP04_0069PE', 'DP04_0070PE', 'DP04_0071PE', 'DP04_0072PE', 'DP04_0073PE', 'DP04_0074PE', 'DP04_0075PE', 'DP04_0076PE', 'DP04_0077PE', 'DP04_0078PE', 'DP04_0079PE', 'DP04_0080PE', 'DP04_0081PE', 'DP04_0082PE', 'DP04_0083PE', 'DP04_0084PE', 'DP04_0085PE', 'DP04_0086PE', 'DP04_0087PE', 'DP04_0088PE', 'DP04_0089PE', 'DP04_0090PE', 'DP04_0091PE', 'DP04_0092PE', 'DP04_0093PE', 'DP04_0094PE', 'DP04_0095PE', 'DP04_0096PE', 'DP04_0097PE', 'DP04_0098PE', 'DP04_0099PE', 'DP04_0100PE', 'DP04_0101PE', 'DP04_0102PE', 'DP04_0103PE', 'DP04_0104PE', 'DP04_0105PE', 'DP04_0106PE', 'DP04_0107PE', 'DP04_0108PE', 'DP04_0109PE', 'DP04_0110PE', 'DP04_0111PE', 'DP04_0112PE', 'DP04_0113PE', 'DP04_0114PE', 'DP04_0115PE', 'DP04_0116PE', 'DP04_0117PE', 'DP04_0118PE', 'DP04_0119PE', 'DP04_0120PE', 'DP04_0121PE', 'DP04_0122PE', 'DP04_0123PE', 'DP04_0124PE', 'DP04_0125PE', 'DP04_0126PE', 'DP04_0127PE', 'DP04_0128PE', 'DP04_0129PE', 'DP04_0130PE', 'DP04_0131PE', 'DP04_0132PE', 'DP04_0133PE', 'DP04_0134PE', 'DP04_0135PE', 'DP04_0136PE', 'DP04_0137PE', 'DP04_0138PE', 'DP04_0139PE', 'DP04_0140PE', 'DP04_0141PE', 'DP04_0142PE', 'DP04_0143PE', 'GEO_ID', 'NAME', 'state', 'county', 'tract']

# # Create form
# class DP04Form(ModelForm):
#     class Meta:
#         model = DP04
#         # OPTIONS = (('DP04_0001PE', 'DP04_0001PE'),('DP04_0002PE','DP04_0002PE',),('DP04_0003PE','DP04_0003PE'))
#         # col_select = forms.ChoiceField(choices=OPTIONS)
#         fields = ('geo_id')

#         # stylize forms with bootstrap
#         # labels = { f:'' for f in fields_list}
#         # widgets = { f:forms.TextInput(attrs={'class':'form-control','placeholder':f + '...'}) for f in fields_list}

#         geo_id = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}))

#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             self.fields['geo_id'].choices= [(d.geo_id, d.geo_id) for d in DP04.objects.all()]
