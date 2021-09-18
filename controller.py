from model import Model
from view import View


class Controller:
    def __init__(self):
        self.model = Model(self)
        self.view = View(self)
        self.get_everything_from_all_contacts()

    def main(self):
        self.view.main()

    def on_btn_click(self, btn):
        self.model.btn_pressed(btn)

    def get_entry_values(self):
        list = self.view.get_entries_from_frame()
        return self.view.get_info_in_entries(list)

    def show_messagebox(self, type, title, message):
        self.view.create_messagebox(type, title, message)

    # def show_everything_from_all_contacts(self, records):
    #     self.view.show_everything_from_all_contacts(records)

    def get_everything_from_all_contacts(self):
        records = self.model.get_everything_from_all_contacts()
        self.view.show_everything_from_all_contacts(records)

    def whats_contact_id(self):
        return self.view.whats_contact_id()

    def show_update_window(self, record):
        self.view.show_update_window(record)

    def get_stored_id_to_update(self):
        return self.view.stored_id_to_update


if __name__ == '__main__':
    agenda = Controller()
    agenda.main()
