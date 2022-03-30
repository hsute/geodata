import tkinter as tk
from cls.statio_converter import Converter


class GeodataApp(tk.Tk):
    label_msg = None
    input_river = None
    input_tolerance = None

    def __init__(self):
        super().__init__()
        self.title('Geodata')
        self.geometry("+600+300")
        self.river = ""
        self.tolerance = 0
        self.create_form()

    def handle_submit(self):
        if not self.validate():
            return

        # pokreni glavni racun
        self.show_message("Pretvaram . . .", color="orange", width=36)
        try:
            converter = Converter()
            ret = converter.run(self.river, self.tolerance)
        except Exception as e:
            self.show_message('ERROR: ' + str(e))
            return
        if ret == 0:
            self.show_message("Great success!", color="green")

    def validate(self):
        self.river = self.input_river.get()
        if self.river == "":
            self.show_message("Vodotok je nužan.")
            return False
        if self.input_tolerance.get() != "":
            try:
                self.tolerance = float(self.input_tolerance.get())
            except ValueError:
                self.show_message("Tolerancija mora biti broj.")
                return False
        else:
            self.tolerance = 0
        self.show_message("")
        return True

    def show_message(self, text, color='red', width=0):
        self.label_msg['text'] = text
        self.label_msg['foreground'] = color
        self.label_msg['width'] = width
        self.label_msg.update_idletasks()

    def create_form(self):
        self.rowconfigure([1, 2], minsize=80)
        self.columnconfigure([0, 1], weight=1)
        app_font = ('Arial', 14, '')

        form = tk.Frame(master=self)
        form.rowconfigure([0, 1], minsize=60, weight=1)
        form.columnconfigure([0], minsize=120, weight=1)
        form.columnconfigure([1], minsize=240, weight=1)

        label_river = tk.Label(master=form, text="Vodotok:", font=app_font)
        label_river.grid(row=0, column=0, sticky='e')
        self.input_river = tk.Entry(master=form, width=24, font=app_font)
        self.input_river.grid(row=0, column=1, sticky='w', padx=10)

        label_tolerance = tk.Label(master=form, text="Tolerancija (m):", font=app_font)
        label_tolerance.grid(row=1, column=0, sticky='e')
        self.input_tolerance = tk.Entry(master=form, width=8, font=app_font)
        self.input_tolerance.grid(row=1, column=1, sticky='w', padx=10)

        form.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.label_msg = tk.Label(master=self, font=app_font)
        self.label_msg.grid(row=1, column=0, columnspan=2, padx=10)

        button_run = tk.Button(master=self, text="Pokreni", font=('Arial', 16, 'bold'), bg='#0abf1c', fg='white',
                               command=self.handle_submit)
        button_run.grid(row=2, column=0, sticky='e', padx=10)

        tk.Button(master=self, text="Zatvori", font=app_font, command=self.destroy)\
            .grid(row=2, column=1, sticky='w', padx=10)


if __name__ == '__main__':
    app = GeodataApp()
    app.mainloop()
