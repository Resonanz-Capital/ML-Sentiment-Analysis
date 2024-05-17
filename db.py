import pyodbc


def get_conn():
    return pyodbc.connect("DSN=Azure Databricks", autocommit=True)