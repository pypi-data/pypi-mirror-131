import os

from airflow.hooks.base_hook import BaseHook
from airflow.operators.bash_operator import BashOperator
from airflow.utils.decorators import apply_defaults


class SqlcmdOperator(BashOperator):

    template_fields = ("task_id", "bash_command", "sql_command", "sql_folder", "sql_file")
    # Currently works only with fixed sqlcmd binary
    # Must keep a whitespace at the end of the string.
    sql_command = "/opt/mssql-tools/bin/sqlcmd -b -C -S {{ params.host }} -U {{ params.login }} -P {{ params.password }} -i {{ params.file }} "

    @apply_defaults
    def __init__(self, task_id, mssql_conn_id, sql_folder, sql_file, *args, **kwargs):

        db = BaseHook.get_connection(mssql_conn_id)

        params = {
            "host": db.host,
            "login": db.login,
            "password": db.password,
            "file": self.sql_script_path(sql_folder, sql_file),
        }

        super(SqlcmdOperator, self).__init__(task_id, bash_command=self.sql_command, params=params, *args, **kwargs)

    def sql_script_path(self, sql_folder, sql_file):
        """Returns the corrected file path with quotation marks."""
        path = os.path.join(sql_folder, sql_file)
        return f"'{path}'"
