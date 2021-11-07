import sqlite3

con = sqlite3.connect("presentations.db")
cur = con.cursor()


def select_table(table_name, *fields):
    query = f"""SELECT {', '.join(fields)} FROM {table_name}"""
    return cur.execute(query).fetchall()


def update(table_name, up_field, up_param, w_field, w_param):
    query = f""" UPDATE {table_name} SET {up_field} = {up_param} WHERE {w_field} = {w_param}"""
    cur.execute(query)
    con.commit()


def insert(table_name, in_field, values):
    query = f'''INSERT INTO {table_name}({in_field}) VALUES("{values}")'''
    cur.execute(query)
    con.commit()
