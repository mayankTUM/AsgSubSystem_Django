from django.contrib import admin
from django.conf.urls import patterns
from django.http import HttpResponse
from django.template import RequestContext
from django.template.loader import get_template
from Submission.models import MyGroup, Student, Assignment, GroupAssignmentMapping
import sqlite3

'''
Created on 16.12.2013

@author: Mayank
'''

'''
code to register different models
'''
admin.site.register(MyGroup)
admin.site.register(Student)
admin.site.register(Assignment)
admin.site.register(GroupAssignmentMapping)



'''
code to define custom django views
'''
def fetchScores(request):
    username = request.user.username
    matrikelNr = request.GET.get('q','')
    conn = sqlite3.connect("/home/mayank/student_db/db.sqlite3")
    c = conn.cursor()
    c.execute("SELECT student_id, groupId_id, assignmentId_id, accepted FROM Submission_groupassignmentmapping WHERE student_id=?" , (matrikelNr,))
    data = c.fetchall()
    template = get_template('admin/studentAssignmentScores.html')
    context = RequestContext(request, {
        'submissions' : data,
        'found' : True,
	'username' : username,
    })
    return HttpResponse(template.render(context))


def studentAssignmentScores(request):
    username = request.user.username
    template = get_template('admin/studentAssignmentScores.html')
    context = RequestContext(request, {
        'username' : username,
    })
    return HttpResponse(template.render(context))

def get_admin_urls(urls):
    def get_urls():
        my_urls = patterns('',
            (r'^studentAssignmentScores/$', admin.site.admin_view(studentAssignmentScores)),
            (r'^fetchScores/$', admin.site.admin_view(fetchScores)),
        )
        return my_urls + urls
    return get_urls

admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls


