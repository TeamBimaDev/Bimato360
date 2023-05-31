from enum import Enum


class Gender(Enum):
    MALE = 'Male'
    FEMALE = 'Female'


def get_gender_choices():
    return [(gender.name, gender.value) for gender in Gender]

