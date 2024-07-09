import mysql.connector



class SQL:
    def __init__(self, user: str, host: str, db: str, password: str) -> None:
        self.__user = user
        self.__host = host
        self.__db = db
        self.__password = password

    def query(self, query: str) -> list[list[str]] | None:
        conn = mysql.connector.connect(
            user = self.__user,
            host = self.__host,
            db = self.__db,
            password = self.__password,
        )

        cursor = conn.cursor()
        cursor.execute(query)
        if cursor.with_rows:
            return [[column for column in row] for row in cursor.fetchall()]

        conn.commit()

