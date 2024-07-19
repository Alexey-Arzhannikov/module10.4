import threading
import time
from queue import Queue


#Класс для столов
class Table:
    def __init__(self, number):
        self.number = number
        self.busy = False


#Класс для симуляции процессов в кафе
class Cafe:
    def __init__(self, tables):
        self.tables = tables
        self.queue = Queue()

    def customer_arrival(self):
        customer_number = 1
        while customer_number <= 20:
            print(f'Посетитель номер {customer_number} прибыл')
            customer_thread = Customer(customer_number, self)
            customer_thread.start()  # начало потока
            customer_number += 1
            time.sleep(1)  # задержка в одну секунду

    def serve_customer(self, сustomer):
        table_found = False
        for table in self.tables:
            if not table.busy:
                table.busy = True
                print(f"Посетитель номер {сustomer.number} сел за стол {table.number}.")
                time.sleep(5)  # время обсуживания одного посетителя
                table.busy = False  # освобождение стола после обслужвания
                print(f"Посетитель номер {сustomer.number} покушал и ушёл.")
                table_found = True
                break
        if not table_found:
            print(f"Посетитель номер {сustomer.number} ожидает свободный стол.")
            self.queue.put(сustomer)
            self.queue.get()


#Класс (поток) посетителя
class Customer(threading.Thread):
    def __init__(self, number, cafe):
        super().__init__()
        self.number = number
        self.cafe = cafe

    def run(self):
        self.cafe.serve_customer(self)


#Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализирум кафе
cafe = Cafe(tables)

# апускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()
