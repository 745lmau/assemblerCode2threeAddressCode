from .gramatica import *
from .cuadrupla import *


def preview(cadena):
    aux = 0
    word = ''
    while cadena[aux] != ' ' and cadena[aux] != ';' and cadena[aux] != ':':
        word += cadena[aux]
        aux += 1
        if aux >= len(cadena):
            break
    return word

def leerPalabra(cadena, indice):
    cadenaAux, indiceAux = cadena, indice
    palabra = ""
    while cadenaAux[indiceAux] != ' ' and indiceAux < (len(cadenaAux)):
        palabra += cadenaAux[indiceAux]
        indiceAux += 1
        if indiceAux >= len(cadenaAux):
            return palabra, indiceAux
    if indiceAux < len(cadenaAux):
        indiceAux = espacio(cadenaAux, indiceAux)
    return palabra, indiceAux

def espacio(cadena, indice):
    cadenaAux, indiceAux = cadena, indice
    while cadenaAux[indiceAux] == ' ':
        indiceAux += 1
    return indiceAux

def comparacionInversa(cadenaP, indice):
    cadena, ind = cadenaP, indice
    op1, ind = leerPalabra(cadena, ind)
    op, ind = leerPalabra(cadena, ind)
    op = inverseCompare(op)
    op2, ind = leerPalabra(cadena, ind)
    return op1 + " " + op + " " + op2, ind

def inverseCompare(op):
    if op == "=" or op == "==":
        return "!="
    elif op == "!=":
        return "="
    elif op == ">":
        return "<="
    elif op == "<":
        return ">="
    elif op == "<=":
        return ">"
    elif op == ">=":
        return "<"
    return "?"    

def comparacion(cadena, indice):
    op1, op, op2 = "", "", ""
    op1, indice = leerPalabra(cadena, indice)
    op, indice = leerPalabra(cadena, indice)
    op2, indice = leerPalabra(cadena, indice)
    return op1 + " " + op + " " + op2, indice

def createTag():
    global indTag
    indTag += 1
    tag = "E" + str(indTag)
    return tag

def crearTabla(table, counter):
    global tagStack, indTag, indTerm
    tabla, operacion = "", ""
    contador, tablaSimbolos = counter, table

    while contador < len(tablaSimbolos):   

        if tablaSimbolos[contador] != "\n":
            operacion += tablaSimbolos[contador]
        else:
            if preview(operacion) == "if":
                etiqueta = createTag()
                tagStack.append(etiqueta)
                palabra, indAux = leerPalabra(operacion, 0)    
                palabra, indAux = comparacionInversa(operacion, indAux)
                
                tabla += "if " + palabra + " goto " + etiqueta + "\n"
                operacion = ""
                contador += 1

                palabra, contador = crearTabla(tablaSimbolos, contador)
                tabla += palabra + tagStack.pop() + ":" + "\n"

            elif preview(operacion) == "while":
                etiqueta = createTag()
                palabra, indAux = leerPalabra(operacion, 0)
                palabra, indAux = comparacion(operacion, indAux)
                
                tabla += etiqueta + ":\n"
                contador += 1
                tab, contador = crearTabla(tablaSimbolos, contador)
                tabla += tab + "if " + palabra + " goto " + etiqueta + "\n"

            elif preview(operacion) == "else":
                palabra, indAux = leerPalabra(operacion, 0) 
                etiqueta = createTag()
                contador += 1

                palabra, contador = crearTabla(tablaSimbolos, contador)
                tabla += "goto " + etiqueta + "\n" + tagStack.pop() +  ":" + "\n" + palabra          
                tagStack.append(etiqueta)

            elif preview(operacion) == "end":
                return tabla, contador
            else:
                cuad, indTerm = cuadrupla(operacion, indTerm)
                setTerm(indTerm)
                tabla += cuad
            operacion = ""
        contador += 1
    return tabla, contador

def leerPrograma(programa = ""):
    tablaSimbolos = (inicioGramatica(programa))
    global tagStack, indTag, indTerm
    indTag = 0
    indTerm = 1
    tagStack = []
    tablaFinal, contarFinal = crearTabla(tablaSimbolos, 0)
    return tablaFinal