from django import forms


class  Loginform(forms.Form):

    
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
   
   
    


