import PySimpleGUI as sg
import operator
import mysql

from middleware.mysql import db

# ------ Patients Layout ------
class PatientsLayout:


    def __init__(self):
        self.__selected_cell = (0, 0)
        self.__order_by = 0
        self.__data = []
        self.__comboGenderData = ["Female", "Male"]
        self.m_window = None

        self.window()




    def window(self) -> sg.Window:
        if self.m_window:
            return self.m_window
            
        self.__data = db.patient.select()

        patients_layout = [
            [
                sg.Text(
                    text="Information System Medical Institution/Patients",
                    #background_color="#000000"
                )
            ],
            [
                sg.Button(
                    button_text="Back",
                    key="-BUTTON_PATIENTS_BACK-",
                    expand_x=True,
                    expand_y=False,
                    enable_events=True
                )
            ],
            [
                sg.Table(
                    values=self.__data,
                    headings=["Id", "Name", "Phone", "Gender", "Weight", "Height"],
                    max_col_width=25,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification="left",
                    right_click_selects=False,
                    num_rows=20,
                    key="-TABLE_PATIENTS-",
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
                        text="Name",
                        size=(5,)
                    ),
                    sg.Input(
                        key="-INPUT_PATIENTS_NAME-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Phone",
                        size=(5,)
                    ),
                    sg.Input(
                        key="-INPUT_PATIENTS_PHONE-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Gender",
                        size=(5,)
                    ),
                    sg.Combo(
                        key="-COMBO_PATIENTS_GENDER-",
                        values=self.__comboGenderData,
                        default_value=self.__comboGenderData[0],
                        readonly=True,
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Weight",
                        size=(5,)
                    ),
                    sg.Input(
                        key="-INPUT_PATIENTS_WEIGHT-",
                        expand_x=True
                    )
                ],
                [
                    sg.Text(
                        text="Height",
                        size=(5,)
                    ),
                    sg.Input(
                        key="-INPUT_PATIENTS_HEIGHT-",
                        expand_x=True
                    )
                ],
                [
                    sg.Button(
                        button_text="Insert",
                        key="-BUTTON_PATIENTS_INSERT-",
                        enable_events=True
                    ),
                    sg.Button(
                        button_text="Update",
                        key="-BUTTON_PATIENTS_UPDATE-",
                        enable_events=True,
                        disabled=True
                    ),
                    sg.Button(
                        button_text="Delete",
                        key="-BUTTON_PATIENTS_DELETE-",
                        enable_events=True,
                        disabled=True
                    )
                ]
            ]
        ]

        self.m_window = sg.Window("Patients", patients_layout, resizable=True, finalize=True)

        return self.m_window




    def __get_record_form(self) -> tuple:
        return (
            self.m_window["-INPUT_PATIENTS_NAME-"].get(),
            self.m_window["-INPUT_PATIENTS_PHONE-"].get(),
            self.__comboGenderData.index(self.m_window["-COMBO_PATIENTS_GENDER-"].get()),
            self.m_window["-INPUT_PATIENTS_WEIGHT-"].get(),
            self.m_window["-INPUT_PATIENTS_HEIGHT-"].get()
        )




    def __set_record_form(self, name : str, phone : str, gender : bool, weight : float, height : float):
        self.m_window["-INPUT_PATIENTS_NAME-"].update(value=name),
        self.m_window["-INPUT_PATIENTS_PHONE-"].update(value=phone)
        self.m_window["-COMBO_PATIENTS_GENDER-"].update(value=self.__comboGenderData[gender])
        self.m_window["-INPUT_PATIENTS_WEIGHT-"].update(value=weight)
        self.m_window["-INPUT_PATIENTS_HEIGHT-"].update(value=height)




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
        if (event == sg.WIN_CLOSED or event == "Cancel") or event == "-BUTTON_PATIENTS_BACK-":
            self.m_window.close()
            return "menu"

        # TABLE CLICKED Event has value in format ("-TABLE-", "+CLICKED+", (row,col))
        # You can also call Table.get_last_clicked_position to get the cell clicked
        elif event[0] == "-TABLE_PATIENTS-":
            key = event[0]
            action = event[1]
            row, col = event[2]

            self.__selected_cell = (row, col)

            # Header was clicked and wasn't the "row" column
            if row == -1 and col != -1:
                self.__order_by = col
                self.__sort_table((self.__order_by, 0))
                self.m_window["-TABLE_PATIENTS-"].update(self.__data)

            elif row is None or col is None:
                self.__selected_cell = None
                self.__set_record_form(*("", "", 0, 0, 0))
                self.m_window["-TABLE_PATIENTS-"].update(select_rows=[])
                self.m_window["-BUTTON_PATIENTS_UPDATE-"].update(disabled=True)
                self.m_window["-BUTTON_PATIENTS_DELETE-"].update(disabled=True)

            else:
                old_record = self.__data[self.__selected_cell[0]]
                self.__set_record_form(*old_record[1:])
                self.m_window["-BUTTON_PATIENTS_UPDATE-"].update(disabled=False)
                self.m_window["-BUTTON_PATIENTS_DELETE-"].update(disabled=False)

        elif event == "-BUTTON_PATIENTS_INSERT-":
            new_record = self.__get_record_form()

            try:
                db.patient.insert(*new_record)

            except mysql.connector.IntegrityError as err:
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                return

            self.__data = db.patient.select()
            self.__sort_table((self.__order_by, 0))
            self.m_window["-TABLE_PATIENTS-"].update(self.__data)

        elif event == "-BUTTON_PATIENTS_UPDATE-":
            if not self.__selected_cell:
                return

            row, col = self.__selected_cell
            old_record = self.__data[row]
            new_record = (old_record[0],) + self.__get_record_form()

            try:
                db.patient.update(*new_record)

            except mysql.connector.IntegrityError as err:
                error = "Error: {}".format(err)
                print(error)
                sg.popup(error)
                return

            self.__data[row] = new_record
            self.__sort_table((self.__order_by, 0))
            self.m_window["-TABLE_PATIENTS-"].update(self.__data)

        elif event == "-BUTTON_PATIENTS_DELETE-":
            if not self.__selected_cell:
                return

            row, col = self.__selected_cell
            old_record = self.__data[row]
            db.patient.delete(old_record[0])
        
            # check results ???

            self.__data.remove(old_record)
            self.__sort_table((self.__order_by, 0))
            self.m_window["-TABLE_PATIENTS-"].update(self.__data)
