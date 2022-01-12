from os import listdir
from os.path import isfile,join
import re
from collections import Counter, defaultdict





def file_names(mypath):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.lower().endswith('.txt')]
    return onlyfiles



def tokenize(s):
	s = s.lower()          #lower case

	s = re.sub('\.+', ".", s)             #Replace multiple instances of fullstop
	 
	arr = re.compile('\s+').split(s)          #Split once for multiple spaces

	arr = [re.sub("[^A-Za-z0-9%.']", '', x) for x in arr]   #Replacing anything that is not a character, number, %, ' or .(decimal point)

	arr = filter(None, arr)       #Remove all empty list elements
	arr = [x[:-1] if x[-1]=='.' else x for x in arr]        #Replacing last character if its a fullstop
   
	return arr



def displayTermPosition():
	intialise()
	global path,fileNames,terms
	message = '<html><head>Total unique terms=%d</head><body><table border="1">'%len(terms)
	f = open('templates/Answer1.html','w')
	f.write(message)
	message = "<tr><th>Term</th>"
	f.write(message)
	message = "<th>Document</th>"
	f.write(message)
	message = "<th>Position</th></tr>"
	f.write(message)
	for x in terms:
		for y in terms[x]:
			message = "<tr><td>%s</td>"%x
			f.write(message)
			message = "<td>%s</td>"%y
			f.write(message)
			message = "<td>%s</td></tr>"%terms[x][y]
			f.write(message)
	message = "</table></body></html>"		
	f.write(message)
	f.close()	


def displayInvIndex():
	intialise()
	global path,fileNames,terms
	message = '<html><head>Total unique terms=%d</head><body><table border="1">'%len(terms)
	f = open('templates/Answer1.html','w')
	f.write(message)
	message = "<tr><th>Term</th>"
	f.write(message)
	message = "<th>Document</th></tr>"
	f.write(message)
	for x in sorted(terms):
		message = "<tr><td>%s</td>"%x
		f.write(message)
		message = "<td>%s</td></tr>"%terms[x].keys()
		f.write(message)
	message = "</table></body></html>"		
	f.write(message)
	f.close()	



def createIndex(path):
	global fileNames,terms
	for f in fileNames:
		file = open(path+f)
		data = file.read()
		tokens = tokenize(data)

		pos = 0
		for z in tokens:
			terms[z][f].append(pos)
			pos+=1
		
	#displayTermPosition()
	#displayInvIndex()



def query(t1,t2,k):
	intialise()
	global path,fileNames,terms
	p1 = terms[t1]
	p2 = terms[t2]
	docs = positionalIntersect(p1,p2,k)
	f = open('templates/Answer.html','w')
	message = '<html><head></head><body><table border="1">'
	f.write(message)
	message = "<tr><th>Document</th>"
	f.write(message)
	message = "<th>Position</th></tr>"
	f.write(message)
	for i in docs:
		message = "<tr><td>%s</td>"%i[0]
		f.write(message)
		message = "<td>%s</td></tr>"%i[1]
		f.write(message)
	message = "</table></body></html>"		
	f.write(message)
	f.close()


def queryInvIndex(s):
	intialise()
	global path,fileNames,terms
	answer = []
	#arr = re.compile('[&|]|\sand\s|\sor\s').split(s)
	#arr = re.split('(\W)', s)
	fn = set(fileNames)
	arr = s.strip().lower().split()
	flag = 1
	for ind in range(1,len(arr),2):
		if not(arr[ind]=="&" or arr[ind]=="|" or arr[ind]=="and" or arr[ind]=="or"):
			flag = 0
	if flag==0:
		print "Invalid Expression."
	else:
		for ind in range(0,len(arr),2):
			if '~' in arr[ind]:
				answer.append(fn - set(terms[arr[ind][2:-1]].keys()))
			else:
				answer.append(set(terms[arr[ind]].keys()))

		x = 1
		for ind in range(1,len(arr),2):
			if arr[ind] == "&" or arr[ind] == "and":
				answer[0] = answer[0] & answer[x]
			elif arr[ind] == "|" or arr[ind] == "or":
				answer[0] = answer[0] | answer[x]
			x+=1
		docs=list(answer[0])
		f = open('templates/Answer.html','w')
		message = '<html><head></head><body><table border="1">'
		f.write(message)
		message = "<tr><th>Document</th></tr>"
		f.write(message)
		for i in docs:
			message = "<tr><td>%s</td></tr>"%i
			f.write(message)
		message = "</table></body></html>"		
		f.write(message)
		f.close()



def positionalIntersect(p1,p2,k):
	intialise()
	answer = []
	intersection = list((set(p1.keys())) & (set(p2.keys())))
	for x in intersection:
		pos1 = p1[x]
		pos2 = p2[x]
		for y in pos1:
			for z in pos2:
				if abs(y-z)<=k:
					answer.append((x,[y,z]))

	return answer

def intialise():
	global path,fileNames,terms
	path = "./"
	fileNames = file_names(path)
	terms = defaultdict(lambda: defaultdict(list))
	createIndex(path)

intialise()



