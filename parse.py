import math
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
"%", "{", "}", "[", "]", "|", "~", "log", "sin", "cos", "tan", "asin",
"acos", "atan", "atan2", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
"k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", " ")

numbers: tuple = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".")

operators: tuple = ("+", "-", "*", "/", "%", "^", "&", "|", "~")

order: tuple = ("(", "{", "[", "^", "*", "/", "%", "+", "-", "&", "|", "~")

functions: tuple = ("log", "sin", "cos", "tan", "asin", "acos", "atan", "fac", "flr", "ceil")

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

def RunFunction(x: float, func: str):
	if func == "log":
		return math.log(x)
	elif func == "sin":
		return math.sin(x)
	elif func == "cos":
		return math.cos(x)
	elif func == "tan":
		return math.tan(x)
	elif func == "asin":
		return math.asin(x)
	elif func == "acos":
		return math.acos(x)
	elif func == "atan":
		return math.atan(x)
	elif func == "fac":
		return math.factorial(x)
	elif func == "flr":
		return math.floor(x)
	elif func == "ceil":
		return math.ceil(x)

def CheckSyntax(text: str) -> bool:
	#making sure syntax is valid
	last: str = ''
	lastSignificant: list = ['', 0]
	closed: bool = True
	reachedNumber: bool = False
	brackets: dict = {
		"(" : 0,
		"{" : 0,
		"[" : 0,
	}
	for index, char in enumerate(text):
		if char in valid:
			if char in numbers and not reachedNumber:
				reachedNumber = True
			if char in operators and not reachedNumber:
				print(f"Error: ")
				print(f"\t{Colours.Bold}{Colours.Red}{text}")
				print(f"\t{Colours.Red}"+f"~"*(index) + "^")
				print(f"{Colours.Default}Character {index + 1}, expected number before operator: '{Colours.Red}{char}{Colours.Default}'")
				return False
			#checking brackets
			if char in precedence:
				closed = sum(brackets.values()) == 0
				if char in ("]", ")", "}") and closed:
					print("Error: ")
					print(f"\t{Colours.Bold}{Colours.Red}{text}")
					print(f"\t{Colours.Red}"+f"~"*(index) + "^")
					print(f"{Colours.Default} Character {index + 1}, mis-matched brackets: '{Colours.Red}{char}{Colours.Default}'")
					return False
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
					return False
			last = char
			if char != " ": lastSignificant = [char, index]
		#invalid character
		else:
			print(f"Error: ")
			print(f"\t{Colours.Bold}{Colours.Red}{text}")
			print(f"\t{Colours.Red}"+f"~"*(index) + "^")
			print(f"{Colours.Default}Character {index + 1}, invalid character: '{Colours.Red}{char}{Colours.Default}'")
			return False
	closed = sum(brackets.values()) == 0
	if not closed:
		print(f"Error: ")
		print(f"Incomplete bracket formatting")
		return False
	return True

def Evaluate(text: list) -> list:
	while len([x for x in text if x in precedence]):
		l: int = 0
		r: int = 0
		for index, char in enumerate(text):
			if char in precedence:
				l = index
				break
		for index, char in enumerate(text[::-1]):
			if char in precedence:
				r = len(text) - 1 - index
				break
		t = text[0:l]
		e = Evaluate(text[l+1:r])
		for s in e:
			t.append(s)
		t = t + text[r+1:len(text)]
		text = t
	for f in functions:
		while f in text:
			ind = text.index(f)
			val = RunFunction(float(text[ind+1]), f)
			text[ind] = val
			del text[ind + 1]
	for o in order:
		while o in text:
			if o == '^':
				ind = len(text) - 1 - text[::-1].index(o)
				a = text[ind - 1]
				b = text[ind + 1]
				val = SimpleCalc(float(a), float(b), o)
				text[ind] = str(val)
				del text[ind - 1]
				del text[ind]
			else:
				ind = text.index(o)
				a = text[ind - 1]
				b = text[ind + 1]
				val = SimpleCalc(float(a), float(b), o)
				text[ind] = str(val)
				del text[ind - 1]
				del text[ind]
	return text

def Parse(text: str) -> float:
	if not CheckSyntax(text):
		return
	symbols: list = []
	curr: str = ""
	for index, char in enumerate(x for x in text if x != ' '):
		if char in operators or char in precedence:
			if curr != "":
				symbols.append(curr)
			symbols.append(char)
			curr = ""
		if char not in operators and char not in precedence:
			curr = curr + char
	if curr != "":
		symbols.append(curr)
	try:
		print(Evaluate(symbols)[0])
	except ZeroDivisionError as e:
		print(f'ZeroDivisionError: {e}')
	except Exception as e:
		print(f"Erorr occured: {e}")