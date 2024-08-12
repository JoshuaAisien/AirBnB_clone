from models.base_model import BaseModel
import re


class Place(BaseModel):
    """A clas representing a place"""
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []


# place = '"38f22813-2753-4d42-b37c-57a17f1e4f88", "age", 89'
# city = '"38f22813-2753-4d42-b37c-57a17f1e4f88", "first_name", "John"'
# value = (city.strip('"'))
# places = place.strip('"')
#
#
# class_name = 'classname'
# value1 = f'{class_name} {value}'
# value2 = f'{class_name} {places} '
# print(value1)
# print(value2)
# match = re.match(r'(\w+)\s([0-9a-fA-F-]+)",\s"([^"]+)",\s"?([^"]+)', value1)
# match1 = re.match(r'(\w+)\s([0-9a-fA-F-]+)",\s"([^"]+)",\s"?([^"]+)', value2)
# class1, class2, class3, class4 = match.groups()
# classa, classb, classc, classd = match1.groups()
# print(class1)
# print(class2)
# print(class3)
# print(class4)
# print(classa)
# print(classb)
# print(classc)
# print(classd)
