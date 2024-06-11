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
        cur.execute("""
            UPDATE clients SET name=%s, surname=%s, email=%s
            WHERE client_id=%s;
            """, (name, surname, email, client_id))
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
        del_phone(cur, client_id)
        cur.execute("""
        DELETE FROM clients 
        WHERE client_id=%s;
            """, (client_id,))
    except Exception as e:
        print(e)
        
# функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону
def find_client(cur, name=None, surname=None, email=None, phone=None):
    if name is not None:
        cur.execute("""
            SELECT * 
            FROM clients 
            WHERE name=%s;
            """, (name,))
    elif surname is not None:
        cur.execute("""
            SELECT * 
            FROM clients 
            WHERE surname=%s;
            """, (surname,))
    elif email is not None:
        cur.execute("""
            SELECT * 
            FROM clients 
            WHERE email=%s;
            """, (email,))
    elif phone is not None:
        cur.execute("""
            SELECT * 
            FROM phones 
            WHERE phone=%s;
            """, (phone,))
    result = cur.fetchone()
    if result is None:
         print('Пользователь не найден')
    else:
        print(result)
        return result


def main():
    conn = psycopg2.connect(database='netology_db', user='postgres', password='12341')   
    with conn.cursor() as cur:
        create_table(cur)   # создаем структуру БД
        add_user(cur, 'Андрей', 'Иванов', 'sа@mail.ru') # добавляем 3х клиентов
        add_user(cur, 'Сергей', 'Петров', 'su@mail.ru')
        add_user(cur, 'Мария', 'Иванова', 'fe@yandex.ru')
        client_id = get_client_id(cur, name='Андрей', surname='Иванов') # получаем client_id на основание имени и фамилии
        if_client_exists(cur, client_id)           # проверяем, что клиент существует
        add_phone(cur, client_id, '+79119999999')  # добавляем к текущему клиенту номер телефона
        add_phone(cur, 3, '+79118888888')          # добавляем номер по id
        update_info(cur, client_id, 'Андрей', 'Иванов', 'changed@mail.ru', '+79117777777') # обновляем текущему клиенту email и номер телефона
        del_phone(cur, client_id, '+79117777777')  # удаляем номер телефона текущего клиента
        del_user(cur, client_id)                   # и его самого
        find_client(cur, email='su@mail.ru')       # ищем клиента по email
        conn.commit()
        
    cur.close()

if __name__ == '__main__':
      main() 