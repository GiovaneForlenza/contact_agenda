import sqlite3


class Model():
    def __init__(self, controller):
        self.controller = controller
        self.db_name = 'contact_agenda.db'
        self.table_name = 'contacts'
        self.conn = self._connect_db()
        self.c = self._get_cursor()
        self._create_table()

    def btn_pressed(self, btn):
        print(btn)
        if btn == 'Add contact':
            self._add_new_contact()

    def _connect_db(self):
        self.conn = sqlite3.connect('address_book.db')
        return self.conn

    def _get_cursor(self):
        self.c = self.conn.cursor()
        return self.c

    def _commit_and_close_db(self):
        self.conn.commit()
        self.conn.close()

    def _create_table(self):
        self.conn = self._connect_db()
        self.c = self._get_cursor()

        self.c.execute(
            f'''CREATE TABLE IF NOT EXISTS {self.table_name}(
                first_name text,
                last_name text,
                phone_number text,
                email text,
                address text,
                city text,
                province text,
                zip_code text
            )'''
        )
        self._commit_and_close_db()

        pass

    def _add_new_contact(self):
        entry_values = self.controller.get_entry_values()
        print(entry_values)
        self.conn = self._connect_db()
        self.c = self._get_cursor()
        try:
            self.c.execute(
                'INSERT INTO ' + self.table_name + ' VALUES (:f_name, :l_name, '
                                                   ':phone_number, :email, :address, :city, '
                                                   ':state, ' \
                                                   ':zip_code)',
                {
                    'f_name': entry_values[0],
                    'l_name': entry_values[1],
                    'phone_number': entry_values[2],
                    'email': entry_values[3],
                    'address': entry_values[2],
                    'city': entry_values[4],
                    'state': entry_values[5],
                    'zip_code': entry_values[6]
                })
            # messagebox.showinfo('Contact added', 'The contact was added successfully')
        except Exception as e:
            # messagebox.showerror('Something went wrong',
            #                      'Something went wrong. Contact was not added')
            print(e)

        self._commit_and_close_db()
