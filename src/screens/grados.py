import tkinter
from datetime import datetime
from tkinter import Tk, ttk, messagebox
from tkcalendar import DateEntry
from ttkthemes import ThemedStyle
from sqlalchemy.orm import Session

from ..services.grado import Grado
from ..services.estudiante import Estudiante
from ..services.anioescolar import AnioEscolar
from ..models import Estudiante as Model
from ..models import Grado as ModelGrado
from ..models import AnioEscolar as ModelAnioEscolar
from ..engine import engine
from ..utils.table_to_pdf import PDFGrado
from ..utils.validate import is_number

grado = ["Primer", "Segundo", "Tercero", "Cuarto", "Quinto"]

def screen_grado(tk: tkinter, window: Tk, degree: int, rol: str):
    connect_grado = Grado(engine)
    connect_estudiante = Estudiante(engine)
    connect_anioescolar = AnioEscolar(engine)

    def verificar_rol():
        if rol == "Profesor":
            button_notas = tk.Button(window, text="Notas", command=notas, bg=verdeclaro, fg="black")
            button_notas.pack()
            button_notas.place(x=1050, y=300)

        elif rol == "Secretaria":
            botonew = tk.PhotoImage(file='src/screens/disenos/botones/botonestablas/botonesnuevo.png')
            button_new = tk.Button(window, text="Nuevo", command=nuevo, bg=verdeclaro, fg="black")
            button_new.pack()
            button_new.place(x=750, y=300)

            button_save = tk.Button(window, text="Guardar", command=guardar, bg=verdeclaro, fg="black")
            button_save.pack()
            button_save.place(x=850, y=300)

            button_notas = tk.Button(window, text="Notas", command=notas, bg=verdeclaro, fg="black")
            button_notas.pack()
            button_notas.place(x=950, y=300)

            button_descargar = tk.Button(window, text="Descargar", command=generar_pdf, bg=verdeclaro, fg="black")
            button_descargar.pack()
            button_descargar.place(x=1050, y=300)

            miFrame13 = tk.Frame(window, width="1200", height="350", bd=1)
            miFrame13.pack(side="bottom", anchor="w")

            tk.Button(miFrame13, text="Editar", command=editar, bg=verdeclaro).pack()

        else:
            botonew = tk.PhotoImage(file='src/screens/disenos/botones/botonestablas/botonesnuevo.png')
            button_new = tk.Button(window, text="Nuevo", command=nuevo, bg=verdeclaro, fg="black")
            button_new.pack()
            button_new.place(x=750, y=300)

            button_save = tk.Button(window, text="Guardar", command=guardar, bg=verdeclaro, fg="black")
            button_save.pack()
            button_save.place(x=850, y=300)

            button_delete = tk.Button(window, text="Eliminar", command=eliminar, bg=verdeclaro, fg="black")
            button_delete.pack()
            button_delete.place(x=950, y=300)

            button_notas = tk.Button(window, text="Notas", command=notas, bg=verdeclaro, fg="black")
            button_notas.pack()
            button_notas.place(x=1050, y=300)

            button_descargar = tk.Button(window, text="Descargar", command=generar_pdf, bg=verdeclaro, fg="black")
            button_descargar.pack()
            button_descargar.place(x=1150, y=300)

            miFrame13 = tk.Frame(window, width="1200", height="350", bd=1)
            miFrame13.pack(side="bottom", anchor="w")

            tk.Button(miFrame13, text="Editar", command=editar, bg=verdeclaro).pack()

    def update_table():
        for i in table.get_children():
            table.delete(i)
        
        with Session(engine) as session:
            estudiantes = session.query(Model).all()

            for estudiante in estudiantes:
                grado = session.query(ModelGrado).filter(ModelGrado.id_estudiante == estudiante.id, ModelGrado.inscrito == degree).first()
                anioescolar = session.query(ModelAnioEscolar).filter_by(id_estudiante=estudiante.id).first()
                seccion = "U"

                if grado is not None and anioescolar is not None:
                    table.insert('', 'end', values=(estudiante.id, estudiante.nombres, estudiante.apellidos, estudiante.cedula, estudiante.telefono, estudiante.fecha_nacimiento, grado.inscrito, seccion, anioescolar.inicio, anioescolar.fin))
            table.pack(fill="both", expand=True)

    def show_students():
        global table

        frame = tk.Frame(window, bg="white", width="1400", height="350", bd=10)
        frame.pack(fill="both", expand=True)
        table = ttk.Treeview(frame, columns=('ID', 'Nombres', 'Apellidos', 'Cedula', 'Telefono', 'Fecha de Nacimiento', 'Grado', 'Seccion', 'Inicio', 'Fin'), show='headings')
        table.column('ID', width=100, anchor='center')
        table.column('Nombres', width=100, anchor='center')
        table.column('Apellidos', width=100, anchor='center')
        table.column('Cedula', width=100, anchor='center')
        table.column('Telefono', width=100, anchor='center')
        table.column('Fecha de Nacimiento', width=100, anchor='center')
        table.column('Grado', width=100, anchor='center')
        table.column('Seccion', width=100, anchor='center')
        table.column('Inicio', width=100, anchor='center')
        table.column('Fin', width=100, anchor='center')
        table.heading('ID', text='ID')
        table.heading('Nombres', text='Nombres')
        table.heading('Apellidos', text='Apellidos')
        table.heading('Cedula', text='Cedula')
        table.heading('Telefono', text='Telefono')
        table.heading('Fecha de Nacimiento', text='Fecha de Nacimiento')
        table.heading('Grado', text='Grado')
        table.heading('Seccion', text='Seccion')
        table.heading('Inicio', text='Inicio')
        table.heading('Fin', text='Fin')

        with Session(engine) as session:
            estudiantes = session.query(Model).all()

            for estudiante in estudiantes:
                grado = session.query(ModelGrado).filter(ModelGrado.id_estudiante == estudiante.id, ModelGrado.inscrito == degree).first()
                anioescolar = session.query(ModelAnioEscolar).filter_by(id_estudiante=estudiante.id).first()
                seccion = "U"

                if grado is not None and anioescolar is not None:
                    table.insert('', 'end', values=(estudiante.id, estudiante.nombres, estudiante.apellidos, estudiante.cedula, estudiante.telefono, estudiante.fecha_nacimiento, grado.inscrito, seccion, anioescolar.inicio, anioescolar.fin))
            table.pack(fill="both", expand=True)
   
    def nuevo():
        try:
            nombres = entries[0].get()
            apellidos = entries[1].get()
            cedula = entries[2].get()
            telefono = entries[3].get()
            fecha_nacimiento = datetime.strptime(entries[4].get(), '%m/%d/%y')
            inicio = datetime.strptime(entries[5].get(), '%m/%d/%y')
            fin = datetime.strptime(entries[6].get(), '%m/%d/%y')

            if not all([nombres, apellidos, cedula, telefono, fecha_nacimiento, inicio, fin]):
                messagebox.showerror("Error", "Todos los campos deben estar rellenos")
                return

            connect_estudiante.create(nombres, apellidos, cedula, telefono, fecha_nacimiento, 1)
            with Session(engine) as session:
                estudiante = session.query(Model).filter_by(cedula=cedula).first()
                connect_grado.create(degree, estudiante.id)
                connect_anioescolar.create(inicio, fin, estudiante.id)
            
            update_table()
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar():
        selected_item = table.selection()[0]
        selected_estudiante = table.item(selected_item)['values'][0]

        with Session(engine) as session:
            estudiante = session.query(Model).filter_by(id=selected_estudiante).first()
            anio_escolar = session.query(ModelAnioEscolar).filter_by(id_estudiante=estudiante.id).first()
            grado = session.query(ModelGrado).filter_by(id_estudiante=estudiante.id).first()

            connect_anioescolar.delete(anio_escolar.id)
            connect_grado.delete(grado.id)
            connect_estudiante.delete(estudiante.id)

        update_table()

    def editar():
        global selected_estudiante
        selected_item = table.selection()[0]
        selected_estudiante = table.item(selected_item)['values']
        omitir = selected_estudiante.pop(6)
        omitir = selected_estudiante.pop(6)
        for i, entry in enumerate(entries):
            if i >= 4:
                dt = datetime.strptime(selected_estudiante[i+1], "%Y-%m-%d %H:%M:%S")
                str_dt = dt.strftime('%m/%d/%y')
                entry.delete(0, 'end')
                entry.insert(0, str_dt)
            else:
                entry.delete(0, 'end')
                entry.insert(0, selected_estudiante[i+1])

    def guardar():
        try:
            nombres = entries[0].get()
            apellidos = entries[1].get()
            cedula = entries[2].get()
            telefono = entries[3].get()
            fecha_nacimiento = datetime.strptime(entries[4].get(), '%m/%d/%y')
            inicio = datetime.strptime(entries[5].get(), '%m/%d/%y')
            fin = datetime.strptime(entries[6].get(), '%m/%d/%y')

            if not all([nombres, apellidos, cedula, telefono, fecha_nacimiento, inicio, fin]):
                messagebox.showerror("Error", "Todos los campos deben estar rellenos")
                return

            with Session(engine) as session:
                estudiante = session.query(Model).filter_by(id=selected_estudiante[0]).first()
                anio_escolar = session.query(ModelAnioEscolar).filter_by(id_estudiante=estudiante.id).first()
                grado = session.query(ModelGrado).filter_by(id_estudiante=estudiante.id).first()

                connect_estudiante.update(estudiante.id, nombres, apellidos, cedula, telefono, fecha_nacimiento, 1)
                connect_anioescolar.update(anio_escolar.id, inicio, fin, estudiante.id)
                connect_grado.update(grado.id, degree, estudiante.id)

            update_table()
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar_campos():
        for entry in entries:
            entry.config(validate="none")
            entry.delete(0, 'end')
            if entry in [entries[2], entries[3]]:
                entry.config(validate="key")

    def generar_pdf():
        pdf = PDFGrado('L', 'mm', 'A4')
        pdf.degree = degree
        pdf.add_page()
        pdf.set_font("Helvetica","", 10)

        with Session(engine) as session:
            estudiantes = session.query(Model).all()

            for estudiante in estudiantes:
                grado = session.query(ModelGrado).filter(ModelGrado.id_estudiante == estudiante.id, ModelGrado.inscrito == degree).first()
                anioescolar = session.query(ModelAnioEscolar).filter_by(id_estudiante=estudiante.id).first()
                seccion = "U"

                if grado is not None and anioescolar is not None:
                    datos = [estudiante.id, estudiante.nombres, estudiante.apellidos, estudiante.cedula, estudiante.telefono, estudiante.fecha_nacimiento, grado.inscrito, seccion, anioescolar.inicio, anioescolar.fin]
                    for dato in datos:
                        str_dato = str(dato)
                        if str_dato == str(datos[5]):
                            dt = datetime.strptime(str_dato, "%Y-%m-%d %H:%M:%S")
                            str_dt = dt.strftime('%m/%d/%y')
                            pdf.cell(40, 5, txt = str_dt, border=1, align = 'C')
                        elif str_dato == str(datos[8]) or str_dato == str(datos[9]):
                            dt = datetime.strptime(str_dato, "%Y-%m-%d %H:%M:%S")
                            str_dt = dt.strftime('%m/%d/%y')
                            pdf.cell(26, 5, txt = str_dt, border=1, align = 'C')
                        else:
                            pdf.cell(26, 5, txt = str_dato, border=1, align = 'C')
                    pdf.ln(5)
        pdf.output(f"src/pdfs/tabla_de_grado{degree}.pdf")
    
    def notas():
        from .notas import screen_notas
        window.destroy()
        screen_notas(tkinter, window=tk.Toplevel(), degree=degree, rol=rol)

    window.title(f"{grado[degree - 1]} año")
    window.geometry("1280x680")
    window.resizable(False, False)
    window.iconbitmap('src/screens/disenos/LUMASIS.ico')
    verdeclaro="#b8f2ca"
    verde="#15a35b"
    window.config(bg=verdeclaro)

    icono= tk.PhotoImage(file='src/screens/disenos/urbaneja.png')
    cintillo = tk.Label(window, text="Registros de Estudiantes",bd=5, bg=verdeclaro,relief="groove", fg="black", font=("Calisto Mt", 16), padx=20, pady=10)
    cintillo.config(image=icono, compound=tk.LEFT)  # Establecer la imagen a la izquierda del texto
    cintillo.image = icono 
    cintillo.pack(side="top")

    miFrame = tk.Frame(window, width="1200", height="250", bd=5)
    miFrame.pack()
    
    
    style = ThemedStyle (window) # Cargar el archivo de estilo personalizado
    style.set_theme("adapta")
    
        
    

    vcomd = window.register(is_number)
    labels = ["Nombres", "Apellidos", "Cedula", "Telefono", "Fecha de Nacimiento", "Inicio", "Fin"]
    entries = [tk.Entry(window, validate='key', validatecommand=(vcomd, '%P')) if label in ["Cedula", "Telefono"] else tk.Entry(window) if label not in ["Fecha de Nacimiento", "Inicio", "Fin"] else DateEntry(window) for label in labels]

    for i, (label, entry) in enumerate(zip(labels, entries)):
        if i < 4:  # Para los primeros cuatro labels y entries
            tk.Label(miFrame, text=label).place(x=250, y=30+i*50)
            entry.place(x=355, y=120+i*50+7)
        else:  # Para los siguientes labels y entries
            tk.Label(miFrame, text=label).place(x=550, y=30+(i-4)*50)
            entry.place(x=755, y=120+(i-4)*50+7)

    verificar_rol()
    show_students()