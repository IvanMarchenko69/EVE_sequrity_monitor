import tkinter as tk
from tkinter import filedialog
import os
import platform
import requests
import time
from win10toast import ToastNotifier
import threading


eve_esi_url_name_to_id = 'https://esi.evetech.net/latest/universe/ids/?datasource=tranquility&language=en'
DIR = '5'
LOC_CHAT = ''
ID_PERS = ''
SEC_CHAT = ''
EVE_SYSTEMS = ''
toast = ToastNotifier()


def get_file_list(chat):
    """Выбор нужного логфайла из папки с логами"""
    file_list = ""
    all_logs = os.listdir(DIR)
    data_base = 0
    for item in all_logs:                                     # цикл отбора файла по ключам времени и имени
        cr_time = os.path.getmtime(f'{DIR}\{item}')
        item1 = item.split("_")
        if chat in item1 and cr_time >= data_base and f'{ID_PERS}.txt' in item1:
            file_list = str(item)
            data_base = cr_time
    return file_list


def find_dangerose_system(logs_secur, sequre_line):
    """Отбор свежих систем из секьюрити чата"""
    f = open(
        EVE_SYSTEMS,
        "r",
        encoding="utf-8",
        errors="ignore"
    )
    text = f.readlines()
    system_list = text[0].split(" ")

    danger_system_list = []
    logs_security = f'{DIR}\{get_file_list(logs_secur)}'  # Выбор файла логирования локального чата
    f = open(
        logs_security,
        "r",
        encoding="utf-16",
        errors="ignore"
    )
    text = f.readlines()
    col_line = len(text)
    if col_line > sequre_line:
        i = sequre_line
        while i < col_line:
            line = text[i].replace("\n", "").replace("*", "").split(" ")
            for item in line:
                if item != '' and item in system_list and item not in danger_system_list:
                    danger_system_list.append(item)
            i += 1
    return danger_system_list, col_line


def push(len_trace):
    """Вывод пуш уведомления в случае если джампов до системы менее 10"""
    plt = platform.system()
    if plt == "Darwin":
        command = '''
        osascript -e 'display notification "Опасность" with title "Враг в {len_trace} системах от вас"'
        '''
    elif plt == "Linux":
        command = f'''
        notify-send "Опасность" "Враг в {len_trace} системах от вас"
        '''
    elif plt == "Windows":
        toast.show_toast("Опасность", f'Враг в {len_trace} системах от вас', duration=20)
        return
    else:
        return
    os.system(command)


def jump_to_danger(current_system, dangerose_sustem):
    """Определение количества джампов до системы из секьюр чата"""
    print(current_system)
    print(f'в джампе{dangerose_sustem}')
    system_list_name_to_id_danger = '["' + '", "'.join(str(element) for element in dangerose_sustem) + '"]'
    system_list_name_to_id_current = '["' + str(current_system.replace("\n", "")) + '"]'
    id_system = requests.post(eve_esi_url_name_to_id, system_list_name_to_id_danger).json()
    print(id_system)
    current_system_id = requests.post(eve_esi_url_name_to_id, system_list_name_to_id_current).json()
    id_systems_request = []
    for item in id_system['systems']:
        id_systems_request.append(item['id'])
        if len(id_systems_request) > 10:
            return True
    for item in id_systems_request:
        print('Последняя проверка')
        trace = requests.get(
            f'https://esi.evetech.net/latest/route/{current_system_id["systems"][0]["id"]}/{item}/?datasource=tranquility&flag=shortest'
        ).json()
        if len(trace) < 10:
            len_trace = len(trace) - 1
            push(len_trace)
    return True


def find_location(local):
    """Помск звезной системы персонажа в локальном чате"""
    col_line_base = 12
    logs_location = f'{DIR}\{get_file_list(local)}'  # Выбор файла логирования локального чата
    f = open(
        logs_location,
        "r",
        encoding="utf-16",
        errors="ignore"
    )
    text = f.readlines()
    col_line = len(text)
    if col_line > col_line_base:
        i = col_line - 1
        while i >= col_line_base:
            line = text[i]
            if line.split(" ")[-2] == 'Локальный:':
                return line.split(" ")[-1]
            i -= 1
    return text[col_line_base][-1]


