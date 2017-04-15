import os
import sentiment_api as sap


rootdir = '/home/prakkk/galgotia-hack/data/sentiment/'
l=[]
directory = []
f1 =[]
for subdir, dirs, files in os.walk(rootdir):
	for f in files:
		l.append(os.path.join(subdir,f))
	for d in dirs:
		directory.append(d)	

for s in l:
	#print s
	#print s.split('/')[6]
	if s.split('/')[6] == 'test' or s.split('/')[6] == 'result.json' or s.split('/')[6] == 'result.json~':
		#print 'abc'
		pass
	else:
		print s
		s1 = '/'+s.split('/')[6]+'/'+s.split('/')[7]+'/'+s.split('/')[8]
		sap.callPath(s1,s.split('/')[6],s.split('/')[7])
		f1.append(s)

#f1.remove('/home/prakkk/galgotia-hack/data/sentiment/result.json')
#names=[]
#for f in f1 :
#	try:
#		directory.remove(f.split('/')[2])
#		try:
#			names[f.split('/')[2]]
#		except:
#			names.append(f.split('/')[2])
#	except:
#		pass
#	print f
#directory.remove('test')
#
#print directory 
#print names

#sap.callPath()
