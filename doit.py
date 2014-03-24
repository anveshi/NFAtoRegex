import copy

def fillMatrix(file, returnMatrix): #reads in the file and fills a matrix accordingly
	elements = readInts(file)
	origStates = int(next(elements))
	accepting = int(next(elements))
	numSymbols = int(next(elements))
	transitions = int(next(elements))
	returnMatrix = [['p' for k in range(origStates+2)] for j in range(origStates+2)]
	returnMatrix[0][1] = 'e' #new start state epsilons to start state
	if accepting < 0:
		start = 1
	else:
		start = 2
	for l in range(start, start+abs(accepting)):
		returnMatrix[l][origStates+1] = 'e' #epsilons from accepting states to new end state
	for element in elements:
		start = int(element)
		to = int(next(elements))
		trans = int(next(elements))
		if trans==0:
			trans = 'e'
		if returnMatrix[start][to] != 'p':
			returnMatrix[start][to] = str(returnMatrix[start][to])+"|"+str(trans)
		else:
			returnMatrix[start][to] = str(trans)
	for l in range(origStates+2): #all states can epsilon to themselves
		if returnMatrix[l][l] == 'p':
			returnMatrix[l][l] = 'e'

	return returnMatrix

def readInts(file): #this gets individual ints, regardless of how they are spaces/line breaks
	for line in file:
		for element in line.split():
			yield element

def prettyPrint(matrix): #print my matrix. not in rows/columns because really long regexes make it cumbersome to read that way
	for i in range(len(matrix)):
		for j in range(len(matrix[i])):
			print("Matrix[%i][%i] = \'%s\'" %(i, j, matrix[i][j]))

def union(str1, str2):
	if str1 == 'p':
		returnString = str2
	elif str2 == 'p':
		returnString = str1 #if either path is p, return the other
	elif str1 == str2:
		returnString = str1 #they are the same, so just return that
	else:
		returnString = str1+"|"+str2 #otherwise, it's an OR
	return returnString

def concatenate(str1, str2):
	if str1=='p' or str2=='p':
		returnString = 'p' #if either has no path, no path can exist
	elif str1=='e':
		returnString = str2
	elif str2=='e':
		returnString = str1 #if either one is e, just return the other
	else: #add any necessary parentheses, slap them together and return it
		str1vert = str1.find('|')
		str1parenth = str1.find(')')
		if str1vert == -1:
			pass
		else:
			if (str1vert > str1parenth) or str1parenth == -1:
				str1 = "("+str1+")"

		str2vert = str2.find('|')
		str2parenth = str2.find('(')
		if str2vert == -1:
			pass
		else:
			if (str2vert < str2parenth) or str2parenth == -1:
				str2 = "("+str2+")"
		returnString = str1+str2
	return returnString

def star(str):
	if str == 'e' or str == 'p':
		returnString = 'e' #if e or p, just return e
	elif len(str) == 1:
		returnString = str+"*" #only one digit? return it with a star
	else:
		returnString = "("+str+")*" #otherwise add some parentheses first
	return returnString

#Since not using global variables, "restore" is not needed. Honestly, this is just a wrapper
#for deepcopy
def saveRegExpr(matrx1):
	return copy.deepcopy(matrx1)

#eliminate a state by matching all paths in with all paths out
def eliminateState(getGone, matrix): 
	for start in range(len(matrix)):
		#print("start ", start)
		if start == getGone:
			continue
		inExpr = matrix[start][getGone]
		if inExpr == 'p':
			continue
		for end in range(len(matrix)):
			#print("end ", end)
			if end == getGone:
				continue
			outExpr = matrix[getGone][end]
			if outExpr == 'p':
				continue
			#print(start, " to ", getGone, " is ", inExpr)
			#print(getGone, " to ", end, " is ", outExpr)
			newExpr = concatenate(inExpr, concatenate(star(matrix[getGone][getGone]), outExpr))
			#print("this becomes ", union(newExpr, matrix[start][end]), " from ", start, " to ", end)
			matrix[start][end] = union(newExpr, matrix[start][end])
		matrix[start][getGone] = 'p'
	for end in range(len(matrix)):
		matrix[getGone][end] = 'p'
	return matrix

#iteratively eliminate the state for all the states except 0 and the final state
def completelyReduce(matrix):
	for i in range(1, len(matrix)-1):
		print("eliminate ", i)
		matrix = eliminateState(i, matrix)
	return matrix

#get a file name
file = input("File name?\n")
while not file:
	file = input("Please enter something\n")
myfile = None
while not myfile or myfile is None:
	try:
		myfile = open(file, 'r')
	except:
		file = input("Something went wrong. Probably invalid file. Try again.\n")
#fill the matrix
workingMatrix = []
workingMatrix = fillMatrix(myfile, workingMatrix)
prettyPrint(workingMatrix)

reducedMatrix = saveRegExpr(workingMatrix)
#behave according to input
keepAtIt = "filler"
while keepAtIt != "exit":
	keepAtIt = input("Eliminate which state? 'exit' to exit, 'complete' to do it all at once\n")
	if keepAtIt == "exit":
		continue
	else:
		if keepAtIt != "complete":
			try: 
				int(keepAtIt)
				reducedMatrix = eliminateState(int(keepAtIt), reducedMatrix)
				prettyPrint(reducedMatrix)
			except:
				keepAtIt = "filler"
				print("That's not a number\n")
		elif(keepAtIt == "complete"):
				completelyReduce(reducedMatrix)
				prettyPrint(reducedMatrix)