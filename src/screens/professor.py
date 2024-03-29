import tkinter
from tkinter import Tk, ttk, messagebox
from ttkthemes import ThemedStyle
from sqlalchemy.orm import Session

from ..services.profesor import Profesor
from ..services.materias import Materias
from ..models import Profesor as Model
from ..models import Materias as ModelMaterias
from ..engine import engine
from ..utils.validate import is_number

def screen_professor(tk: tkinter, window: Tk, rol: str):
    connect = Profesor(engine)
    connect_materias = Materias(engine)

    def update_table():
        for i in table.get_children():
            table.delete(i)
        
        with Session(engine) as session:
            professores = session.query(Model).all()
            for profesor in professores:
                table.insert('', 'end', values=(profesor.id, profesor.nombres, profesor.apellidos, profesor.cedula, profesor.telefono, profesor.titulo, profesor.id_materia))
        table.pack(fill="both", expand=True)

    def show_professores():
        frame = tk.Frame(window, bg="white", width="1400", height="350", bd=10)
        frame.pack(fill="both", expand=True)
        global table
        table = ttk.Treeview(frame, columns=('ID', 'Nombres', 'Apellidos', 'Cedula', 'Telefono', 'Titulo', 'ID Materia'), show='headings')
        table.column('ID', width=100, anchor='center')
        table.column('Nombres', width=100, anchor='center')
        table.column('Apellidos', width=100, anchor='center')
        table.column('Cedula', width=100, anchor='center')
        table.column('Telefono', width=100, anchor='center')
        table.column('Titulo', width=100, anchor='center')
        table.column('ID Materia', width=100, anchor='center')
        table.heading('ID', text='ID')
        table.heading('Nombres', text='Nombres')
        table.heading('Apellidos', text='Apellidos')
        table.heading('Cedula', text='Cedula')
        table.heading('Telefono', text='Telefono')
        table.heading('Titulo', text='Titulo')
        table.heading('ID Materia', text='ID Materia')
        
        with Session(engine) as session:
            professores = session.query(Model).all()
            for profesor in professores:
                table.insert('', 'end', values=(profesor.id, profesor.nombres, profesor.apellidos, profesor.cedula, profesor.telefono, profesor.titulo, profesor.id_materia))
        table.pack(fill="both", expand=True)

    def nuevo():
        try:
            nombres = entries[0].get()
            apellidos = entries[1].get()
            cedula = entries[2].get()
            telefono = entries[3].get()
            titulo = MateriaAsignada.get()
            grado = Grado.get()

            if not all([nombres, apellidos, cedula, telefono, titulo, grado]):
                messagebox.showerror("Error", "Todos los campos deben estar rellenos")
                return

            with Session(engine) as session:
                materia = session.query(ModelMaterias).filter(ModelMaterias.nombre == titulo, ModelMaterias.id_grado == grado).first()
                if not materia:
                    connect_materias.create(titulo[0].upper(), titulo, None, grado)
                    materia = session.query(ModelMaterias).filter(ModelMaterias.nombre == titulo, ModelMaterias.id_grado == grado).first()
                
            connect.create(nombres, apellidos, cedula, telefono, titulo, materia.id)
            limpiar_campos()
            update_table()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar():
        selected_item = table.selection()[0]
        selected_profesor = table.item(selected_item)['values'][0]

        connect.delete(selected_profesor)
        update_table()

    def editar():
        global selected_profesor 
        selected_item = table.selection()[0]
        selected_profesor = table.item(selected_item)['values']
        for i, entry in enumerate(entries):
            entry.delete(0, 'end')
            entry.insert(0, selected_profesor[i+1])

    def guardar():
        try:
            id, nombres, apellidos, cedula, telefono, titulo, id_materia = selected_profesor
            nombres = entries[0].get()
            apellidos = entries[1].get()
            cedula = entries[2].get()
            telefono = entries[3].get()
            titulo = MateriaAsignada.get()
            grado = Grado.get()

            if not all([nombres, apellidos, cedula, telefono, titulo, grado]):
                messagebox.showerror("Error", "Todos los campos deben estar rellenos")
                return

            with Session(engine) as session:
                materia = session.query(ModelMaterias).filter(ModelMaterias.nombre == titulo, ModelMaterias.id_grado == grado).first()
                if not materia:
                    connect_materias.create(titulo[0].upper(), titulo, None, grado)
                    materia = session.query(ModelMaterias).filter(ModelMaterias.nombre == titulo, ModelMaterias.id_grado == grado).first()
                
            connect.update(id, nombres, apellidos, cedula, telefono, titulo, materia.id)
            limpiar_campos()
            update_table()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar_campos():
        for entry in entries:
            entry.config(validate="none")
            entry.delete(0, 'end')
            if entry in [entries[2], entries[3]]:
                entry.config(validate="key")

    window.title("Profesores")
    window.geometry("1280x680")
    window.resizable(False, False)
    window.iconbitmap('src/screens/disenos/LUMASIS.ico')
    verdeclaro="#b8f2ca"
    verde="#15a35b"
    window.config(bg=verdeclaro)

    icono= tk.PhotoImage(file='src/screens/disenos/urbaneja.png')
    cintillo = tk.Label(window, text="Registros de Profesores",bd=5, bg=verdeclaro,relief="groove", fg="black", font=("Calisto Mt", 16), padx=20, pady=10)
    cintillo.config(image=icono, compound=tk.LEFT)  # Establecer la imagen a la izquierda del texto
    cintillo.image = icono 
    cintillo.pack(side="top")


    miFrame = tk.Frame(window, width="1200", height="250", bd=5)
    miFrame.pack()

    style = ThemedStyle (window) # Cargar el archivo de estilo personalizado
    style.set_theme("adapta")

    vcomd = window.register(is_number)
    labels = ["Nombres", "Apellidos", "Cedula", "Telefono", "Materia Asignada", "Grado"]
    entries = [tk.Entry(window, validate='key', validatecommand=(vcomd, '%P')) if label in ["Cedula", "Telefono"] else tk.Entry(window) for label in labels]

    for i, (label, entry) in enumerate(zip(labels, entries)):
        if i < 4:  # Para los primeros cuatro labels y entries
            tk.Label(miFrame, text=label).place(x=350, y=30+i*50)
            entry.place(x=455, y=125+i*50+7)
        elif i == 4:  # Para el quinto label y entry
            MateriaAsignada = tk.StringVar(miFrame)
            MateriaAsignada.set("Materias")
            opciones = ["Arte y patrimonio", "Castellano", "Ciencias Naturales", "Educacion Fisica", "G.H.C", "Ingles", "Matematicas", "Orientación y convivencia", "G.E.R.P", "Fisica", "Quimica"]
            opcion = tk.OptionMenu(miFrame, MateriaAsignada, *opciones)
            opcion.place(x=650, y=30+(i-4)*50+7)
        else:  # Para el sexto label y entry
            Grado = tk.StringVar(miFrame)
            Grado.set("Grados")
            grados = [str(i) for i in range(1, 6)]
            opcion_grado = tk.OptionMenu(miFrame, Grado, *grados)
            opcion_grado.place(x=650, y=30+(i-4)*50+7)


    button_new = tk.Button(window, text="Nuevo", command=nuevo, bg=verdeclaro, fg="black")
    button_new.pack()
    button_new.place(x=800, y=300)

    button_save = tk.Button(window, text="Guardar", command=guardar, bg=verdeclaro, fg="black")
    button_save.pack()
    button_save.place(x=1000, y=300)

    button_delete = tk.Button(window, text="Eliminar", command=eliminar, bg=verdeclaro, fg="black")
    button_delete.pack()
    button_delete.place(x=900, y=300)

    miFrame13 = tk.Frame(window, width="1200", height="350", bd=1)
    miFrame13.pack(side="bottom", anchor="w")

    tk.Button(miFrame13, text="Editar", bg="white", command=editar).pack()

    

    show_professores()