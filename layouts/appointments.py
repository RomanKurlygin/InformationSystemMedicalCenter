import PySimpleGUI as sg
import operator
import mysql

from datetime import datetime

from middleware.mysql import db

# ------ Appointments Layout ------
class AppointmentsLayout:


    def __init__(self):
        self.__selected_cell = (0, 0)
        self.__order_by = 0
        self.__data = []
        self.m_window = None

        self.window()




    def window(self) -> sg.Window:
        if self.m_window:
            return self.m_window
            
        self.__data = db.appointment.select()

        appointments_layout = [
            [
                sg.Text(
                    text="Information System Medical Institution/Appointments",
                    #background_color="#000000"
                )
            ],
            [
                sg.Button(
                    button_text="Back",
                    key="-BUTTON_APPOINTMENTS_BACK-",
                    expand_x=True,
                    expand_y=False,
                    enable_events=True
                )
            ],
            [
                sg.Table(
                    values=self.__data,
                    headings=["Id", "Id_doctor", "Id_patient", "Date"],
                    max_col_width=25,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification="left",
                    right_click_selects=False,
                    num_rows=20,
                    key="-TABLE_APPOINTMENTS-",
                    selected_row_colors="red on yellow",
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    enable_click_events=True
                )
            ],
            [
                [
                    sg.Text(
                        text="Id doctor",
                        size=(8,)
                    ),
                    sg.Input(
                        key="-INPUT_APPOINTMENTS_ID_DOCTORS-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Id patient",
                        size=(8,)
                    ),
                    sg.Input(
                        key="-INPUT_APPOINTMENTS_ID_PATIENTS-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Date",
                        size=(8,)
                    ),
                    sg.Input(
                        key="-INPUT_APPOINTMENTS_DATE-",
                        expand_x=True
                    )
                ],
                [
                    sg.Button(
                        button_text="Insert",
                        key="-BUTTON_APPOINTMENTS_INSERT-",
                        enable_events=True
                    ),
                    sg.Button(
                        button_text="Update",
                        key="-BUTTON_APPOINTMENTS_UPDATE-",
                        enable_events=True,
                        disabled=True
                    ),
                    sg.Button(
                        button_text="Delete",
                        key="-BUTTON_APPOINTMENTS_DELETE-",
                        enable_events=True,
                        disabled=True
                    )
                ]
            ]
        ]

        self.m_window = sg.Window("Appointments", appointments_layout, resizable=True, finalize=True)

        return self.m_window




    def __get_record_form(self) -> tuple:
        return (
            int(self.m_window["-INPUT_APPOINTMENTS_ID_DOCTORS-"].get()),
            int(self.m_window["-INPUT_APPOINTMENTS_ID_PATIENTS-"].get()),
            datetime.strptime(self.m_window["-INPUT_APPOINTMENTS_DATE-"].get(), "%Y.%m.%d %H:%M:%S")
        )




    def __set_record_form(self, id_doctors : int, id_patients : int, date : datetime):
        self.m_window["-INPUT_APPOINTMENTS_ID_DOCTORS-"].update(value=id_doctors),
        self.m_window["-INPUT_APPOINTMENTS_ID_PATIENTS-"].update(value=id_patients),
        self.m_window["-INPUT_APPOINTMENTS_DATE-"].update(value=date.strftime("%Y.%m.%d %H:%M:%S"))




    """ sort a table by multiple columns
    table: a list of lists (or tuple of tuples) where each inner list
            represents a row
    cols:  a list (or tuple) specifying the column numbers to sort by
            e.g. (1,0) would sort by column 1, then by column 0
    """
    def __sort_table(self, cols):
        for col in reversed(cols):
            try:
                self.__data = sorted(self.__data, key=operator.itemgetter(col))
            except Exception as e:
                sg.popup_error("Error in sort_table", "Exception in sort_table", e)




    def events_handler(self, event, values):
        if (event == sg.WIN_CLOSED or event == "Cancel") or event == "-BUTTON_APPOINTMENTS_BACK-":
            self.m_window.close()
            return "menu"

        # TABLE CLICKED Event has value in format ("-TABLE-", "+CLICKED+", (row,col))
        # You can also call Table.get_last_clicked_position to get the cell clicked
        elif event[0] == "-TABLE_APPOINTMENTS-":
            key = event[0]
            action = event[1]
            row, col = event[2]

            self.__selected_cell = (row, col)

            # Header was clicked and wasn't the "row" column
            if row == -1 and col != -1:
                self.__order_by = col
                self.__sort_table((self.__order_by, 0))
                self.m_window["-TABLE_APPOINTMENTS-"].update(self.__data)

            elif row is None or col is None:
                self.__selected_cell = None
                self.__set_record_form(*(0, 0, datetime.now()))
                self.m_window["-TABLE_APPOINTMENTS-"].update(select_rows=[])
                self.m_window["-BUTTON_APPOINTMENTS_UPDATE-"].update(disabled=True)
                self.m_window["-BUTTON_APPOINTMENTS_DELETE-"].update(disabled=True)

            else:
                old_record = self.__data[self.__selected_cell[0]]
                self.__set_record_form(*old_record[1:])
                self.m_window["-BUTTON_APPOINTMENTS_UPDATE-"].update(disabled=False)
                self.m_window["-BUTTON_APPOINTMENTS_DELETE-"].update(disabled=False)

        elif event == "-BUTTON_APPOINTMENTS_INSERT-":
            try:
                new_record = self.__get_record_form()

            except Exception as err:
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                return

            try:
                db.appointment.insert(*new_record)

            except mysql.connector.IntegrityError as err:
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                return

            self.__data = db.appointment.select()
            self.__sort_table((self.__order_by, 0))
            self.m_window["-TABLE_APPOINTMENTS-"].update(self.__data)

        elif event == "-BUTTON_APPOINTMENTS_UPDATE-":
            if not self.__selected_cell:
                return

            row, col = self.__selected_cell
            old_record = self.__data[row]
            new_record = (old_record[0],) + self.__get_record_form()

            try:
                db.appointment.update(*new_record)

            except mysql.connector.IntegrityError as err:
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                return

            self.__data[row] = new_record
            self.__sort_table((self.__order_by, 0))
            self.m_window["-TABLE_APPOINTMENTS-"].update(self.__data)

        elif event == "-BUTTON_APPOINTMENTS_DELETE-":
            if not self.__selected_cell:
                return

            row, col = self.__selected_cell
            old_record = self.__data[row]
            db.appointment.delete(old_record[0])
            
            # check results ???

            self.__data.remove(old_record)
            self.__sort_table((self.__order_by, 0))
            self.m_window["-TABLE_APPOINTMENTS-"].update(self.__data)
