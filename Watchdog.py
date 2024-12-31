import subprocess
import time
import paramiko
import logging


logging.basicConfig(filename='watchdog.log', level=logging.WARNING,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Функция для отправки ping-запроса
def ping(host):
    try:
        output = subprocess.check_output(f"ping -n 4 {host}",
                                         stderr=subprocess.STDOUT, universal_newlines=True, shell=True)
        if "TTL=63" in output:
            logging.info(f"Узел {host} доступен.")
            return True
        else:
            logging.warning(f"Узел {host} недоступен.")
            return False
    except subprocess.CalledProcessError as e:
        logging.error(f"Ошибка при выполнении ping-запроса к узлу {host}: {e}")
        return False


# Функция для перезагрузки узла через SSH
def reboot_node(ssh_host, ssh_user, ssh_password):
    try:
        logging.info(f"Попытка перезагрузки узла {ssh_host} через SSH...")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ssh_host, username=ssh_user, password=ssh_password)
        stdin, stdout, stderr = client.exec_command('reboot')
        stdout.channel.recv_exit_status()
        client.close()
        logging.info(f"Узел {ssh_host} успешно перезагружен.")
    except Exception as e:
        logging.error(f"Ошибка при подключении по SSH к узлу {ssh_host}: {e}")


# Основная логика проверки узлов
def check_nodes():
    nodes = ["192.168.77.81", "192.168.77.52", "192.168.77.36"]
    try:
        while True:
            all_nodes_ok = True
            for node in nodes:
                if not ping(node):
                    all_nodes_ok = False
                    retry_count = 0
                    while retry_count < 3:
                        logging.warning(f"Попытка повторного ping-запроса к узлу {node} (попытка {retry_count + 1})...")
                        time.sleep(20)
                        if ping(node):
                            break
                        retry_count += 1
                    if retry_count == 3 and not ping(node):
                        logging.warning(f"Узел {node} не отвечает после 3 попыток. Перезагрузка узла 192.168.77.64")
                        reboot_node("192.168.77.64", "admin", "admin213")
                        return
            if all_nodes_ok:
                logging.info("Все узлы в порядке. Ожидание 1 минуту.")
                time.sleep(60)
    except KeyboardInterrupt:
        logging.info("Программа была прервана пользователем.")


if __name__ == "__main__":
    check_nodes()
