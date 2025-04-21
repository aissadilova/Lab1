import psycopg2

# Подключаемся к базе данных PostgreSQL с нужными параметрами (имя базы данных, пользователь, пароль и хост)
con = psycopg2.connect(
    dbname='Phonebook',  # Имя базы данных
    user='postgres',  # Имя пользователя базы данных
    password='postgres',  # Пароль пользователя базы данных
    host='localhost',  # Хост базы данных (в данном случае локальный сервер)
    port='5432'  # Порт PostgreSQL
)
cur = con.cursor()  # Создаем курсор для выполнения SQL запросов

# Удаляем старую функцию search_by_pattern, если она существует, чтобы избежать ошибки при создании новой версии
cur.execute('DROP FUNCTION IF EXISTS search_by_pattern(VARCHAR);')

# Создание таблицы phone_book, если она не существует
# Таблица будет содержать 3 столбца: id (автоинкрементируемый), username (имя пользователя) и phone (номер телефона)
cur.execute('''
    CREATE TABLE IF NOT EXISTS phone_book (
        id SERIAL PRIMARY KEY,  -- Уникальный идентификатор пользователя
        username VARCHAR(50),  -- Имя пользователя
        phone VARCHAR(50)  -- Номер телефона
    );
''')

# 1. Функция для поиска записей по шаблону в имени или номере телефона
# Эта функция возвращает таблицу с id, username и phone тех пользователей, чьи имя или номер содержат шаблон
cur.execute('''
    CREATE OR REPLACE FUNCTION search_by_pattern(pattern VARCHAR)
    RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR)  -- Функция возвращает таблицу с 3 столбцами
    AS $$
    BEGIN
        -- Выполняем запрос, который ищет шаблон в username или phone
        RETURN QUERY
        SELECT pb.id, pb.username, pb.phone
        FROM phone_book pb
        WHERE pb.username ILIKE '%' || pattern || '%'  -- Используем ILIKE для поиска без учета регистра
        OR pb.phone ILIKE '%' || pattern || '%';  -- Ищем шаблон в номере телефона
    END;
    $$ LANGUAGE plpgsql;  -- Язык программирования для функции - PL/pgSQL
''')

# 2. Процедура для вставки или обновления пользователя
# Если пользователь с таким именем уже существует, то обновляем его номер телефона, иначе вставляем нового пользователя
cur.execute('''
    CREATE OR REPLACE PROCEDURE insert_or_update_user(name VARCHAR, userphone VARCHAR)
    AS $$
    BEGIN
        IF EXISTS (SELECT 1 FROM phone_book WHERE username = name) THEN
            UPDATE phone_book SET phone = userphone WHERE username = name;
        ELSE
            INSERT INTO phone_book(username, phone) VALUES (name, userphone);
        END IF;
    END;
    $$ LANGUAGE plpgsql;
''')

# 3. Процедура для вставки списка пользователей с проверкой корректности номеров телефонов
# Эта процедура принимает два массива: usernames и phones, и вставляет их в таблицу
# Проверка на правильность номера телефона с помощью регулярного выражения
cur.execute('''
    CREATE OR REPLACE PROCEDURE insert_many_users(usernames TEXT[], phones TEXT[])
    AS $$
    DECLARE
        i INT;  -- Переменная для индексации массива
        invalid_records TEXT := '';  -- Строка для хранения неправильных записей
    BEGIN
        -- Цикл по всем пользователям в массиве
        FOR i IN 1 .. array_length(usernames, 1) LOOP
            -- Проверка на корректность номера телефона с помощью регулярного выражения
            IF phones[i] ~ '^[0-9+\\-()\\s]+$' THEN
                -- Если телефон корректный, вызываем процедуру insert_or_update_user
                CALL insert_or_update_user(usernames[i], phones[i]);
            ELSE
                -- Если телефон некорректный, добавляем пользователя в список ошибок
                invalid_records := invalid_records || usernames[i] || ', ';
            END IF;
        END LOOP;

        -- Если есть некорректные записи, выводим их
        IF invalid_records <> '' THEN
            RAISE NOTICE 'Invalid records: %', invalid_records;
        END IF;
    END;
    $$ LANGUAGE plpgsql;  -- Язык программирования для процедуры - PL/pgSQL
''')

# 4. Функция для пагинации (постраничного вывода)
# Эта функция позволяет получить записи с ограничением по количеству записей и с учетом смещения (например, для отображения страниц)
cur.execute('''
    CREATE OR REPLACE FUNCTION get_paginated(limit_val INT, offset_val INT)
    RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR)  -- Функция возвращает таблицу с 3 столбцами
    AS $$
    BEGIN
        -- Выполняем запрос с ограничением по числу записей и смещением
        RETURN QUERY
        SELECT * FROM phone_book
        ORDER BY id  -- Сортировка по id
        LIMIT limit_val OFFSET offset_val;  -- Ограничение по числу записей и смещение
    END;
    $$ LANGUAGE plpgsql;  -- Язык программирования для функции - PL/pgSQL
''')

# 5. Процедура для удаления записи по имени или номеру телефона
# Эта процедура удаляет запись по имени пользователя или по номеру телефона
cur.execute('''
    CREATE OR REPLACE PROCEDURE delete_by_name_or_phone(query TEXT)
    AS $$
    BEGIN
        -- Удаляем запись из таблицы, если username или phone совпадают с запросом
        DELETE FROM phone_book
        WHERE username = query OR phone = query;
    END;
    $$ LANGUAGE plpgsql;  -- Язык программирования для процедуры - PL/pgSQL
''')

# Подтверждаем выполнение всех CREATE/REPLACE
con.commit()

# Вызовем процедуры и функции

# Вставка или обновление одного пользователя
cur.execute("CALL insert_or_update_user(%s, %s);", ('John Doe', '+1234567890'))
print("Добавлен/обновлен пользователь: John Doe")

# Вставка нескольких пользователей (с одним некорректным номером)
usernames = ['Alice', 'Bob', 'John']
phones = ['+1111111111', '222-333-4444', '+7777777777']
cur.execute("CALL insert_many_users(%s, %s);", (usernames, phones))
print("Пакетная вставка завершена")

# Поиск по шаблону
pattern = 'john'
cur.execute("SELECT * FROM search_by_pattern(%s);", (pattern,))
results = cur.fetchall()
print("\nРезультаты поиска:")
for row in results:
    print(row)

# Пагинация (получаем первые 5 записей)
cur.execute("SELECT * FROM get_paginated(%s, %s);", (5, 0))
paginated = cur.fetchall()
print("\nПервые 5 записей:")
for row in paginated:
    print(row)

# Удаление по имени
cur.execute("CALL delete_by_name_or_phone(%s);", ('Bob',))
print("\nУдален пользователь с именем или телефоном 'Bob'.")

# Завершаем транзакцию
con.commit()

# Закрываем соединение с базой данных
cur.close()
con.close()
