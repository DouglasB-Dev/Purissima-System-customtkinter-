import babel.numbers
import sqlite3
import os
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from CTkTable import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime

# ------------------------------------- Configuraciones ----------------------------------

ctk.set_default_color_theme('blue')
ctk.set_appearance_mode('black')
img_folder = './src/'

database = './db/db.db'

fuente_titulo = ('Arial', 58)
fuente_input = ('Arial', 21)
fuente_boton = ('Arial', 28)

def estilo_tabla():
  # Crear una configuración para las tablas con estilo de modo oscuro
  style = ttk.Style()
  style.theme_use("default")
  style.configure("Treeview",
                  background="#2b2b2b",
                  foreground="#eff3f5",
                  rowheight=25,
                  fieldbackground="#343638",
                  bordercolor="#343638",
                  borderwidth=0,
                  font=('Arial', 11))
  style.map('Treeview', background=[('selected', '#242424')])
  style.configure("Treeview.Heading",
                  background="#565b5e",
                  foreground="#eff3f5",
                  relief="flat",
                  font=('Arial', 11))
  style.map("Treeview.Heading",
            background=[('active', '#242424')])

  # Crear un scroll con estilo de modo oscuro
  style.configure("Dark.Vertical.TScrollbar", background="#242424", darkcolor="#565b5e", lightcolor="#565b5e", troughcolor="#2b2b2b")

# ------------------------------------- Clases y Funciones ----------------------------------

class Database:
   
  def establecer_conexion(self):
    conexion = sqlite3.connect(database)
    return conexion

  def obtener_materiales(self):
    conexion = db.establecer_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM materia_prima')
    materiales = cursor.fetchall()
    return materiales

  def obtener_productos(self):
    conexion = db.establecer_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM productos')
    productos = cursor.fetchall()
    return productos

  def agregar_materiales(self, id_material, cantidad):
    conexion = db.establecer_conexion()
    cursor = conexion.cursor()
    cursor.execute('UPDATE materia_prima SET cantidad = cantidad + ? WHERE id = ?', (cantidad, id_material))
    if cursor.rowcount > 0:
      conexion.commit()
      CTkMessagebox(title='¡Éxito!', message='¡Se ha agregado una nueva materia prima!', icon='check')
    else:
      CTkMessagebox(title='¡Error!', message='¡No se ha encontrado el material!', icon='cancel')
    conexion.close()
    
  def agregar_productos(self, id_producto, cantidad):
    conexion = db.establecer_conexion()
    cursor = conexion.cursor()
    cursor.execute('UPDATE productos SET cantidad = cantidad + ? WHERE id = ?', (cantidad, id_producto))
    if cursor.rowcount > 0:
      conexion.commit()
      CTkMessagebox(title='¡Éxito!', message='¡Se ha agregado un nuevo producto!', icon='check')
    else:
      CTkMessagebox(title='¡Error!', message='¡No se ha encontrado el producto!', icon='cancel')
    conexion.close()
    
  def restar_material(self, cantidad, id_materiales):
    conexion = db.establecer_conexion()
    cursor = conexion.cursor()
    for id_material in id_materiales:
      cursor.execute('UPDATE materia_prima SET cantidad = cantidad - ? WHERE id = ?', (cantidad, id_material))
      if cursor.rowcount > 0:
        conexion.commit()
    conexion.close()
   
  def autenticar_usuario(self, usuario, clave):
    conexion = db.establecer_conexion()
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario = ? AND clave = ?',(usuario, clave))
    usuario = cursor.fetchall()
    if len(usuario) > 0:
      return usuario[0]
    else:
      return ''
   
  def guardar_producto(self, nombre, cantidad, materiales):
    conexion = db.establecer_conexion()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT nombre FROM productos WHERE nombre = ?', (nombre,))
    resultado = cursor.fetchone()
    
    if resultado:
      conexion.close()
      CTkMessagebox(title='¡Error!', message='¡El producto ya existe!', icon='cancel')
    else:
      cursor.execute('INSERT INTO productos (nombre, cantidad, materiales) VALUES (?,?,?)', (nombre, cantidad, materiales))
      conexion.commit()
      conexion.close()
      CTkMessagebox(title='¡Éxito!', message='¡Se ha añadido un nuevo producto!', icon='check')

  def guardar_material(self, nombre, cantidad):
    conexion = db.establecer_conexion()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT nombre FROM materia_prima WHERE nombre = ?', (nombre,))
    resultado = cursor.fetchone()
    
    if resultado:
      conexion.close()
      CTkMessagebox(title='¡Error!', message='¡El material ya existe!', icon='cancel')
    else:
      cursor.execute('INSERT INTO materia_prima (nombre, cantidad) VALUES (?,?)', (nombre, cantidad))
      conexion.commit()
      conexion.close()
      CTkMessagebox(title='¡Éxito!', message='¡Se ha añadido un nuevo material!', icon='check')

  def editar_material(self, id, nombre):
    conexion = db.establecer_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE materia_prima SET nombre = ? WHERE id = ?", (nombre, id))
    conexion.commit()
    conexion.close()
    CTkMessagebox(title='¡Éxito!', message='¡Se ha modificado el material exitosamente!', icon='check')

  def eliminar_producto(self, id_producto):
    conexion = db.establecer_conexion()
    cursor = conexion.cursor()
    rows_affected = cursor.execute('DELETE FROM productos WHERE id = ?', (id_producto,))

    if rows_affected == 0:
      CTkMessagebox(title='Error', message='No se encontró el producto para eliminar', icon='error')
    else: 
      conexion.commit() 
      CTkMessagebox(title='¡Éxito!', message='¡Se ha eliminado el producto!', icon='check')
    conexion.close()

  def eliminar_material(self, id_material):
    conexion = db.establecer_conexion()
    cursor = conexion.cursor()
    rows_affected = cursor.execute('DELETE FROM materia_prima WHERE id = ?', (id_material,))

    if rows_affected == 0:
      CTkMessagebox(title='Error', message='No se encontró el material para eliminar', icon='error')
    else: 
      conexion.commit() 
      CTkMessagebox(title='¡Éxito!', message='¡Se ha eliminado el material!', icon='check')
    conexion.close()

