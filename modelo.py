from tkinter import messagebox
from tkinter import END
from regex_validations import ValidationUtils
from base_de_datos import Database

class Nadador():
    """**Clase principal contiene diferentes metodos que involucran al Nadador.**"""
    def __init__(self) -> None:
        pass
    def alta(self, dni, nombre, tiempo_50_mts, tree):
        """**Metodo de alta de registro.**\n
           Permite ingresar datos como DNI, Nombre y Apellido, y el tiempo registrado en pasadas de 50 metros estilo crol en formato MM:SS.\n
           Esta información se almacena en una base de datos SQLite3.\n
           El usuario recibe una notificación de alta exitosa en forma de pop up."""
        db = Database()
        self.objeto_treeview = Treeview()
        dni_str = str(dni)
        if ValidationUtils.validate_dni(dni_str):
            if ValidationUtils.validate_fullname(nombre):
                if ValidationUtils.validate_tiempo(tiempo_50_mts):
                    sql = "SELECT dni FROM alumnos WHERE dni=?"
                    nuevo_dni = (dni,)
                    db.conexion()
                    cursor = db.con.cursor()
                    datos = cursor.execute(sql, nuevo_dni)
                    resultado = datos.fetchall()
                    if  resultado == []:
                        data=(dni, nombre, tiempo_50_mts)
                        sql="INSERT INTO alumnos(dni, nombre, tiempo_50_mts) VALUES(?, ?, ?)"
                        cursor.execute(sql, data)
                        db.con.commit()
                        self.objeto_treeview.actualizar_treeview(tree)
                        messagebox.showinfo("Alta exitosa!", f'El tiempo de {nombre} fue dado de alta!')
                        db.con.close
                        return "Alta"
                    else:
                        messagebox.showinfo("DNI duplicado", f'El DNI: {dni} ya se encuentra en la base de datos.\n\nModifique el tiempo o nombre del alumno existente.')
                        return 1
                else:
                    messagebox.showerror("Error en '50 metros crol'", f'El tiempo no esta expresado correctamente.\nUse el formato MM:SS')
                    return 1
            else:
                messagebox.showerror("Error en 'Nombre y Apellido'", f'Ingrese un nombre y apellido validos.\nSolo se admiten letras (con o sin tilde), con el formato Nombre espacio Apellido.\nEjemplo: Juan Pérez')
                return 1
        else:
            messagebox.showerror("Error DNI", "Ingrese un DNI valido.\nEjemplo: 30123456).")
            return 1

    def borrar(self, tree):
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
            tree.delete(valor)
            db.con.close()


    def modificar(self,dni, nombre, tiempo_50_mts, tree):
        """**Metodo para modificar un registro**.\n
        Para evitar errores humanos, una validación en forma de pop up se presenta al usuario"""
        self.objeto_treeview = Treeview()
        db = Database()
        if ValidationUtils.validate_tiempo(tiempo_50_mts):
            valor = tree.selection()
            item = tree.item(valor)
            mi_id = item['text']
            data_alumno = item['values']
            alumno = data_alumno[1]
            data = (dni, nombre, tiempo_50_mts,mi_id)
            respuesta = messagebox.askokcancel("Modificar", f"Esta seguro que desea modificar al alumno: {alumno}")
            if respuesta == True:
                db.conexion()
                cursor=db.con.cursor()
                sql="UPDATE alumnos SET dni=?, nombre=?, tiempo_50_mts=? WHERE id=?;"
                cursor.execute(sql, data)
                db.con.commit()
                db.con.close()
                self.objeto_treeview.actualizar_treeview(tree)
                return "Modificado"
        else:
            messagebox.showerror("Error en '50 metros crol'", f'El tiempo no esta expresado correctamente.\nUse el formato MM:SS')
            return 1

    def mejor_tiempo(self, mitreview):
        """**Metodo que nos permite encontrar y mostrar el mejor tiempo registrado.**\n
        Si hubiera multiples alumnos con el mismo mejor tiempo, entonces se mostraran todos los que compartan dicha categoría."""
        db = Database()
        records = mitreview.get_children()
        for element in records:
            mitreview.delete(element)
        sql="""SELECT *
                FROM alumnos
                WHERE tiempo_50_mts = (SELECT MIN(tiempo_50_mts) FROM alumnos)"""
        #con=conexion()
        db.conexion()
        cursor = db.con.cursor()
        datos = cursor.execute(sql)
        resultado = datos.fetchall()
        db.close()
        for fila in resultado:
            mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))

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
            mitreview.insert("", 0, text=fila[0], values=(fila[1], fila[2], fila[3]))


    def seleccion_en_tree(self, event, tree, entry_dni, entry_nombre, entry_tiempo):
        """**Metodo para seleccionar filas en la grilla.**"""
        fila_seleccionada = tree.focus()  # Obtener el item de Tkinter 'fila'
        valores = tree.item(fila_seleccionada, 'values')  # Obtener los valores de la fila seleccionada
        # Llenar los widgets vacios con la fila seleccionada
        entry_dni.configure(state='normal')
        entry_nombre.configure(state='normal')
        entry_tiempo.configure(state='normal')
        entry_dni.delete(0, END)
        entry_nombre.delete(0, END)
        entry_tiempo.delete(0, END)
        if valores:
            entry_dni.insert(0, valores[0])
            entry_nombre.insert(0, valores[1])
            entry_tiempo.insert(0, valores[2])
            entry_dni.configure(state='disabled')


    def scroll_vertical(tree,*args):
        """**Metodo que controla el scroll vertical de la grilla**"""
        tree.yview(*args)

def cerrar_programa(root, tree):
    """**Funcion para cerrar el programa.**\n
       Cierra la ventana y finaliza la aplicación.\n
       El usuario deberá confirmar en la ventana de pop up emergente, que efectivamente desea cerrar la aplicación."""
    result = messagebox.askokcancel("OK o Cancelar", "Esta seguro que desea cerrar el programa?")
    if result == True:
        root.quit()
