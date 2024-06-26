from django import forms
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Department

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    employee_code = forms.CharField(required=True)  # Add employee code field
    
    widget = {
        'password': forms.PasswordInput(),
    }

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        if kwargs.get('instance'):
            instance = kwargs.get('instance')
            self.fields['password'].required = False
            for field in CustomUser._meta.fields:
                if field.name not in ['id', 'user_ptr', 'password']:  # Exclude inherited fields
                    self.fields[field.name].initial = getattr(instance, field.name)
            if instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"
        else:
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if self.instance.pk is None: 
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError("The given email is already registered")
        else: 
            db_email = CustomUser.objects.get(id=self.instance.pk).email.lower()
            if db_email != email:  
                if CustomUser.objects.filter(email=email).exists():
                    raise forms.ValidationError("The given email is already registered")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password", None)
        if self.instance.pk is not None:
            if not password:
                return self.instance.password
        return make_password(password)

    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'email', 'password', 'department', 'employee_code']  # Add employee_code to fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.username = self.cleaned_data["employee_code"] 
        if commit:
            user.save()
        return user
