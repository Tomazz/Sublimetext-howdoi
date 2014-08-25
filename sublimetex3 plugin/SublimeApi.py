#!/usr/bin/python
import sublime
import sublime_plugin
import time
import subprocess

class MyDummyCommand(sublime_plugin.TextCommand):
	def run(self,edit, active_window=True):
		symbols(line_endings)
		if active_window:
			print_active_window()

class MyWinCommand(sublime_plugin.WindowCommand):
	endingConverter = {"py":"python","java":"java"}

	def _saveQuery(self,codeContents,userContext,fileType):
		with open("C:\\Users\\Tomazz\\Documents\\SummerInternship2014\\DB\\buffer.txt","w") as buff:
				buff.write(" allintext:"+userContext+" "+codeContents+" intext:"+self.endingConverter[fileType]+" site:stackoverflow.com")
		#output = subprocess.check_output(["C:\\Python34\\python.exe","C:\\Users\\Tomazz\\Documents\\SummerInternship2014\\DB\\SOGetAnswerCodeSnippetsDB.py"],stderr=subprocess.PIPE)
		subproc = subprocess.Popen(["C:\\Python34\\python.exe","C:\\Users\\Tomazz\\Documents\\SummerInternship2014\\DB\\SODB.py"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell = True)
		print(subproc.communicate()[1])
		print(subproc.communicate()[0])
		

	def _produceQueryParameters(self,userContext):
		view = self.window.active_view()
		fileType = view.file_name().split(".")[-1] #file type of the current file
		sels = view.sel()
		for region in sels:
			codeContents = view.substr(region)
			self._saveQuery(codeContents,userContext,fileType)

	def run(self):
		self.window.show_input_panel("Ask a question about the code", "", self._produceQueryParameters, None, None)
