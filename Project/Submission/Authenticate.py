import sys
import os.path,subprocess


class Auth():
    studentName = ""
    studentEmail = ""
    studentMatrik = ""
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def Authenticate(self):
        java_file = "/var/www/Authenticate/src/Authenticate.java"
        #subprocess.check_call(['javac', java_file])
        java_class,ext = os.path.splitext(java_file)
        index = java_class.rfind('/')
        path = java_class[0:index]
        os.chdir(path)
        java_class = java_class[index+1:] 
        cmd = ['java', java_class,self.username, self.password]
        process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        output = stdout.decode("utf-8")
        output = output.split(":");
        for i,val in enumerate(output) :
            if i == 0 :
                uname = val
            if i == 1 :
                Auth.studentName = val
            if i == 2 :
                Auth.studentEmail = val
            if i == 3 :
                Auth.studentMatrik = val    
        if uname == self.username :
            return True
        else :
            return False
