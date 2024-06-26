from tkinter import messagebox
from tkinter import END
from regex_validations import ValidationUtils
from base_de_datos import Database
from decoradores import log_en_archivo
from observador import Sujeto
from cliente import alta_server_log
from cliente import modificar_server_log
from cliente import borrar_server_log
import subprocess
import threading
import sys
from pathlib import Path
import os

class Nadador(Sujeto):
    """**Clase principal contiene diferentes metodos que involucran al Nadador.**"""
    def __init__(self) -> None:
        super().__init__()
    @log_en_archivo('CRUD.log', "{now}: Alta Decorador de: {nombre}, {apellido} con DNI: {dni}, distancia: {distancia} y tiempo de: {tiempo}\n")
    def alta(self, dni, nombre, apellido, estilo, distancia, tiempo, tree):
        """**Metodo de alta de registro.**\n
           Permite ingresar datos como DNI, Nombre y Apellido,
           y el tiempo registrado en pasadas de 50 metros estilo crol en formato MM:SS.\n
           Esta información se almacena en una base de datos SQLite3.\n
           El usuario recibe una notificación de alta exitosa en forma de pop up."""
        db = Database()
        self.objeto_treeview = Treeview()
        dni_str = str(dni)
        if ValidationUtils.validar_dni(dni_str):
            if ValidationUtils.validar_nombre(nombre):
                if ValidationUtils.validar_apellido(apellido):
                    if ValidationUtils.validar_tiempo(tiempo):
                        sql = "SELECT dni FROM alumnos WHERE dni=?"
                        nuevo_dni = (dni,)
                        db.conexion()
                        cursor = db.con.cursor()
                        datos = cursor.execute(sql, nuevo_dni)
                        resultado = datos.fetchall()
                        if  resultado == []:
                            data=(dni, nombre, apellido, estilo, distancia, tiempo)
                            sql="INSERT INTO alumnos(dni, nombre, apellido, estilo, distancia, tiempo) VALUES(?, ?, ?, ?, ?, ?)"
                            cursor.execute(sql, data)
                            db.con.commit()
                            self.notificar('alta', dni, nombre, tiempo)
                            alta_server_log(dni, nombre, tiempo)
                            self.objeto_treeview.actualizar_treeview(tree)
                            messagebox.showinfo("Alta exitosa!", f'El tiempo de {nombre} {apellido} fue dado de alta!')
                            db.con.close
                            return "Alta"
                        else:
                            messagebox.showinfo("DNI duplicado", f'El DNI: {dni} ya se encuentra en la base de datos.\n\nModifique el tiempo o nombre del alumno existente.')
                            return 1
                    else:
                        messagebox.showerror("Error en tiempo'", f'El tiempo no esta expresado correctamente.\nUse el formato MM:SS')
                        return 1
                else:
                    messagebox.showerror("Error en 'Apellido'", f'Ingrese un apellido valido.\nLetras, no numeros. Se aceptan tildes, guiones y apóstrofes')
                    return 1
            else:
                messagebox.showerror("Error en 'Nombre'", f'Ingrese un nombre valido.\nLetras, no numeros. Se aceptan tildes, guiones y apóstrofes')
                return 1
        else:
            messagebox.showerror("Error DNI", "Ingrese un DNI valido.\nEjemplo: 30123456).")
            return 1

    @log_en_archivo('CRUD.log', "{now}: Baja Decorador de: {nombre}, {apellido} con DNI: {dni}, distancia: {distancia} y tiempo de: {tiempo}\n")
    def borrar(self,dni, nombre, apellido, estilo, distancia, tiempo, tree):
        """**Metodo para borrar un registro.**\n
            El usuario puede eliminar registros de la base de datos, habiendo seleccionando una entrada previa.\n
            Para evitar errores humanos, una validación en forma de pop up se presenta al usuario
        """
        db = Database()
        valor = tree.selection()
        item = tree.item(valor)
        mi_id = item['text']
        data_alumno = item['values']
        alumno=data_alumno[1]
        respuesta = messagebox.askokcancel("Borrar", f"Esta seguro que desea borrar al alumno: {alumno}")
        if respuesta == True:
            db.conexion()
            cursor = db.con.cursor()
            data = (mi_id,)
            sql = "DELETE FROM alumnos WHERE id = ?;"
            cursor.execute(sql, data)
            db.con.commit()
            self.notificar('baja', dni, nombre, apellido, estilo, distancia, tiempo)
            borrar_server_log(dni, nombre)
            tree.delete(valor)
            db.con.close()

    @log_en_archivo('CRUD.log', "{now}: Modificacion Decorador de: {nombre}, {apellido} con DNI: {dni}, estilo {estilo}, distancia: {distancia} y tiempo de: {tiempo}\n")
    def modificar(self,dni, nombre, apellido, estilo, distancia, tiempo, tree):
        """**Metodo para modificar un registro**.\n
        Para evitar errores humanos, una validación en forma de pop up se presenta al usuario"""
        self.objeto_treeview = Treeview()
        db = Database()
        if ValidationUtils.validar_nombre(nombre):
            if ValidationUtils.validar_apellido(apellido):
                if ValidationUtils.validar_tiempo(tiempo):
                    valor = tree.selection()
                    item = tree.item(valor)
                    mi_id = item['text']
                    data_alumno = item['values']
                    alumno = data_alumno[1]
                    data = (dni, nombre, apellido, estilo, distancia, tiempo, mi_id)
                    respuesta = messagebox.askokcancel("Modificar", f"Esta seguro que desea modificar al alumno: {alumno}")
                    if respuesta == True:
                        db.conexion()
                        cursor=db.con.cursor()
                        sql="UPDATE alumnos SET dni=?, nombre=?, apellido=?, estilo=?, distancia=?, tiempo=? WHERE id=?;"
                        print(sql)
                        cursor.execute(sql, data)
                        db.con.commit()
                        self.notificar('modificar', dni, nombre, apellido, estilo, distancia, tiempo)
                        modificar_server_log(dni, nombre, tiempo)
                        db.con.close()
                        self.objeto_treeview.actualizar_treeview(tree)
                        return "Modificado"
                else:
                    messagebox.showerror("Error en '50 metros crol'", f'El tiempo no esta expresado correctamente.\nUse el formato MM:SS')
                    return 1
            else:
                messagebox.showerror("Error en 'Apellido'", f'Ingrese un apellido valido.\nLetras, no numeros. Se aceptan tildes, guiones y apóstrofes')
                return 1
        else:
            messagebox.showerror("Error en 'Nombre'", f'Ingrese un nombre valido.\nLetras, no numeros. Se aceptan tildes, guiones y apóstrofes')
            return 1

    def mejor_tiempo(self, mitreview, reset_callback):
        """**Metodo que nos permite encontrar y mostrar el mejor tiempo registrado.**\n
        Si hubiera multiples alumnos con el mismo mejor tiempo, entonces se mostraran todos los que compartan dicha categoría."""
        db = Database()
        records = mitreview.get_children()
        for element in records:
            mitreview.delete(element)
        sql="""SELECT *
                FROM alumnos
                WHERE tiempo = (SELECT MIN(tiempo) FROM alumnos)"""
        #con=conexion()
        db.conexion()
        cursor = db.con.cursor()
        datos = cursor.execute(sql)
        resultado = datos.fetchall()
        db.close()
        for fila in resultado:
            mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))
        reset_callback()

    def buscar_nadador(self,dni, nombre, apellido, estilo, distancia, tiempo, tree):
        self.objeto_treeview = Treeview()
        query = "SELECT * FROM alumnos WHERE 1=1"
        params = []

        # Check if values are not placeholder or default values
        if dni and dni != "Números, sin puntos.":
            query += " AND dni LIKE ?"
            params.append(f"%{dni}%")
        if nombre and nombre != "Letras, sin espacios":
            query += " AND nombre LIKE ?"
            params.append(f"%{nombre}%")
        if apellido and apellido != "Letras, sin espacios":
            query += " AND apellido LIKE ?"
            params.append(f"%{apellido}%")
        if estilo and estilo != "Estilo":
            query += " AND estilo LIKE ?"
            params.append(f"%{estilo}%")
        if distancia and distancia != "Distancia":
            query += " AND distancia LIKE ?"
            params.append(f"%{distancia}%")
        if tiempo and tiempo != "MM:SS":
            query += " AND tiempo LIKE ?"
            params.append(f"%{tiempo}%")

        # Debugging output
        print(f"Query: {query}")
        print(f"Params: {params}")
        print(params)
        # Execute query
        db = Database()
        db.conexion()
        cursor = db.con.cursor()
        print(query)
        print(params)
        cursor.execute(query, params)
        results = cursor.fetchall()
        print(results)
        db.close()
        # Display results (you might want to update a Treeview or other widget)
        #self.update_treeview(results)
        #self.objeto_treeview.actualizar_treeview(self)
        #self.objeto_treeview.actualizar_treeview(self)
        #for fila in results:
        #    self.objeto_treeview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))
        for item in tree.get_children():
            tree.delete(item)
        for row in results:
            tree.insert("", "end", text=row[0], values=row[1:])
        return "buscar"


