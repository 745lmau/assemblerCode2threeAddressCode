from .gramatica import *
from re import X
import string
alfabetoU = list(string.ascii_uppercase)
alfabetoL = list(string.ascii_lowercase)
numberArray = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def A():
    espacio()
    id, x = "", ""
    
    if '=' in cadena:
        id = Id()
        coincidir('=')
        x = E()
    else:
      if '-' in cadena or '+' in cadena or '/' in cadena or '*' in cadena:
        x = E()
      elif preanalisis in alfabetoU or preanalisis in alfabetoL or preanalisis == "_":
          id = Id()
      elif preanalisis in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:    
        x = E()
          
    if x == "":
        x = "0"
    
    return(id, x)

def Id():
  id = ''
  if preanalisis in alfabetoU or preanalisis in alfabetoL or preanalisis == "_":
    id = preanalisis
    coincidir(preanalisis)
    id += Ide()
  return id

def Ide():
  ide = ''
  if preanalisis in alfabetoU or preanalisis in alfabetoL or preanalisis in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
    ide = preanalisis
    coincidir(preanalisis)
    ide += Ide()
  return ide

def E():
  t = T()
  t = RE(t)
  return t


def RE( her ):
  if preanalisis == '+':
    coincidir('+')
    t = T()
    t = RE( her + " " + t + " " + "+")
    return t
  if preanalisis == '-':
    coincidir('-')
    t = T()
    t = RE( her + " " + t + " " + "-" )
    return t
  else:
    return her
 
def T():
  t = F()
  t = RT(t)
  return t

def RT( her ):
  if preanalisis == '*':
    coincidir('*')
    t = F()
    t = RT( her + " " + t + " " + "*" )
    return t
  elif preanalisis == '/':
    coincidir('/')
    t = F()
    t = RT( her + " " + t + " " + "/" )
    return t
  else:
    return her

def F():
  if preanalisis == '(':
    coincidir('(')
    t = E()
    coincidir(')')
    return t
  elif preanalisis in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
    numero = ''
    while preanalisis in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
      numero += digito()
    return numero
  elif preanalisis in preanalisis in alfabetoU or preanalisis in alfabetoL or preanalisis == "_":
    variable = Id()
    if variable in dictionary:
        return variable
    else:
        dictionary["ERROR_0"] = variable
        raise Exception
  else:
    raise Exception

def digito():
  if preanalisis in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
    return coincidir(preanalisis)
  else:
    raise Exception("La cadena no pertenece a la gramatica")

def espacio():
  while preanalisis == ' ':
      coincidir(' ')


def coincidir(char):
    global indice, length, preanalisis, cadena
    buffer = preanalisis
    indice += 1
    if indice < length:
      preanalisis = cadena[indice]  
    elif indice == length:
      preanalisis = '\0'
    espacio()
    return buffer


def leerGramatica(c = ""):
    global preanalisis, indice, length, cadena, e
    cadena = c
    indice = 0
    length = len(cadena)
    e, a = "", ""
    try:
        preanalisis = cadena[0]
    except:
        e = "No se escribio ninguna cadena"
    else:
        try:
            e, a = A()  
            if indice < length:
                raise Exception("Falta el parentesis de inicio")
        except Exception:
            if "ERROR_0" in dictionary:
                e = "ERROR: Identificador: {} No reconocido".format(dictionary["ERROR_0"])
                del dictionary["ERROR_0"]
            else:
                e = "ERROR: La cadena no forma parte de la gramatica"
    return e, a

def gramaticaInicio(string = "", dictionary_2 = {"" : 0}):
    global dictionary
    dictionary = dictionary_2
    e, a = "", ""
    entry = string
    e, a = leerGramatica(entry)
    dictionary[e] = a
    return e, a, dictionary

def createTerm():
  global indTerm
  term = "t" + str(indTerm)
  indTerm += 1
  return term

def setTerm(indice):
   global indTerm
   indTerm = indice

def leerPostfijo(variable, string):
    char = ''
    arg1, arg2, arg3 = "", "", ""
    i = 0
    if "+" in string or "-" in string or "*" in string or "/" in string: 
      while i < len(string):
        if string[i] == " ":
          if arg1 == "":
            arg1 = char
          elif arg2 == "":
            arg2 = char
          else:
            arg3 = char
          char = ""
        elif string[i] in numberArray or string[i] in alfabetoL or string[i] in alfabetoU:
          char += string[i]
        else:
          if arg3 != "":
            term = createTerm()
            matriz.append([string[i], arg2, arg3, term])
            arg2 = term
            arg3 = ""
          else:
            term = createTerm() 
            matriz.append([string[i], arg1, arg2, term])
            arg1 = term
            arg2 = ""
        i += 1
      matriz.append(["=", arg1, "", variable])
    else:
      matriz.append(["=", string, "", variable])

def cuadrupla(string, indice):
    global indTerm, matriz
    matriz = []
    indTerm = indice
    diccionario = {"A" : "0", "B" : "0", "C" : "0", "D" : "0", "var1" : "0", "var2" : "0", "a" : "0", "b" : "0"}
    cuadrupla = ""
    e, a, diccionario = gramaticaInicio(string, diccionario)
    if e == "ERROR":
        return "ERROR", 0
    leerPostfijo(e, a)
    cuadrupla = arrayToCuadrupla(matriz)
    return cuadrupla, indTerm

def arrayToCuadrupla(matriz):
    strToWrite = ""
    cadenaFinal = ""
    for arr in matriz:
        strToWrite = " "
        for elem in arr:
            if elem == "+" or elem == "-" or elem == "/" or elem == "*" or elem == "=":
                strToWrite += elem + " "
            else:
                strToWrite += elem
                for lenElem in range(0, (10 - len(elem))):
                    strToWrite += " "
                strToWrite += " "
        strToWrite += "\n"
        cadenaFinal += strToWrite
    return cadenaFinal