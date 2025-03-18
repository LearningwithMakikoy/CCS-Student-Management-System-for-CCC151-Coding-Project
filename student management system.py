import tkinter as Tk
from tkinter import Frame, ttk
from tkinter import messagebox
import csv 
import os
import re


#Global functions

def search_data(filename, table, search_entry):
    search_value = search_entry.get().strip().lower()

    for item in table.get_children():
        table.delete(item)  

    try:
        with open(filename, newline='', encoding='utf-8') as n:
            reader = csv.reader(n)
            data = list(reader)

        headers = data[0] 
        for row in data[1:]:  
            if any(search_value in str(cell).lower() for cell in row):  
                table.insert("", "end", values=row)

    except FileNotFoundError:
        messagebox.showerror("Error", f"{filename} not found.")


def sort_table(tree, sort_by, order):
    data = [(tree.set(child, sort_by), child) for child in tree.get_children()]
    
    reverse_order = True if order == "Descending" else False
    data.sort(reverse=reverse_order)

    for index, (_, child) in enumerate(data):
        tree.move(child, "", index)


def delete_program_or_college(file_name, program_code_to_delete):
   
    with open("student.csv", "r", newline='', encoding="utf-8") as student_file:
        reader = csv.DictReader(student_file)
        for row in reader:
            if row["Program Code"] == program_code_to_delete:
                messagebox.showerror("Error", f"Cannot delete {program_code_to_delete} as it is assigned to a student.")
                return  

    with open(file_name, "r", newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data = [row for row in reader if row["Program Code"] != program_code_to_delete]


    with open(file_name, "w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Program Code", "Course", "College"])
        writer.writeheader()
        writer.writerows(data)

    messagebox.showinfo("Success", f"{program_code_to_delete} has been deleted.")

        
#making of Main Frame Student
win = Tk.Tk()
win.geometry("1200x700")


page1=Frame(win)
page2=Frame(win)
page3=Frame(win)


for page in(page1, page2, page3):
    page.grid(row=0,column=0,sticky="nsew")

win.rowconfigure(0,weight=1)
win.columnconfigure(0,weight=1)

win.title("Student Management System")
win.config(bg="lightgrey")

title_label = Tk.Label(page1,text="Student Management System",font=("Cambria Math",14,"bold"),border=2,bg="lightblue",foreground="yellow",relief=Tk.GROOVE,)
title_label.pack(side=Tk.TOP, fill=Tk.X,)

detail_frame = Tk.LabelFrame(page1,text="Enter Student Details",font=("Cambria Math",14,),bg=("blue"),fg=("yellow"),bd=12,relief=Tk.GROOVE,)

detail_frame.place(x=10,y=120,width=420,height=575)

data_frame = Tk.Frame(page1,bd=12,bg="lightblue",relief=Tk.GROOVE)
data_frame.place(x=440,y=120,width=800,height=575)


college_programno = Tk.StringVar()
programno = Tk.StringVar()
college = Tk.StringVar()


#Enter Data For Student

#Variables
idno =Tk.StringVar()
fname=Tk.StringVar()
lname=Tk.StringVar()
level=Tk.StringVar()
ginger=Tk.StringVar()
programno=Tk.StringVar()

search_by=Tk.StringVar()

# Label for Student Details
idno_lbl=Tk.Label(detail_frame,text="ID Number ",font=('Arial',12),bg="lightgrey")
idno_lbl.grid(row=0,column=0,padx=2,pady=2)
idno_ent=Tk.Entry(detail_frame,bd=7,font=("Arial",12),textvariable=idno)
idno_ent.grid(row=0,column=1,padx=2,pady=2)

fname_lbl=Tk.Label(detail_frame,text="First Name ",font=('Arial',12),bg="lightgrey")
fname_lbl.grid(row=1,column=0,padx=2,pady=2)
fname_ent=Tk.Entry(detail_frame,bd=7,font=("Arial",12),textvariable=fname)
fname_ent.grid(row=1,column=1,padx=2,pady=2)

lname_lbl=Tk.Label(detail_frame,text="Last Name ",font=('Arial',12),bg="lightgrey")
lname_lbl.grid(row=2,column=0,padx=2,pady=2)
lname_ent=Tk.Entry(detail_frame,bd=7,font=("Arial",12),textvariable=lname)
lname_ent.grid(row=2,column=1,padx=2,pady=2)

