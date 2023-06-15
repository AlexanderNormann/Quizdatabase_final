import os
import sqlite3

from datetime import datetime
from flask import Blueprint, request, render_template, redirect, Flask
import math

from models.database import (
    sqlite_db,
    search_questions,
    update_question,
    get_question,
    delete_question,
    get_categories,
    insert_question,
    question_exists,
    get_questions_for_date,
    get_questions_with_null_timestamp,
    load_questions_from_docx,
    connect_to_database
)
from models.document_operations import (
    create_document,
    update_last_used,
    save_document,
    filter_rows_by_date
)

routes_blueprint = Blueprint('routes', __name__)
routes_blueprint.config = {}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER = os.path.join(app.root_path, '../backend/uploads')


@routes_blueprint.route('/')
def index():
    return render_template('index.html')


@routes_blueprint.route('/submit_question', methods=['GET', 'POST'])
def submit_question():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        category = request.form['category']

        if question_exists(question):
            return render_template('submit_question.html', show_popup=True)

        insert_question(question, answer, category)

        return redirect('/print_database')
    else:
        return render_template('submit_question.html', show_popup=False)


@routes_blueprint.route('/print_database', methods=['GET', 'POST'])
def print_database():
    connection = sqlite3.connect(sqlite_db)
    cursor = connection.cursor()

    if request.method == 'POST':
        selected_category = request.form.get('category')
    else:
        selected_category = 'all'

    search_query = request.form.get('search')

    categories = get_categories()

    rows = search_questions(selected_category, search_query, cursor)

    connection.close()

    items_per_page = 20
    current_page = int(request.args.get('page', 1))
    paginated_rows, total_pages = paginate_rows(rows, items_per_page, current_page)

    return render_template('print_database.html', rows=paginated_rows, categories=categories,
                           selected_category=selected_category,
                           total_pages=total_pages, current_page=current_page)


@routes_blueprint.route('/delete_questions', methods=['POST'])
def delete_questions_route():
    if request.method == 'POST':
        question_ids = request.form.getlist('question_ids[]')

        for question_id in question_ids:
            delete_question(int(question_id))

        return redirect('/print_database')
    else:
        return "Invalid request method."


@routes_blueprint.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        category = request.form['category']

        update_question(question_id, question, answer, category)

        return redirect('/print_database')
    else:
        question = get_question(question_id)

        if question:
            categories = get_categories()

            return render_template('edit_question.html', question=question, categories=categories)
        else:
            return "Question not found."


@routes_blueprint.route('/select_questions', methods=['GET', 'POST'])
def select_questions():
    categories = get_categories()
    selected_category = request.form.get('category')
    search_query = request.form.get('search')
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    date_comparison = request.form.get('date_comparison')
    show_all = 'show_all' in request.form

    search_query = search_query or ''
    start_date = None
    end_date = None

    if start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            pass

    if start_date and end_date and start_date > end_date:
        pass
    if show_all:
        rows = get_questions_with_null_timestamp('all', '', start_date, end_date, date_comparison, timestamp=None)
    else:
        rows = get_questions_for_date(selected_category, search_query, start_date, end_date, date_comparison)

    updated_last_used = [row[4] for row in rows]

    items_per_page = 20
    current_page = int(request.args.get('page', 1))
    paginated_rows, total_pages = paginate_rows(rows, items_per_page, current_page)

    return render_template(
        'select_questions.html',
        rows=paginated_rows,
        categories=categories,
        selected_category=selected_category,
        last_used=updated_last_used,
        total_pages=total_pages,
        current_page=current_page
    )


@routes_blueprint.route('/generate_document', methods=['GET', 'POST'])
def generate_document(start_date=None, end_date=None):
    if request.method == 'POST':
        selected_questions = request.form.getlist('question')
        amount = int(request.form.get('amount', 10))

        connection, cursor = connect_to_database()

        placeholders = ', '.join(['?'] * len(selected_questions))

        query_conditions = []
        query_values = selected_questions.copy()

        if start_date and end_date:
            query_conditions.append("(last_used >= ? AND last_used <= ?)")
            query_values.extend([start_date, end_date])
        elif start_date:
            query_conditions.append("last_used >= ?")
            query_values.append(start_date)
        elif end_date:
            query_conditions.append("last_used <= ?")
            query_values.append(end_date)

        where_clause = " AND ".join(query_conditions)
        if where_clause:
            select_query = f"SELECT id, question, answer, category, last_used FROM questions WHERE {where_clause} AND id IN ({placeholders}) ORDER BY category"
        else:
            select_query = f"SELECT id, question, answer, category, last_used FROM questions WHERE id IN ({placeholders}) ORDER BY category"

        cursor.execute(select_query, query_values)
        rows = cursor.fetchall()

        items_per_page = 20
        current_page = 1
        total_items = len(rows)
        total_pages = math.ceil(total_items / items_per_page)
        start_index = (current_page - 1) * items_per_page
        end_index = start_index + items_per_page
        paginated_rows = rows[start_index:end_index]

        document = create_document(paginated_rows[:amount])

        updated_last_used = update_last_used(selected_questions[:amount])

        document_path = save_document(document)
        print("Document generated successfully!")
        print("Document saved at: " + os.path.abspath(document_path))

        categories = get_categories()

        selected_category = request.form.get('category')

        return render_template(
            'select_questions.html',
            rows=paginated_rows,
            categories=categories,
            selected_category=selected_category,
            last_used=updated_last_used,
            total_pages=total_pages,
            current_page=current_page
        )

    elif request.method == 'GET':
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        items_per_page = 20
        current_page = int(request.args.get('page', 1))

        connection, cursor = connect_to_database()

        select_query = "SELECT id, question, answer, category, last_used FROM questions ORDER BY category"
        cursor.execute(select_query)
        rows = cursor.fetchall()

        filtered_rows = filter_rows_by_date(rows, start_date, end_date)

        total_items = len(filtered_rows)
        total_pages = math.ceil(total_items / items_per_page)
        start_index = (current_page - 1) * items_per_page
        end_index = start_index + items_per_page
        paginated_rows = filtered_rows[start_index:end_index]

        categories = get_categories()

        return render_template(
            'select_questions.html',
            rows=paginated_rows,
            categories=categories,
            total_pages=total_pages,
            current_page=current_page
        )

    else:
        return redirect('/')


@routes_blueprint.route('/upload_document', methods=['GET', 'POST'])
def upload_document():
    if request.method == 'POST':
        document = request.files['document']
        category = request.form['category']

        if document.filename == '':
            return "No file selected."

        if document:
            document_path = os.path.join(app.config['UPLOAD_FOLDER'], document.filename)
            document.save(document_path)

            load_questions_from_docx(document_path, category)
            os.remove(document_path)

            return render_template('upload_document.html', show_popup=True)

        else:
            return "Error uploading document."

    return render_template('upload_document.html')

import os
from flask import send_file

@routes_blueprint.route('/download_document', methods=['GET'])
def download_document():
    document_path = request.args.get('document_path')
    if document_path:
        return send_file(document_path, as_attachment=True)
    else:
        return "Document path is missing."




def paginate_rows(rows, items_per_page, current_page):
    total_items = len(rows)
    total_pages = math.ceil(total_items / items_per_page)
    start_index = (current_page - 1) * items_per_page
    end_index = start_index + items_per_page
    paginated_rows = rows[start_index:end_index]

    return paginated_rows, total_pages
