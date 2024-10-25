import psycopg2
import numpy as np

from pgvector.psycopg2 import register_vector
from app.settings import settings

from app.config.constant import MONTHS, ORDERS

class PostgreClient():
    def connect_db(self, connection_string):
        '''Connect to Postgres Database'''
        conn = psycopg2.connect(connection_string)

        return conn

    def get_context(self, 
                    query_embedding, 
                    n=3, 
                    table_name="", 
                    threshold=0.2,
                    embedding_col="",
                    column_name=['id', 'title', 'description', 'published_date', 'url', 'publisher', 'full_text', 'embedding_news']):
        '''Get context from certain table'''
        conn = self.connect_db(settings.POSTGRE_CONNECTION_STR)
        embedding_array = np.array(query_embedding)

        # Register pgvector extension
        register_vector(conn)
        cur = conn.cursor()

        # column string
        column_str = ','.join(column_name)
        
        # Get the top 3 most similar documents using the KNN <=> operator
        cur.execute(
            f"SELECT {column_str} <=> %s FROM {table_name} WHERE {embedding_col} <=> %s <= {threshold} ORDER BY {embedding_col} <=> %s Limit {n}", (embedding_array, embedding_array, embedding_array,))
        
        docs = cur.fetchall()
        cur.close()

        return docs

    def get_tourist_cont(self, location, month, year):
        """
        Retrieves the visitor count for a specific location, month, and year from the 'tourist_visits' table.
        """
        conn = self.connect_db(settings.POSTGRE_CONNECTION_STR)
        cursor = conn.cursor()
        query = """
            SELECT location, visitor_count 
            FROM tourist_visits
            WHERE location = %s AND month = %s AND year = %s;
            """
        print(f"Paremeters: {location}, {month}, {year}")
        
        cursor.execute(query, (location, month, year))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if results:
            location, visitor_count = results[0]
            month = MONTHS.get(int(month))
            narrative = f"Jumlah turis dari {location} pada bulan {month} tahun {year} adalah {visitor_count} orang."
        else:
            narrative = f"Tidak ada data turis untuk lokasi {location} pada bulan {month} tahun {year}."

        return narrative

    def get_monthly_trend(self, location, year):
        """
        Retrieves the monthly visitor count trend for a specific location and year from the 'tourist_visits' table.

        """
        conn = self.connect_db(settings.POSTGRE_CONNECTION_STR)
        cursor = conn.cursor()
        query = """
            SELECT month, visitor_count 
            FROM tourist_visits
            WHERE location = %s AND year = %s
            ORDER BY month;
            """

        print(f"Paremeters: {location}, {year}")

        cursor.execute(query, (location, year))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if results:
            narrative = f"Tren jumlah pengunjung bulanan untuk {location} pada tahun {year} adalah sebagai berikut:\n"
            for month, visitor_count in results:
                month = MONTHS.get(int(month))
                narrative += f"- Bulan {month}: {visitor_count} orang\n"
        else:
            narrative = f"Tidak ada data pengunjung untuk lokasi {location} pada tahun {year}."

        return narrative

    def get_top_locations(self, year, limit=5, ascending="DESC"):
        """
        Retrieves the top locations with the highest visitor count for a specific year from the 'tourist_visits' table.
        """
        conn = self.connect_db(settings.POSTGRE_CONNECTION_STR)
        cursor = conn.cursor()
        query = f"""
            SELECT location, SUM(visitor_count) as total_visitor_count
            FROM tourist_visits
            WHERE year = {year}
            GROUP BY location
            ORDER BY total_visitor_count {ascending}
            LIMIT {limit};
            """
        
        print(f"Paremeters: {year} {ascending}")

        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if results:
            ascending_word = ORDERS.get(ascending)
            narrative = f"Top {limit} lokasi dengan jumlah pengunjung {ascending_word} pada tahun {year} adalah sebagai berikut:\n"
            for i, (location, total_visitor_count) in enumerate(results, start=1):
                narrative += f"{i}. {location}: {total_visitor_count} orang\n"
        else:
            narrative = f"Tidak ada data pengunjung untuk tahun {year}."

        return narrative

