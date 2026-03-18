Here's the improved `README.md` file, incorporating the new content while maintaining the existing structure and information:

# Swim Tracker 🏊

A desktop application for tracking and managing swimming performance metrics and swimmer records. Built with Python using the Tkinter GUI framework with an SQLite database backend.

---

## 📋 Overview

**Swim Tracker** is a CRUD (Create, Read, Update, Delete) application designed to record and manage swimming times for swimmers across different styles and distances. The app features a local SQLite database, real-time record management through a graphical interface, and server-side logging capabilities.

### Key Features
- ✅ Register new swimmer records with performance metrics
- ✅ Modify existing swimming times and swimmer information
- ✅ Delete records with confirmation prompts
- ✅ Search swimmers by multiple criteria (DNI, name, surname, style, distance, time)
- ✅ View best swimming records
- ✅ Local SQLite database storage
- ✅ Server-side logging of CRUD operations
- ✅ Input validation for all fields
- ✅ User-friendly Tkinter GUI interface

---

## 🏗️ Architecture & Project Structure

The application follows the **Model-View-Controller (MVC) pattern** with the **Observer pattern** for event notification:

swim_tracker/
├── app.py                    # Main application entry point
├── modelo.py                 # Data models and business logic (Model)
├── vista.py                  # GUI components and user interface (View)
├── observador.py             # Observer pattern implementation
├── base_de_datos.py          # Database connection and management
├── regex_validations.py       # Input validation utilities
├── decoradores.py            # Logging decorators
├── cliente.py                # Client-side server communication
├── src/
│   └── servidor.py           # Server process for remote logging
└── alumnos_natacion.db      # SQLite database file

---

## 🐍 Python Concepts & Best Practices

### 1. **Object-Oriented Programming (OOP)**

The application demonstrates core OOP principles:

#### **Classes & Objects**
# modelo.py - Class-based organization
class Nadador(Sujeto):
    """Main class for swimmer operations"""
    def __init__(self) -> None:
        super().__init__()
- **Concept**: Classes encapsulate data and behavior
- **Best Practice**: Use type hints (`-> None`) for clarity and IDE support

#### **Inheritance**
# observador.py - Parent-child class relationship
class Nadador(Sujeto):  # Nadador inherits from Sujeto
    pass

class Observador:
    def update(self, tipo_notificacion, *args):
        raise NotImplementedError()

class AltaRegistro(Observador):  # AltaRegistro inherits from Observador
    def update(self, tipo_notificacion, *args):
        # Implementation
        pass
- **Concept**: Child classes inherit properties and methods from parent classes
- **Best Practice**: Use inheritance to avoid code duplication and create hierarchies

#### **Polymorphism**
# observador.py - Different observers implement the same interface differently
class AltaRegistro(Observador):
    def update(self, tipo_notificacion, *args):
        if tipo_notificacion == 'alta':
            # Handle alta operation
            pass

class ModificacionRegistro(Observador):
    def update(self, tipo_notificacion, *args):
        if tipo_notificacion == 'modificar':
            # Handle modificar operation
            pass
- **Concept**: Different classes implement the same method with different behavior
- **Best Practice**: Define a base interface and let subclasses provide specific implementations

### 2. **Design Patterns**

#### **Observer Pattern** (Behavioral Pattern)
# observador.py - Implements the Observer pattern
class Sujeto:
    """Subject that notifies observers of changes"""
    observadores = []
    
    def agregar(self, obj):
        self.observadores.append(obj)
    
    def notificar(self, tipo_notificacion, *args):
        for observador in self.observadores:
            observador.update(tipo_notificacion, *args)

# Usage in modelo.py
self.notificar('alta', dni, nombre, tiempo)
- **Purpose**: Decouple event creators from event handlers
- **Benefit**: Multiple observers can react to the same event without tight coupling
- **Real-world use**: Event logging, notifications, real-time updates

#### **Decorator Pattern** (Structural Pattern)
# decoradores.py - Function decorator for logging
def log_en_archivo(file_path, loguear_mensaje_template):
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = datetime.datetime.now()
            # Format and write log message
            with open(file_path, "a") as f:
                f.write(loguear_mensaje)
            return func(*args, **kwargs)
        return wrapper
    return decorador

# Applied to methods
@log_en_archivo('CRUD.log', "{now}: Alta Decorador de: {nombre}...")
def alta(self, dni, nombre, apellido, ...):
    # Method implementation
    pass
