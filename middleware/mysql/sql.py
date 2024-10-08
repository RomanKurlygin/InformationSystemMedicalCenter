class Sql:
    def __init__(self, sql_path):
        self.__m_sql = self.__load(sql_path)

    def __load(self, sql_path) -> list:

        def full_read(sql_path) -> str:
            with open(sql_path, 'r') as f:
                return f.read()

        sql_file = full_read(sql_path)

        sql = sql_file.split(';')
        sql = list(map(lambda x: x.strip(" \t\n"), sql))

        return sql

    def get_sql(self, prefix) -> str:
        for sql in self.__m_sql:
            if sql.startswith(prefix):
                return sql