def limpiar():
  children = app.winfo_children()
  for widget in children:
    if widget is not app and widget is not barra_lateral:
      widget.destroy()

def validar_numeros(input):
  if input.isdigit():
    return True
  elif input == "":
    return True
  else:
    return False

def validar_longitud(input):
  return len(input) <= 3

db = Database()

usuario = []
# ------------------------------------- Botones ----------------------------------
def login():

  def error_login(valor):
    if valor == True:
      error.configure(text='Credenciales Inválidas')
    else:
      error.configure(text='')

  def ingresar(event=None):
    global usuario
    exito = db.autenticar_usuario(input_usuario.get(), input_clave.get())
    if exito == '':
      error_login(True)
    else:
      # usuario = [exito[1], exito[2]]
      usuario.append(exito[1])
      usuario.append(exito[2])
      limpiar()
      inicio()

  # Creación de Widgets
  contenedor_login = ctk.CTkFrame(app, width=400, height=500)
  
  titulo        = ctk.CTkLabel(app, text='Login', font=fuente_titulo, bg_color='#2b2b2b')
  input_usuario = ctk.CTkEntry(app, placeholder_text='Ingresar Usuario...',    font=fuente_input, width=250, height=50)
  input_clave   = ctk.CTkEntry(app, placeholder_text='Ingresar Contraseña...', font=fuente_input, width=250, height=50)
  btn_ingresar  = ctk.CTkButton(app, text='Iniciar sesión', font=fuente_boton, width=250, height=50, command=ingresar)
  error         = ctk.CTkLabel(app, text='', font=('Arial', 16), text_color='red', bg_color='#2b2b2b')
  btn_salir     = ctk.CTkButton(app, text='Salir',          font=fuente_boton, width=200, height=30, command=app.destroy)

  # Posicionamiento
  contenedor_login.place(relx=0.5, rely=0.5, anchor="center")
  titulo.pack           (pady=(100,30))
  input_usuario.pack    (pady=(0,30))
  input_clave.pack      (pady=(0,30))
  btn_ingresar.pack     ()
  error.pack()
  btn_salir.pack        (side='bottom', pady=(0,80))

  input_clave.bind("<Return>", ingresar)

