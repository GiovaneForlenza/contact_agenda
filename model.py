import sqlite3


class Model():

    def __init__(self, controller):

        self.table_name = 'contacts'

        self.controller = controller
        self.conn = self._connect_db()
        self.c = self._get_cursor()
        self._create_table()

        self.contact_id = ''
        self.entry_values = ''

    def btn_pressed(self, btn):
        print(btn)
        if btn == 'Add Contact':
            self._add_new_contact()
        elif btn == 'DELETE EVERYTHING':
            self._delete_all_contacts()
        elif btn == 'Update a Contact':
            self._update_contact(0)
        elif btn == 'Update Contact':
            self._update_contact(1)
        elif btn == 'Delete Contact':
            self._delete_contact()
        elif btn == 'Cancel':
            self._close_update_window()

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
        self._execute_sql_command('create')

    def _add_new_contact(self):
        self.entry_values = self.controller.get_entry_values(self.controller.get_main_form())
        self._execute_sql_command('add')

    def get_everything_from_all_contacts(self):
        records = self._execute_sql_command('get_everything_from_all')
        return records

    def get_everything_from_one_contact(self, id):
        records = self._execute_sql_command('get_everything_from_one', id)
        return records

    def _delete_all_contacts(self):
        self._execute_sql_command('delete_everything')
        self.controller.get_everything_from_all_contacts()

    '''
    This method has 2 states
    Stage 0: Once the user click in the 'Update a Contact' button, in the main window
             This will ask the user for an ID, and search if the ID exists in the DB. 
             If it does, it'll create a new window with a pre-filled form with the information from that ID
             If the ID doesn't exist, shows a MessageBox with an error
    State 1: Once the user clicks in the 'Update Contact' button in the newly created window.
             This will ask the user if they do want to update the user with the new information filled in
             If the user answers 'Yes' the ID will be updated with the new info
             If the user answers 'No' the process is canceled and the new window is closed, taking the user back to 
             the main window
    '''

    def _update_contact(self, stage):
        if stage == 0:
            self.contact_id = self.controller.whats_contact_id()
            if self._id_exists(self.contact_id):
                self.record = self.get_everything_from_one_contact(str(self.contact_id))
                self.controller.show_update_window(self.record)
            else:
                self.controller.show_messagebox('error', 'Contact doesn\'t exist',
                                                'It was not possible to find a contact with the ID "' + str(
                                                    self.contact_id) + '"')
        else:
            answer = self._should_proceed('update')
            self.entry_values = self.controller.get_entry_values(self.controller.get_update_frame())
            if answer:
                self._execute_sql_command('update')

    def _delete_contact(self):
        answer = self._should_proceed('delete')
        if answer:
            self._execute_sql_command('delete')

    # This method deals with ALL SQL commands and which message title/text it should display
    def _execute_sql_command(self, command, id=None):
        message_type = ''
        message_title = ''
        message_text = ''
        message_title_fail = ''
        message_text_fail = ''

        # Figures out which SQL command to execute
        # If the command requires a MessageBox to appear, define the type, title and text for both success and fail
        cmd_to_execute = ''
        if command == 'create':
            cmd_to_execute = f'''CREATE TABLE IF NOT EXISTS {self.table_name}(                
                first_name text,
                last_name text,
                phone_number text,
                email text,
                address text,
                city text,
                province text,
                zip_code text
            )'''
        elif command == 'add':
            message_title = 'Contact Added'
            message_title_fail = 'Something Went wrong'
            message_text = 'The contact was added successfully.'
            message_text_fail = 'There was an error while trying to add the contact. Please try again'
            cmd_to_execute = f'''INSERT INTO {self.table_name} VALUES(
                                '{self.entry_values[0]}',
                                '{self.entry_values[1]}',
                                '{self.entry_values[2]}',
                                '{self.entry_values[3]}',
                                '{self.entry_values[4]}',
                                '{self.entry_values[5]}',
                                '{self.entry_values[6]}',
                                '{self.entry_values[7]}')'''
        elif command == 'update':
            message_title = 'Contact Updated'
            message_title_fail = 'Contact not Updated'
            message_text = 'Contact was updated successfully'
            message_text_fail = 'There was an error while trying to update the contact. Please try again'
            cmd_to_execute = f"""UPDATE {self.table_name}
                                            SET first_name = '{self.entry_values[0]}',
                                                last_name = '{self.entry_values[1]}',
                                                phone_number = '{self.entry_values[2]}',
                                                email = '{self.entry_values[3]}',
                                                address = '{self.entry_values[4]}',
                                                city = '{self.entry_values[5]}',
                                                province = '{self.entry_values[6]}',
                                                zip_code = '{self.entry_values[7]}'
                                            WHERE rowid = {self.contact_id}"""
        elif command == 'delete':
            message_title = 'Contact Deleted'
            message_title_fail = 'Contact not Deleted'
            message_text = 'Contact was updated successfully'
            message_text_fail = 'There was an error while trying to delete the contact. Please try again'
            cmd_to_execute = f'''DELETE FROM {self.table_name} WHERE rowid = {self.contact_id}'''
        elif command == 'delete_everything':
            cmd_to_execute = f'DELETE FROM {self.table_name}'
        elif command == 'get_everything_from_all':
            cmd_to_execute = f'SELECT oid, * FROM {self.table_name}'
        elif command == 'get_everything_from_one':
            cmd_to_execute = f'SELECT oid, * FROM {self.table_name} WHERE ROWID = {id}'

        try:
            # Does the initial connection with the db and executes the command defined
            self.conn = self._connect_db()
            self.c = self._get_cursor()
            self.c.execute(cmd_to_execute)

            # Returns a list with all the information either from all the rows or from a specific one
            if command == 'get_everything_from_all' or command == 'get_everything_from_one':
                return self.c.fetchall()

            self._commit_and_close_db()

            # If the command requires a MessageBox to appear, show the Success message here
            if message_type != '' and message_text != '' and message_title != '':
                self.controller.show_messagebox(message_type, message_title, message_text)

            # If the command was to Update or Delete a Contact it'll close the top window created
            if command == 'update' or command == 'delete':
                self.controller.close_update_window()

            # Updates the list with all the contacts
            self.controller.get_everything_from_all_contacts()

        # If something went wrong show a personalized MessageBox for the fail
        except Exception as e:
            print(e)
            message_type = 'error'
            if message_text_fail != '' and message_title_fail != '':
                self.controller.show_messagebox(message_type, message_title_fail, message_text_fail)


    #Asks the user if they would like to Update/Delete the contact
    #This is used as an extra layer of protection from mistakes, giving the user a chance to change their minds
    def _should_proceed(self, type):
        type_title = 'Update' if type == 'update' else 'Delete'
        type_text = 'update' if type == 'update' else 'delete'
        answer = self.controller.show_messagebox('yesno', f'{type_title} the contact?',
                                                 f'Are you sure you want to {type_text} the contact?')
        if answer:
            return True
        else:
            type_text += 'd' if type == 'update' else 'ed'
            self.controller.show_messagebox('info', f'Contact was not {type_text}', f'The contact was not {type_text}!')

    #Searched in the DB for the given ID
    #Returns True if it finds the ID, returns False if the ID doesn't exist in the db
    def _id_exists(self, id):
        records = self.get_everything_from_all_contacts()
        found = False
        if len(records):
            for i in records:
                if records[records.index(i)][0] == int(id):
                    # print('FOUND')
                    found = True
        return found

    def _close_update_window(self):
        self.controller.close_update_window()
