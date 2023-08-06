#!/usr/bin/python3
import sys
import psutil
import os

# Echo parameter for VHL
toEcho = 0
# Default variable to be inserted into VHL
dInt = 255

# Global 2D array for VHL
dbs = [
	# Standard datablock(DB) named 'STD'
        [sys.getsizeof(dInt), "STD", hex(id(dInt))]
      ]

#__________CLASSES__________

# VHL (Variable Handler)
class vhl:

	# Create new DB
	def CrtNewDB(var, gvnName):
		gvnSize = sys.getsizeof(var)
		gvnMemAddr = hex(id(var))
		try:

			# Inserting to the top after the STD DB
			dbs.insert(1,[gvnSize, gvnName, gvnMemAddr])
			if toEcho == 1:
				print("[WTF-DBS] Variable added with name: "+gvnName)
		except:
			raise Exception("CNDB - ERROR AT INSERTING TO DBS")
	# Get all DBs
	def GetAllDB():
		print("|---------[WTFPY - DBS]---------|")
		print("|SIZE\t|NAME\t|Mem. Addr\t|")
		print("--------------------------------|")
		for x in dbs:
                	for y in x:
                        	print(y, end = "\t|")
                	print("\n--------------------------------|")

	# Search for a DB by it's name
	def SrcSingleDB(name):
		print("Searching for: " + name)
		try:
			for x in dbs:
				for y in x:
					if name == y:
						print("SIZE | NAME | Mem Addr. |")
						print(x)
						print("--------------------------------|")
		except:
			raise Exception("[WTF-DBS] SSDB - DATABLOCK NOT FOUND")

	# Delete a DB by it's name
	def DelSingleDB(name):
		print("[WTF-DBS] Deleting: "+name)
		for x in dbs:
			for y in x:
				if name == y:
					dbs.remove(x)
					if toEcho == 1:
						print("[WTF-DBS] Removed: "+str(x))

#________FUNCTIONS________

# Get kwargs for variables
def variable_kwargs(**kwargs):
     return kwargs

# Get runtime value of a variable
def RuntmVal(var, name=""):
	print("[OUTPUT OF "+str(name)+"]: "+str(var))

# Set runtime value of a variable
def SetRuntmVal(var, val, name=""):
	oldvar = var
	var = val
	print("["+str(name)+" is changed TO: "+str(val)+" FROM: "+str(oldvar)+"]")

# Get memory address of a variable
def MemAddr(var):
	return hex(id(var))

# Check if two variable are referencing to the same memory address
def RefCheck(var1, var2):
	if id(var1) == id(var2):
		bln = True
		print("[REFCHECK]: ",bln, "(",var1,",",var2,")")
	else:
		bln = False
		print("[REFCHECK]: ",bln, "(",var1,",",var2,")")

# Get size of a variable
def GetSize(var):
	return sys.getsizeof(var)

# Get the memory usage of your program. Displaying in % and MB
def GetMemoryUsage():
    pid = psutil.Process(os.getpid())
    mempcnt = pid.memory_percent()
    inmb = (psutil.virtual_memory().total / 100 * mempcnt) / 1000000
    print("Memory usage: %.2f%% - %.2fMB" % (mempcnt, inmb))

# Turn off comfirmation messages from VHL
def EchoTurnOff():
	toEcho = 0

# De-reference a variable
def DeRef(var):
	var = None

def GetType(var):
    if str(type(var))[8:].strip("'>") == "str": print("String") 
    if str(type(var))[8:].strip("'>") == "int": print("Integer") 
    if str(type(var))[8:].strip("'>") == "float": print("Float")
