from logging import raiseExceptions
from re import X
import string
alfabetoU = list(string.ascii_uppercase)
alfabetoL = list(string.ascii_lowercase)
numberArray = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def espacio():
  while preanalisis == ' ':
      coincidir(' ')

def newline():
  if preanalisis == "\n":
    coincidir(preanalisis)
  espacio()

def coincidir(char):
    global indice, length, preanalisis, cadena
    buffer = preanalisis
    indice += 1
    if indice < length:
      preanalisis = cadena[indice]  
    elif indice == length:
      preanalisis = '\0'
    return buffer

def leerGramatica(c = ""):
    global preanalisis, indice, length, cadena, e
    cadena = c
    indice = 0
    length = len(cadena)
    e = ""
    preanalisis = cadena[0]
    try:
      e = programa()
    except:
      e = "ERROR"
    return e

def preview():
  global indice, cadena
  aux = indice
  word = ''
  while cadena[aux] != ' ' and cadena[aux] != ';' and cadena[aux] != ':':
    word += cadena[aux]
    aux += 1
    if aux >= len(cadena):
      break
  return word

def inDicc(elem):
  if dicc == {}:
    return False
  for key in dicc.keys():
    lista = dicc[key]
    if elem in lista:
      return key
  return False

def addDicc(tipo, lista):
  for var in lista:
    if inDicc(var) != False:
      dicc[inDicc(var)].remove(var)
    dicc[tipo].append(var)

def listaVar(string):
  lista = []
  word = ''
  if string != '':
    for i in range(0, len(string)):
      if (string[i] != ' '):
        if (string[i] == ','):
          lista.append(word)
          word = ''
        else:
          word += string[i]
  if word != '':
    lista.append(word)
  return lista

def compare(op1, op, op2):
  op1 = operadorValor(op1)
  op2 = operadorValor(op2)
  if op == '=' or op == "==":
    return eval("op1==op2")
  elif op == '>' or op == ">>":
    return eval("op1>op2")
  elif op == '<' or op == "<<":
    return eval("op1<op2")
  elif op == '<=' or op == "=<":
    return eval("op1<=op2")
  elif op == '>=' or op == "=>":
    return eval("op1>=op2")
  elif op == '<>' or op == "><" or op == "!=":
    return eval("op1!=op2")

def operadorValor(o):
  if len(o) > 0:
    if o[0] in numberArray:
      if '.' in o:
        o = float(o)
      else:
        o = int(o)
    else:
      if o in dictionary:
          o = dictionary[o]
      else:
          raise Exception
  else:
    o = 0
  return o

def iniciarVar():
  for key in dicc.keys():
    if key == 'entero':
      lista = dicc[key]
      for elem in lista:
        dictionary[elem] = 0
    elif key == 'real':
      lista = dicc[key]
      for elem in lista:
        dictionary[elem] = 0.0
  pass

def declaraciones():
  declaracion()
  if preanalisis == ';':
    coincidir(';')
    espacio()
    newline()
    sigDeclaraciones()
  else:
    raise Exception
  
def sigDeclaraciones():
  if preview() == "entero" or preview() == "real":
    declaraciones()
  else:
    pass

def declaracion():
  t = tipo()
  l = listaVariables()
  addDicc(t, listaVar(l))

def tipo():
  word = identificador()
  if word == "entero" or word == "real":
    return word
  else:
    raise Exception

def listaVariables():
  word = identificador()
  if preanalisis == ',':
    word += sigListaVariables()
  return word

def sigListaVariables():
  coincidir(',')
  espacio()
  word = ", "
  word += identificador()
  if preanalisis == ',':
    word += sigListaVariables()
  return word

def identificador():
  word = letra()
  if (preanalisis in alfabetoU or preanalisis in alfabetoL or preanalisis in numberArray) and preanalisis != ';':
    word += restoLetras()
  espacio()
  newline()
  return word

def letra():
  word = ''
  if (preanalisis in alfabetoU or preanalisis in alfabetoL) and preanalisis != ';':
    word = preanalisis
    coincidir(preanalisis)
  return word

def restoLetras():
  word = ''
  while (preanalisis in alfabetoU or preanalisis in alfabetoL or preanalisis in numberArray) and preanalisis != ';':
    word += preanalisis
    coincidir(preanalisis)
  return word

def programa():
  word = identificador()
  newline()
  if word == "begin":
    declaraciones()
    iniciarVar()
    ordenes(True)
    word = identificador()
    newline()
    if word == "end":
      return 0
    else:
      raise Exception
  else:
    raise Exception

def ordenes(flag):
  if preview() != "end" and preview() != "else":
    orden(flag)
    ordenes(flag)
    
def orden(flag):
  if preview != "else":
    if preview() == "if":
      condicion(flag)
    elif preview() == "while":
      bucleWhile(flag)
    else:
      asignar(flag)

