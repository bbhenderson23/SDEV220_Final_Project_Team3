from tkinter import *
import sqlite3

root = Tk()
root.title("Student Information System")
root.geometry("1280x720")

# Create or Connect to a DB. As written, creates a new db stored in memory for each run.

# conn = sqlite3.connect(':memory:')

# Commented out line below will create a db in the directory
conn = sqlite3.connect('SIS.db')

# Create a cursor
cur = conn.cursor()

# Create a table
cur.execute(""" CREATE TABLE IF NOT EXISTS student_records (
    f_name text,
    l_name text, 
    address text,
    city text,
    state text,
    zip_code integer,
    phone_area integer,
    phone_prefix integer,
    phone_line integer,
    email text,
    grade_point real,
    grade_level integer)
    """)

# Commit Changes and close connection
conn.commit()


def create_record_window():
    top = Toplevel()
    # Dropdown Student/Teacher box
    user_type = StringVar()
    user_type.set("Student")
    # Text boxes

    f_name = Entry(top, width=30)
    f_name.grid(row=1, column=1, columnspan=10, sticky=W)
    l_name = Entry(top, width=30)
    l_name.grid(row=1, column=12, columnspan=10, sticky=W)
    address = Entry(top, width=61)
    address.grid(row=2, column=1, columnspan=40, sticky=W)
    city = Entry(top, width=30)
    city.grid(row=3, column=1, columnspan=10, sticky=W)
    state = Entry(top, width=5)
    state.grid(row=3, column=12, columnspan=2, sticky=W)
    zip_code = Entry(top, width=10)
    zip_code.grid(row=3, column=15, columnspan=5, sticky=W)
    phone_area = Entry(top, width=3)
    phone_area.grid(row=4, column=1, sticky=W)
    phone_prefix = Entry(top, width=3)
    phone_prefix.grid(row=4, column=2, sticky=W)
    phone_line = Entry(top, width=7)
    phone_line.grid(row=4, column=3, sticky=W)
    email = Entry(top, width=30)
    email.grid(row=5, column=1, sticky=W, columnspan=10)
    grade_point = Entry(top, width=5)
    grade_point.grid(row=6, column=1, sticky=W)
    grade_level = Entry(top, width=5)
    grade_level.grid(row=6, column=3, sticky=W)

    # Textbox labels
    f_name_label = Label(top, text="First Name")
    f_name_label.grid(row=1, column=0)
    l_name_label = Label(top, text="Last Name")
    l_name_label.grid(row=1, column=11)
    address_label = Label(top, text="Street Address")
    address_label.grid(row=2, column=0)
    city_label = Label(top, text="City")
    city_label.grid(row=3, column=0)
    state_label = Label(top, text="State")
    state_label.grid(row=3, column=11)
    zip_code_label = Label(top, text="Zip code")
    zip_code_label.grid(row=3, column=14)
    phone_label = Label(top, text="Phone Number")
    phone_label.grid(row=4, column=0)
    email_label = Label(top, text="Email")
    email_label.grid(row=5, column=0)
    grade_point_label = Label(top, text="GPA")
    grade_point_label.grid(row=6, column=0)
    grade_level_label = Label(top, text="Grade Level")
    grade_level_label.grid(row=6, column=2)

    def submit():
        # Have to create a connection and cursor inside a function
        # conn = sqlite3.connect(':memory:')  # for testing purposes. Uncomment next line when deployed
        conn = sqlite3.connect('SIS.db')
        cur = conn.cursor()

        # Insert Entry data into db
        with conn:
            cur.execute("INSERT INTO student_records VALUES (:f_name, :l_name, :address, :city, :state, \
                :zip_code, :phone_area, :phone_prefix, :phone_line, :email, :grade_point, :grade_level)",
                        {
                            'f_name': f_name.get(),
                            'l_name': l_name.get(),
                            'address': address.get(),
                            'city': city.get(),
                            'state': state.get(),
                            'zip_code': zip_code.get(),
                            'phone_area': phone_area.get(),
                            'phone_prefix': phone_prefix.get(),
                            'phone_line': phone_line.get(),
                            'email': email.get(),
                            'grade_point': grade_point.get(),
                            'grade_level': grade_level.get()

                        })

        f_name.delete(0, END)
        f_name.delete(0, END)
        l_name.delete(0, END)
        address.delete(0, END)
        city.delete(0, END)
        state.delete(0, END)
        zip_code.delete(0, END)
        phone_area.delete(0, END)
        phone_prefix.delete(0, END)
        phone_line.delete(0, END)
        email.delete(0, END)
        grade_point.delete(0, END)
        grade_level.delete(0, END)

    # Submit Button
    submit_button = Button(top, text="Add Record to Database", command=submit)
    submit_button.grid(row=8, column=14, columnspan=3)


