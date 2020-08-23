from django import forms


class ModelExampleForm(forms.ModelForm):

    occupation = forms.ChoiceField(choices=[
        ('study', 'Study'),
        ('work', 'Work')
    ], )
    study = forms.CharField(label='Name Institution', required=False,
                            widget=forms.TextInput(attrs={'class': "occupation j__study"}))
    semester = forms.CharField(label='Semester', required=False,
                               widget=forms.TextInput(attrs={'class': "occupation j__study"}))
    company = forms.CharField(required=False,
                              widget=forms.TextInput(attrs={'class': "occupation j__work"}))
    position = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={'class': "occupation j__work"}))

    photo = forms.BooleanField(required=False, label='Add photo?', help_text='Select if you want to add a photo',
                               widget=forms.CheckboxInput())
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': "j__photo"}))
