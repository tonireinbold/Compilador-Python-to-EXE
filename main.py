import PySimpleGUI as sg
import subprocess
import os
import sys

def create_window():
    layout = [
        [sg.Text("Selecione o script Python:")],
        [sg.Input(key="script_path", size=(40, 1)), sg.FileBrowse(file_types=(("Python Files", "*.py"),))],
        [sg.Text("Escolha o formato de saída:"), sg.Radio("Arquivo Único", "RADIO1", default=True, key="output_type"),
         sg.Radio("Pasta", "RADIO1", key="output_type_folder")],
        [sg.Text("Selecione o local de saída:"), sg.FolderBrowse(key="output_folder"), sg.Input(key="output_path", visible=False)],
        [sg.Text("Modo de Execução:"), sg.Radio("Console", "RADIO2", default=True, key="console_mode"),
         sg.Radio("Interface Gráfica", "RADIO2", key="gui_mode")],
        [sg.Button("Compilar para .exe"), sg.Button("Sair")]
    ]

    return sg.Window("Compilador Python - Toni Reinbold", layout, finalize=True)

def main():
    window = create_window()

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Sair":
            break
        elif event == "Compilar para .exe":
            script_path = values["script_path"]
            output_folder = values["output_folder"]
            output_type = "--onefile" if values["output_type"] else "--onedir"
            mode = "--console" if values["console_mode"] else "--windowed"

            if script_path:
                try:
                    window['Compilar para .exe'].update(disabled=True)
                    subprocess.run(['pyinstaller', output_type, mode, script_path, '--distpath', output_folder], check=True)
                    sg.popup("Sucesso", "Compilação para .exe concluída com sucesso!")
                except subprocess.CalledProcessError as e:
                    sg.popup_error(f"Erro ao compilar: {e}")
                except Exception as e:
                    sg.popup_error(f"Erro inesperado: {e}")
                finally:
                    window['Compilar para .exe'].update(disabled=False)
            else:
                sg.popup_warning("Selecione um script Python antes de compilar.")

    window.close()

if __name__ == "__main__":
    main()
