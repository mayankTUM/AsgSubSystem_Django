from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from Submission.models import Student,MyGroup,Assignment,GroupAssignmentMapping
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from Submission.Authenticate import Auth 
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import logging, os
import random
import subprocess
import shutil
# Create your views here.
logger = logging.getLogger(__name__)

#number of students per group
no_of_students_per_group = 1;
timeout_in_seconds = 3;
    
def login(request):
    c = {}
    c.update(csrf(request))
    template = get_template('Submission/login.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

@login_required(login_url='/Submission/')
def logout(request):
    auth.logout(request)
    template = get_template('Submission/logout.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def invalidLogin(request):
    template = get_template('Submission/invalidLogin.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def home(request):
    template = get_template('Submission/home.html')
    context = RequestContext(request, {
         'studentUserName' : request.user.username,  
         'numberOfStudentsPerGroup' :  no_of_students_per_group                             
    })
    return HttpResponse(template.render(context))


def authenticateStudent(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    x = Auth(username, password)
    if x.Authenticate() is True :
        #either create a user or if it already exists check for password updation
        try :
            user = User.objects.get(username=username)
        except ObjectDoesNotExist :
            user = None    
        if user is not None :
            user.set_password(password) # update password according to tum auth ldap
            user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return HttpResponseRedirect('home')
        else :
            user = User.objects.create_user(username, '', password)
            user.save()
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return HttpResponseRedirect('studentDetails')
    else:
        return HttpResponseRedirect('invalidLogin')


@login_required(login_url='/Submission/')
def studentDetails(request):
    fullName = Auth.studentName
    index = fullName.find(",")
    lastName = fullName[0:index]
    firstName = fullName[index+2:]
    template = get_template('Submission/studentDetails.html')
    context = RequestContext(request, {
        'studentUserName' : Auth.studentName,     
        'studentFirstName' : firstName,
        'studentLastName' : lastName,
        'studentEmail' : Auth.studentEmail,
        'studentMatrik' : Auth.studentMatrik,
        'numberOfStudentsPerGroup' :  no_of_students_per_group
    })
    return HttpResponse(template.render(context))

@login_required(login_url='/Submission/')
def updateStudentDetails(request):
    matrikel = request.POST.get('matrikel','')
    firstname = request.POST.get('fisrtname','')
    lastname = request.POST.get('lastname','')
    emailid = request.POST.get('emailid','')
    user = User.objects.get(username__exact=request.user.username)
    student = Student(matrikelNr=matrikel)
    student.user=user
    student.firstName = firstname
    student.lastName = lastname
    student.emailId = emailid
    student.save()
    '''
    if number of students per group is one, create the group automatically
    '''
    if no_of_students_per_group == 1:
        createGroupAutomatically(student,request.user.username);
    
    
    return HttpResponseRedirect('/Submission/home')
    
def createGroupAutomatically(student,username):
    count = MyGroup.objects.all().count() + 1
    group_id = 'group'+str(count)
    group_name = str(username) 
    group_desc = group_name+"-desc"
    group_password = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
    group_git = 'www.webgit.com/'+group_id+'/save.git'
    group=MyGroup(groupId=group_id)
    group.groupPassword=group_password
    group.groupName=group_name
    group.groupDesc=group_desc
    group.webGitId=group_git
    group.save()
    student.groupId = group
    student.save()
        
    
@login_required(login_url='/Submission/')    
def assignments(request):
    template = get_template('Submission/assignments.html')
    context = RequestContext(request, {
        'studentUserName' : request.user.username, 
        'assignments' : Assignment.objects.all(),
        'numberOfStudentsPerGroup' :  no_of_students_per_group
    })
    return HttpResponse(template.render(context))

@login_required(login_url='/Submission/')    
def assignmentDetails(request):
    
    student = None
    students = Student.objects.all() 
    for e in students:
        if e.user.username == request.user.username :
            student = e
            break   

    group = student.groupId    
    assignmentID = request.GET.get('q','')
    warningsOrErrors = "False"
    if request.GET.get('warningsOrErrors','') :
        warningsOrErrors = request.GET.get('warningsOrErrors','')
    assignment = Assignment(assignmentId = assignmentID)
    grpAsgMapping = None 
    success = False
    accepted = ""
    if GroupAssignmentMapping.objects.filter(groupId=group,assignmentId=assignment) :
        grpAsgMapping = GroupAssignmentMapping.objects.filter(groupId=group,assignmentId=assignment)[0]
        success = True
        if grpAsgMapping.accepted is True:
            accepted = "Accepted"
        else :
            accepted = "Not Accepted"
        
    assignment = Assignment.objects.get(pk=assignmentID)
    duedate = assignment.dueDate
    currentdate = timezone.now()
    deadlinePassed = duedate < currentdate
    template = get_template('Submission/'+assignmentID+'.html')
    
    
    if success is False :
        context = RequestContext(request, {
            'studentUserName' : request.user.username, 
            'deadlinePassed' : deadlinePassed,
            'assignmentID' : assignmentID,
            'submitted' : success,
            'numberOfStudentsPerGroup' :  no_of_students_per_group,
            'warnings' : warningsOrErrors
        })
    else :
        context = RequestContext(request, {
            'studentUserName' : request.user.username, 
            'assignmentID' : assignmentID,
            'assignmentName': assignment.assignmentDesc,
            'time': grpAsgMapping.dateOfSubmission,
            'score': accepted,
            'resultFile':grpAsgMapping.resultFile,
            'submittedBy':grpAsgMapping.submittedBy,
            'submitted' : success,
            'numberOfStudentsPerGroup' :  no_of_students_per_group,
            'deadlinePassed' : deadlinePassed,
            'warnings' : warningsOrErrors
        })    
    return HttpResponse(template.render(context))


def submission(request):
   
    
    assignmentID = request.GET.get('q','')
    student = None
    students = Student.objects.all() 
    for e in students:
        if e.user.username == request.user.username :
            student = e
            break  
    if student.groupId is None :
        template = get_template('Submission/noGroup.html')
        context = RequestContext(request, {
                'studentUserName' : request.user.username, 
                'numberOfStudentsPerGroup' :  no_of_students_per_group
        })
        return HttpResponse(template.render(context))
    
    for key, file in request.FILES.items():
        directory = "/home/mayank/StudentUploadedFiles/"+ assignmentID + "/" + str(student.groupId);
        if not os.path.exists(directory):
            os.makedirs(directory)
        path = directory+"/"+file.name
        dest = open(path, 'wb')
        if file.multiple_chunks:
            for c in file.chunks():
                dest.write(c)
        else:
            dest.write(file.read())
        dest.close()
        
        '''
        code to create group assignment mapping
        TODO: calculate scores for the assignments 
        '''
        assignment = Assignment(assignmentId = assignmentID)
        
        
        '''
        *************************************
        TODO :before calculating the scores,
        I need to execute the code and check for warnings.
        Replace score with passed or fail.
        *************************************
        '''
        
        returnedValues = compileFile(directory,file.name,assignment).split('|||')
        warningsOrErrors = returnedValues[0]
        output = returnedValues[1]
        resultDirectory = "/var/www/Project/media/"+assignmentID+"/"+request.user.username;
        if not os.path.exists(resultDirectory):
            os.makedirs(resultDirectory,mode=0777)
        os.chdir(resultDirectory)    
        result_file = "result.txt"
        notAccepted = "False"    
            
        if warningsOrErrors == "True" :
            writeOutputToFile(result_file,output)
            notAccepted = "True"
        else :
            outputMessage = runTestCases(directory,file.name,assignment,resultDirectory)
            if outputMessage != "0" :
                notAccepted = "True"
            
        studentsForScores = Student.objects.filter(groupId = student.groupId)
        i = 0
        while i < studentsForScores.count() :
            studentToGetScore = studentsForScores[i] 
            if GroupAssignmentMapping.objects.filter(groupId = student.groupId,assignmentId = assignment,student = studentToGetScore) :
                groupAsgMapping = GroupAssignmentMapping.objects.filter(groupId = student.groupId,assignmentId = assignment)[0]
                groupAsgMapping.student =  studentToGetScore 
                groupAsgMapping.dateOfSubmission = timezone.now()
                if notAccepted == "True" :
                    groupAsgMapping.accepted = False # accepted or not accepted
                else :
                    groupAsgMapping.accepted = True    
                groupAsgMapping.submittedBy = student.firstName + " " + student.lastName
                groupAsgMapping.resultFile = "/media/"+assignmentID+"/"+request.user.username+"/"+result_file
                groupAsgMapping.save()
            else :
                groupAsgMapping = GroupAssignmentMapping(groupId = student.groupId)
                groupAsgMapping.student = Student(matrikelNr = studentToGetScore.matrikelNr)
                groupAsgMapping.assignmentId = assignment 
                groupAsgMapping.dateOfSubmission = timezone.now()
                if notAccepted == "True" :
                    groupAsgMapping.accepted = False # accepted or not accepted
                else :
                    groupAsgMapping.accepted = True    
                groupAsgMapping.submittedBy = student.firstName + " " + student.lastName
                groupAsgMapping.resultFile = "/media/"+assignmentID+"/"+request.user.username+"/"+result_file
                groupAsgMapping.save()
            i = i + 1
            
        return HttpResponseRedirect('Submission/assignmentDetails?q='+assignmentID+'&warningsOrErrors='+notAccepted)
            
    return HttpResponseRedirect('Submission/submission?q='+assignmentID)
         
def compileFile(directory,fileName,assignment):
    warnings = "False"
    asgId = assignment.assignmentId
    os.chdir(directory)
    outputName,ext = os.path.splitext(fileName)
    '''
    CODE TO COPY MAIN.C AND .H FILES TO THE STUDENT DIRECTORY
    '''
    shutil.copy2('/home/mayank/StudentUploadedFiles/'+asgId+'/main.c', directory+'/')
    shutil.copy2('/home/mayank/StudentUploadedFiles/'+asgId+'/'+outputName+'.h', directory+'/')
    os.chmod('main.c', 0777)
    os.chmod(outputName+'.h', 0777)
    os.chmod(outputName+'.c', 0777)
    output = ""
    '''
    ----------------------------------------- THIS NEEDS TO BE CHANGED -----------------------------------------
    '''
    if asgId == "assignment1" :
        # subprocess.check_call(['gcc','-std=gnu99','-pthread','-Wall','-o',str(outputName),str(fileName)],stdout= subprocess.PIPE, stderr = subprocess.STDOUT,shell=False)
        cmd = ['gcc','-std=gnu99','-pthread','-Wall','-o',str(outputName+'.o'),str(fileName),"main.c"]
        process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stderr.__contains__("warning") :
            warnings = "True"
            output = stderr

    return warnings+"|||"+output
    
def writeOutputToFile(fileName,output):
    f = open(fileName, 'w+')
    f.write(output)
    f.close()
    os.chmod(fileName, 0777)
       
    
def runTestCases(directory,fileName,assignment,resultDirectory) :
    asgId = assignment.assignmentId    
    outputName,ext = os.path.splitext(fileName)
    os.chdir(directory)
    shutil.copy2('/home/mayank/StudentUploadedFiles/'+asgId+'/testCases.c', directory+'/')
    output = ""
    if asgId == "assignment1" :
        cmd = ['gcc','-std=gnu99','-pthread','-Wall','-o',outputName+'.o',str(fileName),"testCases.c"]
        process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        cmd = ['timeout',str(timeout_in_seconds),'./'+outputName+'.o',resultDirectory]
        process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        output = stdout
    return output        

         
@login_required(login_url='/Submission/')
def createGroup(request):
    template = get_template('Submission/createGroup.html')
    context = RequestContext(request, {
        'studentUserName' : request.user.username,
        'numberOfStudentsPerGroup' :  no_of_students_per_group                               
    })
    return HttpResponse(template.render(context))

@login_required(login_url='/Submission/')
def newGroup(request):
    
    student = None
    flag=True
    students = Student.objects.all() 
    for e in students:
        if e.user.username == request.user.username :
            if e.groupId is not None :
                flag = True
            else :
                flag = False
                student = e
            break        
    
    if flag is False : 
        count = MyGroup.objects.all().count() + 1
        group_name = request.POST.get('groupname','')
        group_desc = request.POST.get('grpdesc','')
        group_id = 'group'+str(count)
        group_password = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
        group_git = 'www.webgit.com/'+group_id+'/save.git'
        
        group=MyGroup(groupId=group_id)
        group.groupPassword=group_password
        group.groupName=group_name
        group.groupDesc=group_desc
        group.webGitId=group_git
        group.save()
    
        student.groupId = group
        student.save()
        return HttpResponseRedirect('assignments')
    else :
        return HttpResponseRedirect('createGroup')

@login_required(login_url='/Submission/')
def showGroup(request):
    template = get_template('Submission/showGroup.html')
    context = RequestContext(request, {
        'studentUserName' : request.user.username,      
        'allStudents' : Student.objects.all(),
        'allGroups' : MyGroup.objects.all(),        
        'numberOfStudentsPerGroup' :  no_of_students_per_group                 
    })
    return HttpResponse(template.render(context))


@login_required(login_url='/Submission/')
def joinGroup(request):
    student = None
    flag=False
    group_id = request.POST.get('selectedGroup','')
    students = Student.objects.all() 
    for e in students:
        if e.user.username == request.user.username :
            if e.groupId is not None :
                flag = True
            else :
                flag = False
                student = e
            break        
    if flag is False :
        group=MyGroup(groupId=group_id)
        student.groupId = group
        student.save()
        return HttpResponseRedirect('assignments')
    else :
        return HttpResponseRedirect('assignments')
   
@login_required(login_url='/Submission/')
def leaveGroup(request):
    student = None
    students = Student.objects.all() 
    for e in students:
        if e.user.username == request.user.username :
            student = e
            break  
    
    if student.groupId is None :
        template = get_template('Submission/noGroup.html')
        context = RequestContext(request, {
                'studentUserName' : request.user.username,
                'numberOfStudentsPerGroup' :  no_of_students_per_group 
        })
        return HttpResponse(template.render(context))    
        
    
    currentGroup = student.groupId.groupName
    template = get_template('Submission/leaveGroup.html')
    context = RequestContext(request, {
        'studentUserName' : request.user.username,      
        'currentGroup' : currentGroup,
        'numberOfStudentsPerGroup' :  no_of_students_per_group
    })
    return HttpResponse(template.render(context))

@login_required(login_url='/Submission/')
def removeStudentFromGroup(request):
    student = None
    students = Student.objects.all() 
    for e in students:
        if e.user.username == request.user.username :
            student = e
            break  
   
    student.groupId = None
    student.save()  
    template = get_template('Submission/removeStudentFromGroup.html')
    context = RequestContext(request, {
        'studentUserName' : request.user.username,      
        'numberOfStudentsPerGroup' :  no_of_students_per_group
    })
    return HttpResponse(template.render(context))


@login_required(login_url='/Submission/')
def aboutMyGroup(request):
   
    student = None
    students = Student.objects.all() 
    for e in students:
        if e.user.username == request.user.username :
            student = e
            break  
    
    if student.groupId is None :
        template = get_template('Submission/noGroup.html')
        context = RequestContext(request, {
                'studentUserName' : request.user.username, 
                'numberOfStudentsPerGroup' :  no_of_students_per_group
        })
        return HttpResponse(template.render(context))
           
    group_name = student.groupId.groupName
    group_members = student.groupId.student_set.all()
    group_username = student.groupId.groupId
    group_password = student.groupId.groupPassword
    group_desc = student.groupId.groupDesc
    template = get_template('Submission/aboutMyGroup.html')
    context = RequestContext(request, {
         'studentUserName' : request.user.username,       
         'groupName' : group_name,
         'groupMembers' : group_members,
         'groupUsername' : group_username,
         'groupPassword' : group_password,
         'group_desc' : group_desc,                         
         'numberOfStudentsPerGroup' :  no_of_students_per_group
    })
    return HttpResponse(template.render(context))



@login_required(login_url='/Submission/')
def renameGroup(request):
    student = None
    students = Student.objects.all() 
    for e in students:
        if e.user.username == request.user.username :
            student = e
            break  
    
    newGroupname = request.POST.get('newGrpName','')
    student.groupId.groupName = newGroupname
    student.groupId.save()
    return HttpResponseRedirect('/Submission/home')

def contact(request):
    username =""
    if request:
        username = request.user.username
    template = get_template('Submission/contact.html')
    context = RequestContext(request, {
            'studentUserName' : username, 
    })
    return HttpResponse(template.render(context))

def about(request):
    username =""
    template = get_template('Submission/about.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

