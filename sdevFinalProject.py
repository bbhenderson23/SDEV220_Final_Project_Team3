from tkinter import *
import sqlite3
from functools import partial

root = Tk()
root.title("Student Information System")
root.geometry("1280x720")

# global search_key
global confirm

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
    cancel_button = Button(top, text="Cancel", command=top.destroy)
    cancel_button.grid(row=9, column=14, columnspan=3)


def update_record_window():
    # At bottom of this section, creates the update window
    top = Tk()
    top.title("Update Records")

    # Create a frame
    master_frame = Frame(top)
    master_frame.grid(row=8, columnspan=20, sticky=NW)

    # scrollbar = Scrollbar(master_frame, orient=VERTICAL)
    # scrollbar.grid(row=0, column=50, sticky=E)

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

    def populate_records(results):
        update_button_ids = []
        delete_button_ids = []
        clear_update_frame(master_frame)
        oid_records = []
        f_name_records = []
        l_name_records = []
        address_records = []
        city_records = []
        state_records = []
        zip_code_records = []
        phone_area_records = []
        phone_prefix_records = []
        phone_line_records = []
        email_records = []
        grade_point_records = []
        grade_level_records = []

        def change_database(search_key, updated_f_name,
                            updated_l_name,
                            updated_address,
                            updated_city,
                            updated_state,
                            updated_zip_code,
                            updated_phone_area,
                            updated_phone_prefix,
                            updated_phone_line,
                            updated_email,
                            updated_grade_point,
                            updated_grade_level,):

            conn = sqlite3.connect('SIS.db')

            # Create a cursor
            cur = conn.cursor()
            print("Search key = ", search_key)

            with conn:
                cur.execute("""UPDATE student_records SET
                            f_name = :f_name,
                            l_name = :l_name,
                            address = :address,
                            city = :city,
                            state = :state,
                            zip_code = :zip_code,
                            phone_area = :phone_area,
                            phone_prefix = :phone_prefix,
                            phone_line = :phone_line,
                            email = :email,
                            grade_point = :grade_point,
                            grade_level = :grade_level

                            WHERE oid= :oid""",
                            {
                                'f_name': updated_f_name,
                                'l_name': updated_l_name,
                                'address': updated_address,
                                'city': updated_city,
                                'state': updated_state,
                                'zip_code': updated_zip_code,
                                'phone_area': updated_phone_area,
                                'phone_prefix': updated_phone_prefix,
                                'phone_line': updated_phone_line,
                                'email': updated_email,
                                'grade_point': updated_grade_point,
                                'grade_level': updated_grade_level,
                                'oid': search_key

                            })

            conn.commit()
            conn.close()
            return_search_results()




        def delete_record(n):

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
                yes_button = Button(button_frame, text="Yes", command=partial(delete_from_db, n, confirm))
                yes_button.grid(row=0, column=4, columnspan=3)
                return confirm

            def delete_from_db(n, confirm):
                confirm.destroy()
                clicked_button = (delete_button_ids[n])
                delete_search_key = delete_oid_dict.get(clicked_button)
                print("delete_search_key =", delete_search_key)

                conn = sqlite3.connect('SIS.db')

                # Create a cursor
                cur = conn.cursor()
                print("Delete Search key = ", delete_search_key)

                with conn:
                    cur.execute("DELETE from student_records WHERE oid=:oid",
                                {'oid': delete_search_key})

                conn.commit()
                conn.close()
                return_search_results()

            delete_record_confirm()



        def update_records(n):
            clicked_button = (update_button_ids[n])
            search_key = oid_dict.get(clicked_button)

            def update_text():
                # Will need this for all vars

                updated_f_name = f_name_update.get()
                updated_l_name = l_name_update.get()
                updated_address = address_update.get()
                updated_city = city_update.get()
                updated_state = state_update.get()
                updated_zip_code = zip_code_update.get()
                updated_phone_area = phone_area_update.get()
                updated_phone_prefix = phone_prefix_update.get()
                updated_phone_line = phone_line_update.get()
                updated_email = email_update.get()
                updated_grade_point = grade_point_update.get()
                updated_grade_level = grade_level_update.get()


                change_database(search_key, updated_f_name,
                                updated_l_name,
                                updated_address,
                                updated_city,
                                updated_state,
                                updated_zip_code,
                                updated_phone_area,
                                updated_phone_prefix,
                                updated_phone_line,
                                updated_email,
                                updated_grade_point,
                                updated_grade_level)

                update_pop.destroy()

            conn = sqlite3.connect('SIS.db')
            # Create a cursor
            cur = conn.cursor()

            cur.execute("SELECT * FROM student_records WHERE oid =" + search_key)
            update_results = cur.fetchall()

            updated_f_name_records = update_results[0][0]
            updated_l_name_records = update_results[0][1]
            updated_address_records = update_results[0][2]
            updated_city_records = update_results[0][3]
            updated_state_records = update_results[0][4]
            updated_zip_code_records = update_results[0][5]
            updated_phone_area_records = update_results[0][6]
            updated_phone_prefix_records = update_results[0][7]
            updated_phone_line_records = update_results[0][8]
            updated_email_records = update_results[0][9]
            updated_grade_point_records = update_results[0][10]
            updated_grade_level_records = update_results[0][11]

            update_pop = Toplevel()
            update_pop.title("Update Record")
            address_update = StringVar()
            updated_address = StringVar()
            f_name_update = Entry(update_pop, width=30)
            f_name_update.grid(row=1, column=1, columnspan=10, sticky=W)
            l_name_update = Entry(update_pop, width=30)
            l_name_update.grid(row=1, column=13, columnspan=10, sticky=W)
            address_update = Entry(update_pop, width=61, textvariable=updated_address)
            address_update.grid(row=2, column=1, columnspan=40, sticky=W)
            city_update = Entry(update_pop, width=30)
            city_update.grid(row=3, column=1, columnspan=10, sticky=W)
            state_update = Entry(update_pop, width=5)
            state_update.grid(row=3, column=12, columnspan=2, sticky=W)
            zip_code_update = Entry(update_pop, width=10)
            zip_code_update.grid(row=3, column=15, columnspan=5, sticky=W)
            phone_area_update = Entry(update_pop, width=3)
            phone_area_update.grid(row=4, column=1)
            phone_prefix_update = Entry(update_pop, width=3)
            phone_prefix_update.grid(row=4, column=2)
            phone_line_update = Entry(update_pop, width=4)
            phone_line_update.grid(row=4, column=3)
            email_update = Entry(update_pop, width=30)
            email_update.grid(row=5, column=1, sticky=W, columnspan=10)
            grade_point_update = Entry(update_pop, width=5)
            grade_point_update.grid(row=6, column=1, sticky=W)
            grade_level_update = Entry(update_pop, width=5)
            grade_level_update.grid(row=6, column=3, sticky=W)

            # Textbox labels
            f_name_label = Label(update_pop, text="First Name")
            f_name_label.grid(row=1, column=0)
            l_name_label = Label(update_pop, text="Last Name")
            l_name_label.grid(row=1, column=12)
            address_label = Label(update_pop, text="Street Address")
            address_label.grid(row=2, column=0)
            city_label = Label(update_pop, text="City")
            city_label.grid(row=3, column=0)
            state_label = Label(update_pop, text="State")
            state_label.grid(row=3, column=11)
            zip_code_label = Label(update_pop, text="Zip code")
            zip_code_label.grid(row=3, column=14)
            phone_label = Label(update_pop, text="Phone Number")
            phone_label.grid(row=4, column=0)
            email_label = Label(update_pop, text="Email")
            email_label.grid(row=5, column=0)
            grade_point_label = Label(update_pop, text="GPA")
            grade_point_label.grid(row=6, column=0)
            grade_level_label = Label(update_pop, text="Grade Level")
            grade_level_label.grid(row=6, column=2)

            f_name_update.insert(0, updated_f_name_records)
            f_name_update.bind("<FocusIn>",
                               lambda event: f_name_update.delete(0, "end") if f_name_update.get() ==
                                                                               updated_f_name_records else None)
            f_name_update.bind("<FocusOut>", lambda event: f_name_update.insert(0,
                                                                                updated_f_name_records) if f_name_update == "" else None)
            f_name_update.bind("<FocusOut>",
                               lambda
                                   event: f_name_update.get() if f_name_update.get() != updated_f_name_records else None)
            l_name_update.insert(0, updated_l_name_records)
            l_name_update.bind("<FocusIn>",
                               lambda event: l_name_update.delete(0, "end") if l_name_update.get() ==
                                                                               updated_l_name_records else None)
            l_name_update.bind("<FocusOut>", lambda event: l_name_update.insert(0,
                                                                                updated_l_name_records) if l_name_update == "" else None)
            l_name_update.bind("<FocusOut>",
                               lambda
                                   event: l_name_update.get() if l_name_update.get() != updated_l_name_records else None)
            address_update.insert(0, updated_address_records)

            address_update.bind("<FocusIn>",
                                lambda event: address_update.delete(0, "end") if address_update.get() ==
                                                                                 updated_address_records else None)
            address_update.bind("<FocusOut>", lambda event: address_update.insert(0,
                                                                                  updated_address_records) if address_update == "" else None)
            address_update.bind("<FocusOut>",
                                lambda
                                    event: address_update.get() if address_update.get() != updated_address_records else None)
            city_update.insert(0, updated_city_records)
            city_update.bind("<FocusIn>",
                             lambda event: city_update.delete(0, "end") if city_update.get() ==
                                                                           updated_city_records else None)
            city_update.bind("<FocusOut>", lambda event: city_update.insert(0,
                                                                            updated_city_records) if city_update == "" else None)
            city_update.bind("<FocusOut>",
                             lambda
                                 event: city_update.get() if city_update.get() != updated_city_records else None)
            state_update.insert(0, updated_state_records)
            state_update.bind("<FocusIn>",
                              lambda event: state_update.delete(0, "end") if state_update.get() ==
                                                                             updated_state_records else None)
            state_update.bind("<FocusOut>", lambda event: state_update.insert(0,
                                                                              updated_state_records) if state_update == "" else None)
            state_update.bind("<FocusOut>",
                              lambda
                                  event: state_update.get() if state_update.get() != updated_state_records else None)
            zip_code_update.insert(0, updated_zip_code_records)
            zip_code_update.bind("<FocusIn>",
                                 lambda event: zip_code_update.delete(0, "end") if zip_code_update.get() ==
                                                                                   updated_zip_code_records else None)
            zip_code_update.bind("<FocusOut>", lambda event: zip_code_update.insert(0,
                                                                                    updated_zip_code_records) if zip_code_update == "" else None)
            zip_code_update.bind("<FocusOut>",
                                 lambda
                                     event: zip_code_update.get() if zip_code_update.get() != updated_zip_code_records else None)
            phone_area_update.insert(0, updated_phone_area_records)
            phone_area_update.bind("<FocusIn>",
                                   lambda event: phone_area_update.delete(0, "end") if phone_area_update.get() ==
                                                                                       updated_phone_area_records else None)
            phone_area_update.bind("<FocusOut>", lambda event: phone_area_update.insert(0,
                                                                                        updated_phone_area_records) if phone_area_update == "" else None)
            phone_area_update.bind("<FocusOut>",
                                   lambda
                                       event: phone_area_update.get() if phone_area_update.get() != updated_phone_area_records else None)
            phone_prefix_update.insert(0, updated_phone_prefix_records)
            phone_prefix_update.bind("<FocusIn>",
                                     lambda event: phone_prefix_update.delete(0, "end") if phone_prefix_update.get() ==
                                                                                           updated_phone_prefix_records else None)
            phone_prefix_update.bind("<FocusOut>", lambda event: phone_prefix_update.insert(0,
                                                                                            updated_phone_prefix_records) if phone_prefix_update == "" else None)
            phone_prefix_update.bind("<FocusOut>",
                                     lambda
                                         event: phone_prefix_update.get() if phone_prefix_update.get() != updated_phone_prefix_records else None)
            phone_line_update.insert(0, updated_phone_line_records)
            phone_line_update.bind("<FocusIn>",
                                   lambda event: phone_line_update.delete(0, "end") if phone_line_update.get() ==
                                                                                       updated_phone_line_records else None)
            phone_line_update.bind("<FocusOut>", lambda event: phone_line_update.insert(0,
                                                                                        updated_phone_line_records) if phone_line_update == "" else None)
            phone_line_update.bind("<FocusOut>",
                                   lambda
                                       event: phone_line_update.get() if phone_line_update.get() != updated_phone_line_records else None)
            email_update.insert(0, updated_email_records)
            email_update.bind("<FocusIn>",
                              lambda event: email_update.delete(0, "end") if email_update.get() ==
                                                                             updated_email_records else None)
            email_update.bind("<FocusOut>", lambda event: email_update.insert(0,
                                                                              updated_email_records) if email_update == "" else None)
            email_update.bind("<FocusOut>",
                              lambda
                                  event: email_update.get() if email_update.get() != updated_email_records else None)
            grade_point_update.insert(0, updated_grade_point_records)
            grade_point_update.bind("<FocusIn>",
                                    lambda event: grade_point_update.delete(0, "end") if grade_point_update.get() ==
                                                                                         updated_grade_point_records else None)
            grade_point_update.bind("<FocusOut>", lambda event: grade_point_update.insert(0,
                                                                                          updated_grade_point_records) if grade_point_update == "" else None)
            grade_point_update.bind("<FocusOut>",
                                    lambda
                                        event: grade_point_update.get() if grade_point_update.get() != updated_grade_point_records else None)
            grade_level_update.insert(0, updated_grade_level_records)
            grade_level_update.bind("<FocusIn>",
                                    lambda event: grade_level_update.delete(0, "end") if grade_level_update.get() ==
                                                                                         updated_grade_level_records else None)
            grade_level_update.bind("<FocusOut>", lambda event: grade_level_update.insert(0,
                                                                                          updated_grade_level_records) if grade_level_update == "" else None)
            grade_level_update.bind("<FocusOut>",
                                    lambda
                                        event: grade_level_update.get() if grade_level_update.get() != updated_grade_level_records else None)

            confirm_button = Button(update_pop, text="Save Changes", command=update_text)
            confirm_button.grid(row=9, column=20)
            cancel_button = Button(update_pop, text="Cancel", command=update_pop.destroy)
            cancel_button.grid(row=9, column=21)



        i = 0
        for result in range(len(results)):
            oid_records.append(str(results[i][12]))
            f_name_records.append(str(results[i][0]))
            l_name_records.append(str(results[i][1]))
            address_records.append(str(results[i][2]))
            city_records.append(str(results[i][3]))
            state_records.append(str(results[i][4]))
            zip_code_records.append(str(results[i][5]))
            phone_area_records.append(str(results[i][6]))
            phone_prefix_records.append(str(results[i][7]))
            phone_line_records.append(str(results[i][8]))
            email_records.append(str(results[i][9]))
            grade_point_records.append(str(results[i][10]))
            grade_level_records.append(str(results[i][11]))
            i += 1

        for i in range(len(results)):
            update_frame = Frame(master_frame, highlightbackground="black", highlightthickness=2)
            update_frame.grid(row=i + 8, columnspan=20, sticky=NW)

            f_name = Entry(update_frame, width=30)
            f_name.grid(row=1, column=3, columnspan=10, sticky=W)
            l_name = Entry(update_frame, width=30)
            l_name.grid(row=1, column=15, columnspan=10, sticky=W)
            address = Entry(update_frame, width=61)
            address.grid(row=2, column=1, columnspan=40, sticky=W)
            city = Entry(update_frame, width=30)
            city.grid(row=3, column=1, columnspan=10, sticky=W)
            state = Entry(update_frame, width=5)
            state.grid(row=3, column=12, columnspan=2, sticky=W)
            zip_code = Entry(update_frame, width=10)
            zip_code.grid(row=3, column=15, columnspan=5, sticky=W)
            phone_area = Entry(update_frame, width=3)
            phone_area.grid(row=4, column=1)
            phone_prefix = Entry(update_frame, width=3)
            phone_prefix.grid(row=4, column=2)
            phone_line = Entry(update_frame, width=4)
            phone_line.grid(row=4, column=3)
            email = Entry(update_frame, width=30)
            email.grid(row=5, column=1, sticky=W, columnspan=10)
            grade_point = Entry(update_frame, width=5)
            grade_point.grid(row=6, column=1, sticky=W)
            grade_level = Entry(update_frame, width=5)
            grade_level.grid(row=6, column=3, sticky=W)

            # Textbox labels
            f_name_label = Label(update_frame, text="First Name")
            f_name_label.grid(row=1, column=2)
            l_name_label = Label(update_frame, text="Last Name")
            l_name_label.grid(row=1, column=14)
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
            oid_label = Label(update_frame, text="ID Number")
            oid_label.grid(row=1, column=0, sticky=W)
            oid = Label(update_frame, text=oid_records[i])
            oid.grid(row=1, column=1, sticky=W)

            f_name.insert(0, f_name_records[i])
            l_name.insert(0, l_name_records[i])
            address.insert(0, address_records[i])
            city.insert(0, city_records[i])
            state.insert(0, state_records[i])
            zip_code.insert(0, zip_code_records[i])
            phone_area.insert(0, phone_area_records[i])
            phone_prefix.insert(0, phone_prefix_records[i])
            phone_line.insert(0, phone_line_records[i])
            email.insert(0, email_records[i])
            grade_point.insert(0, grade_point_records[i])
            grade_level.insert(0, grade_level_records[i])

            f_name.configure(state='readonly')
            l_name.configure(state='readonly')
            address.configure(state='readonly')
            city.configure(state='readonly')
            state.configure(state='readonly')
            zip_code.configure(state='readonly')
            phone_area.configure(state='readonly')
            phone_prefix.configure(state='readonly')
            phone_line.configure(state='readonly')
            email.configure(state='readonly')
            grade_point.configure(state='readonly')
            grade_level.configure(state='readonly')

            update_button = Button(update_frame, text="Update", command=partial(update_records, i))
            update_button.grid(row=9, column=20)
            update_button_ids.append(update_button)

            delete_button = Button(update_frame, text="Delete Record", command=partial(delete_record, i))
            delete_button.grid(row=10, column=20)
            delete_button_ids.append(delete_button)




        print("oid_records = ", oid_records)
        oid_dict = {update_button_ids[i]: oid_records[i] for i in range(len(results))}
        delete_oid_dict = {delete_button_ids[i]: oid_records[i] for i in range(len(results))}
        print(oid_dict)
        print(delete_oid_dict)

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
        grade_point_head = Label(results_frame, text="GPA")
        grade_point_head.grid(row=2, column=9, sticky=W, padx=10)
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
                           zip_code_records, phone_records, email_records, grade_point_records, grade_level_records):
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
            grade_point_results_label = Label(results_frame, text=grade_point_records)
            grade_point_results_label.grid(row=4, column=9)
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
            grade_point_records = ''
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
                grade_point_records += str(result[10]) + "\n"
                grade_level_records += str(result[11]) + "\n"

            create_results(oid_records, f_name_records, l_name_records, address_records, city_records, state_records,
                           zip_code_records, phone_records, email_records, grade_point_records, grade_level_records)

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
            grade_point_records = ''
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
                grade_point_records += str(result[10]) + "\n"
                grade_level_records += str(result[11]) + "\n"

            create_results(oid_records, f_name_records, l_name_records, address_records, city_records, state_records,
                           zip_code_records, phone_records, email_records, grade_point_records, grade_level_records)

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
            grade_point_records = ''
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
                grade_point_records += str(result[10]) + "\n"
                grade_level_records += str(result[11]) + "\n"

                create_results(oid_records, f_name_records, l_name_records, address_records, city_records,
                               state_records, zip_code_records, phone_records, email_records, grade_point_records,
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
            grade_point_records = ''
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
                grade_point_records += str(result[10]) + "\n"
                grade_level_records += str(result[11]) + "\n"

            create_results(oid_records, f_name_records, l_name_records, address_records, city_records, state_records,
                           zip_code_records, phone_records, email_records, grade_point_records, grade_level_records)

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
            grade_point_records = ''
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
                grade_point_records += str(result[10]) + "\n"
                grade_level_records += str(result[11]) + "\n"

                create_results(oid_records, f_name_records, l_name_records, address_records, city_records,
                               state_records, zip_code_records, phone_records, email_records, grade_point_records,
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