- **Purpose**: Add behavior to functions without modifying them
- **Benefit**: Separates cross-cutting concerns (logging) from business logic
- **Best Practice**: Use `functools.wraps` to preserve function metadata

#### **MVC Pattern** (Architectural Pattern)
- **Model** (`modelo.py`): Contains business logic (Nadador, Treeview, Servidor)
- **View** (`vista.py`): GUI components (Ventana class with Tkinter widgets)
- **Controller**: Implicit in event handlers that connect View to Model
- **Benefit**: Separates concerns, making code more maintainable and testable

### 3. **Data Validation & Regular Expressions**

# regex_validations.py - Input validation using regex
class ValidationUtils():
    @staticmethod
    def validar_dni(dni):
        """Validates DNI format: 7-8 digits"""
        regex_dni = r'^\d{7,8}$'
        return bool(re.match(regex_dni, dni_str))
    
    @staticmethod
    def validar_tiempo(tiempo):
        """Validates time format: MM:SS"""
        regex_tiempo = r'([0-9]{2}):([0-5][0-9])$'
        return bool(re.match(regex_tiempo, tiempo))
    
    @staticmethod
    def validar_nombre(nombre):
        """Validates names with accents and special characters"""
        regex_nombre = r"^[A-ZÁÉÍÓÚÜÑa-záéíóúüñ]+(([' -][A-ZÁÉÍÓÚÜÑa-záéíóúüñ])?...)*$"
        return bool(re.match(regex_nombre, nombre))
- **Concept**: Regular expressions (regex) for pattern matching
- **Best Practice**: 
  - Use raw strings (`r''`) for regex patterns to avoid escape issues
  - Store regex patterns as constants for reuse
  - Always validate user input before database operations

### 4. **Database Management with SQLite**

