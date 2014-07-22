from os import listdir
import os.path


mypath = "D:\\StackOverflowDBDump\\"
testPath = mypath+"tests\\"

onlyFiles = [ f for f in listdir(mypath) if os.path.isfile(os.path.join(mypath,f)) ]
print(onlyFiles)
for filename in onlyFiles:
	if os.path.splitext(filename)[1] == ".xml":
		with open(mypath+filename,"r") as SODumpFile:
			with open(testPath+filename,"w") as testFile:
				for x in range(50):
					testFile.write(SODumpFile.readline())
				testFile.write("</"+(os.path.splitext(filename)[0]).lower()+">")
