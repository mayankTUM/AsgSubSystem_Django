'''
Created on 16.12.2013

@author: Mayank
'''

from Submission.models import MyGroup,Student
from django.contrib.auth.models import User
import random

'''
group = MyGroup(groupId = 1)
group.groupName = "X-Men"
group.webGitId = "www.webgit.com/group1/save.git"
group.save()
'''

'''
user = User.objects.get(username__exact='abcd')
student=Student(matrikelNr=1234)
student.user = user
student.firstName = "abcd"
student.lastName = "wxyz"
student.emailId = "mayank_lucky6@yahoo.co.in"
student.save()    
'''
'''
user = User.objects.get(username__exact='abcd')
students = Student.objects.all()
for student in students:
    if student.user.username == 'abcd' :
        print('found')
        break
'''

group_password = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
print(group_password)


