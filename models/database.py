import os
import sqlite3

from docx import Document

sqlite_db = 'quizdata.db'


def create_database():
    try:
        sqlite3.connect(sqlite_db).close()

        # Reset the exitsting database. Mainly for testing local
        # if os.path.exists(sqlite_db):
        #     os.remove(sqlite_db)

        connection = sqlite3.connect(sqlite_db)
        cursor = connection.cursor()

        create_table_query = '''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                category TEXT,
                difficulty TEXT,
                last_used TIMESTAMP DEFAULT (datetime('now', 'localtime'))
            )
        '''

        cursor.execute(create_table_query)

        print("Database created successfully!")

        cursor.close()
        connection.close()

    except sqlite3.Error as error:
        print("Error creating database: ", error)


def insert_question(question, answer, category):
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    insert_query = "INSERT INTO questions (question, answer, category, last_used) VALUES (?, ?, ?, ?)"
    cursor.execute(insert_query, (question, answer, category, None))
    connection.commit()
    connection.close()


def update_question(question_id, question, answer, category):
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    update_query = "UPDATE questions SET question=?, answer=?, category=? WHERE id=?"
    cursor.execute(update_query, (question, answer, category, question_id))
    connection.commit()
    connection.close()


def delete_question(question_id):
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    delete_query = "DELETE FROM questions WHERE id=?"
    cursor.execute(delete_query, (question_id,))
    connection.commit()
    connection.close()


def get_question(question_id):
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    select_query = "SELECT * FROM questions WHERE id=?"
    cursor.execute(select_query, (question_id,))
    row = cursor.fetchone()
    connection.close()
    return row


def get_categories():
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    categories_query = "SELECT DISTINCT category FROM questions"
    cursor.execute(categories_query)
    categories = cursor.fetchall()
    connection.close()
    return categories


def get_questions_by_category(category, search_query=None):
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()

    if search_query:
        select_query = "SELECT * FROM questions WHERE category=? AND question LIKE ? ORDER BY last_used DESC"
        cursor.execute(select_query, (category, '%' + search_query + '%'))
    else:
        select_query = "SELECT * FROM questions WHERE category=? ORDER BY last_used DESC"
        cursor.execute(select_query, (category,))

    rows = cursor.fetchall()

    connection.close()
    return rows


def get_all_questions():
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    select_query = "SELECT * FROM questions"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    connection.close()
    return rows


def question_exists(question):
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    select_query = "SELECT * FROM questions WHERE question=?"
    cursor.execute(select_query, (question,))
    row = cursor.fetchone()
    connection.close()
    return row is not None


def is_question_duplicate(question, cursor):
    select_query = "SELECT COUNT(*) FROM questions WHERE question = ?"
    cursor.execute(select_query, (question['question'],))
    result = cursor.fetchone()

    return result[0] > 0


def search_questions(selected_category, search_query, cursor):
    if selected_category == 'all':
        if search_query:
            select_query = "SELECT * FROM questions WHERE question LIKE ? ORDER BY category"
            cursor.execute(select_query, ('%' + search_query + '%',))
        else:
            select_query = "SELECT * FROM questions ORDER BY category"
            cursor.execute(select_query)
    else:
        if search_query:
            select_query = "SELECT * FROM questions WHERE category=? AND question LIKE ? ORDER BY category"
            cursor.execute(select_query, (selected_category, '%' + search_query + '%'))
        else:
            select_query = "SELECT * FROM questions WHERE category=? ORDER BY category"
            cursor.execute(select_query, (selected_category,))

    rows = cursor.fetchall()

    return rows


def get_questions_with_null_timestamp(selected_category, search_query, start_date, end_date, date_comparison,
                                      timestamp=None):
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    query = "SELECT * FROM questions WHERE last_used IS NULL"
    cursor.execute(query)
    rows = cursor.fetchall()

    return rows


def insert_question_document(question, answer, category, last_used):
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    insert_query = "INSERT INTO questions (question, answer, category, last_used) VALUES (?, ?, ?, ?)"
    cursor.execute(insert_query, (question, answer, category, last_used))
    connection.commit()
    connection.close()


def get_questions_for_date(selected_category, search_query, start_date, end_date, date_comparison):
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()

    if not selected_category or selected_category == 'all':
        select_query = "SELECT id, question, answer, category, last_used FROM questions WHERE question LIKE ?"
        if start_date and end_date:
            if date_comparison == 'within':
                select_query += " AND last_used >= ? AND last_used <= ?"
            elif date_comparison == 'outside':
                select_query += " AND (last_used < ? OR last_used > ?)"
            cursor.execute(select_query, ('%' + search_query + '%', start_date, end_date))
        else:
            cursor.execute(select_query, ('%' + search_query + '%',))
    else:
        select_query = "SELECT id, question, answer, category, last_used FROM questions WHERE category=? AND question LIKE ?"
        if start_date and end_date:
            if date_comparison == 'within':
                select_query += " AND last_used >= ? AND last_used <= ?"
            elif date_comparison == 'outside':
                select_query += " AND (last_used < ? OR last_used > ?)"
            cursor.execute(select_query, (selected_category, '%' + search_query + '%', start_date, end_date))
        else:
            cursor.execute(select_query, (selected_category, '%' + search_query + '%'))

    rows = cursor.fetchall()
    connection.close()
    return rows


def load_questions_from_docx(docx_file, category):
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()

    document = Document(docx_file)

    questions = []
    current_question = None

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if not text:
            continue

        if current_question is None:

            current_question = {'question': text}
        else:

            current_question['answer'] = text

            if not is_question_duplicate(current_question, cursor):
                current_question['last_used'] = None
                questions.append(current_question)

            current_question = None

    for question in questions:
        insert_question_document(question['question'], question['answer'], category, question['last_used'])

    connection.commit()
    connection.close()


def connect_to_database():
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()
    return connection, cursor


def execute_query(query, *args):
    connection, cursor = connect_to_database()
    cursor.execute(query, args)
    connection.commit()


def fetch_rows(query, *args):
    connection, cursor = connect_to_database()
    cursor.execute(query, args)
    rows = cursor.fetchall()
    return rows
