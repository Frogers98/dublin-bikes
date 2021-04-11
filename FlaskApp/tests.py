##------------------APP---------------##
## 
##User:     Disappster
##DC:       2021-03-24
##DLM:      2021-03-24
##MC:       COMP30830
##SD:       TEST CASES FOR THE FLASK APPLICATION
##
##------------------APP---------------##

from FlaskApp.methods import *


##------------------01. Connection Tests---------------##

def connection_test(host,user,password,port,db):
    """Test if a connection to the database was established"""
    connection_result=connect_db_engine(host,user,password,port,db)
    
    test_result=True
    #Error Value returned in the method
    if connection_result[0]==1:
        test_result=False

    return test_result





##------------------999. Run all Connection Tests---------------##

def run_tests(host,user,password,port,db):
    """Run all test cases"""

    runnable=True

    #Run through each of the test case functions here. Technically this isn't really the best case to define them but should be okay. 
    while runnable:
        runnable=connection_test(host,user,password,port,db)

    return runnable