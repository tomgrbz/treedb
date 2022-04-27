from django import forms



class CreateNewTree(forms.Form):
    scientific_name = forms.CharField(label="Scientific Name", max_length=64)
    street = forms.CharField(label="Street", max_length=64)
    neighborhood = forms.CharField(label="Neigborhood", max_length=64)
    alive = forms.BooleanField(required=False)
    radius = forms.DecimalField(label='Current Radius')
    rad_year = forms.IntegerField(label='Year this Radius was measured')
    rad_month = forms.IntegerField(label='Month this Radius was measured')
    biomass = forms.DecimalField(label="Biomass at time of recording")
    desc = forms.CharField(label='Description of the Tree:')
    #add stuff for calculation/biomass/radius data/result


class DeleteForm(forms.Form):
    confirmation = forms.CharField(label="Please Type Confirm that you would like to delete this tree")



