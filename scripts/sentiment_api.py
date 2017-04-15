import httplib, urllib, base64
import os
import json
# from pathlib import Path
def callPath( directory , sess, studentkey ) :
	global student_key
	student_key=studentkey
	global session
	session=sess
	print directory
	callSentiment(directory)
	
	
def writeText( name , data_json , session ):
        print('Creating new text file') 
    	# try:
        final_score=0.0
        # file_write = open(name,'r+')
        # print(file_write.read())
        print("before")
        with open(name) as json_data:
            data_result = json.load(json_data)
            print(data_result)
        # data_json=json.load("result.json",)
        print("after")
        print "yeand dd"
        data_json=json.loads(data_json)

        # for i in range(len(data_score)):
        print data_json
        print data_json[0]["scores"]["anger"]
        final_score-=(data_json[0]["scores"]["anger"])*0.3
        final_score-=data_json[0]["scores"]["disgust"]*0.2
        final_score+=data_json[0]["scores"]["neutral"]*0.7
        final_score+=data_json[0]["scores"]["fear"]*0.2
        final_score-=data_json[0]["scores"]["sadness"]*0.5
        final_score+=data_json[0]["scores"]["surprise"]*0.7
        final_score+=data_json[0]["scores"]["happiness"]*0.4

        # if length > session :
        print final_score
        print "yeand"
        print data_result[student_key]
	#if student_key not in data_value:
    	#	data_result[student_key]=[{"session":session,"value":final_score}]
	#else:
    	#	data_result[student_key].append({"session":session,"value":final_score})
        data_result[student_key].append({"session":session,"value":final_score})
        print(data_result)
        f=open(name,"w")
        f.write(json.dumps(data_result))
        f.close()
        return    
        # file.close()

    # except Exception as e:
    #     print(e)
    #     print('Something went wrong! Can\'t tell what?')
        # sys.exit(0) # quit Python



headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '2e6c3722c3e44249919bda3c27c5e7d5',
}

def callSentiment(extendedPath):
	params = urllib.urlencode({})
	path="http://9153fc16.ngrok.io/"+extendedPath
	print path
	body="{ \"url\":\""+path+"\"}"
	try:
	    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
	    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
	    response = conn.getresponse()
	    data = response.read()
	    print(data)
	    # name = raw_input('Enter name of text file: ')+'.json'
	    name = "/home/prakkk/galgotia-hack/data/sentiment/result1.json"
	    print(name)
	    print(session)
	    conn.close()
	    writeText(name,data,session)
	    # with open(name , "")
	    # with open(name, "a") as myfile:
	    #     myfile.write(data)

	    print("test")

	except Exception as e:
	    print e
	    # print("[Errno {0}] {1}".format(e.errno, e.strerror))


