import mysql.connector
import pandas
from CRUDHandler import CRUD
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
crud = CRUD()
database_name = 'fakestore'
table_name = 'data'
db_user = 'shravan'
db_pwd = 'Vvu8z9D'


@app.route('/')
@app.route("/ingress", methods=["GET", "POST"])
def upload():
    if request.method == "POST" and request.files:
        csv_file = request.files["file"]
        csv_dataframe = pandas.read_csv(csv_file)
        try:
            mydb, check = crud.establish_connection(db_user, db_pwd)
            if check is not True:
                raise mysql.connector.Error

            command = "CREATE TABLE `fakestore`.`data` (" \
                      "`ID` int NOT NULL," \
                      "`TITLE` varchar(300) DEFAULT NULL," \
                      "`PRICE` decimal(20,2) DEFAULT NULL," \
                      "`DESCRIPTION` varchar(3000) DEFAULT NULL," \
                      "`CATEGORY` varchar(150) DEFAULT NULL," \
                      "`IMAGE` varchar(500) DEFAULT NULL," \
                      "`RATING_RATE` decimal(5,2) DEFAULT NULL," \
                      "`RATING_COUNT` int DEFAULT NULL," \
                      "PRIMARY KEY (`ID`))"
            if crud.create_table(mydb, database_name, table_name, command) is not True:
                raise mysql.connector.Error

            value_list = []
            for i, row in csv_dataframe.iterrows():
                value_list.append(tuple(row))

            command = "INSERT INTO `fakestore`.`data` " \
                      "(ID, TITLE, PRICE, DESCRIPTION, CATEGORY, IMAGE, RATING_RATE, RATING_COUNT) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            if crud.insert_values(mydb, command, value_list) is not True:
                raise mysql.connector.Error

            mydb.close()
        except mysql.connector.Error:
            print("MySQL ERROR, Program Terminate")

        except Exception:
            print("Unknown ERROR, Program Terminate")

        return redirect("/view")
    return render_template("Upload.html")


@app.route('/view')
def table():
    try:
        mydb, check = crud.establish_connection(db_user, db_pwd)
        if check is not True:
            raise mysql.connector.Error
        database_cursor = mydb.cursor()

        command = f'SELECT * FROM {database_name}.{table_name}'
        database_cursor.execute(command)
        result = database_cursor.fetchall()
        # result_df = pandas.read_sql(command, mydb)
        # print(result_df)
        mydb.commit()
        dict_keys = {'id': '', 'title': '', 'price': '', 'description': '', 'category': '', 'image': '',
                     'rating_rate': '', 'rating_count': ''}

        data_list = []
        for x in result:
            temp = dict(zip(dict_keys, list(x)))
            data_list.append(temp)

        database_cursor.close()
        mydb.close()
    except mysql.connector.Error:
        print("MySQL ERROR, Program Terminate")

    except Exception:
        print("Unknown ERROR, Program Terminate")

    return render_template('View.html', htmlList=data_list)


@app.route('/modify', methods=["GET", "POST"])
def remove():
    try:
        if request.method == "POST":
            if request.form.get("delete"):
                key_value = request.form.get("delete")
                mydb, check = crud.establish_connection(db_user, db_pwd)
                if check is not True:
                    raise mysql.connector.Error

                if crud.delete_rows(mydb, database_name, table_name, 'ID', key_value) is not True:
                    raise mysql.connector.Error

                mydb.close()
                return redirect("/view")

            if request.form.get("update"):
                return redirect(url_for('.change', key=request.form.get("update")))

            if request.form.get("backup"):
                mydb, check = crud.establish_connection(db_user, db_pwd)
                if check is not True:
                    raise mysql.connector.Error

                if crud.backup(mydb, database_name, table_name) is not True:
                    raise mysql.connector.Error
                mydb.close()
                return redirect("/view")

            if request.form.get("restore"):
                mydb, check = crud.establish_connection(db_user, db_pwd)
                if check is not True:
                    raise mysql.connector.Error

                if crud.restore(mydb, database_name, table_name) is not True:
                    raise mysql.connector.Error
                mydb.close()
                return redirect("/view")

    except mysql.connector.Error:
        print("MySQL ERROR, Program Terminate")

    except Exception:
        print("Unknown ERROR, Program Terminate")

    return redirect("/view")


@app.route('/update', methods=["GET", "POST"])
def change():
    try:
        key = request.args['key']
        mydb, check = crud.establish_connection(db_user, db_pwd)
        if check is not True:
            raise mysql.connector.Error
        database_cursor = mydb.cursor()

        command = f'SELECT * FROM {database_name}.{table_name} WHERE ID={key}'
        database_cursor.execute(command)
        result = database_cursor.fetchall()
        mydb.commit()
        dict_keys = {'id': '', 'title': '', 'price': '', 'description': '', 'category': '', 'image': '',
                     'rating_rate': '', 'rating_count': ''}
        data_list = []
        for x in result:
            temp = dict(zip(dict_keys, list(x)))
            data_list.append(temp)
        database_cursor.close()
        mydb.close()

    except mysql.connector.Error as error:
        print("MySQL ERROR, Program Terminate", error)

    except Exception:
        print("Unknown ERROR, Program Terminate")

    return render_template('Update.html', htmlList=data_list)


@app.route('/update_db', methods=["GET", "POST"])
def update():
    try:
        if request.method == "POST":
            if request.form.get("update"):
                mydb, check = crud.establish_connection(db_user, db_pwd)
                if check is not True:
                    raise mysql.connector.Error

                update_list = [request.form.get("rating_rate"), request.form.get("rating_count"),
                               request.form.get("description"), request.form.get("price"),
                               request.form.get("update")]
                command = f"UPDATE {database_name}.{table_name} SET " \
                          f"RATING_RATE={update_list[0]}, " \
                          f"RATING_COUNT={update_list[1]}, " \
                          f"DESCRIPTION='{update_list[2]}', " \
                          f"PRICE={update_list[3]} " \
                          f"WHERE ID={update_list[4]}"
                crud.update_values(mydb, command)
                mydb.close()
                return redirect("/view")

    except mysql.connector.Error as error:
        print("MySQL ERROR, Program Terminate", error)

    except Exception:
        print("Unknown ERROR, Program Terminate")

    return redirect("/view")


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