# base_de_datos.py - Database abstraction layer
class Database:
    def __init__(self, db_name="alumnos_natacion.db"):
        self.db_name = db_name
        self.con = None
    
    def conexion(self):
        """Establish database connection"""
        try:
            self.con = sqlite3.connect(self.db_name)
        except sqlite3.Error as e:
            print("Error:", e)
    
    def create_table(self):
        """Create table with schema"""
        cursor = self.con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS alumnos
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           dni INTEGER NOT NULL,
                           nombre TEXT NOT NULL,
                           apellido TEXT NOT NULL,
                           estilo TEXT NOT NULL,
                           distancia INTEGER NOT NULL,
                           tiempo TEXT NOT NULL)""")
    
    def close(self):
        """Close database connection"""
        if self.con:
            self.con.close()

**Best Practices Applied:**
- **Connection Management**: Always close connections after use (prefer context managers)
- **Parameterized Queries**: Use `?` placeholders to prevent SQL injection
# Safe: prevents SQL injection
sql = "SELECT * FROM alumnos WHERE dni = ?"
cursor.execute(sql, (dni,))

# Unsafe: vulnerable to SQL injection
sql = f"SELECT * FROM alumnos WHERE dni = {dni}"  # DON'T DO THIS!
- **Error Handling**: Try-except blocks for database errors
- **Schema Validation**: IF NOT EXISTS clause prevents duplicate table errors

### 5. **Functional Programming Concepts**

#### **Lambda Functions**
# vista.py - Lambda for event binding
boton_alta = Button(text="Registrar tiempo", 
                   command=lambda: alta_vista())

self.tree.bind("<<TreeviewSelect>>", 
              lambda event: self.objeto_treeview.seleccion_en_tree(...))
- **Use Case**: Short, anonymous functions for callbacks
- **Best Practice**: Use lambdas only for simple operations; use named functions for complex logic

#### **Variable Arguments (*args, **kwargs)**
# observador.py - Flexible argument passing
def notificar(self, tipo_notificacion, *args):
    """Accept variable number of arguments"""
    for observador in self.observadores:
        observador.update(tipo_notificacion, *args)

# decoradores.py - Dynamic argument unpacking
def wrapper(*args, **kwargs):
    func_args = func.__code__.co_varnames[:func.__code__.co_argcount]
    args_dict = dict(zip(func_args, args))
    args_dict.update(kwargs)
- **Concept**: `*args` for positional arguments, `**kwargs` for keyword arguments
- **Benefit**: Create flexible functions that adapt to different call signatures

### 6. **String Formatting**

# decoradores.py - f-strings and format templates
loguear_mensaje = loguear_mensaje_template.format(
    now=now, **args_dict
)

# modelo.py - f-strings for readability
messagebox.showinfo("Alta exitosa!", 
                   f'El tiempo de {nombre} {apellido} fue dado de alta!')
- **Best Practice**: Use f-strings (Python 3.6+) for clarity and performance

### 7. **Module Organization & Imports**

# modelo.py - Organized imports
from tkinter import messagebox
from tkinter import END
from regex_validations import ValidationUtils
from base_de_datos import Database
from decoradores import log_en_archivo
from observador import Sujeto
from cliente import alta_server_log
import subprocess
import threading
import sys
from pathlib import Path
import os

**Best Practices:**
- Group imports: standard library, third-party, local modules
- Use absolute imports
- Import only what you need
- Use `from pathlib import Path` for modern file path handling

### 8. **Type Hints & Documentation**

# modelo.py - Type hints for clarity
def __init__(self) -> None:
    super().__init__()

# Docstrings for documentation
def alta(self, dni, nombre, apellido, estilo, distancia, tiempo, tree):
    """**Metodo de alta de registro.**
    
    Permite ingresar datos como DNI, Nombre y Apellido,
    y el tiempo registrado en pasadas de 50 metros estilo crol 
    en formato MM:SS.
    
    Esta información se almacena en una base de datos SQLite3.
    """
    pass
- **Benefit**: Enables IDE autocomplete, static type checking, and better documentation

### 9. **Error Handling & User Feedback**

# modelo.py - Cascading validation with user feedback
if ValidationUtils.validar_dni(dni_str):
    if ValidationUtils.validar_nombre(nombre):
        # Process data
        pass
    else:
        messagebox.showerror("Error en 'Nombre'", 
                            'Ingrese un nombre valido.')
        return 1
else:
    messagebox.showerror("Error DNI", 
                        "Ingrese un DNI valido.")
    return 1

**Best Practices:**
- Validate input early and provide specific error messages
- Use dialog boxes for user confirmation (askokcancel)
- Return status codes for operation results

### 10. **Threading for Non-Blocking Operations**

# modelo.py - Threading for server launch
def try_connection(self):
    threading.Thread(target=self.lanzar_servidor, 
                     args=(True,), daemon=True).start()

def lanzar_servidor(self, var):
    global theproc
    theproc = subprocess.Popen([sys.executable, el_path])
- **Purpose**: Launch long-running tasks without freezing the GUI
- **Best Practice**: Use daemon threads for background processes that should exit with the main program

---

## 🚀 Quick Start

### Prerequisites
- Python 3.6+
- Tkinter (usually included with Python)
- SQLite3 (included with Python)

### Installation

1. Clone the repository:
git clone https://github.com/matias-espinosa/swim_tracker.git
cd swim_tracker

2. Create a virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Run the application:
python vista.py

Or create a main entry point if needed:
# main.py
from tkinter import Tk
from vista import Ventana

if __name__ == "__main__":
    root = Tk()
    app = Ventana(root)
    root.mainloop()

---

## 📊 CRUD Operations

### Create (Alta)
Register a new swimmer with their performance metrics:
- DNI validation (7-8 digits)
- Name and surname validation (letters, accents, hyphens allowed)
- Time format validation (MM:SS)
- Duplicate DNI checking

### Read (Consulta)
- View all swimmers and their records
- Search by any field combination
- Filter by style, distance, time

### Update (Modificar)
Modify existing swimmer records with validation and confirmation

### Delete (Baja)
Remove swimmer records with user confirmation prompt

---

## 🗄️ Database Schema

### Table: `alumnos`
CREATE TABLE alumnos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    estilo TEXT NOT NULL,         -- Estilo: Mariposa, Espalda, Pecho, Crol
    distancia INTEGER NOT NULL,   -- Distance in meters
    tiempo TEXT NOT NULL          -- Time in MM:SS format
)

---

## 📝 Configuration & Validation

### Accepted Swimming Styles
- Mariposa (Butterfly)
- Espalda (Backstroke)
- Pecho (Breaststroke)
- Crol (Freestyle/Crawl)

### Supported Distances
- 50m, 100m, 200m, 500m, 1000m, 2000m

### Input Validation Rules
| Field | Format | Example |
|-------|--------|---------|
| DNI | 7-8 digits | 30123456 |
| Name | Letters (with accents/hyphens) | Juan, María-José |
| Surname | Letters (with accents/hyphens) | García, O'Connor |
| Time | MM:SS | 02:15, 01:45 |

---

## 🔧 Logging

The application maintains two types of logs:

### 1. File Logging (`CRUD.log`)
Automated by the `@log_en_archivo` decorator:
2026-03-16 14:25:30.123456: Alta Decorador de: Juan, García con DNI: 30123456, distancia: 100 y tiempo de: 02:15

### 2. Server Logging
Remote logging via UDP socket to localhost:9999:
# cliente.py
def alta_server_log(dni, nombre, tiempo):
    loguear_mensaje = f"Alta con Server prendido: DNI={dni}, Name={nombre}, Time={tiempo}"
    enviar_mensaje_log(loguear_mensaje)

---

## 🌟 Key Python Learnings

This project is excellent for learning:

1. **OOP Principles**: Inheritance, polymorphism, encapsulation
2. **Design Patterns**: Observer, Decorator, MVC
3. **GUI Development**: Tkinter widgets, event binding, layout management
4. **Database Interaction**: SQLite, parameterized queries, connection management
5. **Input Validation**: Regular expressions, error handling
6. **Code Organization**: Module structure, import management
7. **Asynchronous Programming**: Threading, subprocess management
8. **Logging & Debugging**: Decorators, file I/O, socket communication

---

## 📚 Files Reference

| File | Purpose | Key Classes |
|------|---------|------------|
| `modelo.py` | Business logic | `Nadador`, `Treeview`, `Servidor` |
| `vista.py` | GUI interface | `Ventana` |
| `observador.py` | Event notification | `Sujeto`, `Observador`, observers |
| `base_de_datos.py` | Database ops | `Database` |
| `regex_validations.py` | Input validation | `ValidationUtils` |
| `decoradores.py` | Logging decorator | `log_en_archivo` |
| `cliente.py` | Server communication | `enviar_mensaje_log` |

---

## 🔐 Security Considerations

- ✅ **SQL Injection Prevention**: Uses parameterized queries
- ✅ **Input Validation**: Regex patterns validate all user input
- ✅ **Confirmation Prompts**: Delete/modify operations require user confirmation
- ⚠️ **Future Enhancement**: Add data encryption for sensitive information

---

## 🐛 Common Issues & Solutions

### Issue: Database Lock
**Cause**: Connection not properly closed  
**Solution**: Ensure `db.close()` is called in all code paths

### Issue: GUI Freezes
**Cause**: Long-running operations on main thread  
**Solution**: Use `threading.Thread()` for blocking operations

### Issue: Validation Failures
**Cause**: Incorrect input format  
**Solution**: Check placeholder text in input fields; follow exact formats

---

## 📈 Potential Improvements

1. **Use Context Managers**: 
# Better: Automatically closes connection
with Database() as db:
    cursor = db.con.cursor()
    # operations

2. **Add Type Hints**:
def alta(self, dni: int, nombre: str, apellido: str, 
         estilo: str, distancia: int, tiempo: str, 
         tree: ttk.Treeview) -> str:
    pass

3. **Separate Configuration**:
# config.py
ESTILOS = ["Mariposa", "Espalda", "Pecho", "Crol"]
DISTANCIAS = ["50", "100", "200", "500", "1000", "2000"]
DB_NAME = "alumnos_natacion.db"

4. **Unit Testing**:
# test_validations.py
import unittest
from regex_validations import ValidationUtils

class TestValidations(unittest.TestCase):
    def test_valid_dni(self):
        assert ValidationUtils.validar_dni("30123456")
    
    def test_invalid_dni(self):
        assert not ValidationUtils.validar_dni("123")

5. **Logging Module** (instead of print statements):
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Base de Datos conectada.")

---

## 📄 License

This project is cloned from: https://github.com/matias-espinosa/swim_tracker

---

## 🤝 Contributing

Feel free to fork, modify, and learn from this code. Perfect for:
- Python learners
- GUI development practice
- Design pattern study
- Database interaction examples

---

## ✨ Summary

**Swim Tracker** demonstrates professional Python development practices including OOP principles, design patterns, GUI development with Tkinter, database management, input validation, and error handling. It's an excellent reference for learning how to build real-world desktop applications with Python.

Happy coding! 🏊‍♂️

This revised README maintains the original structure while enhancing clarity, coherence, and completeness. It provides a comprehensive overview of the project, its architecture, and best practices, making it easier for users and contributors to understand and engage with the Swim Tracker application.