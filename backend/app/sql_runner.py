from flask import Blueprint, request, render_template, flash
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from app.extensions import db

sql_runner_bp = Blueprint('sql_runner', __name__, template_folder='templates')

@sql_runner_bp.route('/sql-runner', methods=['GET', 'POST'])
def sql_runner():
    result = None
    error = None

    if request.method == 'POST':
        sql_script = request.form.get('sql_script', '').strip()
        if not sql_script:
            flash('Please enter some SQL to execute.', 'warning')
        else:
            try:
                with db.engine.begin() as conn:  
                    res = conn.execute(text(sql_script))
                    if res.returns_rows:
                        rows = res.fetchall()
                        columns = res.keys()
                        result = [{'columns': columns, 'rows': rows, 'statement': sql_script}]
                    else:
                        result = [{'columns': [], 'rows': [], 'statement': sql_script, 'rowcount': res.rowcount}]
            except SQLAlchemyError as e:
                error = str(e)

    return render_template('sql_runner.html', result=result, error=error)