def inicio():
  limpiar()
  global usuario

  barra_lateral.pack(side='left', fill='both')
  barra_lateral.pack_propagate(0)

  bienvenido = ctk.CTkLabel(app, text='Bienvenido a Purissima', font=('Arial', 45), text_color='#5C5C5C')

  # Creación de Widgets
  titulo       = ctk.CTkLabel(barra_lateral,  text=f"""Purissima System
                                       
{usuario[1]}""",    font=fuente_input,   width=180, height=15)
  inicio        = ctk.CTkButton(barra_lateral, text='Inicio',    font=fuente_input, command=limpiar,     width=180, height=15)
  productos     = ctk.CTkButton(barra_lateral, text='Productos', font=fuente_input, command=productos_f, width=180, height=15)
  materia_prima = ctk.CTkButton(barra_lateral, text='Materiales',font=fuente_input, command=materiales,  width=180, height=15)
  reporte       = ctk.CTkButton(barra_lateral, text='Reporte PDF',font=fuente_input, command=reporte_pdf,width=180, height=15)
  salir         = ctk.CTkButton(barra_lateral, text='Salir',     font=fuente_input, command=app.destroy, width=180, height=15)

  # Posicionamiento
  bienvenido.place(relx= 0.63, rely= 0.5, anchor='center')

  titulo.pack       (pady=(10, 100), padx=10)
  inicio.pack       (pady=(0, 10),   padx=10)
  productos.pack    (pady=(0, 10),   padx=10)
  materia_prima.pack(pady=(0, 10),   padx=10)
  reporte.pack      (pady=(0, 10),   padx=10)
  salir.pack        (pady=(0, 10),   padx=10, side='bottom')

