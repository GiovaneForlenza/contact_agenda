from model import Model
from view import View


class Controller:
    def __init__(self):
        self.view = View(self)
        self.model = Model(self)

    def main(self):
        self.view.main()

    def on_btn_click(self, btn):
        self.model.btn_pressed(btn)

    def get_entry_values(self):
        list = self.view.get_entries_from_frame()
        return self.view.get_info_in_entries(list)

if __name__ == '__main__':
    agenda = Controller()
    agenda.main()
