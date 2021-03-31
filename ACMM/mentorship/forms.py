from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from .models import MentorProfile,MenteeProfile,MentorQualification,MenteeQualification
from django.forms import inlineformset_factory

# options
SPECIALTY_CHOICES= [
    ('Personal Statement', 'Personal Statement'),
    ('Interview', 'Interview'),
    ('Entrance Exam', 'Entrance Exam'),
    ('Work Experience', 'Work Experience'),
    ('Choosing a University', 'Choosing a University ')]
APPLICATION_STAGES=SPECIALTY_CHOICES[:-2]   
INTERVIEW_EXPERIENCE_CHOICES = [
    ('Panel', 'Panel'),
    ('MMI', 'MMI'),
    ('Group', 'Group')]
YEAR_APPLIED_CHOICES = [
    ('A level', 'A level'),
    ('International Baccalaureate', 'International Baccalaureate'),
    ('Graduate', 'Graduate')]
ENTRANCE_EXAM_CHOICES = [
    ('BMAT', 'BMAT'),
    ('UKCAT', 'UKCAT'),
    ('GAMSAT', 'GAMSAT')]
OCCUPATION_CHOICES = [
    ('Doctor', 'Doctor'),
    ('Dentist', 'Dentist'),
    ('Medical Student', 'Medical Student'),
    ('Dental student', 'Dental student'),
    ('Graduate Medical Student', 'Graduate Medical Student'),
    ('Graduate Dentist Student', 'Graduate Dentist Student'),
    ('Medical Student Studying Abroad', 'Medical Student Studying Abroad'),
    ('Dental Student Studying Abroad', 'Dental Student Studying Abroad')]
INTREST_CHOICES = [
    ('Outreach Programmes', 'Outreach Programmes'),
    ('Speaking at events', 'Speaking at events'),
    ('Support for events', 'Support for events'),
    ('Provision of work experience/volunteering opportunities', 'Provision of work experience/volunteering opportunities'),
    ('Additional guidance for mentors (one off)', 'Additional guidance for mentors (one off)')]
COURSE_CHOICES =[
    ('Medicine', 'Medicine'),
    ('Dentistry', 'Dentistry'),
    ('Graduate Medicine', 'Graduate Medicine'),
]
TRUE_FALSE_CHOICES = [
    (True, 'Yes'),
    (False, 'No')
]

EDUCATION_LEVEL_CHOICES = [
    ("A Level", 'A Level'),
    ("A/S Level", 'A/S Level'),
    ("Undergraduate", 'Undergraduate'),
    ("Masters", 'Masters'),
    ("Doctorate", 'Doctorate')
]

GRADE_CHOICES = [
    ("A*", 'A*'),
    ("A", 'A'),
    ("B", 'B'),
    ("C", 'C'),
    ("D", 'D'),
    ("E", 'E'),
    ("F", 'F'),
    ("1st", '1st'),
    ("2:1", '2:1'),
    ("2:2", '2:2'),
    ("3rd", '3rd'),
    ("1", '1'),
    ("2", '2'),
    ("3", '3'),
    ("4", '4'),
    ("5", '5'),
    ("6", '6'),
    ("7", '7')
]

#list(zip(x,y))

SEX_CHOICES = [
    ("M","M"),
    ("F","F")
]

class MentorForm(forms.ModelForm):
    occupation=forms.ChoiceField(choices = OCCUPATION_CHOICES,required=True) 
    
    area_of_support = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=SPECIALTY_CHOICES,label="Position/Specialty:")   
    application_strength= forms.ChoiceField(widget=forms.RadioSelect,choices=APPLICATION_STAGES,label="What was your strength in the application?")                            
    
    year_of_study = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],required=False, help_text='For Students')
    entrance_exam_experience = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=ENTRANCE_EXAM_CHOICES,label="Entrance Exam Experience:")
    interview_experience = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=INTERVIEW_EXPERIENCE_CHOICES,label="Interview Experience:")
    year_applied = forms.ChoiceField(widget=forms.RadioSelect,
                                          choices=YEAR_APPLIED_CHOICES,label="Year Applied:")
   
    sex = forms.ChoiceField(choices = SEX_CHOICES,required=True) 
    class Meta:
        model = MentorProfile
        exclude=('is_active',)

class MentorQualificationForm(forms.ModelForm):
    education_level=forms.ChoiceField(choices = EDUCATION_LEVEL_CHOICES ,required=True) 
    class Meta:
        model = MentorQualification
        exclude = ('profile',)

MentorQualificationFormSet = forms.inlineformset_factory(MentorProfile,model = MentorQualification, form=MentorQualificationForm,extra=1)


class MenteeForm(forms.ModelForm):
    course = forms.ChoiceField(choices = COURSE_CHOICES,required=True,label="What course are you applying to?") 
    
    area_of_support = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=SPECIALTY_CHOICES,label="What do you need help with?")   
    entrance_exam_experience = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=ENTRANCE_EXAM_CHOICES,label="What entrance exam experience have you had?")
    interview_experience = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=INTERVIEW_EXPERIENCE_CHOICES,label="What interview exam experience have you had?")
    year_applied = forms.ChoiceField(widget=forms.RadioSelect,
                                          choices=YEAR_APPLIED_CHOICES,label="What level are you currently studying at?")
    current_application=forms.ChoiceField(choices = TRUE_FALSE_CHOICES ,required=True ,label="Are you applying this year?") 
    
    mentor_need = forms.CharField(widget=forms.Textarea(attrs={
                'rows': '5',
                'cols': '90',
                'maxlength': '200',
            }),required=True ,label="Why do you want a mentor and what do you hope to gain ?")
  
    mentor_help = forms.CharField(widget=forms.Textarea(attrs={
                'rows': '5',
                'cols': '90',
                'maxlength': '200',
            }),required=True ,label="How will a mentor help with your application?")
    
    mentor_relationship = forms.CharField(widget=forms.Textarea(attrs={
                'rows': '5',
                'cols': '90',
                'maxlength': '200',
            }),required=True ,label="How will you go about fostering a good relationship your mentor?")
    
    sex = forms.ChoiceField(choices = SEX_CHOICES,required=True) 
    class Meta:
        model = MenteeProfile
        exclude=('date_joined','assigned_mentor')
        
class MenteeQualificationForm(forms.ModelForm):
    education_level=forms.ChoiceField(choices = EDUCATION_LEVEL_CHOICES ,required=True) 
    grade=forms.ChoiceField(choices = GRADE_CHOICES ,required=True) 
    predicted=forms.ChoiceField(choices = TRUE_FALSE_CHOICES ,required=True ,label="Predicted ?") 
    class Meta:
        model = MenteeQualification
        exclude = ('profile',)

MenteeQualificationFormSet = forms.inlineformset_factory(MenteeProfile,model = MenteeQualification, form=MenteeQualificationForm,extra=1)




