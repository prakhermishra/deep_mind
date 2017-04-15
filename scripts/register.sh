#!/bin/sh
/home/prakkk/openface/util/align-dlib.py /home/prakkk/galgotia-hack/data/class/ align outerEyesAndNose /home/prakkk/galgotia-hack/data/aligned-images/ --size 96
/home/prakkk/openface/batch-represent/main.lua -outDir /home/prakkk/galgotia-hack/data/generated-embeddings/ -data /home/prakkk/galgotia-hack/data/aligned-images/
/home/prakkk/openface/demos/classifier.py train /home/prakkk/galgotia-hack/data/generated-embeddings/

