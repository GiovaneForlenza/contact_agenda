from tkinter import *
from tkinter import ttk
from tkinter import simpledialog, messagebox
import tkinter as tk


class View(tk.Tk):
    PADDING = 10
    MAX_BUTTON_PER_ROW = 4
    button_captions = [
        # 'Show all contacts',
        # 'Update a contact',
        'DELETE EVERYTHING'
    ]
    entry_captions = [
        'First Name',
        'Last Name',
        'Phone Number',
        'Email',
        'Address',
        'City',
        'Province',
        'Zip Code'
    ]

    def __init__(self, controller):
        self.controller = controller
        super().__init__()
        self.title('Agenda')

        self._make_main_frame()
        # self._make_entry()
        # self._make_buttons()
        self._create_main_form()
        self._create_other_commands_form()
        self._fill_entry_info()
        self._create_all_contacts_frame()
        # self.show_everything_from_all_contacts()
        # self._center_window()

    def main(self):
        self.mainloop()

    def _make_main_frame(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=self.PADDING, pady=self.PADDING)

    def _make_entries(self, frame):
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
        btn = Button(frame, text='Add contact',
                     command=lambda button='Add contact': self.controller.on_btn_click(button))

        btn.grid(row=row + 1, column=column, columnspan=columnspan, padx=self.PADDING,
                 pady=self.PADDING)

    def _make_other_commands(self, frame):
        for caption in self.button_captions:
            btn = Button(frame, text=caption,
                         command=lambda button=caption: self.controller.on_btn_click(button))
            btn.pack(padx=self.PADDING, pady=self.PADDING)

    def _get_entry_texts(self):
        _list = self.main_form.winfo_children()

        for item in _list:
            if item.winfo_children():
                pass
                # print(item.winfo_children())

    def _create_main_form(self):
        self.main_form = LabelFrame(self.main_frame, text='Contact Info', width=500)
        self.main_form.pack(side='left', padx=self.PADDING, pady=self.PADDING)
        self._make_entries(self.main_form)

    def _create_all_contacts_frame(self):
        self.all_contacts_frame = LabelFrame(self.main_frame, text='All Contacts')
        self.all_contacts_frame.pack(side='right', padx=self.PADDING, pady=self.PADDING)
        # self._make_entries(self.main_form)

    def _create_other_commands_form(self):
        self.other_commands_form = LabelFrame(self.main_frame, text='Other Commands', width=500)
        self.other_commands_form.pack(side='right', padx=self.PADDING, pady=self.PADDING)
        self._make_other_commands(self.other_commands_form)

    def _center_window(self):
        self.update()
        width = self.winfo_width()
        height = self.winfo_height()
        x_offset = int((self.winfo_screenwidth() - width * 3))
        y_offset = int((self.winfo_screenheight() - height * 6))
        self.geometry(f'{width}x{height}+{x_offset}+{y_offset}')

    # def _make_buttons(self, frame):
    #     for caption in self.entry_captions:
    #         btn = ttk.Button(frame, text=caption, command=
    #         lambda button=caption: self.controller.on_btn_click(button))
    #         btn.pack(padx=self.PADDING / 2, pady=self.PADDING)

    def _fill_entry_info(self):
        info = [
            'Giovane',
            'Forlenza',
            '123-456-7890',
            'email@provider.com',
            '123 A Street N',
            'Toronto',
            'ON',
            'A1A-2B2'
        ]

        entries = self.get_entries_from_frame()
        count = 0
        for i in entries:
            # value = StringVar()
            # value.set(info[int(i)])
            i.insert(0, str(info[count]))
            count += 1

    def get_entries_from_frame(self):
        children_widgets = self.main_form.winfo_children()
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
            grid_padding = 5
            columns = ['Full Name', 'Phone', 'Email', 'Address', 'City', 'State', 'Postal Code']
            grid_row = 0
            #Adds the 'Header' for the form
            for column in columns:
                label = Label(self.all_contacts_frame, text=column)
                label.grid(sticky="W", row=0, column=grid_row, ipadx=50)
                grid_row += 1
            Label(self.all_contacts_frame, text='\n').grid(row=1, column=0)

            grid_row = 1
            #Adds each info from each contact as a label
            for record in records:
                for i in record:
                    if record.index(i) == 0:
                        full_name = record[1] + ', ' + record[0]
                        label = Label(self.all_contacts_frame, text=str(full_name), cursor='hand2',
                                      anchor=W)
                        label.grid(row=grid_row, column=record.index(i), padx=grid_padding,
                                   pady=grid_padding)
                        # Makes the label clickable for further requests
                        # label.bind('<Button-1>', lambda e:print('aaa'))
                    elif record.index(i) != 1:
                        grid_column = record.index(i)
                        if grid_column != 0:
                            grid_column -= 1
                        Label(self.all_contacts_frame, text=i, anchor=W).grid(row=grid_row,
                                                                              column=grid_column,
                                                                              padx=grid_padding,
                                                                              pady=grid_padding)
                grid_row += 1
        else:
            label = Label(self.all_contacts_frame, text='No contacts were found').grid(row=0,
                                                                                       column=0,
                                                                                       padx=self.PADDING,
                                                                                       pady=self.PADDING)

    def clear_all_contacts_frame(self):
        children_widgets = self.all_contacts_frame.winfo_children()
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Label':
                child_widget.grid_remove()
