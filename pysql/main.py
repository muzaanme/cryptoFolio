import sqlite3

con = sqlite3.connect('myDB.db')

cObj = con.cursor()

cObj.execute("CREATE TABLE IF NOT EXISTS employee(id INTEGER PRIMARY KEY, name TEXT, salary REAL, department TEXT, position TEXT)")
con.commit()


def insert_values(id, name, salary, department, position):
    cObj.execute("INSERT INTO employee VALUES(?, ?, ?, ?, ?)", (id, name, salary, department, position))
    con.commit()


def update_department(dep, id):
    cObj.execute("UPDATE employee SET department = ? WHERE id=?", (dep, id))
    con.commit()

def sql_fetch():
    cObj.execute("SELECT * FROM employee")
    result = cObj.fetchall()

    for i in result:
        print(i)


def delete_all():
    cObj.execute("DELETE FROM employee")
    con.commit()

# insert_values(1, "Shubham", 80000, "Python", "Developer")

delete_all()  


cObj.close()
con.close()