def circle():
    """Основной цикл"""
    lbl_eve_circle.configure(text='Мониторинг запущен')
    global LOC_CHAT, SEC_CHAT
    sequre_line = 16
    local = LOC_CHAT
    logs_security = SEC_CHAT
    try:
        while True:
            location_sustem = find_location(local).replace("*", "")
            print(f'текущая система - {location_sustem}')
            dangerose_sustem, col_count_line = find_dangerose_system(logs_security, sequre_line)
            print(f' список систем - {dangerose_sustem}')
            if dangerose_sustem != []:
                print(f'Проверяем число джампов')
                jump_to_danger(location_sustem, dangerose_sustem)
            sequre_line = col_count_line
            if lbl_eve_circle.cget('text') == 'Монитринг остановлен':
                break
            time.sleep(5)
    except KeyboardInterrupt:
        pass


window = tk.Tk()
window.title("Eve sequrity alarm")
window.geometry('600x350')

dir_log_path = ''


def open_directory_logfile():
    """Выбор папки с логами чатов"""
    global DIR, ID_PERS, SEC_CHAT, LOC_CHAT, dir_log_path
    dir_log_path = filedialog.askdirectory()
    if dir_log_path != '':
        lbl_dir_log.configure(text=dir_log_path.replace("/", r"\\"))
        DIR = dir_log_path.replace("/", r"\\")
        ID_PERS = txt_name_pers.get()
        SEC_CHAT = txt_sequre_chat.get()
        LOC_CHAT = txt_local_chat.get()


def open_eve_system_file():
    """Выбор файла со списком звездных систем"""
    global DIR, EVE_SYSTEMS
    eve_system_file = filedialog.askopenfilename()
    if eve_system_file != '':
        lbl_eve_system_file.configure(text=eve_system_file.replace("/", r"\\"))
        EVE_SYSTEMS = eve_system_file
        start_button.configure(state='active')


def stop():
    """Остановка функции мониторинга логов"""
    lbl_eve_circle.configure(text='Монитринг остановлен')


txt_name_pers = tk.Entry(window, width=20)
txt_name_pers.grid(column=0, row=0, pady=10)
txt_name_pers.insert(0, '')
lbl_name_pers = tk.Label(window, text='Введите id персонажа', )
lbl_name_pers.grid(column=1, row=0, pady=10)

open_dir_button = tk.Button(
    window,
    text='Директория логов',
    command=open_directory_logfile
)
open_dir_button.grid(column=0, row=1, pady=10)
lbl_dir_log = tk.Label(window, text='Директория логфайлов не выбрана')
lbl_dir_log.grid(column=1, row=1, pady=10)

txt_sequre_chat = tk.Entry(window, width=20)
txt_sequre_chat.grid(column=0, row=3, pady=10)
txt_sequre_chat.insert(0, '')
lbl_sequre_chat = tk.Label(window, text='Введите название чата безопасности')
lbl_sequre_chat.grid(column=1, row=3, pady=10)

txt_local_chat = tk.Entry(window, width=20)
txt_local_chat.grid(column=0, row=4, pady=10)
txt_local_chat.insert(0, '')
lbl_local_chat = tk.Label(window, text='Введите название локального чата')
lbl_local_chat.grid(column=1, row=4, pady=10)

lbl_eve_system_file = tk.Label(window, text='Выберите файл с системами EVE-online')
lbl_eve_system_file.grid(column=1, row=5, pady=10)
open_eve_system_button = tk.Button(
    window,
    text='Файл систем',
    command=open_eve_system_file
)
open_eve_system_button.grid(column=0, row=5, pady=10)

lbl_eve_circle = tk.Label(window, text='Монитринг остановлен')
lbl_eve_circle.grid(column=1, row=6, pady=10)

start_button = tk.Button(
    window,
    text='Запустить мониторинг',
    command=lambda: threading.Thread(target=circle).start(), state='disabled'
)
start_button.grid(column=0, row=6, pady=10)

stop_button = tk.Button(
    window,
    text='Остановить мониторинг',
    command=stop,
)
stop_button.grid(column=3, row=6, pady=10)

if __name__ == "__main__":
    window.mainloop()
