import PySimpleGUI as sg
import operator
import mysql

from middleware.mysql import db

# ------ Medical records Layout ------
class MedicalRecordsLayout:


    def __init__(self):
        self.__selected_cell = (0, 0)
        self.__order_by = 0
        self.__data = []
        self.m_window = None

        self.window()




    def window(self) -> sg.Window:
        if self.m_window:
            return self.m_window
            
        self.__data = db.medical_record.select()

        medical_records_layout = [
            [
                sg.Text(
                    text="Information System Medical Institution/Medical records",
                    #background_color="#000000"
                )
            ],
            [
                sg.Button(
                    button_text="Back",
                    key="-BUTTON_MEDICAL_RECORDS_BACK-",
                    expand_x=True,
                    expand_y=False,
                    enable_events=True
                )
            ],
            [
                sg.Table(
                    values=self.__data,
                    headings=["Id", "Id_patient", "Diagnosis"],
                    max_col_width=25,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification="left",
                    right_click_selects=False,
                    num_rows=20,
                    key="-TABLE_MEDICAL_RECORDS-",
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
                        text="Id patient",
                        size=(8,)
                    ),
                    sg.Input(
                        key="-INPUT_MEDICAL_RECORDS_ID_PATIENTS-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Diagnosis",
                        size=(8,)
                    ),
                    sg.Input(
                        key="-INPUT_MEDICAL_RECORDS_DIAGNOSIS-",
                        expand_x=True
                    )
                ],
                [
                    sg.Button(
                        button_text="Insert",
                        key="-BUTTON_MEDICAL_RECORDS_INSERT-",
                        enable_events=True
                    ),
                    sg.Button(
                        button_text="Update",
                        key="-BUTTON_MEDICAL_RECORDS_UPDATE-",
                        enable_events=True,
                        disabled=True
                    ),
                    sg.Button(
                        button_text="Delete",
                        key="-BUTTON_MEDICAL_RECORDS_DELETE-",
                        enable_events=True,
                        disabled=True
                    )
                ]
            ]
        ]

        self.m_window = sg.Window("Medical records", medical_records_layout, resizable=True, finalize=True)

        return self.m_window




    def __get_record_form(self) -> tuple:
        return (
            int(self.m_window["-INPUT_MEDICAL_RECORDS_ID_PATIENTS-"].get()),
            self.m_window["-INPUT_MEDICAL_RECORDS_DIAGNOSIS-"].get()
        )




    def __set_record_form(self, id_patients : int, diagnosis : str):
        self.m_window["-INPUT_MEDICAL_RECORDS_ID_PATIENTS-"].update(value=id_patients),
        self.m_window["-INPUT_MEDICAL_RECORDS_DIAGNOSIS-"].update(value=diagnosis)




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
        if (event == sg.WIN_CLOSED or event == "Cancel") or event == "-BUTTON_MEDICAL_RECORDS_BACK-":
            self.m_window.close()
            return "menu"

        # TABLE CLICKED Event has value in format ("-TABLE-", "+CLICKED+", (row,col))
        # You can also call Table.get_last_clicked_position to get the cell clicked
        elif event[0] == "-TABLE_MEDICAL_RECORDS-":
            key = event[0]
            action = event[1]
            row, col = event[2]

            self.__selected_cell = (row, col)

            # Header was clicked and wasn't the "row" column
            if row == -1 and col != -1:
                self.__order_by = col
                self.__sort_table((self.__order_by, 0))
                self.m_window["-TABLE_MEDICAL_RECORDS-"].update(self.__data)

            elif row is None or col is None:
                self.__selected_cell = None
                self.__set_record_form(*(0, ""))
                self.m_window["-TABLE_MEDICAL_RECORDS-"].update(select_rows=[])
                self.m_window["-BUTTON_MEDICAL_RECORDS_UPDATE-"].update(disabled=True)
                self.m_window["-BUTTON_MEDICAL_RECORDS_DELETE-"].update(disabled=True)

            else:
                old_record = self.__data[self.__selected_cell[0]]
                self.__set_record_form(*old_record[1:])
                self.m_window["-BUTTON_MEDICAL_RECORDS_UPDATE-"].update(disabled=False)
                self.m_window["-BUTTON_MEDICAL_RECORDS_DELETE-"].update(disabled=False)

        elif event == "-BUTTON_MEDICAL_RECORDS_INSERT-":
            try:
                new_record = self.__get_record_form()

            except Exception as err:
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                return

            try:
                db.medical_record.insert(*new_record)

            except mysql.connector.IntegrityError as err:
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                return

            self.__data = db.medical_record.select()
            self.__sort_table((self.__order_by, 0))
            self.m_window["-TABLE_MEDICAL_RECORDS-"].update(self.__data)

        elif event == "-BUTTON_MEDICAL_RECORDS_UPDATE-":
            if not self.__selected_cell:
                return

            row, col = self.__selected_cell
            old_record = self.__data[row]
            new_record = (old_record[0],) + self.__get_record_form()

            try:
                db.medical_record.update(*new_record)

            except mysql.connector.IntegrityError as err:
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                return

            self.__data[row] = new_record
            self.__sort_table((self.__order_by, 0))
            self.m_window["-TABLE_MEDICAL_RECORDS-"].update(self.__data)

        elif event == "-BUTTON_MEDICAL_RECORDS_DELETE-":
            if not self.__selected_cell:
                return

            row, col = self.__selected_cell
            old_record = self.__data[row]
            db.medical_record.delete(old_record[0])
            
            # check results ???

            self.__data.remove(old_record)
            self.__sort_table((self.__order_by, 0))
            self.m_window["-TABLE_MEDICAL_RECORDS-"].update(self.__data)
