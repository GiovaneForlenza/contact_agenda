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
        # if btn == 'Show all contacts':
        #     self.get_everything_from_all_contacts()
        elif btn == 'DELETE EVERYTHING':
            self._delete_all_contacts()
        elif btn == 'Update a contact':
            self._update_contact(0)
        elif btn == 'Update contact':
            self._update_contact(1)

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

        self.c.execute(f'''CREATE TABLE IF NOT EXISTS {self.table_name}(                
                first_name text,
                last_name text,
                phone_number text,
                email text,
                address text,
                city text,
                province text,
                zip_code text
            )''')
        self._commit_and_close_db()

        pass

    def _add_new_contact(self):
        entry_values = self.controller.get_entry_values()
        # print(entry_values)
        self.conn = self._connect_db()
        self.c = self._get_cursor()
        try:
            self.c.execute('INSERT INTO ' + self.table_name + ' VALUES (:f_name, :l_name, '
                                                              ':phone_number, :email, :address, :city, '
                                                              ':state, ' \
                                                              ':zip_code)',
                           {'f_name': entry_values[0], 'l_name': entry_values[1], 'phone_number': entry_values[2],
                            'email': entry_values[3], 'address': entry_values[4], 'city': entry_values[5],
                            'state': entry_values[6], 'zip_code': entry_values[7]})
            self.controller.show_messagebox('info', 'Contact Added', 'The contact was added '
                                                                     'successfully.')

        except Exception as e:
            self.controller.show_messagebox('error', 'Something Went wrong', 'Something went '
                                                                             'wrong while trying '
                                                                             'to add the contact.')
            print(e)

        self._commit_and_close_db()
        self.controller.get_everything_from_all_contacts()

    def get_everything_from_all_contacts(self):
        self.conn = self._connect_db()
        self.c = self._get_cursor()
        self.c.execute(f'SELECT oid, * FROM {self.table_name}')
        records = self.c.fetchall()
        self._commit_and_close_db()
        return records  # self.controller.show_everything_from_all_contacts(records)

    def _delete_all_contacts(self):
        self.conn = self._connect_db()
        self.c = self._get_cursor()
        self.c.execute(f'DELETE FROM {self.table_name}')
        self._commit_and_close_db()
        self.controller.get_everything_from_all_contacts()

    def get_everything_from_one_contact(self, id):
        self.conn = self._connect_db()
        self.c = self._get_cursor()
        self.c.execute(f'SELECT oid, * FROM {self.table_name} WHERE ROWID = {id}')
        records = self.c.fetchall()
        self._commit_and_close_db()
        return records

    def _update_contact(self, stage):
        if stage == 0:
            contact_id = self.controller.whats_contact_id()
            if self._id_exists(contact_id):
                record = self.get_everything_from_one_contact(str(contact_id))
                self.controller.show_update_window(record)
            else:
                self.controller.show_messagebox('error', 'Contact doesn\'t exist',
                                                'It was not possible to find a contact with the ID "' + str(
                                                    contact_id) + '"')
        #For some reason this is not being called after the 'Update Contact' in the new window is pressed
        else:
            print('a')
            print(self.controller.get_stored_id_to_update())

    def _id_exists(self, id):
        records = self.get_everything_from_all_contacts()
        found = False
        if len(records):
            for i in records:
                if records[records.index(i)][0] == int(id):
                    # print('FOUND')
                    found = True
        return found
