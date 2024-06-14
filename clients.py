import psycopg2

# функция, создающая структуру БД (таблицы)
def create_table(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
        client_id SERIAL PRIMARY KEY,
        name VARCHAR(40) NOT NULL,
        surname VARCHAR(40) NOT NULL,
        email VARCHAR(40) NOT NULL UNIQUE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
        phone_id SERIAL PRIMARY KEY,
        client_id SERIAL REFERENCES clients(client_id),
        phone VARCHAR(100) NOT NULL UNIQUE
        );
    """)

# функция, позволяющая добавить нового клиента
def add_user(cur, name, surname, email):
    try:
        cur.execute("""
        INSERT INTO clients(name, surname, email) 
        VALUES(%s, %s, %s);
        """, (name, surname, email))       
    except Exception as e:
        print(e)

# функция, позволяющая добавить телефон для существующего клиента
def add_phone(cur, client_id, phone):
    try:
       cur.execute("""
       INSERT INTO phones(client_id, phone) 
       VALUES(%s, %s);
    """, (client_id, phone))
    except Exception as e:
        print(e)
       

# функия получения id клиента по имени и фамилии
def get_client_id(cur, name: str, surname: str) -> int:
    try:
        cur.execute("""
        SELECT client_id 
        FROM clients 
        WHERE name=%s
        AND surname=%s;
        """, (name, surname,))
        return cur.fetchone()
    except Exception as e:
        print(e)

# функия проверки существует ли клиент в БД
def if_client_exists(cur, client_id):
    try:
        if client_id is None:
            answer = input('клиента не сущесвует. Создать? ')
            if answer == "да":
                name = input('Введите имя ')
                surname = input('Введите фамилию ')
                email = input('Введите почту ')
                add_user(cur, name, surname, email)
    except Exception as e:
        print(e)

# функция, позволяющая изменить данные о клиенте
def update_info(cur, client_id, name=None, surname=None, email=None, phone=None):
    try:
        if name:
            cur.execute("""
                UPDATE clients SET name=%s
                WHERE client_id=%s;
                """, (name, client_id))
        if surname:
            cur.execute("""
                UPDATE clients SET surname=%s
                WHERE client_id=%s;
                """, (surname, client_id))
        if email:
            cur.execute("""
                UPDATE clients SET email=%s
                WHERE client_id=%s;
                """, (email, client_id))
        if phone:
            cur.execute("""
                UPDATE phones SET phone=%s
                WHERE client_id=%s;
                """, (phone, client_id))
    except Exception as e:
        print(e)

# функция, позволяющая удалить телефон для существующего клиента
def del_phone(cur, client_id, phone):
    try:
        cur.execute("""
            DELETE FROM phones 
            WHERE client_id=%s AND phone=%s;
            """, (client_id, phone))
    except Exception as e:
        print(e)

# функция, позволяющая удалить существующего клиента
def del_user(cur, client_id):
    try:
        cur.execute("""
        DELETE FROM phones 
        WHERE client_id=%s;
            """, (client_id,))
        cur.execute("""
        DELETE FROM clients 
        WHERE client_id=%s;
            """, (client_id,))
    except Exception as e:
        print(e)
        
# функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону
def find_client(cur, name='%', surname='%', email='%', phone=None):
    if not phone:
        cur.execute("""
            SELECT name, surname, email
            FROM clients 
            WHERE name LIKE %s
            AND surname LIKE %s 
            AND email LIKE %s;
            """, (name, surname, email))
    else:
        cur.execute("""
            SELECT name, surname, email, phone
            FROM phones 
                RIGHT JOIN clients
                ON phones.client_id = clients.client_id
                WHERE name LIKE %s
                AND surname LIKE %s 
                AND email LIKE %s
                AND phone LIKE %s;
            """, (name, surname, email, phone))
    result = cur.fetchall()
    if len(result) == 0:
        print('Пользователь не найден')
    else:
        print(result)
        return result

def del_table(cur):
    cur.execute("""
        DROP TABLE IF EXISTS phones;
        """)
    cur.execute("""
        DROP TABLE IF EXISTS clients;
        """)          


def main():
    with psycopg2.connect(database='netology_db', user='postgres', password='12341') as conn:
        with conn.cursor() as cur:
            # del_table(cur) # для отладки
            create_table(cur)   # создаем структуру БД
            add_user(cur, 'Андрей', 'Иванов', 'sаlute@mail.ru') # добавляем клиентов
            add_user(cur, 'Сергей', 'Петров', 'summary@mail.ru')
            add_user(cur, 'Мария', 'Иванова', 'fest@yandex.ru')
            add_user(cur, 'Валерий', 'Сергеев', 'stant@gmail.com')
            client_id = get_client_id(cur, name='Андрей', surname='Иванов') # получаем client_id на основании имени и фамилии
            if_client_exists(cur, client_id)           # проверяем, что клиент существует
            add_phone(cur, client_id, '+79111234567')  # добавляем к текущему клиенту номер телефона
            add_phone(cur, 2, '+79211112222')          # добавляем номер телефона по id
            add_phone(cur, 3, '+79998889999')
            update_info(cur, client_id, email = 'sаlute_backup@mail.ru', phone = '79111237654') # обновляем текущему клиенту email и номер телефона
            del_phone(cur, client_id, '79111237654')   # удаляем номер телефона текущего клиента
            del_user(cur, client_id)                   # удаляем все телефоны клиента и его самого из БД
            find_client(cur, name='Сергей', phone='+79211112222')       # ищем клиента 
        cur.close()
    conn.close()

if __name__ == '__main__':
      main() 