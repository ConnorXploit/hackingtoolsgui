from hackingtools.core import Logger, Utils, Config
if Utils.amIdjango(__name__):
	from hackingtools.core import hackingtools as ht
else:
	import hackingtools as ht
	
import os

config = Config.getConfig(parentKey='modules', key='ht_hash')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		self._main_gui_func_ = 'hashContent'
		self.__gui_label__ = 'Hash Calculator'

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_hash'), debug_module=True)

	def hashContent(self, content):
		try:
			content.lower()
			contador = 1
			a = 23
			b = 35
			c = 36
			d = 75
			e = 72
			f = 24
			g = 63
			h = 62
			i = 56
			j = 63
			k = 19
			l = 37
			n = 47
			m = 48
			o = 634
			p = 745
			q = 85
			r = 756
			s = 4
			t = 48
			u = 36
			v = 473
			w = 7
			x = 7342
			y = 65
			z = 46
			pt = 342
			kh = 576
			valores = ("")
			if "a" in  content:
				
				contador = content.count("a")     
				ac = contador*a*b*contador*c*d*e*f**contador*g*h*i*j*k*l*m*n*s**t*u*v*contador*w*x*y*z*pt*contador
				
			if "b" in  content:
				contador = content.count("b")
				bc = a*pt*j*d*contador**l*f*t*contador**h*u*j*h*x*l*contador*l*o*z*u*v*c*c*q*z*pt
			if "c" in content:
				contador = content.count("c")
				cc = f*h*j*e*+f*f*g*contador*h*u*j*h*k*e*contador*a*o*z*u*v*c*c*q*h**s+h+contador**u*j*h*x*l*l
			if "d" in content:
				contador = content.count("d")
				dc = f*h*j**g*contador*h*e*+f*u*j*h*k*e*contador*a*e*+f*f*h**s+h+contador**u*j*h*+f*f*e+f*f*x*l*l
			if "e" in content:
				contador = content.count("e")
				ec = f*h*k*j*h*k*e*contador*a+h+contador**u*j*h*+f*f*e+f*f*e*+f*f*h**s*x*l*l
			if "f" in content:
				contador = content.count("f")
				fc = f*j*e+f+k*l*m*n*s**f*x+h*s+k*l*m*n*contador*s**d+f*a*l*l*contador
			if "g" in content:
				contador = content.count("g")
				gc = f*h*j*j*h*+f*f*e+f*f*x*l**g*contador*h*e**s+h+contador**u
			if "h" in content:
				contador = content.count("h")
				hc = f*h*j**g*contador*h*e*x+h*s+k*l*e*contador*h+contador**u*x+h*s+k*l*m
			if "i" in content:
				contador = content.count("i")
				ic = f*u*j*h*k*e*contador*a*e*+f*f+k*e*contador*a*e*+f*u*j*h*k*e*contador*a*e*+f*f*f*h**s+h+contador**u*j*h*+f*f*e+f*f*x*l*l
			if "j" in content:
				contador = content.count("j")
				jc = f*k*l*m*n*s**t*u*contador*j*h*k*e+j*h*k*e
			if "k" in content:
				contador = content.count("k")
				kc = f*h*f*f*e*+f*u*j*h*e+f*f*x*l*l*s+h+contador**u*j*h*+f*f*e+f*f*x*l*l
			if "l" in content:
				contador = content.count("l")
				lc = f*h*j*h*+f*f*e+f*f*x*l+h+contador**u*j*h*+f*f*e+f*f*x*l*l
			if "n" in content:
				contador = content.count("n")
				nc = f*h*j**g*contador*h*e*+j*h*e+f*f*x*l+f*x*l*l
			if "m" in content:
				contador = content.count("m")
				mc = f*h*j**g*contador*h*e*+f*u+u*j*h*+f*f*e+f*f*x*l*l
			if "o" in content:
				contador = content.count("o")
				oc = f*h*j**g*contador*h*e*+f*u*j*h*+f*f*e+f*f*x*l**x*l*l
			if "p" in content:
				contador = content.count("p")
				pc = f*h*j**g*contador*h*e*+f*h*+f*f*e+f*f*x*l**k*e+j*h*k*e
			if "q" in content:
				contador = content.count("q")
				qc = f*h*j**g*contador*h*e*+f*u*j*h*k*e+j*h*k*e+f*f*x*l*l
			if "r" in content:
				contador = content.count("r")
				rc = f*h*j**g*contador*h*e*+f*u*j*h**s+h+contador**u*j*h*+f*f*e+f*f*x*l*l
			if "s" in content:
				contador = content.count("s")
				sc = f*h*j**g*contador*h*e*+f*u*j*h*h*i*j*k*l*m*n*s**j*h*+h*i*j*k*l*m*n*s**f*e+f*f*x*l*l
			if "t" in content:
				contador = content.count("t")
				tc = f*h*h*i*j*k*l*m*n*s**t*h*k*e*contador*a*e+f*e+f*f*x*l*l
			if "u" in content:
				contador = content.count("u")
				uc = contador*h*e*+f*u*h*i*j*k*l*m*n*s**t*+f*f*e+f*f*x*l*l
			if "v" in content:
				contador = content.count("v")
				vc = f*h*j**g*contador*h*e*+f*u**l*m*u*j*h*k*e*n*s**t*k*h*+f*f*e+f*f*x*l*l
			if "w" in content:
				contador = content.count("w")
				wc = f*h*j**g*contador*h*e*+f*u*j*h*k*e*u*j*h*k*e*e+f*f*e+f*f*x**x*l*l
			if "x" in content:
				contador = content.count("x")
				xc = f*h*j**g*contador*h*e*+f*u*j*h*k*e*contador*a*e*+f*f*h**s+h+contador**u*j*h*+f*f*e+f*f*x*l*l
			if "y" in content:
				contador = content.count("y")
				yc = f*h*j*l*m*n*s**t*k+contador*u*j*h*+f*f*h**s+h+contador
			if "z" in content:
				contador = content.count("z")
				zc = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if " " in content:
				contador = content.count(" ")
				espacio = f*h*k*l*m*n*s*j+g*contador*h*e*i*j*k*j*k*l*m*n*s
			if "." in content:
				contador = content.count(".")
				punto = f*h**k*l+h*k*l*m*n*s*j+m*n*s*k*l*m*n*s+h-f**+i*j*k*l*m*n*s
			if "-" in content:
				contador = content.count("-")
				barra = +j+g*contador*h*s+i*j+k*l*m*n*s*k*l*m*n*s
			if "_" in content:
				contador = content.count("_")
				barrabaja = f*h**k*l*m*n*s*e*contador*a*h**s+i*j*k*l*m*n*s
			if "}" in content:
				contador = content.count("}")
				corcheteuno = f*h*j+g*contador*h*e*i*j*kh**s+i*j*k*l*m*n*s+l*m*n*s
			if "{" in content:
				contador = content.count("{")
				corchetedos = f*h*j+g*contador*h*e*i*j*k*l*l*m*n*s+l*m*n**contador*a*h**s+i*j*k*l*m*n*s
			if "+" in content:
				contador = content.count("+")
				mas = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "*" in content:
				contador = content.count("*")
				asterisco = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "," in content:
				contador = content.count(",")
				coma = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if ";" in content:
				contador = content.count(";")
				puntoycoma = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if ":" in content:
				contador = content.count(":")
				dospuntos = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "1" in content:
				contador = content.count("1")
				uno = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "2" in content:
				contador = content.count("2")
				dos = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "3" in content:
				contador = content.count("3")
				tres = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "4" in content:
				contador = content.count("4")
				cuatro = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "5" in content:
				contador = content.count("5")
				cinco = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "6" in content:
				contador = content.count("6")
				seis = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "7" in content:
				contador = content.count("7")
				siete = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "8" in content:
				contador = content.count("8")
				ocho = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "9" in content:
				contador = content.count("9")
				nueve = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "0" in content:
				contador = content.count("z")
				cero = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "[" in content:
				contador = content.count("[")
				corchetetres = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "]" in content:
				contador = content.count("]")
				corchetecuatro = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if '"' in content:
				contador = content.count('"')
				comilla = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "'" in content:
				contador = content.count("'")
				comi = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "=" in content:
				contador = content.count("z")
				igual = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "(" in content:
				contador = content.count("(")
				parentesisa = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if ")" in content:
				contador = content.count(")")
				parentesisb = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "!" in content:
				contador = content.count("!")
				exclamacion = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "@" in content:
				contador = content.count("@")
				arroba = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "#" in content:
				contador = content.count("#")
				almoadilla = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "$" in content:
				contador = content.count("$")
				dinero = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "/" in content:
				contador = content.count("/")
				barra = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "´" in content:
				contador = content.count("´")
				tildea = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "`" in content:
				contador = content.count("`")
				tildeb = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s
			if "¨" in content:
				contador = content.count("¨")
				tildec = f*h*j+g*contador*h*e*i*j*k*l*m*n*s**t*k*e*contador*a*h**s+i*j*k*l*m*n*s


			if "a" not in  content:
				ac = 45336
			if "b" not in  content:
				bc = 8363
			if "c" not in content:
				cc = 53524
			if "d" not in content:
				dc = 485353
			if "e" not in content:
				ec = 976524
			if "f" not in content:
				fc = 73562
			if "g" not in content:
				gc = 36455
			if "h" not in content:
				hc = 64572
			if "i" not in content:
				ic = 74522
			if "j" not in content:
				jc = 3635
			if "k" not in content:
				kc = 55534
			if "l" not in content:
				lc = 9846
			if "n" not in content:
				nc = 83654
			if "m" not in content:
				mc = 34133
			if "o" not in content:
				oc = 3735
			if "p" not in content:
				pc = 30372
			if "q" not in content:
				qc = 64522
			if "r" not in content:
				rc = 3524
			if "s" not in content:
				sc = 83624
			if "t" not in content:
				tc = 52233
			if "u" not in content:
				uc = 677563
			if "v" not in content:
				vc = 74386442
			if "w" not in content:
				wc = 2735222
			if "x" not in content:
				xc = 77454
			if "y" not in content:
				yc = 5343332
			if "z" not in content:
				zc = 84624
			if "." not in content:
				punto = 86454
			if "-" not in content:
				barra = 74536
			if " " not in content:
				espacio = 73253
			if "'" not in content:
				comi = 73535
			if "_" not in content:
				barrabaja = 73546
			if "{" not in content:
				corcheteuno = 764535
			if "}" not in content:
				corchetedos = 735334
			if "[" not in content:
				corchetetres = 734232
			if "]" not in content:
				corchetecuatro = 6346
			if "1" not in content:
				uno = 95635
			if "2" not in content:
				dos = 35232
			if "3" not in content:
				tres = 342527
			if "4" not in content:
				cuatro = 45242
			if "5" not in content:
				cinco = 84537
			if "6" not in content:
				seis = 36241
			if "7" not in content:
				siete = 24361
			if "8" not in content:
				ocho = 84523
			if "9" not in content:
				nueve = 51423
			if "0" not in content:
				cero = 34261
			if ";" not in content:
				puntoycoma = 94524
			if ":" not in content:
				dospuntos = 83521
			if "=" not in content:
				igual = 4535
			if "!" not in content:
				exclamacion = 72525
			if "@" not in content:
				arroba = 12322
			if "$" not in content:
				dinero = 74533
			if "/" not in content:
				barra = 3523
			if "´" not in content:
				tildea = 84724
			if "`" not in content:
				tildeb = 324
			if "¨" not in content:
				tildec = 64835
			if "+" not in content:
				mas = 84624
			if ")" not in content:
				parentesisa = 84624
			if "(" not in content:
				parentesisb = 84624

			return str(ac*cc*bc+dc*ec+fc*gc*hc*ic+jc+kc+lc*ac*nc*mc*oc-pc*qc+rc+sc-tc*uc*wc*xc*yc*zc-rc+sc-tc*nc*a-barra*tildea+tildeb+tildec*mas+parentesisa*parentesisb+dinero+dinero*exclamacion+igual+puntoycoma-dospuntos+uno+dos*3+cuatro*cinco+seis*ocho+nueve*cero+corcheteuno-corchetedos*corchetetres+corchetecuatro+barrabaja+comi+espacio+barra-punto)
		except Exception as e:
			return str(e)
