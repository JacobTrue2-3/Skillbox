from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

class UserBioForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(label='Your age', min_value=1, max_value=120)
    bio = forms.CharField(label='Biography', widget=forms.Textarea)

#фуннкции валидации (ограничения загрузки файла)
def validate_file_name(file: bytes) -> None:
    if file.name and 'virus' in file.name:
        raise forms.ValidationError('File name should not contain "virus"')
    
def validate_file_size(file: InMemoryUploadedFile) -> None:
    if file.size > 1048576:
        raise forms.ValidationError('File size should not exceed 1MB')
    
def validate_file_extention(file: InMemoryUploadedFile) -> None:
    if not file.content_type in ['image/png', 'image/jpg', 'image/jpeg']:
        raise forms.ValidationError('File type is not supported')

class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name, validate_file_size, validate_file_extention])

