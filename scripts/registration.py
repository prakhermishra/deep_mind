import os
import subprocess
import openface
import sys
#firebase.put(category,'check','testvalue')

register_script = open('register.sh','w')



register_script.write('#!/bin/sh')
register_script.write("\n")
register_script.write('/home/prakkk/openface/util/align-dlib.py /home/prakkk/galgotia-hack/data/class/ align outerEyesAndNose /home/prakkk/galgotia-hack/data/aligned-images/ --size 96')
register_script.write("\n")
register_script.write('/home/prakkk/openface/batch-represent/main.lua -outDir /home/prakkk/galgotia-hack/data/generated-embeddings/ -data /home/prakkk/galgotia-hack/data/aligned-images/')
register_script.write("\n")
register_script.write('/home/prakkk/openface/demos/classifier.py train /home/prakkk/galgotia-hack/data/generated-embeddings/')
register_script.write("\n")

os.system('chmod 777 -R *')

register_script.close()

subprocess.call(['./register.sh'])

#os.system('chmod 777 -R *')


#print result



