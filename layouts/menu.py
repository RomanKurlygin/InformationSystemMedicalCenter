import PySimpleGUI as sg

# ------ Menu Layout ------
class MenuLayout:
    def __init__(self):
        self.m_window = None

        self.window()

    def window(self):
        if self.m_window:
            return self.m_window

        menu_layout = [
            [
                sg.Text(
                    text="Information System Medical Institution/",
                    #background_color="#000000"
                )
            ],
            [
                sg.Button(
                    button_text="Doctors",
                    auto_size_button=True,
                    key='-BUTTON_DOCTORS-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                ),
                sg.Button(
                    button_text="Patients",
                    auto_size_button=True,
                    key='-BUTTON_PATIENTS-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                )
            ],
            [
                sg.Button(
                    button_text="Appointments",
                    auto_size_button=True,
                    key='-BUTTON_APPOINTMENTS-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                ),
                sg.Button(
                    button_text="Medical records",
                    auto_size_button=True,
                    key='-BUTTON_MEDICAL_RECORDS-',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True
                )
            ]
        ]

        self.m_window = sg.Window("Menu", menu_layout, resizable=True, finalize=True)

        return self.m_window


    def events_handler(self, event, values):
        if (event == sg.WIN_CLOSED or event == "Cancel"):
            return "exit"

        elif event == "-BUTTON_DOCTORS-":
            self.m_window.hide()
            return "doctors"

        elif event == "-BUTTON_PATIENTS-":
            self.m_window.hide()
            return "patients"

        elif event == "-BUTTON_APPOINTMENTS-":
            self.m_window.hide()
            return "appointments"

        elif event == "-BUTTON_MEDICAL_RECORDS-":
            self.m_window.hide()
            return "medical_records"
