'''
Created on 17.12.2013

@author: Mayank
'''
from django.conf.urls import patterns, url

from Submission import views

urlpatterns = patterns('', 
    url(r'^$', views.login, name='index'),
    url(r'studentDetails', views.studentDetails, name='studentDetails'),
    url(r'assignments', views.assignments, name='assignments'),
    url(r'createGroup', views.createGroup, name='createGroup'),
    url(r'aboutMyGroup', views.aboutMyGroup, name='aboutMyGroup'),
    url(r'logout', views.logout, name='logout'),
    url(r'invalidLogin', views.invalidLogin, name='invalidLogin'),
    url(r'authenticateStudent', views.authenticateStudent, name='authenticateStudent'),
    url(r'updateStudentDetails', views.updateStudentDetails, name='updateStudentDetails'),
    url(r'newGroup', views.newGroup, name='newGroup'),
    url(r'showGroup', views.showGroup, name='showGroup'),
    url(r'joinGroup', views.joinGroup, name='joinGroup'),
    url(r'home', views.home, name='home'),
    url(r'renameGroup', views.renameGroup, name='renameGroup'), 
    url(r'assignmentDetails', views.assignmentDetails, name='assignmentDetails'),
    url(r'submission', views.submission, name='submission'),
    url(r'leaveGroup', views.leaveGroup, name='leaveGroup'),
    url(r'removeStudentFromGroup', views.removeStudentFromGroup, name='removeStudentFromGroup'),
    url(r'contact', views.contact, name='contact'),
    url(r'about', views.about, name='about'),
)