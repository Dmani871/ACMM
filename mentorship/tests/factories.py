import factory.fuzzy
import random
import itertools
from mentorship import models


def generate_combinations(choices):
    options = sum([list(map(list, itertools.combinations(choices, i))) for i in range(1, len(choices) + 1)], [])
    return options


def unpack_choices(choices):
    return [c_tuple[0] for c_tuple in choices]


entrance_exam_experience_opts = generate_combinations(models.ENTRANCE_EXAMS_TYPES)
interview_experience_opts = generate_combinations(unpack_choices(models.INTERVIEW_EXPERIENCE_CHOICES))
area_of_support_opts = generate_combinations(unpack_choices(models.SPECIALTY_CHOICES))
course_opts = unpack_choices(models.COURSE_CHOICES)
year_applied_opts = unpack_choices(models.YEAR_APPLIED_CHOICES)
hear_about_us_opts = unpack_choices(models.HEAR_ABOUT_US_CHOICES)
occupation_opts = unpack_choices(models.OCCUPATION_CHOICES)
education_level_opt = unpack_choices(models.EDUCATION_LEVEL_CHOICES)
sex_opts=unpack_choices(models.SEX_CHOICES)

class MenteeFactory(factory.Factory):
    class Meta:
        model = models.MenteeProfile

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda user: '{}.{}@example.com'.format(user.first_name, user.last_name).lower())
    sex = factory.fuzzy.FuzzyChoice(sex_opts)
    year_applied = factory.fuzzy.FuzzyChoice(year_applied_opts)
    hear_about_us = factory.fuzzy.FuzzyChoice(hear_about_us_opts)
    entrance_exam_experience = factory.fuzzy.FuzzyChoice(entrance_exam_experience_opts)
    interview_experience = factory.fuzzy.FuzzyChoice(interview_experience_opts)
    area_of_support = factory.fuzzy.FuzzyChoice(area_of_support_opts)
    course = factory.fuzzy.FuzzyChoice(course_opts)
    mentor_need = factory.fuzzy.FuzzyText(length=200)
    mentor_help = factory.fuzzy.FuzzyText(length=200)
    mentor_relationship = factory.fuzzy.FuzzyText(length=200)

    @factory.post_generation
    def qualifications(obj, create, extracted, **kwargs):
        if not create:
            return
        obj.save()
        number_of_qualifications = random.randint(2, 4)
        for n in range(number_of_qualifications):
            q = MenteeQualificationFactory(profile=obj)
            q.save()


class MenteeQualificationFactory(factory.Factory):
    class Meta:
        model = models.MenteeQualification

    name = factory.fuzzy.FuzzyChoice([
        'Biology',
        'Chemisty',
        'Mathematics',
        'Further Mathematics',
        'Physics',
        'French',
        'Biomedical Science',
        'Psychology'])
    education_level = factory.fuzzy.FuzzyChoice(education_level_opt)
    grade = factory.fuzzy.FuzzyChoice(models.GRADES)
    profile = factory.SubFactory(MenteeFactory)


class MentorFactory(factory.Factory):
    class Meta:
        model = models.MentorProfile

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.LazyAttribute(lambda user: '{}.{}@example.com'.format(user.first_name, user.last_name).lower())
    sex = factory.fuzzy.FuzzyChoice(sex_opts)
    year_applied = factory.fuzzy.FuzzyChoice(year_applied_opts)
    hear_about_us = factory.fuzzy.FuzzyChoice(hear_about_us_opts)
    entrance_exam_experience = factory.fuzzy.FuzzyChoice(entrance_exam_experience_opts)
    interview_experience = factory.fuzzy.FuzzyChoice(interview_experience_opts)
    area_of_support = factory.fuzzy.FuzzyChoice(area_of_support_opts)
    occupation = factory.fuzzy.FuzzyChoice(occupation_opts)

    @factory.post_generation
    def qualifications(obj, create, extracted, **kwargs):
        if not create:
            return
        obj.save()
        number_of_qualifications = random.randint(2, 4)
        for n in range(number_of_qualifications):
            q = MentorQualificationFactory(profile=obj)
            q.save()


class MentorQualificationFactory(factory.Factory):
    class Meta:
        model = models.MentorQualification

    name = factory.fuzzy.FuzzyChoice([
        'Biology',
        'Chemistry',
        'Mathematics',
        'Further Mathematics',
        'Physics',
        'French',
        'Biomedical Science',
        'Psychology'])
    education_level = factory.fuzzy.FuzzyChoice(education_level_opt)
    profile = factory.SubFactory(MenteeFactory)