def update_record_window():
    pass


def search_record_window():
#PUT SEARCH BAR HERE

    def search_selection():

        def f_name_search():
            # Commented out line below will create a db in the directory
            conn = sqlite3.connect('SIS.db')

            # Create a cursor
            cur = conn.cursor()

            f_name_search_query = search_bar.get()
            cur.execute("SELECT * FROM student_records WHERE f_name=?", (f_name_search_query,))
            f_name_results = cur.fetchall()
            results_label = Label(top, text=f_name_results).grid(row=25, column=5)
            print(f_name_results)

        def l_name_search():
            # Commented out line below will create a db in the directory
            conn = sqlite3.connect('SIS.db')

            # Create a cursor
            cur = conn.cursor()


            l_name_search_query = search_bar.get()
            print("l_name_search_query = ", l_name_search_query)
            cur.execute("SELECT * FROM student_records WHERE l_name=?", (l_name_search_query,))
            l_name_results = cur.fetchall()
            results_label = Label(top, text=l_name_results).grid(row=25, column=5)
            print(l_name_results)
            cur.execute("SELECT * FROM student_records")
            all_records = cur.fetchall()
            print(all_records)

        def address_search():
            # Commented out line below will create a db in the directory
            conn = sqlite3.connect('SIS.db')

            # Create a cursor
            cur = conn.cursor()


            address_search_query = search_bar.get()
            cur.execute("SELECT * FROM student_records WHERE address=?", (address_search_query,))
            address_results = cur.fetchall()
            results_label = Label(top, text=address_results).grid(row=25, column=5)

        def email_search():
            # Commented out line below will create a db in the directory
            conn = sqlite3.connect('SIS.db')

            # Create a cursor
            cur = conn.cursor()


            email_search_query = search_bar.get()
            cur.execute("SELECT * FROM student_records WHERE email=?", (email_search_query,))
            email_results = cur.fetchall()
            results_label = Label(top, text=email_results).grid(row=25, column=5)

        def grade_level_search():
            # Commented out line below will create a db in the directory
            conn = sqlite3.connect('SIS.db')

            # Create a cursor
            cur = conn.cursor()
            grade_level_search_query = search_bar.get()
            cur.execute("SELECT * FROM student_records WHERE grade_level=?", (grade_level_search_query,))
            grade_level_results = cur.fetchall()
            results_label = Label(top, text=grade_level_results).grid(row=25, column=5)

        drop_menu = drop_menu_selection.get()
        print("Drop Menu: ", drop_menu)
        if drop_menu == "First Name":
            f_name_search()
        elif drop_menu == "Last Name":
            l_name_search()
        elif drop_menu == "Address":
            address_search()
        elif drop_menu == "Email":
            email_search()
        elif drop_menu == "Grade Level":
            grade_level_search()

    top = Toplevel()

    drop_menu_selection = StringVar()
    drop_menu_selection.set("First Name")

    drop_menu = OptionMenu(top, drop_menu_selection, "First Name", "Last Name", "Address", "Email", "Grade Level")\
        .grid(row=1, column=1)
    search_bar = Entry(top, width=30)
    search_bar.grid(row=1, column=2, columnspan=10, sticky=W)
    print("Search bar entry:", search_bar.get)
    search_records = Button(top, text="Search Records", command=search_selection).grid(row=1, column=14)


create_btn = Button(root, text="Create a New Record", command=create_record_window)
create_btn.grid(row=3, column=1, pady=20)
update_btn = Button(root, text="Update a  Record", command=update_record_window)
update_btn.grid(row=3, column=2, pady=20)
search_btn = Button(root, text="Search Records", command=search_record_window)
search_btn.grid(row=3, column=3, pady=20)
quitBtn = Button(root, text="Quit", padx=30, command=root.destroy)
quitBtn.grid(row=21, column=3)

root.mainloop()
