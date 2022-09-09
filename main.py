from sys import stderr
import sql_query
import queries
import gui
import layout_main
from PySimpleGUI import popup

dataset = None
attendance = None


# Return anything different from None to terminate the program
def main_loop(window, event, values):
    if event == '-FILE-':
        return select_file(window, values['-FILE-'])
    if event == '-ACTIVITIES-':
        return select_activities(window, values['-ACTIVITIES-'])
    if event == '-EXPORT-':
        return export(values['-EXPORT-'])


def select_file(window, file: str):
    global dataset, attendance

    # New dataset, reset all global variables
    dataset = None
    attendance = None

    try:
        dataset = sql_query.read_file(file)
        
        activities = sql_query.execute_query(dataset, queries.QUERY_SELECT_ACTIVITY_NAMES)
        activities = activities['Activity Name']
        
        window['-ACTIVITIES-'].update(activities)
    except Exception as e:
        print(e, file=stderr)

        window['-ACTIVITIES-'].update([])

    window['-ATTENDANCE-'].update([])


def select_activities(window, selection: list):
    global attendance

    # If no activity has been selected, don't show anything
    if len(selection) == 0:
        attendance = None
        window['-ATTENDANCE-'].update([])
        window['-EXPORT-'].update(disabled=True)

        return
    
    attendance = sql_query.execute_query(dataset, queries.QUERY_SELECT_ACTIVITY_FREQUENCY(selection))

    # Convert from array of columns (pandas df) to array of rows
    attendance_table_data = [[elem[1].Rank, elem[1].Surname, elem[1].Name, elem[1].Attendance] for elem in attendance.iterrows()]
    window['-ATTENDANCE-'].update(attendance_table_data)

    window['-EXPORT-'].update(disabled=False)


def export(file: str):
    try:
        sql_query.write_file(file, attendance)
        popup('Export successful')
    except Exception as e:
        popup('Export failed')
        print(e, file=stderr)


if __name__ == '__main__':
    gui.run('HWASONG Attendance Report Viewer', layout_main.layout, main_loop)
