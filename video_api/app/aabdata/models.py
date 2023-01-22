from pydantic import BaseModel
from typing import Optional, List

class Document(BaseModel):
    _type: Optional[str] # E.g.: "SubjectResource", "SubjectTopic", "SubjectCourse", "Subject" ... Useful for structuring your json

class SubjectResource(Document):
    title: str
    link: str
    description: Optional[str] # You don't have to add a description

class SubjectTopic(Document):
    title: str # E.g.: Classes, Staticmethods ...
    week: int
    description: Optional[str] # You don't have to add a description
    resources: Optional[List[SubjectResource]] # The list of resources for this specific subjectcourse

class SubjectCourse(Document):
    title: str
    description: Optional[str]
    topics: List[SubjectTopic] # The list of topics we're handling: E.g.: Classes, Staticmethods ...
    resources: Optional[List[SubjectResource]] # The list of resources for this specific subjectcourse

class Subject(Document):
    _id: Optional[int] # Randomly generated ID by MongoDB
    title: str # E.g.: Object Oriented Programming
    weight: int # Used to sort the order of the subjects
    description: str # A short description what this subject is about
    courses: List[SubjectCourse] # The list of courses where this subject is being taught, 
    resources: Optional[List[SubjectResource]] # The list of resources