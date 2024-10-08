import PySimpleGUI as sg

# import layouts classes
from layouts.menu import MenuLayout
from layouts.doctors import DoctorsLayout
from layouts.patients import PatientsLayout
from layouts.appointments import AppointmentsLayout
from layouts.medical_records import MedicalRecordsLayout


# add a touch of color
#sg.theme("DarkAmber")


def main():
    # create the Menu layout
    menu_layout = MenuLayout()

    # other layouts
    doctors_layout = None
    patients_layout = None
    appointments_layout = None
    medical_records_layout = None

    def get_layout(window : sg.Window):
        for layout in [menu_layout, doctors_layout, patients_layout, appointments_layout, medical_records_layout]:
            if not layout:
                continue

            if layout.window() == window:
                return layout

        return None

    # event loop to process "events" and get the "values" of the inputs
    while True:
        window, event, values = sg.read_all_windows()
    
        layout = get_layout(window)

        if not layout:
            print("layout not found")
            break

        cmd = layout.events_handler(event, values)

        if layout == menu_layout:
            if cmd == "exit":
                break

            elif cmd == "doctors":
                doctors_layout = DoctorsLayout()

            elif cmd == "patients":
                patients_layout = PatientsLayout()
                pass

            elif cmd == "appointments":
                appointments_layout = AppointmentsLayout()
                pass

            elif cmd == "medical_records":
                medical_records_layout = MedicalRecordsLayout()
                pass

        elif layout in [doctors_layout, patients_layout, appointments_layout, medical_records_layout]:
            if cmd in ["exit", "menu"]:
                menu_layout.window().un_hide()
                doctors_layout = None

    menu_layout.window().close()

if __name__ == '__main__':
    main()
