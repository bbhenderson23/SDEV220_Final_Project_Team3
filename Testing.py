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
    # At bottom of this section, creates the update window
    top = Tk()
    top.title("Update Records")



    # Create a frame
    master_frame = Frame(top)
    master_frame.grid(row=8, columnspan=20, sticky=NW)
    scrollbar = Scrollbar(master_frame, orient=VERTICAL)
    scrollbar.grid(row=0, column=50)


    # Create the search bar and buttons
    drop_menu_selection = StringVar()
    drop_menu_selection.set("Last Name")
    search_by_label = Label(top, text="Search by: ")
    search_by_label.grid(row=1, column=0, sticky=W)
    drop_menu = OptionMenu(top, drop_menu_selection, "First Name", "Last Name", "Address", "Email", "Grade Level")
    drop_menu.config(width=10)
    drop_menu.grid(row=1, column=1, sticky=W)
    search_bar = Entry(top, width=60)
    search_bar.grid(row=1, column=2, columnspan=10, sticky=W)
    update_frame = Frame(master_frame)
    update_frame.grid(row=8, columnspan=20, sticky=NW)

    def clear_update_frame(master_frame):
        # Clears the old results from the frame
        for widgets in master_frame.winfo_children():
            widgets.destroy()
        master_frame = Frame(top)
        master_frame.grid(row=8, columnspan=20, sticky=NW)




    def update_records():
        pass

    def populate_records(results):

        clear_update_frame(master_frame)
        oid_records = []
        f_name_records = []
        l_name_records = []
        address_records = []
        city_records = []
        state_records = []
        zip_code_records = []
        phone_records = []
        email_records = []
        gpa_records = []
        grade_level_records = []

        i = 0
        for result in range(len(results)):
            oid_records.append(str(results[i][12]))
            f_name_records.append(str(results[i][0]))
            l_name_records.append(str(results[i][1]))
            address_records.append(str(results[i][2]))
            city_records.append(str(results[i][3]))
            state_records.append(str(results[i][4]))
            zip_code_records.append(str(results[i][5]))
            phone_records.append(str(results[i][6]) + str(results[i][7]) + str(results[i][8]))
            email_records.append(str(results[i][9]))
            gpa_records.append(str(results[i][10]))
            grade_level_records.append(str(results[i][11]))
            i += 1

        for i in range(len(results)):
            update_frame = Frame(master_frame)
            update_frame.grid(row=i+8, columnspan=20, sticky=NW)



            f_name = Entry(update_frame, width=30)
            f_name.grid(row=1, column=1, columnspan=10, sticky=W)
            l_name = Entry(update_frame, width=30)
            l_name.grid(row=1, column=12, columnspan=10, sticky=W)
            address = Entry(update_frame, width=61)
            address.grid(row=2, column=1, columnspan=40, sticky=W)
            city = Entry(update_frame, width=30)
            city.grid(row=3, column=1, columnspan=10, sticky=W)
            state = Entry(update_frame, width=5)
            state.grid(row=3, column=12, columnspan=2, sticky=W)
            zip_code = Entry(update_frame, width=10)
            zip_code.grid(row=3, column=15, columnspan=5, sticky=W)
            phone = Entry(update_frame, width=3)
            email = Entry(update_frame, width=30)
            email.grid(row=5, column=1, sticky=W, columnspan=10)
            grade_point = Entry(update_frame, width=5)
            grade_point.grid(row=6, column=1, sticky=W)
            grade_level = Entry(update_frame, width=5)
            grade_level.grid(row=6, column=3, sticky=W)

            # Textbox labels
            f_name_label = Label(update_frame, text="First Name")
            f_name_label.grid(row=1, column=0)
            l_name_label = Label(update_frame, text="Last Name")
            l_name_label.grid(row=1, column=11)
            address_label = Label(update_frame, text="Street Address")
            address_label.grid(row=2, column=0)
            city_label = Label(update_frame, text="City")
            city_label.grid(row=3, column=0)
            state_label = Label(update_frame, text="State")
            state_label.grid(row=3, column=11)
            zip_code_label = Label(update_frame, text="Zip code")
            zip_code_label.grid(row=3, column=14)
            phone_label = Label(update_frame, text="Phone Number")
            phone_label.grid(row=4, column=0)
            email_label = Label(update_frame, text="Email")
            email_label.grid(row=5, column=0)
            grade_point_label = Label(update_frame, text="GPA")
            grade_point_label.grid(row=6, column=0)
            grade_level_label = Label(update_frame, text="Grade Level")
            grade_level_label.grid(row=6, column=2)

            update_button = Button(update_frame, text="Update", command=update_records)
            update_button.grid(row=9, column=20)
            delete_btn = Button(update_frame, text="Delete Record", command=delete_record_confirm)
            delete_btn.grid(row=10, column=20)

            f_name.insert(0, f_name_records[i])
            l_name.insert(0, l_name_records[i])
            address.insert(0, address_records[i])
            city.insert(0, city_records[i])
            state.insert(0, state_records[i])
            zip_code.insert(0, zip_code_records[i])
            phone.insert(0, phone_records[i])
            email.insert(0, email_records[i])
            grade_point.insert(0, gpa_records[i])
            grade_level.insert(0, grade_level_records[i])





    def return_search_results():  # returns all results in separate frames

        # Connect to DB
        conn = sqlite3.connect('SIS.db')
        # Create a cursor
        cur = conn.cursor()
        # Search based on search_bar entry
        query = search_bar.get()

        drop_menu = drop_menu_selection.get()
        if drop_menu == "First Name":
            cur.execute("SELECT *,oid FROM student_records WHERE f_name LIKE" + "'%" + query + "%'")
            results = cur.fetchall()
            populate_records(results)
        elif drop_menu == "Last Name":
            cur.execute("SELECT *,oid FROM student_records WHERE l_name LIKE" + "'%" + query + "%'")
            results = cur.fetchall()
            populate_records(results)
        elif drop_menu == "Address":
            cur.execute("SELECT *,oid FROM student_records WHERE address LIKE" + "'%" + query + "%'")
            results = cur.fetchall()
            populate_records(results)
        elif drop_menu == "Email":
            cur.execute("SELECT *,oid FROM student_records WHERE email LIKE" + "'%" + query + "%'")
            results = cur.fetchall()
            populate_records(results)
        else:
            cur.execute("SELECT *,oid FROM student_records WHERE grade_level LIKE" + "'%" + query + "%'")
            results = cur.fetchall()
            populate_records(results)






    def delete_record():
        pass

    def delete_record_confirm():
        confirm = Tk()
        confirm.title("Delete Confirmation")
        confirm_label = Label(confirm, text="""This will permanently delete this record.
        \n This cannot be undone. \n Are you sure you want to delete the record?""")
        confirm_label.grid(row=2, rowspan=10, column=0, columnspan=6)

        button_frame = Frame(confirm)
        button_frame.grid(row=20, columnspan=6)
        no_button = Button(button_frame, text="No", command=confirm.destroy)
        no_button.grid(row=0, column=1, columnspan=3)
        yes_button = Button(button_frame, text="Yes", command=delete_record)
        yes_button.grid(row=0, column=4, columnspan=3)





    search_records = Button(top, text="Search Records", command=return_search_results)
    search_records.grid(row=1, column=15)
    close_btn = Button(top, text="Close", padx=30, command=top.destroy)
    close_btn.grid(row=1, column=18)


