from pydantic import BaseModel

class Student(BaseModel):
    name: str

new_Student = {'name': 'Bharti'}
student = Student(**new_Student)

print(student)