def productos_f():
  limpiar()
  
  def agregar():
      
    id_producto = []
    
    def seleccion_material(valor):
      id_producto.clear()
      for fila in data:
        if (valor == fila[1]):
          id_producto.append(fila[0])
    
    def cancelar():
      btn_agregar.configure(text='Agregar', command=agregar)
      list_productos.destroy()
      cantidad.destroy()
      if usuario[0] == 1 or usuario[0] == 0:
        btn_cancelar.destroy()

      # btn_modificar.configure(text='Modificar',state='disabled', command=modificar)
      tabla_productos.selection_remove(tabla_productos.selection())
    
    def guardar(data):
      if cantidad.get() == '':
        CTkMessagebox(title='¡Error!',message='Ingrese la cantidad de producto a añadir', icon='cancel')
      else:
        materiales = db.obtener_materiales()
        faltantes = []
        faltantes_id = []
        
        for fila in data:
          if id_producto[0] == fila[0]:
            requisitos = ([int(x) for x in fila[3].split(",")])

        for i, req in enumerate(requisitos):
          for material in materiales:

            if material[0] == req and material[2] < int(cantidad.get()) :
              faltantes.append(material[1])
              faltantes_id.append(material[0])
        
        if len(faltantes) > 0:
          CTkMessagebox(title='¡Error!',message="""Se requieren los siguientes materiales: 
                        
""" + """, 
""".join(faltantes), icon='cancel')
        else:   

          db.agregar_productos(id_producto[0], cantidad.get())
          db.restar_material(int(cantidad.get()), requisitos)
          
          data = db.obtener_productos()
          
          tabla_productos.delete(*tabla_productos.get_children())
          for fila in data:
            tabla_productos.insert("", 'end', values=fila[1:])
            
          cancelar()
  
    # Creación de Widgets
    list_productos  = ctk.CTkComboBox(app, values=[fila[1] for fila in data], state='readonly', font=fuente_input, width=250, height=15, command=seleccion_material)
    cantidad = ctk.CTkEntry(app, placeholder_text='Cantidad...', validate="key", validatecommand=(app.register(validar_numeros), '%P'), font=fuente_input, width=230, height=15)
    
    if usuario[0] == 1 or usuario[0] == 0:
      btn_cancelar            = ctk.CTkButton(app, text='Cancelar', font=fuente_input, width=230, height=15, command=cancelar)
      btn_cancelar.place        (x= 520, y= 580)
    
    # Configuración
    list_productos.set('Seleccione')
    btn_agregar.configure(text='Guardar', command=lambda: guardar(data))
    
    # Posicionamiento
    list_productos.place  (x= 260, y= 530)
    cantidad.place        (x= 520, y= 530)

    # Widgets modificados
    # if usuario[0] == 0:
    #   btn_modificar.configure(text='Cancelar',state='normal', command=cancelar)

  def busqueda_productos():
    texto_busqueda = input_buscar_producto.get().lower()
    tabla_productos.delete(*tabla_productos.get_children())
    for fila in data:
      if texto_busqueda in fila[1].lower():
        tabla_productos.insert("", 'end', values=fila[1:])

  def nuevo_producto():
    seleccion = []
    requisitos = []
    seleccion_id = []
    requisitos_id = []
    
    def seleccion_material(valor):
      seleccion.clear()
      seleccion_id.clear()
      for fila in materiales:
        if valor == fila[1]:
          if fila[1] not in seleccion:
            seleccion.append(fila[1])
            seleccion_id.append(str(fila[0]))
            
      if len(requisitos) <= 0:
        requisitos.append(seleccion[0])
        requisitos_id.append(str(seleccion_id[0]))
      else:
        if seleccion[0] in requisitos:
          requisitos.remove(seleccion[0])
          requisitos_id.remove(str(seleccion_id[0]))
        else:
          requisitos.append(seleccion[0])
          requisitos_id.append(str(seleccion_id[0]))
        
      requisitos_seleccionados.configure(state='normal')
      requisitos_seleccionados.delete(1.0, 'end')
      for req in requisitos:
        requisitos_seleccionados.insert('end', req + '\n')
      requisitos_seleccionados.configure(state='disabled')

    def guardar():
      if nombre.get() != '' and cantidad.get() != '' and requisitos_seleccionados.get(1.0, 'end-1c') != '':
        db.guardar_producto(nombre.get(), cantidad.get(), str(', '.join(requisitos_id)))
        app_producto.destroy()
          
        data = db.obtener_productos()
        
        tabla_productos.delete(*tabla_productos.get_children())
        for fila in data:
          tabla_productos.insert("", 'end', values=fila[1:])

      else:
        CTkMessagebox(title='¡Error!', message='¡Los campos no pueden estar vacíos!', icon='cancel')
    
    app_producto = ctk.CTkToplevel(app)
    
    # Obtener las dimensiones de la ventana principal
    ancho_ventana_principal = app.winfo_width()
    alto_ventana_principal = app.winfo_height()

		# Calcular la posición para centrar la ventana secundaria
    posicion_x = app.winfo_x() + (ancho_ventana_principal - 167) // 2  # Centrar horizontalmente
    posicion_y = app.winfo_y() + (alto_ventana_principal - 130) // 2  # Centrar verticalmente

		# Establecer la geometría de la ventana secundaria para centrarla
    app_producto.geometry("390x226+{}+{}".format(1000, posicion_y))
    
    app_producto.focus_set()
    app_producto.resizable(0, 0)
    
    materiales = db.obtener_materiales()
    
    # Creación de widgets
    titulo       = ctk.CTkLabel(app_producto, text='Nuevo Producto', font=fuente_input, width=180, height=15)
    nombre       = ctk.CTkEntry(app_producto, placeholder_text='Nombre Producto...', font=('Arial',18), width=180, height=15)
    cantidad     = ctk.CTkEntry(app_producto, placeholder_text='Cantidad...', validate="key", validatecommand=(app.register(validar_numeros), '%P'), font=('Arial',18), width=180, height=15)
    cantidad.insert(0, 0)
    list_materiales  = ctk.CTkComboBox(app_producto, values=[fila[1] for fila in materiales], state='readonly', font=fuente_input, width=370, height=15, command=seleccion_material)
    requisitos_seleccionados =  ctk.CTkTextbox(app_producto, height=60, width=370, state='disabled')
    btn_guardar     = ctk.CTkButton(app_producto, text='Guardar', font=fuente_input, width=370, height=15, command=guardar)
    
    # Posicionamiento de widgets
    titulo.place         (x= 110,y= 8)
    nombre.place         (x= 10, y= 40)
    cantidad.place       (x= 200,y= 40)
    list_materiales.place(x= 10, y= 75)
    requisitos_seleccionados.place  (x= 10, y= 115)
    btn_guardar.place    (x= 10, y= 186)
  
  def eliminar(event, data_f):
    global data
    item_seleccionado = tabla_productos.selection()
    valor_seleccionado = tabla_productos.item(item_seleccionado, "values")

    for fila in data_f:
      if (str(valor_seleccionado[0]) == str(fila[1])):
        id_producto = fila[0]

    msg = CTkMessagebox(title='Aviso', message='¿Desea eliminar este producto?', icon='warning', option_1='No', option_2='Si')

    if msg.get()=='Si':
      db.eliminar_producto(id_producto)
      
      data_nueva = db.obtener_productos()
        
      tabla_productos.delete(*tabla_productos.get_children())
      for fila in data_nueva:
        tabla_productos.insert("", 'end', values=fila[1:])
      
      data = data_nueva

  # def modificar(data_f):
  #   global data
  #   item_seleccionado = tabla_productos.selection()
  #   valor_seleccionado = tabla_productos.item(item_seleccionado, "values")
    
  #   for fila in data_f:
  #     if (str(valor_seleccionado[0]) == str(fila[1])):
  #       producto = fila
        
  #   print(producto)
    
  # def cancelar_modificar():
  #   btn_agregar.configure(text='Agregar', command=agregar)
  #   btn_modificar.configure(state='disabled')
  #   tabla_productos.selection_remove(tabla_productos.selection())
      
  # def habilitar_modificar(event=None):
  #   btn_agregar.configure(text='Cancelar', command=cancelar_modificar)
  #   btn_modificar.configure(state='normal')  
    
  # Creación de Widgets
  input_buscar_producto      = ctk.CTkEntry(app, placeholder_text='Buscar Producto...', font=fuente_input, width=180, height=15)
  btn_agregar                = ctk.CTkButton(app, text='Agregar', font=fuente_input, width=250, height=15, command=agregar)
  contenedor_tabla_productos = ctk.CTkFrame(app, width=510, height=400)
  tabla_productos            = ttk.Treeview(contenedor_tabla_productos, columns=('Material', 'Cantidad'), show="headings")
  scroll                     = ttk.Scrollbar(contenedor_tabla_productos, orient="vertical", style="Dark.Vertical.TScrollbar")

  if usuario[0] == 0:
    btn_nuevo                = ctk.CTkButton(app, text='Nuevo Producto', font=fuente_input, width=180, height=15, command=nuevo_producto)
    btn_nuevo.place            (x= 570, y= 50)

    # btn_modificar            = ctk.CTkButton(app, text='Modificar', font=fuente_input, width=230, height=15, command= lambda: modificar(data), state='disabled')
    # btn_modificar.place        (x= 520, y= 580)

    tabla_productos.bind("<Double-1>", lambda event: eliminar(event, data))
    # tabla_productos.bind("<Button-1>", habilitar_modificar)

  # Configuraciones
  contenedor_tabla_productos.pack_propagate(0)
  tabla_productos.heading('Material', text='Material')
  tabla_productos.heading('Cantidad', text='Cantidad')

  data = db.obtener_productos()

  for fila in data:   # Insertar datos en la tabla
    tabla_productos.insert("", 'end', values=fila[1:])
    
  scroll.config(command=tabla_productos.yview)
  tabla_productos.config(yscrollcommand=scroll.set)
  
  input_buscar_producto.bind("<KeyRelease>", lambda event: busqueda_productos())

  # Posicionamiento
  input_buscar_producto.place      (x= 260, y= 50)
  btn_agregar.place                (x= 260, y= 580)
  contenedor_tabla_productos.place (relx= 0.63, rely= 0.5, anchor='center')
  tabla_productos.pack             (side='left', expand=True, fill='both', padx=(5,0), pady=(5,0))
  scroll.pack                      (side="right",             fill="y",    padx=(0,5), pady=(5,0))

  estilo_tabla()

