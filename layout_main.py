import PySimpleGUI as sg


_file_column = [
    [
        sg.Text('Attendance file'),
        sg.In(
            size=40,
            enable_events=True,
            key='-FILE-'),
        sg.FileBrowse(
            'Browse',
            target='-FILE-',
            file_types=(('Excel, CSV', '*.xlsx *.csv'),)),
    ],
    [
        sg.Listbox(
            values=[],
            enable_events=True,
            size=(65, 20),
            select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
            key='-ACTIVITIES-')
    ],
    [
        sg.Push(),
        sg.FileSaveAs(
            'Export selection',
            file_types=(('Excel', '*.xlsx'), ('CSV', '*.csv'),),
            default_extension='xlsx',
            enable_events=True,
            target='-EXPORT-',
            size=(58,1),
            # expand_x=True,
            disabled=True,
            key='-EXPORT-')
    ]
]

_attendance_column = [
    [
        sg.Table(
            headings=['Rank', 'Surname', 'Name', 'Attendance'],
            values=[],
            col_widths=[4, 20, 20, 10],
            auto_size_columns=False,
            # cols_justification=['l', 'l', 'r'],
            num_rows=22,
            key='-ATTENDANCE-')
    ],
    [
        sg.Push(),
        sg.Text('Developed by Davide Ponzini (davide.ponzini95@gmail.com)')
    ]
]

layout = [
    [
        sg.Column(_file_column),
        sg.VSeperator(),
        sg.Column(_attendance_column),
    ]
]