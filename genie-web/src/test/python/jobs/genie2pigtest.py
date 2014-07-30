##
#
#  Copyright 2013 Netflix, Inc.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
##

import sys
sys.path.append('../utils')

import time
import eureka
import jobs
import json
import os
import uuid
import urllib2 

jobID = "job-" + str(uuid.uuid4())
# the S3 prefix where the tests are located
GENIE_TEST_PREFIX = os.getenv("GENIE_TEST_PREFIX")

# get the serviceUrl from the eureka client
serviceUrl = eureka.EurekaClient().getServiceBaseUrl() + '/genie/v2/jobs'
def testConflictJob():
    print serviceUrl
    print "Running testJsonSubmitjob "
    clusterTags = json.dumps([{"tags" : ['adhoc','h2query']}])
    cmdTags = json.dumps(['pig11_mr2'])
    payload = '''
        {
            "id":"testblah",
            "name": "Genie2TestPigJob", 
            "clusterCriterias" : ''' + clusterTags + ''',
            "user" : "genietest", 
            "version" : "1",
            "group" : "hadoop", 
            "commandArgs" : "-f pig2.q", 
            "commandCriteria" :''' + cmdTags + ''',
            "fileDependencies":"''' + GENIE_TEST_PREFIX + '''/pig2.q"
        }
    '''
    print payload
    print "\n"
    jobs.submitJob(serviceUrl, payload)
    sleep(30)
    return jobs.submitJob(serviceUrl, payload)

def testNoClusterJob():
    print serviceUrl
    print "Running testJsonSubmitjob "
    clusterTags = json.dumps([{"tags" : ['adhoc','h2query1']}])
    cmdTags = json.dumps(['pig11_mr2'])
    payload = '''
        {
            "id":"''' + jobID +'''",
            "name": "Genie2TestPigJob", 
            "clusterCriterias" : ''' + clusterTags + ''',
            "user" : "genietest", 
            "version" : "1",
            "group" : "hadoop", 
            "commandArgs" : "-f pig2.q", 
            "commandCriteria" :''' + cmdTags + ''',
            "fileDependencies":"''' + GENIE_TEST_PREFIX + '''/pig2.q"
        }
    '''
    print payload
    print "\n"
    return jobs.submitJob(serviceUrl, payload)

def testGoodJob():
    print serviceUrl
    print "Running testJsonSubmitjob "
    clusterTags = json.dumps([{"tags" : ['adhoc','h2query']}])
    cmdTags = json.dumps(['pig11_mr2'])
    payload = '''
        {
            "id":"''' + jobID +'''",
            "name": "Genie2TestPigJob", 
            "clusterCriterias" : ''' + clusterTags + ''',
            "user" : "genietest", 
            "version" : "1",
            "group" : "hadoop", 
            "commandArgs" : "-f pig2.q", 
            "commandCriteria" :''' + cmdTags + ''',
            "fileDependencies":"''' + GENIE_TEST_PREFIX + '''/pig2.q"
        }
    '''
    print payload
    print "\n"
    return jobs.submitJob(serviceUrl, payload)

# driver method for all tests                
if __name__ == "__main__":
   print "Running unit tests:\n"
   try:
    #jobID = testConflictJob()
    #jobID = jobs.submitJob()
    jobID = testGoodJob()
   except urllib2.HTTPError, e:
    print "Caught Exception"
    print "code = " + str(e.code)
    print "message =" + e.msg
    print "read =" + e.read()
    sys.exit(0)
   print "\n"
   while True:
       print jobs.getJobInfo(serviceUrl, jobID)
       print "\n"
       status = jobs.getJobStatus(serviceUrl, jobID)
       print "Status =%s" % status
       print "\n"

       if (status != 'RUNNING') and (status != 'INIT'):
           print "Final status: ", status
           print "Job has terminated - exiting"
           break
              
       time.sleep(5)
