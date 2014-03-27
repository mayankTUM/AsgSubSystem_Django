import unittest
import os
import subprocess


class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_output(self):
        directory = "/var/www/Project/media";
        os.chdir(directory)    
        result_file = "ga39tal"+"_result_"+"pthread_hello_world_v0.txt"
        data = ""
        with open (result_file, "r") as myfile:
            data=myfile.read()
        self.assertEqual(data,"Hello World from MAIN !!\nHello World from pthread!\n")      
    
    def test_pi(self):
        outputName = "/home/mayank/ParallelProgramming2014/My_Practise/dynamic_work_distribution_v2/dynamic_work_distribution_v2.o"
        fileName = "/home/mayank/ParallelProgramming2014/My_Practise/dynamic_work_distribution_v2/main.c"
        
        cmd = ['gcc','-std=gnu99','-pthread','-Wall','-o',str(outputName),str(fileName),'-lm']
        process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        cmd = [outputName]
        process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        self.assertEqual(stdout,"Calculate PI is 3.1415926539\nError in PI is -0.0000000003\n")
    
if __name__ == '__main__':
    unittest.main()