level_lbl=Tk.Label(detail_frame,text="Year Level ",font=('Arial',12),bg="lightgrey")
level_lbl.grid(row=3,column=0,padx=2,pady=2)
level_ent=Tk.Entry(detail_frame,bd=7,font=("Arial",12),textvariable=level)
level_ent.grid(row=3,column=1,padx=2,pady=2)

ginger_lbl=Tk.Label(detail_frame,text="Gender ",font=('Arial',12),bg="lightgrey")
ginger_lbl.grid(row=4,column=0,padx=2,pady=2)
ginger_ent=ttk.Combobox(detail_frame,font=('Arial',12),state="readonly",textvariable=ginger)
ginger_ent['values']=("Male","Female","Others")
ginger_ent.grid(row=4,column=1,padx=2,pady=2)

programno_lbl=Tk.Label(detail_frame,text="Program Code ",font=('Arial',12),bg="lightgrey")
programno_lbl.grid(row=5,column=0,padx=2,pady=2)
programno_ent=ttk.Combobox(detail_frame,font=("Arial",12),state="readonly", textvariable=programno)
programno_ent.grid(row=5,column=1,padx=2,pady=2)

#Student Functions
#CSV Load
def update_program_combobox():
    """Update the program combobox with the latest program codes from program.csv."""
    programs = []
    if os.path.exists("program.csv"):
        with open("program.csv", "r", newline='', encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            programs = [row[0] for row in reader]  # Extract Program Codes
    
    programno_ent['values'] = programs  # Update combobox values
    
    # If the current selection is not valid, reset to 'N/A'
    if programno.get() not in programs:
        programno.set('N/A')

def load_csv():
    try:
        with open("student.csv", newline='', encoding='utf-8') as n:
            reader = csv.DictReader(n)
            
            # Clear table before inserting new data
            student_table.delete(*student_table.get_children())

            for row in reader:
                student_table.insert(
                    "", "end",
                    values=(row["ID Number"], row["First Name"], row["Last Name"], 
                            row["Year Level"], row["Gender"], row["Program Code"])
                )
    except FileNotFoundError:
        print("Error: 'student.csv' not found.")

#Edit
def edit_student():
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No student selected for editing.")
        return

    item = student_table.item(selected_item, "values")
    idno.set(item[0])  
    fname.set(item[1])
    lname.set(item[2])
    level.set(item[3])
    ginger.set(item[4])
    programno.set(item[5])

    save_btn.config(state=Tk.NORMAL)  

#Save Changes
def save_student_edit():
    selected_item = student_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No student selected for saving changes.")
        return

  
    with open("student.csv", "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)


    for i in range(1, len(data)): 
        if data[i][0] == idno.get():  
            data[i] = [idno.get(), fname.get(), lname.get(), level.get(), ginger.get(), programno.get()]
            break

   
    with open("student.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    load_csv()  
    
    messagebox.showinfo("Success", "Student details updated successfully!")

#Check ID Only Accepts YYYY-####
def check_id():
    id_value = idno.get()
    pattern = r"^\d{4}-\d{4}$"  
    if not re.fullmatch(pattern, id_value):
        messagebox.showerror("Error", "Invalid ID! Use format YYYY-####.")
        return False
    return True

#Check Year level Only Accepts #
def check_yearlevel():
    """ Check if the entered Year Level fully matches # """
    yearlevel_value = level.get()
    pattern = r"^\d$" #format = # only
    if not re.fullmatch(pattern, yearlevel_value):
        messagebox.showerror("Error", "Invalid Year Level! Use format #.")
        return False
    return True

#Add 
def add_student():
    if not check_id():
        return 
    
    if not check_yearlevel():
        return 
    
    if not (idno.get() and fname.get() and lname.get() and level.get() and ginger.get() and programno.get()):
        messagebox.showerror("Error", "All fields must be filled!")
        return
    file_exists = os.path.exists("student.csv")

    # Check for duplicate ID
    if file_exists:
        try:
            with open("student.csv", "r", newline='', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["ID Number"] == idno.get():
                        messagebox.showerror("Error", "Duplicate ID Number! Student already exists.")
                        return
        except FileNotFoundError:
            pass

    with open("student.csv","a",newline='',encoding="utf-8")as file:
        writer=csv.writer(file)
        if not file_exists:
               writer.writerow(["ID Number", "First Name", "Last Name", "Year Level", "Gender", "Program Code"])
        writer.writerow([idno.get(), fname.get(), lname.get(), level.get(), ginger.get(), programno.get()])
    messagebox.showinfo("Adding Update","Student added successfully!")

#Clearing of Input Fields for Add function
idno.set("")
fname.set("")
lname.set("")
level.set("")
ginger.set("")
programno.set("")    

#delete Function
def delete_student():
    selected_items = student_table.selection()  
    if not selected_items:
        return 

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected student(s)?")
    if not confirm:
        return

    with open('student.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader) 

    selected_values = [student_table.item(item, "values")[0] for item in selected_items]

    for row in data:
        if row[0] in selected_values:
            row[5] = ""  # Set Program Code to null instead of preventing deletion

    with open('student.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    for item in selected_items:
        student_table.delete(item)
    messagebox.showinfo("Success", "Student deleted successfully!")
#Buttons

btn_frame=Tk.Frame(detail_frame,bg="lightgrey",bd=10,relief=Tk.GROOVE)
btn_frame.place(x=20,y=250,width=340,height=200)

#add
add_btn=Tk.Button(btn_frame,bg="lightgrey",text="Add",bd=7,font=("Arial",12),width=15, command=add_student)
add_btn.grid(row=0,column=0,padx=2,pady=2)

#update 
update_btn=Tk.Button(btn_frame,bg="lightgrey",text="Update",bd=7,font=("Arial",12),width=15, command=load_csv)
update_btn.grid(row=0,column=1,padx=2,pady=2)
update_btn.grid()

#delete
delete_btn=Tk.Button(btn_frame,bg="lightgrey",text="Delete",bd=7,font=("Arial",12),width=15, command=delete_student)
delete_btn.grid(row=1,column=0,padx=2,pady=2)

edit_btn = Tk.Button(btn_frame, text="Edit",bd=7, font=("Arial", 12), width=15, command=edit_student)
edit_btn.grid(row=1, column=1, padx=2, pady=2)

blank_btn = Tk.Button(btn_frame, text="b", font=("Arial", 1), width=1,height=18)
blank_btn.grid(row=2, column=0, padx=2, pady=2)

save_btn = Tk.Button(btn_frame, text="Save Changes",bd=7, font=("Arial", 12), width=15, command=save_student_edit)
save_btn.grid(row=6, column=0, padx=2, pady=2)

#Search
search_frame=Tk.Frame(data_frame,bg="lightgrey",bd=10,relief=Tk.GROOVE)
search_frame.pack(side=Tk.TOP,fill=Tk.X)

search_lbl=Tk.Label(search_frame,text="Search:",font=("Arial",12),bg="lightgrey")
search_lbl.grid(row=0,column=0,padx=12,pady=2)

search_entry_student = Tk.Entry(search_frame, font=("Arial", 12))  # Student search bar
search_entry_student.grid(row=0, column=1, padx=12, pady=2)

search_btn_student = Tk.Button(search_frame, text="Search", font=("Arial", 12), bd=9, width=14, bg="lightgrey",
                               command=lambda: search_data("student.csv", student_table, search_entry_student))
search_btn_student.grid(row=0, column=2, padx=12, pady=2)

reset_btn_student = Tk.Button(search_frame, text="Reset", font=("Arial", 12), bd=9, width=14, bg="lightgrey",
                              command=lambda: [search_entry_student.delete(0, Tk.END), load_csv()])
reset_btn_student.grid(row=0, column=3, padx=12, pady=2)                              

# Sort
sort_lbl = Tk.Label(search_frame, text="Sort by:", font=("Arial", 12), bg="lightgrey")
sort_lbl.grid(row=1,column=0,padx=12,pady=2)

sort_opts = ttk.Combobox(search_frame, font=("Arial", 12), state="readonly")
sort_opts["values"] = ("ID Number", "First Name", "Last Name", "Year Level", "Gender", "Program Code")
sort_opts.grid(row=1,column=1,padx=12,pady=2)

order_opts = ttk.Combobox(search_frame, font=("Arial", 12), state="readonly")
order_opts["values"] = ("Ascending", "Descending")
order_opts.grid(row=1,column=2,padx=12,pady=2)

sort_button = Tk.Button(search_frame, text="Sort", font=("Arial", 12),bd=9,width=14,bg="lightgrey",command=lambda: sort_table(student_table, sort_opts.get(), order_opts.get()))
sort_button.grid(row=1,column=3,padx=12,pady=2)


#Database Frame

main_frame = Tk.Frame(data_frame,bg="lightgrey",bd=11,relief=Tk.GROOVE)
main_frame.pack(fill=Tk.BOTH,expand=True)

y_scroll=Tk.Scrollbar(main_frame,orient=Tk.VERTICAL)
x_scroll=Tk.Scrollbar(main_frame,orient=Tk.HORIZONTAL)

student_table=ttk.Treeview(main_frame,columns=("ID Number","First Name","Last Name","Year Level","Gender","Program Code"),yscrollcommand=y_scroll.set,xscrollcommand=x_scroll.set)

y_scroll.config(command=student_table.yview)
x_scroll.config(command=student_table.xview)

y_scroll.pack(side=Tk.RIGHT,fill=Tk.Y)
x_scroll.pack(side=Tk.BOTTOM,fill=Tk.X)

student_table.heading("ID Number",text="ID Number")
student_table.heading("First Name",text="First Name")
student_table.heading("Last Name",text="Last Name")
student_table.heading("Year Level",text="Year Level")
student_table.heading("Gender",text="Gender")
student_table.heading("Program Code",text="Program Code")

student_table['show']='headings'

student_table.column("ID Number",width=100)
student_table.column("First Name",width=100)
student_table.column("Last Name",width=100)
student_table.column("Year Level",width=100)
student_table.column("Gender",width=100)
student_table.column("Program Code",width=100)

student_table.pack(fill=Tk.BOTH,expand=True)

#Program Frame
Tk.Label(page2,text="",font=("Arial", 12))  
title2_label = Tk.Label(
    page2,
    text="Student Management System",
    font=("Cambria Math",14,"bold"),
    border=2,
    bg="lightblue",
    foreground="yellow",
    relief=Tk.GROOVE,
)
title2_label.pack(side=Tk.TOP, fill=Tk.X,)

detail_frame = Tk.LabelFrame(page2,text="Enter Program Details",font=("Cambria Math",14,),bg=("blue"),fg=("yellow"),bd=12,relief=Tk.GROOVE,)

detail_frame.place(x=10,y=120,width=420,height=575)

data_frame = Tk.Frame(page2,bd=12,bg="lightblue",relief=Tk.GROOVE)
data_frame.place(x=440,y=120,width=750,height=575)

#Enter Data For Program

#Variables

college_programno=Tk.StringVar()
course=Tk.StringVar()
college=Tk.StringVar()
search_by=Tk.StringVar()

# Label for Program Details
college_programno_lbl=Tk.Label(detail_frame,text="Program Code ",font=('Arial',12),bg="lightgrey")
college_programno_lbl.grid(row=0,column=0,padx=2,pady=2)
college_programno_ent=Tk.Entry(detail_frame,bd=7,font=("Arial",12),textvariable=college_programno)
college_programno_ent.grid(row=0,column=1,padx=2,pady=2)

course_lbl=Tk.Label(detail_frame,text="College Course ",font=('Arial',12),bg="lightgrey")
course_lbl.grid(row=1,column=0,padx=2,pady=2)
course_ent=Tk.Entry(detail_frame,bd=7,font=("Arial",12),textvariable=course)
course_ent.grid(row=1,column=1,padx=2,pady=2)

college_lbl=Tk.Label(detail_frame,text="College Code",font=('Arial',12),bg="lightgrey")
college_lbl.grid(row=2,column=0,padx=2,pady=2)
college_ent=ttk.Combobox(detail_frame,font=("Arial",12),state="readonly",textvariable=college)
college_ent['values']=("CCS","CASS","COET","CSM","CED","CEBA","CHS")
college_ent.grid(row=2,column=1,padx=2,pady=2)

#Functions for Program
#CSV Load for Program
def load_program_csv():
    try:
        with open("program.csv", newline='', encoding='utf-8') as n:
            reader = csv.DictReader(n)
            
            # Clear table before inserting new data
            program_table.delete(*program_table.get_children())

            for row in reader:
                program_table.insert("", "end",
                    values=(row["Program Code"], row["Course"], row["College Code"])
                )
    except FileNotFoundError:
        print("Error: 'program.csv' not found.")

def is_valid_program_no(program_no):
    """Check if the program code contains only capital letters."""
    return bool(re.fullmatch(r'[A-Z]+', program_no)) 
#Add  
def add_program():
    program_no = college_programno.get()
    if not is_valid_program_no(program_no):
        messagebox.showerror("Error", "Invalid Program Code! Only capital letters are allowed.")
        return 
    
    if not (college_programno.get() and course.get() and college.get()):
        messagebox.showerror("Error", "All fields must be filled!")
        return
    
    file_exists = os.path.exists("program.csv")
    
    # Check for duplicate Program Code
    if file_exists:
        try:
            with open("program.csv", "r", newline='', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Program Code"] == college_programno.get():
                        messagebox.showerror("Error", "Duplicate Program Code! Program already exists.")
                        return
        except FileNotFoundError:
            pass

    with open("program.csv", "a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Program Code", "Course", "College Code"])
        writer.writerow([college_programno.get(), course.get(), college.get()])
    
    messagebox.showinfo("Adding Update", "Program Data added successfully!")

    update_program_combobox()  # Ensure student combobox updates

    
#Clearing of Input Fields
college_programno.set("")
course.set("")
college.set("") 

#delete Function
def delete_program():
    selected_items = program_table.selection()
    if not selected_items:
        return 

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected program(s)?")
    if not confirm:
        return    

    with open('student.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)

    selected_values = [program_table.item(item, "values")[0] for item in selected_items]

    for row in data:
        if row[5] in selected_values:
            row[5] = ""  # Set Program Code to null instead of preventing deletion

    with open('student.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    with open('program.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
    
    updated_data = [row for row in data if row[0] not in selected_values]
    
    with open('program.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_data)

    for item in selected_items:
        program_table.delete(item)

    messagebox.showinfo("Success", "Program deleted successfully!")

    update_program_combobox()  # Ensure combobox gets updated

def edit_program():
    selected_item = program_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No program selected for editing.")
        return

    item = program_table.item(selected_item, "values")
    
    college_programno.set(item[0])
    course.set(item[1])
    college.set(item[2])

    save_btn.config(state=Tk.NORMAL)

def save_program_edit():
    selected_item = program_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No program selected for saving changes.")
        return

    with open("program.csv", "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)

    for i in range(1, len(data)):
        if data[i][0] == college_programno.get():
            data[i] = [college_programno.get(), course.get(), college.get()]
            break

    with open("program.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    load_program_csv()
    messagebox.showinfo("Success", "Program details updated successfully!")


#Buttons

btn_frame=Tk.Frame(detail_frame,bg="lightgrey",bd=10,relief=Tk.GROOVE)
btn_frame.place(x=20,y=250,width=340,height=200)

#Add
add_btn=Tk.Button(btn_frame,bg="lightgrey",text="Add",bd=7,font=("Arial",12),width=15, command=add_program)
add_btn.grid(row=0,column=0,padx=2,pady=2)

#Update
update_btn=Tk.Button(btn_frame,bg="lightgrey",text="Update",bd=7,font=("Arial",12),width=15, command=load_program_csv)
update_btn.grid(row=0,column=1,padx=2,pady=2)
update_btn.grid()

#Delete
delete_btn=Tk.Button(btn_frame,bg="lightgrey",text="Delete",bd=7,font=("Arial",12),width=15, command=delete_program)
delete_btn.grid(row=1,column=0,padx=2,pady=2)

#Edit
edit_btn = Tk.Button(btn_frame, text="Edit",bd=7, font=("Arial", 12), width=15, command=edit_program)
edit_btn.grid(row=1, column=1, padx=2, pady=2)

blank_btn = Tk.Button(btn_frame, text="b", font=("Arial", 1), width=1,height=18)
blank_btn.grid(row=2, column=0, padx=2, pady=2)

#Save
save_btn = Tk.Button(btn_frame, text="Save Changes",bd=7, font=("Arial", 12), width=15, command=save_program_edit)
save_btn.grid(row=6, column=0, padx=2, pady=2)


#Search
search_frame=Tk.Frame(data_frame,bg="lightgrey",bd=10,relief=Tk.GROOVE)
search_frame.pack(side=Tk.TOP,fill=Tk.X)

search_lbl=Tk.Label(search_frame,text="Search:",font=("Arial",12),bg="lightgrey")
search_lbl.grid(row=0,column=0,padx=12,pady=2)

search_entry_program = Tk.Entry(search_frame, font=("Arial", 12))  # Program search bar
search_entry_program.grid(row=0, column=1, padx=12, pady=2)

search_btn_program = Tk.Button(search_frame, text="Search", font=("Arial", 12), bd=9, width=14, bg="lightgrey",
                               command=lambda: search_data("program.csv", program_table, search_entry_program))
search_btn_program.grid(row=0, column=2, padx=12, pady=2)

reset_btn_program = Tk.Button(search_frame, text="Reset", font=("Arial", 12), bd=9, width=14, bg="lightgrey",
                              command=lambda: [search_entry_program.delete(0, Tk.END), load_program_csv()])
reset_btn_program.grid(row=0, column=3, padx=12, pady=2)                              

#Sort
sort_lbl2 = Tk.Label(search_frame, text="Sort by:", font=("Arial", 12), bg="lightgrey")
sort_lbl2.grid(row=1,column=0,padx=12,pady=2)

sort_opts2 = ttk.Combobox(search_frame, font=("Arial", 12), state="readonly")
sort_opts2["values"] = ("Program Code","Course","College Code")
sort_opts2.grid(row=1,column=1,padx=12,pady=2)

order_opts2 = ttk.Combobox(search_frame, font=("Arial", 12), state="readonly")
order_opts2["values"] = ("Ascending", "Descending")
order_opts2.grid(row=1,column=2,padx=12,pady=2)

sort_button2 = Tk.Button(search_frame, text="Sort", font=("Arial", 12),bd=9,width=14,bg="lightgrey", command=lambda: sort_table(program_table, sort_opts2.get(), order_opts2.get()))
sort_button2.grid(row=1,column=3,padx=12,pady=2)

#Database Frame

main_frame = Tk.Frame(data_frame,bg="lightgrey",bd=11,relief=Tk.GROOVE)
main_frame.pack(fill=Tk.BOTH,expand=True)

y_scroll=Tk.Scrollbar(main_frame,orient=Tk.VERTICAL)
x_scroll=Tk.Scrollbar(main_frame,orient=Tk.HORIZONTAL)

program_table=ttk.Treeview(main_frame,columns=("Program Code","Course","College Code"),yscrollcommand=y_scroll.set,xscrollcommand=x_scroll.set)

y_scroll.config(command=program_table.yview)
x_scroll.config(command=program_table.xview)

y_scroll.pack(side=Tk.RIGHT,fill=Tk.Y)
x_scroll.pack(side=Tk.BOTTOM,fill=Tk.X)

program_table.heading("Program Code",text="Program Code")
program_table.heading("Course",text="Course")
program_table.heading("College Code",text="College Code")

program_table['show']='headings'

program_table.column("Program Code",width=100)
program_table.column("Course",width=100)
program_table.column("College Code",width=100)

program_table.pack(fill=Tk.BOTH,expand=True)

#College Frame
Tk.Label(page3,text="",font=("Arial", 12)) 
title3_label = Tk.Label(
    page3,
    text="Student Management System",
    font=("Cambria Math",14,"bold"),
    border=2,
    bg="lightblue",
    foreground="yellow",
    relief=Tk.GROOVE,
)
title3_label.pack(side=Tk.TOP, fill=Tk.X,)

detail_frame = Tk.LabelFrame(page3,text="Enter College Details",font=("Cambria Math",14,),bg=("blue"),fg=("yellow"),bd=12,relief=Tk.GROOVE,)

detail_frame.place(x=10,y=120,width=420,height=575)

data_frame = Tk.Frame(page3,bd=12,bg="lightblue",relief=Tk.GROOVE)
data_frame.place(x=440,y=120,width=750,height=575)

#Enter Data For College

#Variables

college_code=Tk.StringVar()
college_name=Tk.StringVar()

search_by=Tk.StringVar()

# Label for College Details
college_code_lbl=Tk.Label(detail_frame,text="College Code ",font=('Arial',12),bg="lightgrey")
college_code_lbl.grid(row=0,column=0,padx=2,pady=2)
college_code_ent=Tk.Entry(detail_frame,bd=7,font=("Arial",12),textvariable=college_code)
college_code_ent.grid(row=0,column=1,padx=2,pady=2)

college_name_lbl=Tk.Label(detail_frame,text="Name of College",font=('Arial',12),bg="lightgrey")
college_name_lbl.grid(row=1,column=0,padx=2,pady=2)
college_name_ent=Tk.Entry(detail_frame,bd=7,font=("Arial",12),textvariable=college_name)
college_name_ent.grid(row=1,column=1,padx=2,pady=2)

#CSV Load
        
def load_college_csv():
    try:
        with open("college.csv", newline='', encoding='utf-8') as n:
            reader = csv.DictReader(n)
            
           
            college_table.delete(*college_table.get_children())

            for row in reader:
                college_table.insert("", "end",
                    values=(row["College Code"], row["College Name"])
                )
    except FileNotFoundError:
        print("Error: 'college.csv' not found.")


#Functions
def is_valid_college_no(college_no):
    """Check if the program code contains only capital letters."""
    return bool(re.fullmatch(r'[A-Z]+', college_no)) 
def add_college():
    college_no = college_code.get()
    if not is_valid_program_no(college_no):
        messagebox.showerror("Error", "Invalid College Code! Only capital letters are allowed.")
        return 
    if not (college_code.get(), college_name.get() ):
        messagebox.showerror("Error", "All fields must be filled!")
        return
    file_exists = os.path.exists("college.csv")
     # Check for duplicate Program Code and Course
    if file_exists:
        try:
            with open("college.csv", "r", newline='', encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["College Code"] == college_code.get():
                        messagebox.showerror("Error", "Duplicate College Code! College Code already exists.")
                        return
                    if row["College Name"] == college_name.get():
                        messagebox.showerror("Error", "Duplicate College Name! College Name already exists.")
                        return
        except FileNotFoundError:
            pass
    with open("college.csv","a",newline='',encoding="utf-8")as file:
        writer=csv.writer(file)
        if not file_exists:
               writer.writerow(["College Code","College Name"])
        writer.writerow([college_code.get(), college_name.get()])
    messagebox.showinfo("Adding Update","College Data added successfully!")
    
#Clearing of Input Fields
college_code.set("")
college_name.set("")

#delete Function
def delete_college():
    selected_items = college_table.selection()  
    if not selected_items:
        return 

    confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected college(s)?")
    if not confirm:
        return    

    with open('program.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)  

    selected_values = [college_table.item(item, "values")[0] for item in selected_items]  

    for row in data:
        if row[2] in selected_values:
            row[2] = ""  # Set College Code to null instead of preventing deletion

    with open('program.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    with open('college.csv', 'r', newline='') as file:
        reader = csv.reader(file)
        data = list(reader)  
    
    updated_data = [row for row in data if row[0] not in selected_values]
    
    with open('college.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_data)

    for item in selected_items:
        college_table.delete(item)

    messagebox.showinfo("Success", "College deleted successfully!")

def edit_college():
    selected_item = college_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No college selected for editing.")
        return

    item = college_table.item(selected_item, "values")
    
    college_code.set(item[0])
    college_name.set(item[1])

    save_btn.config(state=Tk.NORMAL)

def save_college_edit():
    selected_item = college_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No college selected for saving changes.")
        return

    with open("college.csv", "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        data = list(reader)

    for i in range(1, len(data)):
        if data[i][0] == college_code.get():
            data[i] = [college_code.get(), college_name.get()]
            break

    with open("college.csv", "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)

    load_college_csv()

    messagebox.showinfo("Success", "College details updated successfully!")


#Buttons

btn_frame=Tk.Frame(detail_frame,bg="lightgrey",bd=10,relief=Tk.GROOVE)
btn_frame.place(x=20,y=250,width=340,height=200)

#Add
add_btn=Tk.Button(btn_frame,bg="lightgrey",text="Add",bd=7,font=("Arial",12),width=15, command=add_college)
add_btn.grid(row=0,column=0,padx=2,pady=2)

#Update
update_btn=Tk.Button(btn_frame,bg="lightgrey",text="Update",bd=7,font=("Arial",12),width=15, command=load_college_csv)
update_btn.grid(row=0,column=1,padx=2,pady=2)
update_btn.grid()

#Delete
delete_btn=Tk.Button(btn_frame,bg="lightgrey",text="Delete",bd=7,font=("Arial",12),width=15, command=delete_college)
delete_btn.grid(row=1,column=0,padx=2,pady=2)

#Edit
edit_btn = Tk.Button(btn_frame, text="Edit",bd=7, font=("Arial", 12), width=15, command=edit_college)
edit_btn.grid(row=1, column=1, padx=2, pady=2)

blank_btn = Tk.Button(btn_frame, text="b", font=("Arial", 1), width=1,height=18)
blank_btn.grid(row=2, column=0, padx=2, pady=2)

#Save
save_btn = Tk.Button(btn_frame, text="Save Changes",bd=7, font=("Arial", 12), width=15, command=save_college_edit)
save_btn.grid(row=6, column=0, padx=2, pady=2)

#Search
search_frame=Tk.Frame(data_frame,bg="lightgrey",bd=10,relief=Tk.GROOVE)
search_frame.pack(side=Tk.TOP,fill=Tk.X)

search_lbl=Tk.Label(search_frame,text="Search:",font=("Arial",12),bg="lightgrey")
search_lbl.grid(row=0,column=0,padx=12,pady=2)

search_entry_college = Tk.Entry(search_frame, font=("Arial", 12))  # College search bar
search_entry_college.grid(row=0, column=1, padx=12, pady=2)

search_btn_college = Tk.Button(search_frame, text="Search", font=("Arial", 12), bd=9, width=14, bg="lightgrey",
                               command=lambda: search_data("college.csv", college_table, search_entry_college))
search_btn_college.grid(row=0, column=2, padx=12, pady=2)

reset_btn_college = Tk.Button(search_frame, text="Reset", font=("Arial", 12), bd=9, width=14, bg="lightgrey",
                              command=lambda: [search_entry_college.delete(0, Tk.END), load_college_csv()])
reset_btn_college.grid(row=0, column=3, padx=12, pady=2)                              

#Sort
sort_lbl3 = Tk.Label(search_frame, text="Sort by:", font=("Arial", 12), bg="lightgrey")
sort_lbl3.grid(row=1,column=0,padx=12,pady=2)

sort_opts3 = ttk.Combobox(search_frame, font=("Arial", 12), state="readonly")
sort_opts3["values"] = ("College Code","College Name")
sort_opts3.grid(row=1,column=1,padx=12,pady=2)

order_opts3 = ttk.Combobox(search_frame, font=("Arial", 12), state="readonly")
order_opts3["values"] = ("Ascending", "Descending")
order_opts3.grid(row=1,column=2,padx=12,pady=2)

sort_button3 = Tk.Button(search_frame, text="Sort", font=("Arial", 12), command=lambda: sort_table(college_table, sort_opts3.get(), order_opts3.get()))
sort_button3.grid(row=1,column=3,padx=12,pady=2)

#Database Frame

main_frame = Tk.Frame(data_frame,bg="lightgrey",bd=11,relief=Tk.GROOVE)
main_frame.pack(fill=Tk.BOTH,expand=True)

y_scroll=Tk.Scrollbar(main_frame,orient=Tk.VERTICAL)
x_scroll=Tk.Scrollbar(main_frame,orient=Tk.HORIZONTAL)

college_table=ttk.Treeview(main_frame,columns=("College Code","College Name"),yscrollcommand=y_scroll.set,xscrollcommand=x_scroll.set)

y_scroll.config(command=college_table.yview)
x_scroll.config(command=college_table.xview)

y_scroll.pack(side=Tk.RIGHT,fill=Tk.Y)
x_scroll.pack(side=Tk.BOTTOM,fill=Tk.X)

college_table.heading("College Code",text="College Code")
college_table.heading("College Name",text="College Name")

college_table['show']='headings'

college_table.column("College Code",width=100)
college_table.column("College Name",width=100)

college_table.pack(fill=Tk.BOTH,expand=True)

#Navigation Buttons
Tk.Button(page1,text="Student",command=lambda:page1.tkraise(),font=("Arial",12)).place(x=55, y=582, width=100, height=40)
Tk.Button(page1,text="Program",command=lambda:[page2.tkraise(),load_program_csv()],font=("Arial",12)).place(x=160, y=582, width=100, height=40)
Tk.Button(page1,text="College",command=lambda:[page3.tkraise(),load_college_csv()],font=("Arial",12)).place(x=265, y=582, width=100, height=40)
Tk.Button(page2,text="Student",command=lambda:page1.tkraise(),font=("Arial",12)).place(x=55, y=582, width=100, height=40)
Tk.Button(page2,text="Program",command=lambda:[page2.tkraise(),load_program_csv()],font=("Arial",12)).place(x=160, y=582, width=100, height=40)
Tk.Button(page2,text="College",command=lambda:[page3.tkraise(),load_college_csv()],font=("Arial",12)).place(x=265, y=582, width=100, height=40)
Tk.Button(page3,text="Student",command=lambda:page1.tkraise(),font=("Arial",12)).place(x=55, y=582, width=100, height=40)
Tk.Button(page3,text="Program",command=lambda:[page2.tkraise(),load_program_csv()],font=("Arial",12)).place(x=160, y=582, width=100, height=40)
Tk.Button(page3,text="College",command=lambda:[page3.tkraise(),load_college_csv()],font=("Arial",12)).place(x=265, y=582, width=100, height=40)

load_csv()
page1.tkraise()
win.mainloop()

