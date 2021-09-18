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

    def show_everything_from_all_contacts(self, records):
        self.view.show_everything_from_all_contacts(records)

    def get_everything_from_all_contacts(self):
        self.model.get_everything_from_all_contacts()

if __name__ == '__main__':
    agenda = Controller()
    agenda.main()
