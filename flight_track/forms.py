from django import forms
from .models import AirportRoute

class NthNodeForm(forms.Form):
    """
    Form to select the Nth node (route) for a specific airport and position.

    Fields:
        airport_code (CharField): The IATA/airport code (max length 10).
        position (ChoiceField): Direction of the node, 'L' for Left, 'R' for Right.
        n (IntegerField): The position number of the node to fetch (must be >= 1).
    """
    airport_code = forms.CharField(
        max_length=10,
        label="Airport Code",
        
    )
    position = forms.ChoiceField(
        choices=[('L', 'Left'), ('R', 'Right')],
        label="Position",
        
    )
    n = forms.IntegerField(
        min_value=1,
        label="N",
        
    )