def search_record_window():
    # at the bottom of this function, the search_record_window is created. Functions had to come first as
    # they are referenced in the window creation.

    def create_headers():
        # Set results window headers:
        oid_head = Label(results_frame, text="ID number")
        oid_head.grid(row=2, column=0, sticky=W, padx=10)
        f_name_head = Label(results_frame, text="First Name")
        f_name_head.grid(row=2, column=1, sticky=W, padx=10)
        l_name_head = Label(results_frame, text="Last Name")
        l_name_head.grid(row=2, column=2, sticky=W, padx=10)
        address_head = Label(results_frame, text="Address")
        address_head.grid(row=2, column=3, sticky=W, padx=10)
        city_head = Label(results_frame, text="City")
        city_head.grid(row=2, column=4, sticky=W, padx=10)
        state_head = Label(results_frame, text="State")
        state_head.grid(row=2, column=5, sticky=W, padx=10)
        zip_code_head = Label(results_frame, text="Zip Code")
        zip_code_head.grid(row=2, column=6, sticky=W, padx=10)
        phone_head = Label(results_frame, text="Phone Number")
        phone_head.grid(row=2, column=7, sticky=W, padx=10)
        email_head = Label(results_frame, text="Email")
        email_head.grid(row=2, column=8, sticky=W, padx=10)
        gpa_head = Label(results_frame, text="GPA")
        gpa_head.grid(row=2, column=9, sticky=W, padx=10)
        grade_level_head = Label(results_frame, text="Grade Level")
        grade_level_head.grid(row=2, column=10, sticky=W, padx=10)

    def search_selection():
        # When the search_records button is pushed, this program is run. It will first clear the frame
        # and then create a new one
        def clear_frame():
            # Clears the old results from the frame
            for widgets in results_frame.winfo_children():
                widgets.destroy()

        clear_frame()

        def create_results(oid_records, f_name_records, l_name_records, address_records, city_records, state_records,
                           zip_code_records, phone_records, email_records, gpa_records, grade_level_records):
            create_headers()

            # Creates a list of results

            oid_results_label = Label(results_frame, text=oid_records)
            oid_results_label.grid(row=4, column=0)
            f_name_results_label = Label(results_frame, text=f_name_records)
            f_name_results_label.grid(row=4, column=1)
            l_name_results_label = Label(results_frame, text=l_name_records)
            l_name_results_label.grid(row=4, column=2)
            address_results_label = Label(results_frame, text=address_records)
            address_results_label.grid(row=4, column=3)
            city_results_label = Label(results_frame, text=city_records)
            city_results_label.grid(row=4, column=4)
            state_results_label = Label(results_frame, text=state_records)
            state_results_label.grid(row=4, column=5)
            zip_code_results_label = Label(results_frame, text=zip_code_records)
            zip_code_results_label.grid(row=4, column=6)
            phone_results_label = Label(results_frame, text=phone_records)
            phone_results_label.grid(row=4, column=7)
            email_results_label = Label(results_frame, text=email_records)
            email_results_label.grid(row=4, column=8)
            gpa_results_label = Label(results_frame, text=gpa_records)
            gpa_results_label.grid(row=4, column=9)
            grade_level_results_label = Label(results_frame, text=grade_level_records)
            grade_level_results_label.grid(row=4, column=10)

        # This section of functions searches the records based on the criteria set in the drop menu
        def f_name_search():
            # Connect to DB
            conn = sqlite3.connect('SIS.db')
            # Create a cursor
            cur = conn.cursor()
            # Search based on search_bar entry
            f_name_search_query = search_bar.get()
            # cur.execute("SELECT *,oid FROM student_records WHERE f_name= ?", (f_name_search_query,))
            cur.execute("SELECT *,oid FROM student_records WHERE f_name LIKE" + "'%" + f_name_search_query + "%'")
            f_name_results = cur.fetchall()

            oid_records = ''
            f_name_records = ''
            l_name_records = ''
            address_records = ''
            city_records = ''
            state_records = ''
            zip_code_records = ''
            phone_records = ''
            email_records = ''
            gpa_records = ''
            grade_level_records = ''

            for result in f_name_results:
                oid_records += str(result[12]) + "\n"
                f_name_records += str(result[0]) + "\n"
                l_name_records += str(result[1]) + "\n"
                address_records += str(result[2]) + "\n"
                city_records += str(result[3]) + "\n"
                state_records += str(result[4]) + "\n"
                zip_code_records += str(result[5]) + "\n"
                phone_records += str(result[6]) + str(result[7]) + str(result[8]) + "\n"
                email_records += str(result[9]) + "\n"
                gpa_records += str(result[10]) + "\n"
                grade_level_records += str(result[11]) + "\n"

            create_results(oid_records, f_name_records, l_name_records, address_records, city_records, state_records,
                           zip_code_records, phone_records, email_records, gpa_records, grade_level_records)

        def l_name_search():
            # Connect to DB
            conn = sqlite3.connect('SIS.db')
            # Create a cursor
            cur = conn.cursor()

            l_name_search_query = search_bar.get()
            cur.execute("SELECT *,oid FROM student_records WHERE l_name LIKE" + "'%" + l_name_search_query + "%'")
            l_name_results = cur.fetchall()

            oid_records = ''
            f_name_records = ''
            l_name_records = ''
            address_records = ''
            city_records = ''
            state_records = ''
            zip_code_records = ''
            phone_records = ''
            email_records = ''
            gpa_records = ''
            grade_level_records = ''

            for result in l_name_results:
                oid_records += str(result[12]) + "\n"
                f_name_records += str(result[0]) + "\n"
                l_name_records += str(result[1]) + "\n"
                address_records += str(result[2]) + "\n"
                city_records += str(result[3]) + "\n"
                state_records += str(result[4]) + "\n"
                zip_code_records += str(result[5]) + "\n"
                phone_records += str(result[6]) + str(result[7]) + str(result[8]) + "\n"
                email_records += str(result[9]) + "\n"
                gpa_records += str(result[10]) + "\n"
                grade_level_records += str(result[11]) + "\n"

            create_results(oid_records, f_name_records, l_name_records, address_records, city_records, state_records,
                           zip_code_records, phone_records, email_records, gpa_records, grade_level_records)

        def address_search():
            # Connect to DB
            conn = sqlite3.connect('SIS.db')
            # Create a cursor
            cur = conn.cursor()

            address_search_query = search_bar.get()
            cur.execute("SELECT *,oid FROM student_records WHERE address LIKE" + "'%" + address_search_query + "%'")
            address_results = cur.fetchall()

            oid_records = ''
            f_name_records = ''
            l_name_records = ''
            address_records = ''
            city_records = ''
            state_records = ''
            zip_code_records = ''
            phone_records = ''
            email_records = ''
            gpa_records = ''
            grade_level_records = ''

            for result in address_results:
                oid_records += str(result[12]) + "\n"
                f_name_records += str(result[0]) + "\n"
                l_name_records += str(result[1]) + "\n"
                address_records += str(result[2]) + "\n"
                city_records += str(result[3]) + "\n"
                state_records += str(result[4]) + "\n"
                zip_code_records += str(result[5]) + "\n"
                phone_records += str(result[6]) + str(result[7]) + str(result[8]) + "\n"
                email_records += str(result[9]) + "\n"
                gpa_records += str(result[10]) + "\n"
                grade_level_records += str(result[11]) + "\n"

                create_results(oid_records, f_name_records, l_name_records, address_records, city_records,
                               state_records, zip_code_records, phone_records, email_records, gpa_records,
                               grade_level_records)

        def email_search():
            # Connect to DB
            conn = sqlite3.connect('SIS.db')
            # Create a cursor
            cur = conn.cursor()

            email_search_query = search_bar.get()
            cur.execute("SELECT *,oid FROM student_records WHERE email LIKE" + "'%" + email_search_query + "%'")
            email_results = cur.fetchall()

            oid_records = ''
            f_name_records = ''
            l_name_records = ''
            address_records = ''
            city_records = ''
            state_records = ''
            zip_code_records = ''
            phone_records = ''
            email_records = ''
            gpa_records = ''
            grade_level_records = ''

            for result in email_results:
                oid_records += str(result[12]) + "\n"
                f_name_records += str(result[0]) + "\n"
                l_name_records += str(result[1]) + "\n"
                address_records += str(result[2]) + "\n"
                city_records += str(result[3]) + "\n"
                state_records += str(result[4]) + "\n"
                zip_code_records += str(result[5]) + "\n"
                phone_records += str(result[6]) + str(result[7]) + str(result[8]) + "\n"
                email_records += str(result[9]) + "\n"
                gpa_records += str(result[10]) + "\n"
                grade_level_records += str(result[11]) + "\n"

            create_results(oid_records, f_name_records, l_name_records, address_records, city_records, state_records,
                           zip_code_records, phone_records, email_records, gpa_records, grade_level_records)

        def grade_level_search():
            # Connect to DB
            conn = sqlite3.connect('SIS.db')
            # Create a cursor
            cur = conn.cursor()

            grade_level_search_query = search_bar.get()
            cur.execute(
                "SELECT *,oid FROM student_records WHERE grade_level LIKE" + "'%" + grade_level_search_query + "%'")
            grade_level_results = cur.fetchall()

            oid_records = ''
            f_name_records = ''
            l_name_records = ''
            address_records = ''
            city_records = ''
            state_records = ''
            zip_code_records = ''
            phone_records = ''
            email_records = ''
            gpa_records = ''
            grade_level_records = ''

            for result in grade_level_results:
                oid_records += str(result[12]) + "\n"
                f_name_records += str(result[0]) + "\n"
                l_name_records += str(result[1]) + "\n"
                address_records += str(result[2]) + "\n"
                city_records += str(result[3]) + "\n"
                state_records += str(result[4]) + "\n"
                zip_code_records += str(result[5]) + "\n"
                phone_records += str(result[6]) + str(result[7]) + str(result[8]) + "\n"
                email_records += str(result[9]) + "\n"
                gpa_records += str(result[10]) + "\n"
                grade_level_records += str(result[11]) + "\n"

                create_results(oid_records, f_name_records, l_name_records, address_records, city_records,
                               state_records, zip_code_records, phone_records, email_records, gpa_records,
                               grade_level_records)

        drop_menu = drop_menu_selection.get()
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

    top = Tk()
    top.title("Search Records")

    # Create a frame
    results_frame = Frame(top)
    results_frame.grid(row=8, columnspan=20, sticky=NW)

    # Create the search bar and buttons
    drop_menu_selection = StringVar()
    drop_menu_selection.set("Last Name")
    search_by_label = Label(top, text="Search by: ")
    search_by_label.grid(row=1, column=0, sticky=W)
    drop_menu = OptionMenu(top, drop_menu_selection, "First Name", "Last Name", "Address", "Email", "Grade Level")
    drop_menu.config(width=10)
    drop_menu.grid(row=1, column=1, sticky=W)
    search_bar = Entry(top, width=60)
    search_bar.grid(row=1, column=2, columnspan=10, sticky=W)

    search_records = Button(top, text="Search Records", command=search_selection)
    search_records.grid(row=1, column=15)
    close_btn = Button(top, text="Close", padx=30, command=top.destroy)
    close_btn.grid(row=1, column=18)


create_btn = Button(root, text="Create a New Record", command=create_record_window)
create_btn.grid(row=3, column=1, pady=20)
update_btn = Button(root, text="Update a  Record", command=update_record_window)
update_btn.grid(row=3, column=2, pady=20)
search_btn = Button(root, text="Search Records", command=search_record_window)
search_btn.grid(row=3, column=3, pady=20)
quitBtn = Button(root, text="Quit", padx=30, command=root.destroy)
quitBtn.grid(row=21, column=3)

root.mainloop()
