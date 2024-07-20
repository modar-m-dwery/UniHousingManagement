from django import forms
from institute.models import Student
from workers.models import Worker


class StudentForm(forms.ModelForm):
    COMMUNITY_CHOICES = (
        ( None, 'Select'),
        ('GEN', 'GEN'),
        ('OBC', 'OBC'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('EWS', 'EWS')
    )

    BLOOD_GROUP_CHOICES = (
        ( None, 'Select'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )


    blood_group = forms.CharField(max_length=25, required=True, widget=forms.Select(choices=BLOOD_GROUP_CHOICES))
    father_name = forms.CharField(max_length=100, required=True)
    mother_name = forms.CharField(max_length=100, required=True)
    community = forms.CharField(max_length=25, required=True, widget=forms.Select(choices=COMMUNITY_CHOICES),)
    # branch = forms.CharField(max_length=25, required=True, widget=forms.Select(choices=BRANCH_CHOICES))

    class Meta:
        model = Student
        fields = '__all__'

        

        BOOLEAN_CHOICES = (
            (True, 'Yes'), 
            (False, 'No')
        )


        BRANCH_CHOICES=(
            ( None,'Select'),
            ('BIO','Biotechnology'),
            ('CHE','Chemical Engineering'),
            ('CIV','Civil Engineering'),
            ('CSE','Computer Science and Engineering'),
            ('EEE','Electrical and Electronics Engineering'),
            ('ECE','Electronics and Communication Engineering'),
            ('MEC','Mechanical Engineering'),
            ('MME','Metallurgical and Materials Engineering'),
        )


        widgets = {
            'branch': forms.Select(choices=BRANCH_CHOICES),
            'pwd': forms.Select(choices=BOOLEAN_CHOICES),
            'is_hosteller': forms.Select(choices=BOOLEAN_CHOICES),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 5}),
        }

        labels = {
            'pwd': 'Person with Disability',
            'regd_no': 'Registration No.',
            'is_hosteller': 'Hosteller',
            'dob': 'Date of Birth',
        }

        help_texts = {
            'is_hosteller': 'Yes for Hosteller. No for Day Scholar.',
        }

class WorkerForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ['staff_id', 'name', 'designation', 'account_email', 'email', 'phone', 'gender', 'block']

        DESGINATION_CHOICES = (
            (None, 'Select'),
            ('Doctor', 'Doctor'),
            ('Electrician','Electrician'), 
            ('Estate Staff','Estate Staff'), 
            ('General Servant','General Servant'),
            ('Gym Trainer','Gym Trainer'),
            ('Mess Incharge', 'Mess Incharge'),
            ('PT/Games Coach','PT/Games Coach'),
            ('Scavenger','Scavenger'),
        )

        widgets = {
            'designation': forms.Select(choices=DESGINATION_CHOICES)
        }