def materiales():
  limpiar()
  
  def agregar():
    
    id_material = []
    
    def seleccion_material(valor):
      for fila in data:
        if (valor == fila[1]):
          id_material.append(fila[0])
    
    def cancelar():
      btn_agregar.configure(text='Agregar', command=agregar)
      if usuario[0] == 0:
        btn_modificar.configure(text='Modificar', command=lambda: modificar(data), state='disabled')
      list_materiales.destroy()
      cantidad.destroy()
      if usuario[0] == 1:
        btn_cancelar.destroy()

      tabla_materiales.selection_remove(tabla_materiales.selection())
    
    def guardar():
      if cantidad.get() == '':
        CTkMessagebox(title='¡Error!',message='Ingrese la cantidad de material a añadir', icon='cancel')
      else:
        db.agregar_materiales(id_material[0], cantidad.get())
        data = db.obtener_materiales()
        tabla_materiales.delete(*tabla_materiales.get_children())
        for fila in data:
          tabla_materiales.insert("", 'end', values=fila[1:])
        cancelar()
    
    # Creación de Widgets
    list_materiales = ctk.CTkComboBox(app, values=[fila[1] for fila in data], state='readonly', font=fuente_input, width=250, height=15, command=seleccion_material)
    cantidad        = ctk.CTkEntry(app, placeholder_text='Cantidad...', validate="key", validatecommand=(app.register(validar_numeros), '%P'), font=fuente_input, width=230, height=15)
    if usuario[0] == 1:
      btn_cancelar            = ctk.CTkButton(app, text='Cancelar', font=fuente_input, width=230, height=15, command=cancelar)
      btn_cancelar.place        (x= 520, y= 580)
    
    # Configuración
    list_materiales.set('Seleccione')
    btn_agregar.configure(text='Guardar', command=guardar)
    
    # Posicionamiento
    list_materiales.place (x= 260, y= 530)
    cantidad.place        (x= 520, y= 530)
    
    # Widgets modificados
    if usuario[0] == 0:
      btn_modificar.configure(text='Cancelar', command=cancelar, state='normal')

  def busqueda_materiales():
    texto_busqueda = input_buscar_material.get().lower()
    tabla_materiales.delete(*tabla_materiales.get_children())
    for fila in data:
      if texto_busqueda in fila[1].lower():
        tabla_materiales.insert("", 'end', values=fila[1:])

  def nuevo_material():

    def guardar():
      if nombre.get() != '' and cantidad.get() != '':
        db.guardar_material(nombre.get(), cantidad.get())
        app_producto.destroy()
        
        data = db.obtener_materiales()
        
        tabla_materiales.delete(*tabla_materiales.get_children())
        for fila in data:
          tabla_materiales.insert("", 'end', values=fila[1:])
          
      else:
        CTkMessagebox(title='¡Error!', message='¡Los campos no pueden estar vacíos!', icon='cancel')
    
    app_producto = ctk.CTkToplevel(app)
    
    # Obtener las dimensiones de la ventana principal
    ancho_ventana_principal = app.winfo_width()
    alto_ventana_principal = app.winfo_height()

		# Calcular la posición para centrar la ventana secundaria
    posicion_x = app.winfo_x() + (ancho_ventana_principal - 167) // 2  # Centrar horizontalmente
    posicion_y = app.winfo_y() + (alto_ventana_principal - 130) // 2  # Centrar verticalmente

		# Establecer la geometría de la ventana secundaria para centrarla
    app_producto.geometry("390x226+{}+{}".format(1000, posicion_y))
    
    app_producto.focus_set()
    app_producto.resizable(0, 0)
    
    # Creación de widgets
    titulo       = ctk.CTkLabel(app_producto, text='Nuevo Material', font=fuente_input, width=180, height=15)
    nombre       = ctk.CTkEntry(app_producto, placeholder_text='Nombre Material...', font=('Arial',18), width=180, height=15)
    cantidad     = ctk.CTkEntry(app_producto, placeholder_text='Cantidad...', validate="key", validatecommand=(app.register(validar_numeros), '%P'), font=('Arial',18), width=180, height=15)
    cantidad.insert(0, 0)
    btn_guardar     = ctk.CTkButton(app_producto, text='Guardar', font=fuente_input, width=370, height=15, command=guardar)
    
    # Posicionamiento de widgets
    titulo.place         (x= 110,y= 8)
    nombre.place         (x= 10, y= 40)
    cantidad.place       (x= 200,y= 40)
    btn_guardar.place    (x= 10, y= 186)
    
  def eliminar(event, data_f):
    global data
    item_seleccionado = tabla_materiales.selection()
    valor_seleccionado = tabla_materiales.item(item_seleccionado, "values")

    for fila in data_f:
      if (str(valor_seleccionado[0]) == str(fila[1])):
        id_material = fila[0]

    msg = CTkMessagebox(title='Aviso', message='¿Desea eliminar este material?', icon='warning', option_1='No', option_2='Si')

    if msg.get()=='Si':
      db.eliminar_material(id_material)
      
      data_nueva = db.obtener_materiales()
        
      tabla_materiales.delete(*tabla_materiales.get_children())
      for fila in data_nueva:
        tabla_materiales.insert("", 'end', values=fila[1:])
      
      data = data_nueva
    
  def modificar(data_f):

    def cancelar_modificar():
      btn_agregar.configure(text='Agregar', command=agregar)
      btn_modificar.configure(text='Modificar', command= lambda: modificar(data), state='disabled')
      input_material.destroy()
      tabla_materiales.selection_remove(tabla_materiales.selection())
    
    def guardar(id, nombre):
      global data
      if input_material.get() == '':
        CTkMessagebox(title='¡Error!', message='¡El campo no puede estar vacío!', icon='cancel')
      elif input_material.get() == str(nombre):
        CTkMessagebox(title='Aviso!', message='¡No hay ningún cambio a realizar!', icon='warning')
      else:
        db.editar_material(id, input_material.get())
        
        data_nueva = db.obtener_materiales()
        
        tabla_materiales.delete(*tabla_materiales.get_children())
        for fila in data_nueva:
          tabla_materiales.insert("", 'end', values=fila[1:])
          
        data = data_nueva  
        cancelar_modificar()
    
    item_seleccionado = tabla_materiales.selection()
    valor_seleccionado = tabla_materiales.item(item_seleccionado, "values")
    
    for fila in data_f:
      if (str(valor_seleccionado[0]) == str(fila[1])):
        material = fila

    btn_agregar.configure(text='Cancelar', command=cancelar_modificar)
    btn_modificar.configure(text='Guardar', command= lambda: guardar(material[0], material[1]))
    
    input_material = ctk.CTkEntry(app, font=fuente_input, width=250, height=15)
    input_material.insert(0, str(material[1]))
    input_material.place (x= 260, y= 530)
      
  def habilitar_modificar(event=None):
    btn_modificar.configure(state='normal')

  # Creación de Widgets
  input_buscar_material     = ctk.CTkEntry(app, placeholder_text='Materia Prima...', font=fuente_input, width=180, height=15)
  btn_agregar               = ctk.CTkButton(app, text='Agregar', font=fuente_input, width=250, height=15, command=agregar)
  contenedor_tabla_materias = ctk.CTkFrame(app, width=510, height=400)
  tabla_materiales          = ttk.Treeview(contenedor_tabla_materias, columns=('Material', 'Cantidad'), show="headings")
  scroll                    = ttk.Scrollbar(contenedor_tabla_materias, orient="vertical", style="Dark.Vertical.TScrollbar")

  if usuario[0] == 0:
    btn_nuevo                = ctk.CTkButton(app, text='Nuevo Material', font=fuente_input, width=180, height=15, command=nuevo_material)
    btn_nuevo.place            (x= 570, y= 50)
    
    btn_modificar            = ctk.CTkButton(app, text='Modificar', font=fuente_input, width=230, height=15, command=lambda: modificar(data), state='disabled')
    btn_modificar.place        (x= 520, y= 580)

    tabla_materiales.bind("<Double-1>", lambda event: eliminar(event, data))
    tabla_materiales.bind("<Button-1>", habilitar_modificar)

  # Configuraciones
  contenedor_tabla_materias.pack_propagate(0)
  tabla_materiales.heading('Material', text='Material')
  tabla_materiales.heading('Cantidad', text='Cantidad')

  data = db.obtener_materiales()

  for fila in data:   # Insertar datos en la tabla
    tabla_materiales.insert("", 'end', values=fila[1:])
    
  scroll.config(command=tabla_materiales.yview)
  tabla_materiales.config(yscrollcommand=scroll.set)
  
  input_buscar_material.bind("<KeyRelease>", lambda event: busqueda_materiales())

  # Posicionamiento
  input_buscar_material.place      (x= 260, y= 50)
  btn_agregar.place                (x= 260, y= 580)
  contenedor_tabla_materias.place  (relx= 0.63, rely= 0.5, anchor='center')
  tabla_materiales.pack            (side='left', expand=True, fill='both', padx=(5,0), pady=(5,0))
  scroll.pack                      (side="right",             fill="y",    padx=(0,5), pady=(5,0))

  estilo_tabla()

