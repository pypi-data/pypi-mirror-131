# airflow-sqlcmd-operator
Custom Airflow BashOperator for the Microsoft sqlcmd.

This package utilizes the sqlcmd to run Microsoft SQLServer scripts on Linux like you would use them on SSMS for example. 

The **sqlcmd** supports SQLServer scripts with commands like GO, USE [db_name], etc, and multiple statements.
## Requirements
You must have **sqlcmd** already installed and (currently) on following location: "/opt/mssql-tools/bin/sqlcmd".

Installing on Ubuntu with apt:

```bash
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# install required packages for pyodbc
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev mssql-tools && apt-get clean
```

## Usage

On a dag, you can call it like this:

```python
from airflow_sqlcmd_operator import SqlcmdOperator

sqlcmd = SqlcmdOperator("MyDB", "/scripts/folder/mydag", "do_stuff.sql", dag=dag)
```