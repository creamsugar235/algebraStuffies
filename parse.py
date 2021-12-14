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

precedence = ("(", ")",  "{", "}", "[", "]")

valid: tuple = ("=", "+", "-", "(", ")", ".", ",", "/", "*", "&", "^",
"%", "!", "{", "}", "[", "]", "|", "~", "log", "sin", "cos", "tan", "asin",
"acos", "atan", "atan2", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
"k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " ")

numbers: tuple = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".")

operators: tuple = ("+", "-", "*", "/", "%", "^", "&", "|", "~")

order: tuple = ("(", "{", "[", "^", "*", "/", "%", "+", "-", "&", "|", "~")

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

def SimpleCalc(a: float, b: float, operator: str):
	if operator == "^":
		return a ** b
	if operator == "*":
		return a * b
	if operator == "/":
		return a / b
	if operator == "%":
		return a % b
	if operator == "+":
		return a + b
	if operator == "-":
		return a - b
	if operator == "&":
		return int(a) & int(b)
	if operator == "|":
		return int(a) | int(b)
	if operator == "~":
		return int(a) ^ int(b)

def GetNums(text: str) -> tuple:
	s: str = ""
	ls: list = []
	for char in text:
		if char not in numbers and s != "":
			ls.append(s)
			s = ""
		else:
			s = s + char
	if len(ls) and s != "":
		ls.append(s)
	return ls

def Evaluate(text : str) -> float:
	tmp: str = text
	for o in order:
		while o in tmp:
			if o == '^':
				ind = len(tmp) - tmp[::-1].index(o)
				l: int = 0
				r: int = 0
				reachedNumber: bool = False
				for i in range(0, ind, -1):
					if tmp[i] in numbers and not reachedNumber:
						reachedNumber = True
					if reachedNumber and tmp[i] not in numbers:
						l = i + 1
				for i in range(ind, len(tmp)):
					if tmp[i] in numbers and not reachedNumber:
						reachedNumber = True
					if reachedNumber and tmp[i] not in numbers:
						r = i
				print(l, r, len(tmp), ind)
				op: str = [x for x in tmp[l:r] if x in operators][0]
				a: str = ""
				b: str = ""
				for char in tmp[l:r]:
					if char not in numbers:
						break
					a = a + char
				for char in tmp[tmp[l:r].index(op):r]:
					if char in numbers:
						b = b + char
				t = tmp[:l]
				print(t, l)
				t = t + str(SimpleCalc(float(a), float(b), op))
				t = t + tmp[r:len(tmp)]
				tmp = t
			else:
				ind = tmp.index(o)
				l: int = 0
				r: int = 0
				if len([x for x in tmp if x in operators]) != 1:
					reachedNumber: bool = False
					for i in range(0, ind):
						if tmp[i] in numbers and not reachedNumber:
							reachedNumber = True
						if reachedNumber and tmp[i] not in numbers:
							l = i + 1
					for i in range(ind, len(tmp)):
						if tmp[i] in numbers and not reachedNumber:
							reachedNumber = True
						if reachedNumber and tmp[i] not in numbers:
							r = i
				else:
					r = len(tmp)
					l = 0
				print(l, r, tmp, tmp[l:r])
				op: str = [x for x in tmp[l:r] if x in operators][0]
				a: str = ""
				b: str = ""
				for char in tmp[l:r]:
					if char not in numbers:
						break
					a = a + char
				for char in tmp[tmp[l:r].index(op):r]:
					if char in numbers:
						b = b + char
				t = tmp[:l]
				print(t, l)
				t = t + str(SimpleCalc(float(a), float(b), op))
				t = t + tmp[r:len(tmp)]
				tmp = t
				print(t)

		

def Parse(text: str) -> float:
	print(text)

	#parsing
	last: str = ''
	lastSignificant: list = ['', 0]
	closed: bool = True
	reachedNumber: bool = False
	brackets: dict = {
		"(" : 0,
		"{" : 0,
		"[" : 0,
	}
	#making sure syntax is valid
	for index, char in enumerate(text):
		if char in valid:
			if char in numbers and not reachedNumber:
				reachedNumber = True
			if char in operators and not reachedNumber:
				print(f"Error: ")
				print(f"\t{Colours.Bold}{Colours.Red}{text}")
				print(f"\t{Colours.Red}"+f"~"*(index) + "^")
				print(f"{Colours.Default}Character {index + 1}, expected number before operator: '{Colours.Red}{char}{Colours.Default}'")
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
			if lastSignificant[0] in operators:
				if char in operators:
					print("Error: ")
					print(f"\t{Colours.Bold}{Colours.Red}{text}")
					print(f"\t{Colours.Red}"+f"~"*(lastSignificant[1] + (index - lastSignificant[1])) + "^")
					print(f"{Colours.Default} Character {index + 1}, unexpected operator: '{Colours.Red}{char}{Colours.Default}'")
			last = char
			if char != " ": lastSignificant = [char, index]
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

	def Deepest(text: str, xcpt: tuple = ()):
		ind: int = 0
		deepest: int = 0
		howDeep: int = 0
		if sum([text.count('('), text.count('{'), text.count('{')]):
			try:
				return text.index("("), text.index("(")
			except: pass
			try:
				return text.index("{"), text.index("{")
			except: pass
			try:
				return text.index("["), text.index('[')
			except:
				pass
			
		for index, char in enumerate(text):
			if char in ("(", "{", "["):
				if howDeep > deepest and index not in xcpt:
					deepest = howDeep
					ind = index
				howDeep += 1
			elif char in (")", "}", "]"):
				howDeep -= 1
		return (ind, deepest)

	mostNestedIndexes: list = []
	i: int = 0
	char: str = ''
	bracketsToEvaluate: int = text.count('(') + text.count("{") + text.count("[")
	Evaluate(text)
	while i < len(text):
		char = text[i]
		if bracketsToEvaluate > 0:
			i = Deepest(text, mostNestedIndexes)[0] + 1
			mostNestedIndexes.append(i)
			nextBracket: int = 0
			for t in range(i, len(text)):
				if text[t] in (")", "}", "]"):
					nextBracket = t
					break
			tmp: str = text[i: nextBracket]
			print(tmp, i)
			opers: list = [x for x in tmp if x in operators]
			nums: list = GetNums(tmp)
			print(opers, nums)
			Evaluate(text)
			bracketsToEvaluate -= 1
		i += 1