def reporte_pdf():
  datos_productos = db.obtener_productos()
  datos_materiales = db.obtener_materiales()
  data = []
  for producto in datos_productos:
    requisitos_suma = []
    requisitos = producto[3].split(',')
    requisitos_array = [int(requisito) for requisito in requisitos]

    for material in datos_materiales:
      for req in requisitos_array:
        if req == material[0]:
          requisitos_suma.append(material[1])

    data.append((producto[0], producto[1], producto[2], ', '.join(requisitos_suma)))

  def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.drawString(50, 50, "Página %d" % (doc.page))
    fecha_actual = datetime.now().strftime("%d/%m/%Y | %I:%M %p")
    canvas.drawRightString(550, 50, fecha_actual)
    canvas.restoreState()

    canvas.line(50, 40, 550, 40)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(250, 20, "Departamento de Programación")

    canvas.setFillColorRGB(0, 0, 0, alpha=0.3)
    canvas.drawImage("src/logo.png", 50, 300, width=500, height=184, mask='auto')

  # Crear el contenido del PDF
  def create_pdf(file_name, data):
    doc = SimpleDocTemplate(file_name, pagesize=letter)

    # Estilos de párrafo
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
    styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))

    # Configurar el texto y estilos
    content = []
    content.append(Paragraph("Reporte de Productos - Purissima", styles["Title"]))
    content.append(Paragraph("<br/><br/>", styles["BodyText"]))

    # Crear la tabla
    table_data = [['ID', 'Nombre', 'Cantidad', 'Requisitos']]
    for producto in data:
      requisitos = producto[3]
      requisitos_paragraph = Paragraph(requisitos, getSampleStyleSheet()["BodyText"])
      table_data.append([producto[0], producto[1], producto[2], requisitos_paragraph])

    t = Table(table_data, colWidths=[30, 150, 50, 300])

    t.setStyle(TableStyle([
      ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
      ('ALIGN', (2, 1), (-1, -1), 'CENTER'),
      ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
      ('ALIGN', (2, 0), (2, 0), 'CENTER'),
      ('ALIGN', (3, 0), (3, 0), 'CENTER'),
    ]))

    content.append(t)

    # Generar el PDF
    doc.build(content, onFirstPage=add_footer, onLaterPages=add_footer)

  # Llamar a la función para crear el PDF
  create_pdf("./pdf/reporte_productos.pdf", data)
  file_path = os.path.abspath("./pdf/reporte_productos.pdf")
  os.startfile(file_path)

# ------------------------------------- Creación de la ventana ----------------------------------
app = ctk.CTk()

app.title('Purissima - Sistema')
app.geometry('800x620+160+200')
app.resizable(0, 0)

login()
container_width = app.winfo_width()
barra_lateral = ctk.CTkFrame(master=app, width=int(container_width * 0.25), bg_color='black')
scroll = ttk.Scrollbar(orient="vertical", style="Dark.Vertical.TScrollbar")

# inicio()

app.mainloop()