class Treeview:
    """**Clase que interactua con el Treeview**\n
         Grilla de datos donde se encuentran los nadadores que estan la Base de Datos"""
    def __init__(self) -> None:
        pass
    def actualizar_treeview(self, mitreview):
        """Metodo que actualiza el listado de la grilla"""
        db = Database()
        records = mitreview.get_children()
        for element in records:
            mitreview.delete(element)
        sql = "SELECT * FROM alumnos ORDER BY id ASC"
        db.conexion()
        cursor=db.con.cursor()
        datos=cursor.execute(sql)
        resultado = datos.fetchall()
        db.close()
        for fila in resultado:
            mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6]))


    def seleccion_en_tree(self, event, tree, entry_dni, entry_nombre, entry_apellido,combo_estilos, combo_distancias, entry_tiempo):
        """**Metodo para seleccionar filas en la grilla.**"""
        fila_seleccionada = tree.focus()
        valores = tree.item(fila_seleccionada, 'values')

        entry_dni.configure(state='normal')
        entry_nombre.configure(state='normal')
        entry_apellido.configure(state='normal')
        #entry_estilo.configure(state='normal')
        entry_tiempo.configure(state='normal')
        entry_dni.delete(0, END)
        entry_nombre.delete(0, END)
        entry_apellido.delete(0, END)
        #combo_estilos.set(self)
        #combo_distancias.set(self)
        entry_tiempo.delete(0, END)
        if valores:
            entry_dni.insert(0, valores[0])
            entry_nombre.insert(0, valores[1])
            entry_apellido.insert(0, valores[2])
            combo_estilos.set(valores[3])
            combo_distancias.set(valores[4])
            entry_tiempo.insert(0, valores[5])
            entry_dni.configure(state='disabled')



    def scroll_vertical(tree,*args):
        """**Metodo que controla el scroll vertical de la grilla**"""
        tree.yview(*args)

