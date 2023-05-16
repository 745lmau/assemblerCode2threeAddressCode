# Importaciones de Tkinter para trabajar con interfaces gráficas
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, constants, Toplevel

# Importación del Analizador Sintáctico
from src.tabla import leerPrograma as get_response

# Declaración de errores constantes
SINTAX_PARSER_RESPONSES = [
    "Sintaxis válida",
    "ERROR - Error de sintaxis",
    "ERROR - No se ingresó un programa",
]

# Declaración de variables globales
global text_output, dictionary
text_output = ""
dictionary = {}

# Función para cargar archivo
def load_file():
    file_path = filedialog.askopenfilename()
    # Abrir el archivo en modo lectura
    with open(file_path, 'r') as file:
        file_content = file.read()
    if file_content == "":
        display_sintax_response(SINTAX_PARSER_RESPONSES[2])
        return
    response = get_response(file_content)
    if response == "":
        display_sintax_response(SINTAX_PARSER_RESPONSES[1])
        return
    display_sintax_response(SINTAX_PARSER_RESPONSES[0])
    three_address_code(response)
    code_entry.delete("1.0", constants.END)
    return

# Función para leer entrada de texto
def read_entry():
    # Limpiamos respuesta del analizador sintáctico
    display_sintax_response("")
    # Lectura de la cadena ingresada en el widget de texto
    code = str(code_entry.get("1.0", constants.END))
    # Eliminamos salto de línea por defecto
    code = code.rstrip("\n")
    if code == "":
        display_sintax_response(SINTAX_PARSER_RESPONSES[2])
        return
    response = get_response(code)
    if response == "":
        display_sintax_response(SINTAX_PARSER_RESPONSES[1])
        return
    display_sintax_response(SINTAX_PARSER_RESPONSES[0])
    three_address_code(response)
    code_entry.delete("1.0", constants.END)
    return

def display_sintax_response(text):
    response_output.config(text=text)

# Función para mostrar el código de tres direcciones
def three_address_code(response):
    tac_string = "Código de tres direcciones:\n---------------------------\n"
    tac_string += response
    tac_string += "---------------------------"
    newWindow = Toplevel(window)
    newWindow.title("Código de tres direcciones")
    newWindow.geometry("200x250")
    cuadrupla_Label = ttk.Label(master = newWindow, text ="")
    cuadrupla_Label.grid(row=0, column=0)
    cuadrupla_Label.config(text=tac_string)

# Declaración de la ventana principal
window = tk.Tk()

# Parámetros de la ventana principal
window.title("Validador y código de tres direcciones")
window.geometry("400x250")
window.eval('tk::PlaceWindow . center')

# Configuración de columnas de la ventana principal
window.columnconfigure(0, weight=10)
window.columnconfigure(1, weight=10)

# Etiqueta de instrucciones
string_label = ttk.Label(text="Ingresa un programa:")
string_label.grid(row=0, column=0)

# Widget para ingresar el programa manualmente
code_entry = tk.Text(window, height=10, width=20)
code_entry.grid(row=1, column=0)

# Etiqueta para cargar archivo
string_label2 = ttk.Label(text="O carga un archivo:")
string_label2.grid(row=0, column=1)

# Botón para validar el programa ingresado manualmente
read_entry_button = ttk.Button(text="Validar", command=read_entry)
read_entry_button.grid(row=2, column=0)

# Botón para cargar archivo
file_button = tk.Button(text="Seleccionar archivo", command=load_file)
file_button.grid(row=1, column=1)

# Etiqueta para la respuesta del analizador sintáctico
string_label3 = ttk.Label(text="Respuesta analizador sintáctico:")
string_label3.grid(row=2, column=1)

# Respuesta del analizador sintáctico
response_output = ttk.Label()
response_output.grid(row=3, column=1)

# Ejecución de la ventana principal
window.mainloop()