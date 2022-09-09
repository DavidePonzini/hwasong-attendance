import PySimpleGUI as sg


# Func: return anything different from None to terminate the program
def run(title: str, layout: list, func, **kwargs) -> None:
    window = sg.Window(title, layout, **kwargs)

    while True:
        event, values = window.read()

        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        
        ret = func(window, event, values)

        if ret is not None:
            break
    
    window.close()

def is_exit(event) -> bool:
    return 