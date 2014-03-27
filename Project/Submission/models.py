from django.db import models
from django.contrib.auth.models import User

'''
Created on 16.12.2013

@author: Mayank
'''

class MyGroup(models.Model):
    groupId = models.CharField(primary_key=True,max_length=20)
    groupName = models.CharField(max_length=200)
    groupPassword = models.CharField(max_length=200)
    webGitId = models.CharField(max_length=200)  
    groupDesc = models.CharField(max_length=1000)
    def __str__(self):  
        return self.groupName + '_' + self.groupId   
   
   
class Student(models.Model):
    user = models.OneToOneField(User)
    matrikelNr = models.CharField(default=0, unique=True, primary_key = True, max_length=50)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    emailId = models.EmailField(max_length=70, unique=True)
    groupId = models.ForeignKey(MyGroup,null=True)
    def __str__(self):  
        return self.firstName + ' ' + self.lastName  


class Assignment(models.Model):
    assignmentId = models.CharField(primary_key=True, max_length=50)
    assignmentDesc = models.CharField(max_length=500)
    issueDate = models.DateTimeField('date of issue')
    dueDate = models.DateTimeField('last date of submission')
    def __str__(self):  
        return self.assignmentDesc    
    
    
class GroupAssignmentMapping(models.Model):
    groupId = models.ForeignKey(MyGroup)
    assignmentId = models.ForeignKey(Assignment)
    student = models.ForeignKey(Student)
    dateOfSubmission = models.DateTimeField('date of submission')
    submittedBy = models.CharField(max_length=200)
    accepted = models.BooleanField(default = False)
    resultFile = models.CharField(max_length=200)
    unique_together = (groupId,assignmentId)  
    def __str__(self):  
        return self.student.matrikelNr + '_' + self.assignmentId.assignmentDesc
'''    
class Lecture(models.Model):
    lectId = models.CharField(primary_key=True,max_length=10)
    lectName = models.CharField(max_length=50)
    chair = models.CharField(max_length=50)
    semester = models.CharField(max_length=2)
    professor = models.CharField(max_length=50)
    tutors = models.CharField(max_length=50)
    credits = models.IntegerField();
    def __str__(self):  
        return "Lecture Id :" + 'self.lectId' + "\tLectureName: " + self.lectName
'''          