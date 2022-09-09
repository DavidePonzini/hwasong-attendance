import sql_query
import PySimpleGUI as sg
import sys


QUERY_SELECT_ACTIVITY_NAMES = 'SELECT DISTINCT `Activity Name` FROM dataset ORDER BY 1'
def QUERY_SELECT_ACTIVITY_FREQUENCY(activities: list) -> str:
    if len(activities) == 0:
        where_clause = ''
    else:
        where_clause = 'WHERE `Activity Name` = \'{}\''.format(activities[0])
        for activity in activities[1:]:
            where_clause += ' OR `Activity Name` = \'{}\''.format(activity)     # Note the space at line start!

    return '''
        SELECT
            Name,
            Surname,
            COUNT(*) as Attendance,
            DENSE_RANK() OVER(ORDER BY COUNT(*) DESC) as Rank
        FROM
            dataset
        {where_clause}
        GROUP BY
            Name, Surname
        ORDER BY
            Attendance DESC, Surname, Name

    '''.format(where_clause=where_clause)


# GUI Layout
file_column = [
    [
        sg.Text('Attendance file'),
        sg.In(size=40, enable_events=True, key='-FILE-'),
        sg.FileBrowse(file_types=(('Excel, CSV', '*.xlsx *.csv'),)),
    ],
    [
        sg.Listbox(
            values=[],
            enable_events=True,
            size=(65, 20),
            select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
            key='-ACTIVITY-')
    ],
]

attendance_column = [
    [
        sg.Table(
            headings=['Rank', 'Surname', 'Name', 'Attendance'],
            values=[],
            col_widths=[4, 20, 20, 10],
            auto_size_columns=False,
            # cols_justification=['l', 'l', 'r'],
            num_rows=20,
            key='-ATTENDANCE-')
    ],
    [
        sg.Text(
            'Developed by Davide Ponzini (davide.ponzini95@gmail.com)',
            justification='right',
            size=56,
            expand_x=True)
    ]
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_column),
        sg.VSeperator(),
        sg.Column(attendance_column),
    ]
]



if __name__ == '__main__':
    dataset = None
    #res = sql_query.execute_query(dataset, 'SELECT * FROM dataset LIMIT 10')
    
    window = sg.Window('HWASONG Attendance Report Viewer', layout)

    # Run the Event Loop
    while True:
        event, values = window.read()
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        
        # File selected
        if event == '-FILE-':
            file = values['-FILE-']
            try:
                dataset = sql_query.read_file(file)
                activity_names = sql_query.execute_query(dataset, QUERY_SELECT_ACTIVITY_NAMES)
                activity_names = activity_names['Activity Name']
            except Exception as e:
                dataset = None
                activity_names = []
                print(e, file=sys.stderr)
            window['-ACTIVITY-'].update(activity_names)
            window['-ATTENDANCE-'].update([])
        
        # Activity selected
        elif event == '-ACTIVITY-':
            if dataset is None:
                continue
            
            activities = values['-ACTIVITY-']
            
            if len(activities) == 0:
                attendance = []
            else:
                attendance = sql_query.execute_query(dataset, QUERY_SELECT_ACTIVITY_FREQUENCY(activities=activities))

                # Convert from array of columns (pandas df) to array of rows
                attendance = [[elem[1].Rank, elem[1].Surname, elem[1].Name, elem[1].Attendance] for elem in attendance.iterrows()]
            
            window['-ATTENDANCE-'].update(attendance)


    window.close()
        