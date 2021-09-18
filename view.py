from tkinter import *
from tkinter import ttk
from tkinter import simpledialog, messagebox
import tkinter as tk


class View(tk.Tk):
    PADDING = 10
    MAX_BUTTON_PER_ROW = 4
    button_captions = [  # 'Show all contacts',
        'Update a contact', 'DELETE EVERYTHING']
    entry_captions = [  # 'Contact ID',
        'First Name', 'Last Name', 'Phone Number', 'Email', 'Address', 'City', 'Province', 'Zip Code']

    def __init__(self, controller):
        self.controller = controller
        super().__init__()
        self.title('Agenda')

        self._create_main_frame()
        self._create_main_form()
        self._create_other_commands_form()
        self._fill_entry_info(self.main_form, 0)
        self._create_all_contacts_frame()

    def main(self):
        self.mainloop()

    def _create_main_frame(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=self.PADDING, pady=self.PADDING)

    def _create_entries(self, frame, step):
        row = 0
        column = 0
        columnspan = 2
        for caption in self.entry_captions:
            entry_name = StringVar()
            entry_name.set(caption)
            label = Label(frame, text=caption)
            label.grid(row=row, column=column, sticky='E', padx=self.PADDING, pady=self.PADDING)
            entry = Entry(frame)
            entry.grid(row=row, column=column + 1, padx=self.PADDING, pady=self.PADDING)
            row += 2
        btn = Button(frame, text='Add contact' if step == 0 else 'Update Contact', command=lambda
            button='Add contact' if step == 0 else 'Update Contact': self.controller.on_btn_click(button))

        btn.grid(row=row + 1, column=column, columnspan=columnspan, padx=self.PADDING, pady=self.PADDING)

    def _create_update_window(self):
        self.update_window = Toplevel()
        self.update_window.title('Contact Update')

    def _create_update_frame(self):
        self.update_frame = LabelFrame(self.update_window, text='Contact Update')
        self.update_frame.pack(padx=self.PADDING, pady=self.PADDING)

    def _make_other_commands(self, frame):
        for caption in self.button_captions:
            btn = Button(frame, text=caption, command=lambda button=caption: self.controller.on_btn_click(button))
            btn.pack(padx=self.PADDING, pady=self.PADDING)

    def _get_entry_texts(self):
        _list = self.main_form.winfo_children()

        for item in _list:
            if item.winfo_children():
                pass  # print(item.winfo_children())

    def _create_main_form(self):
        self.main_form = LabelFrame(self.main_frame, text='Contact Info', width=500)
        self.main_form.pack(side='left', padx=self.PADDING, pady=self.PADDING)
        self._create_entries(self.main_form, 0)

    def _create_all_contacts_frame(self):
        self.all_contacts_frame = LabelFrame(self.main_frame, text='All Contacts')
        self.all_contacts_frame.pack(side='right', padx=self.PADDING, pady=self.PADDING, ipadx=self.PADDING,
                                     ipady=self.PADDING)  # self._make_entries(self.main_form)

    def _create_other_commands_form(self):
        self.other_commands_form = LabelFrame(self.main_frame, text='Other Commands', width=500)
        self.other_commands_form.pack(side='bottom', padx=self.PADDING, pady=self.PADDING)
        self._make_other_commands(self.other_commands_form)

    def _center_window(self):
        self.update()
        width = self.winfo_width()
        height = self.winfo_height()
        x_offset = int((self.winfo_screenwidth() - width * 3))
        y_offset = int((self.winfo_screenheight() - height * 6))
        self.geometry(f'{width}x{height}+{x_offset}+{y_offset}')

    def _fill_entry_info(self, frame, record):
        info = ['Giovane', 'Forlenza', '123-456-7890', 'email@provider.com', '123 A Street N', 'Toronto', 'ON',
                'A1A-2B2']

        entries = self.get_entries_from_frame(frame)
        count = 0
        for i in entries:
            if record == 0:
                i.insert(0, str(info[count]))
            else:
                i.insert(0, record[0][count + 1])
            count += 1

    def get_entries_from_frame(self, frame):
        children_widgets = frame.winfo_children()
        list = []
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Entry':
                list.append(child_widget)
        return list

    def get_info_in_entries(self, list):
        values = []
        for child_widget in list:
            if child_widget.winfo_class() == 'Entry':
                values.append(child_widget.get())
        return values

    def create_messagebox(self, type, title, message):
        if type == 'info':
            messagebox.showinfo(title, message)
        elif type == 'error':
            messagebox.showerror(title, message)
        elif type == 'warning':
            messagebox.showwarning(title, message)
        elif type == 'yesno':
            messagebox.askyesno(title, message)

    def show_everything_from_all_contacts(self, records):
        self.clear_all_contacts_frame()
        if len(records):
            all_contacts_info_frame = Frame(self.all_contacts_frame)
            all_contacts_info_frame.pack(padx=self.PADDING, pady=self.PADDING)
            # all_contacts_info_frame.columnconfigure(0, weight=1)
            # all_contacts_info_frame.columnconfigure(1, weight=2)
            # all_contacts_info_frame.columnconfigure(2, weight=2)
            grid_padding = 5
            columns = ['Contact ID', 'Full Name', 'Phone', 'Email', 'Address', 'City', 'State', 'Postal Code']
            grid_column = 0
            grid_row = 0
            # Adds the 'Header' for the form
            for column in columns:
                label = Label(all_contacts_info_frame, text=column, bg='red')
                label.grid(sticky="W", row=grid_row, column=grid_column)
                grid_column += 1
            grid_row += 1
            counter = 0

            # Adds the records for each contact
            for record in records:
                for i in record:
                    full_name = ''
                    bg_color = 'lightblue'
                    grid_column = record.index(i)

                    # If the column == 1 ('Full Name'), set the text to be 'Last_Name, First_name'
                    if record.index(i) == 1:
                        full_name = record[2] + ', ' + record[1]
                    # Ignores the 2nd index as it's used in the Full Name
                    elif record.index(i) != 2:
                        if grid_column != 0:
                            grid_column -= 1  # Decides if the text should be the  # inserted or the Full_Name based on the index
                    label = Label(all_contacts_info_frame, text=i if record.index(i) != 1 else full_name, anchor=W,
                                  bg=bg_color)
                    label.grid(sticky="W", row=grid_row, column=grid_column, padx=grid_padding, pady=grid_padding,
                               ipadx=50)
                    counter += 1
                counter = 0
                grid_row += 1
        else:
            row_frame = Frame(self.all_contacts_frame)
            row_frame.pack()
            Label(row_frame, text='No contacts were found').grid(row=0, column=0, padx=self.PADDING, pady=self.PADDING)

    def clear_all_contacts_frame(self):
        children_widgets = self.all_contacts_frame.winfo_children()
        for child_widget in children_widgets:
            # print(child_widget.winfo_class())
            if child_widget.winfo_class() == 'Frame':
                child_widget.pack_forget()

    # def record_row_clicked(self, label, counter):
    #     print(str(counter))
    #     children_widgets = self.all_contacts_frame.winfo_children()
    #     for child_widget in children_widgets:
    #         child = child_widget.winfo_children()
    #         print(child[counter]['text'])
    #         # for child in child_widget:
    #     print('----\n')
    #     # if child_widget.winfo_class() == 'Frame':
    #     # child_widget.pack_forget()

    def whats_contact_id(self):
        id_update = simpledialog.askstring(title="Update a record", prompt="What's the ID you'd like to update?")
        return id_update

    def show_update_window(self, record):
        self._create_update_window()
        self._create_update_frame()
        self._create_entries(self.update_frame, 1)
        self._fill_entry_info(self.update_frame, record)
        self.stored_id_to_update = record[0][0]
        # print(self.stored_id_to_update)
        print(record)
