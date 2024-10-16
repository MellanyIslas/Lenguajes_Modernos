from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc

app = Flask(__name__)

#SQLSERVER CONNECTION
app.config['SQL_SERVER_DRIVER'] = ''
app.config['SQL_SERVER_SERVER'] = ''
app.config['SQL_SERVER_DATABASE'] = ''
app.config['SQL_SERVER_USERNAME'] = ''

connection_string = (
    f"DRIVER={app.config['SQL_SERVER_DRIVER']};"
    f"SERVER={app.config['SQL_SERVER_SERVER']};"
    f"DATABASE={app.config['SQL_SERVER_DATABASE']};"
    "Trusted_Connection=yes;"
)

mysql = pyodbc.connect(connection_string)


#Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cursor = mysql.cursor()
    cursor.execute('SELECT * FROM task')
    data = cursor.fetchall()
    return render_template('index.html', tasks = data)

@app.route('/add_task', methods=['POST'])
def add_task():
    if(request.method == 'POST'):
        TASK = request.form['TASK']
        FECHA_INICIO = request.form['FECHA_INICIO']
        FECHA_FIN = request.form['FECHA_FIN']
        DESCRIPCION = request.form['DESCRIPCION']
        cursor = mysql.cursor()
        cursor.execute('INSERT INTO task (TASK, FECHA_INICIO, FECHA_FIN, DESCRIPCION) VALUES (?, ?, ?, ?)', (TASK, FECHA_INICIO, FECHA_FIN, DESCRIPCION))
        mysql.commit()
        flash('Tarea agregada con exito')
        return redirect(url_for('index'))

@app.route('/getTask/<id>')
def edit_task(id):
    cursor = mysql.cursor()
    cursor.execute('SELECT * FROM task WHERE id = ?', id)
    data = cursor.fetchall()
    return render_template('modifyTask.html', task = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update(id):
    if request.method == 'POST':
        TASK = request.form['TASK']
        FECHA_INICIO = request.form['FECHA_INICIO']
        FECHA_FIN = request.form['FECHA_FIN']
        DESCRIPCION = request.form['DESCRIPCION']

        cursor = mysql.cursor()
        cursor.execute("""
            UPDATE task
            SET TASK = ?,
            FECHA_INICIO = ?,
            FECHA_FIN = ?,
            DESCRIPCION = ?
            WHERE ID = ?
        """, (TASK, FECHA_INICIO, FECHA_FIN, DESCRIPCION, id))
        mysql.commit()
        flash('Tarea actualizada con exito')
        return redirect(url_for('index'))


@app.route('/delete/<string:id>')
def delete_contact(id):
    cursor = mysql.cursor()
    cursor.execute('DELETE FROM task WHERE ID = ?', id)
    mysql.commit()
    flash('Tarea eliminada con exito')
    return redirect(url_for('index'))

if(__name__ == '__main__'):
    app.run(port=3000, debug = True)
