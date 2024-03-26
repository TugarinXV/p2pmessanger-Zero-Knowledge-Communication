import subprocess

def open_new_terminal(script_path):
    """Функция для запуска команды в новом терминале Windows."""
    command = f'python "{script_path}"'
    subprocess.Popen(f"cmd.exe /c start cmd.exe /k {command}", shell=True)

# Пути к твоим скриптам
beacon_script = r'C:\\Users\\Ben Diesel\\Documents\\VSCodeworkflow\\p2pmessanger-Zero-Knowledge-Communication\\Becon_folder\\test_beacon.py'
client_path = r'C:\\Users\\Ben Diesel\\Documents\\VSCodeworkflow\\p2pmessanger-Zero-Knowledge-Communication\\users'
client_script = [f'{client_path}\\user1\\TestA.py',
                 f'{client_path}\\user2\\TestB.py',
                 f'{client_path}\\user3\\TestC.py']

# Запуск сервера
open_new_terminal(beacon_script)

# Запуск трех клиентов
for path in client_script:
    open_new_terminal(path)