class Servidor:
    """**Clase que interactua con el Servidor**\n"""
    def __init__(self) -> None:
        global theproc
        theproc = None

        self.raiz = Path(__file__).resolve().parent
        self.ruta_server = os.path.join(self.raiz, 'src', 'servidor.py')

    def check_server_status(self):
        command = 'netstat -ano | findstr :9999'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            messagebox.showinfo("Status Servidor", "El Servidor esta corriendo.")
        else:
            messagebox.showinfo("Server Servidor", "El Servidor NO esta corriendo")
    def try_connection(self):
        global theproc
        if theproc is not None:
            theproc.kill()
        threading.Thread(target=self.lanzar_servidor, args=(True,), daemon=True).start()

    def lanzar_servidor(self, var):
        el_path = self.ruta_server
        print(f"Lanzando servidor con path: {el_path}")
        if var:
            global theproc
            theproc = subprocess.Popen([sys.executable, el_path])
        else:
            print("Servidor no inicializado porque var es False")

    def stop_server(self):
        global theproc
        if theproc is not None:
            print("Apangando Servidor")
            theproc.kill()
            theproc = None
        else:
            print("No se encontro proceso de Servidor")

def cerrar_programa(root, tree):
    """**Funcion para cerrar el programa.**\n
       Cierra la ventana y finaliza la aplicación.\n
       El usuario deberá confirmar en la ventana de pop up emergente, que efectivamente desea cerrar la aplicación."""
    result = messagebox.askokcancel("OK o Cancelar", "Esta seguro que desea cerrar el programa?")
    if result == True:
        root.quit()
