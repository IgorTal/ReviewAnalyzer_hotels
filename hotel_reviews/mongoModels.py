from mongoengine import *

#connect('employeeDB')
class Employee(Document):
    name = StringField(max_length=50)
    age = IntField(required=False)
