#import re as regex
class Colours:
	Header = '\033[95m'
	EndC = '\033[0m'
	Bold = '\033[1m'
	Underline = '\033[4m'
	Red = '\033[31m'
	Green = '\033[92m'
	Blue = '\033[94m'
	Cyan = '\033[96m'
	White = '\033[97m'
	Yellow = '\033[93m'
	Grey = '\033[90m'
	Black = '\033[90m'
	Default = '\033[39m'

variables: tuple = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
"m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")

precedence = ("(", ")", "{", "}", "[", "]")

valid: tuple = ("=", "+", "-", "(", ")", ".", ",", "/", "*", "&", "^",
"%", "!", "{", "}", "[", "]", "|", "~", "log", "sin", "cos", "tan", "asin",
"acos", "atan", "atan2", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
"k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " ")

numbers: tuple = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".")

operators: tuple = ("+", "-", "*", "/", "%", "^", "&", "|", "~")

#functions: tuple = ("log", "sin", "cos", "tan", "asin", "acos", "atan", "atan2")

def LastIndex(ls: tuple, vals: list):
	index: int = 0
	for i, item in enumerate(ls):
		if item in vals:
			index = i
	return index

def CountVariables(ls: list):
	i: int = 0
	for char in ls:
		if char in variables:
			i += 1
	return i

def CountValid(ls: list):
	i: int = 0
	for char in ls:
		if char in valid:
			i += 1

def CountOperators(ls: list):
	i: int = 0
	for char in ls:
		if char in operators:
			i += 1

def IndexVariables(ls: list):
	indexes: list = []
	for i in range(len(ls)):
		if ls[i] in variables:
			indexes.append(i)
	return indexes

def IndexValid(ls: list):
	indexes: list = []
	for i in range(len(ls)):
		if ls[i] in valid:
			indexes.append(i)
	return indexes

def Parse(text: str):
	print(text)

	#parsing
	values: list = []
	val: str = ""
	last: str = ''
	closed: bool = True
	brackets: dict = {
		"(" : 0,
		"{" : 0,
		"[" : 0,
	}
	#making sure syntax is valid
	for index, char in enumerate(list(text)):
		if char in valid:
			if char == " ":
				values.append(val)
				val = ""
			#checking brackets
			if char in precedence:
				closed = sum(brackets.values()) == 0
				if char in ("]", ")", "}") and closed:
					print("Error: ")
					print(f"\t{Colours.Bold}{Colours.Red}{text}")
					print(f"\t{Colours.Red}"+f"~"*(index) + "^")
					print(f"{Colours.Default} Character {index + 1}, mis-matched brackets: '{Colours.Red}{char}{Colours.Default}'")
				if char in ("(", "{", "["):
					brackets[char] += 1
				elif char in (")", "}", "]"):
					if char == ")":
						brackets["("] -= 1
					elif char == "}":
						brackets["{"] -= 1
					else:
						brackets["["] -= 1
			#checking syntax
			if last in numbers:
				if char not in numbers:
					values.append(val)
					val = ""
				else:
					val = val + char
			elif last in operators:
				if char in operators:
					print("Error: ")
					print(f"\t{Colours.Bold}{Colours.Red}{text}")
					print(f"\t{Colours.Red}"+f"~"*(index) + "^")
					print(f"{Colours.Default} Character {index + 1}, unexpected operator: '{Colours.Red}{char}{Colours.Default}'")
				if char not in operators:
					values.append(val)
					val = ""
				else:
					val = val + char
			elif last in variables:
				if char not in variables:
					values.append(val)
					val = ""
				else:
					val = val + char
			last = char
		#invalid character
		else:
			print(f"Error: ")
			print(f"\t{Colours.Bold}{Colours.Red}{text}")
			print(f"\t{Colours.Red}"+f"~"*(index) + "^")
			print(f"{Colours.Default}Character {index + 1}, invalid character: '{Colours.Red}{char}{Colours.Default}'")
			return None
	closed = sum(brackets.values()) == 0
	if not closed:
		print(f"Error: ")
		print(f"Incomplete bracket formatting")
	
	deepestIndex: int = 0
	opened: int = 0