def comparacion():
    global tablaSimbolos
    op1 = operador()
    op = condicionOp()
    op2 = operador()
    tablaSimbolos += op1 + " " + op + " " + op2 + "\n"
    return compare(op1, op, op2)

def operador():
  word = ''
  if preanalisis in numberArray:
    word = numeros()
    espacio()
  elif preanalisis == '-':
    word = '0'
    return word
  elif preanalisis in preanalisis in alfabetoU or preanalisis in alfabetoL:
    word = identificador()
  else:
    raise Exception
  return word

def condicionOp():
  espacio()
  op = ''
  if preanalisis in ['=', '>', '<']:
    op = preanalisis
    coincidir(preanalisis)
    if preanalisis in ['=', '<', '>']:
      op += preanalisis
      coincidir(preanalisis)
    espacio()
  else:
    raise Exception
  return op

def bucleWhile(flag):
  global tablaSimbolos
  word = identificador()
  tablaSimbolos += word + " "
  pos = getPosicion()
  coincidir('(')
  espacio()
  comp = comparacion()
  coincidir(')')
  espacio()
  newline()
  if flag == False:
    comp = not comp
  ordenes(comp)
  longitud = len(tablaSimbolos)
  repetirWhile(pos, flag)
  recortarTabla(longitud)
  word = identificador()
  if word != "end":
    raise Exception
  tablaSimbolos += "end\n"
  coincidir(';')
  espacio()
  newline()

def repetirWhile(pos, flag):
  if flag == True:
    setPosicion(pos)
    coincidir('(')
    espacio()
    comp = comparacion()
    coincidir(')')
    espacio()
    newline()
    ordenes(comp)
    if comp == True:
      repetirWhile(pos, flag)

def asignar(flag):
  global tablaSimbolos
  id = identificador()
  tablaSimbolos += id + " = "
  coincidir(':')
  coincidir('=')
  espacio()
  num = expresionAritmetica()
  tablaSimbolos += "\n"
  if flag == True:
    updateDict(id, eval(num))
  coincidir(';')
  espacio()
  newline()
  ordenes(flag) 

def expresionAritmetica():
    global tablaSimbolos
    expr = ''
    n = ""
    if preanalisis == '(':
        coincidir('(')
        espacio()
        expr += expresionAritmetica()
        expr += operadorAritmetico()
        coincidir(')')
        espacio()
        expr += expArit()
    else:
        if preanalisis in numberArray or preanalisis == '-':
            n += numeros()
            expr += n
            tablaSimbolos += n + " "
            espacio()
            expr += expArit()
        elif preanalisis in preanalisis in alfabetoU or preanalisis in alfabetoL:
            id = identificador()
            expr += str(dictionary[id])
            tablaSimbolos += id + " "
            expr += expArit()
    return expr
 
def expArit():
  global tablaSimbolos
  expr, op = '', ""
  if preanalisis in ['+', '-', '*', '/']:
    op += operadorAritmetico()
    tablaSimbolos += op + " "
    expr += op
    expr += expresionAritmetica()
    expr += expArit()
  return expr

def operadorAritmetico():
  op = ''
  if preanalisis in ['+', '-', '*', '/']:
    op = preanalisis
    coincidir(preanalisis)
    espacio()
  return op

def updateDict(id, num):
  if inDicc(id) != False:
    key = inDicc(id)
    if key == "entero":
      dictionary[id] = int(num)
    else:
      dictionary[id] = float(num)
  else:
    raise Exception

def condicion(flag):
  global tablaSimbolos
  word = identificador()
  tablaSimbolos += word + " "
  coincidir('(')
  espacio()
  comp = comparacion()
  coincidir(')')
  espacio()
  newline()
  if flag == False:
    comp = not comp
  ordenes(comp)
  if preview() == "else":
    tablaSimbolos += "else\n"
    word = identificador()
    newline()
    if flag == False:
      comp = True
    ordenes(not comp)
  word = identificador()
  if word != "end":
    raise Exception
  tablaSimbolos += "end\n"
  coincidir(';')
  newline()
  espacio()

def numeros():
  number = ''
  if preanalisis == '-':
    return "0"
  while preanalisis in numberArray:
    number += numero()
  if preanalisis == '.':
    number += '.'
    coincidir('.')
    while preanalisis in numberArray:
      number += numero()
  return number

def numero():
  number = ''
  if preanalisis in numberArray:
    number = preanalisis
    coincidir(preanalisis)
  else:
    raise Exception
  return number

def getPosicion():
  global indice
  return indice

def setPosicion(posicion):
  global indice
  indice = posicion

def recortarTabla(lon):
    global tablaSimbolos
    tablaSimbolos = tablaSimbolos[0:lon]

def inicioGramatica(cadena):
    global tablaSimbolos, dicc, dictionary
    tablaSimbolos = ""
    dicc = {"entero" : [], "real" : []}
    dictionary = {}
    try:
        e = leerGramatica(cadena)
        if e == "ERROR":
          return e
    except:
        return "ERROR"
    return tablaSimbolos
