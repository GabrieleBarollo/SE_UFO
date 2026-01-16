from database.DB_connect import DBConnect
from model.state import State


class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_years():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT(YEAR(s_datetime)) AS anno
                    FROM sighting
                    WHERE YEAR(s_datetime) >= 1910 AND YEAR(s_datetime) <= 2014"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_shapes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT DISTINCT(shape) AS forma
                        FROM sighting"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["forma"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_states():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id, name, lat, lng 
                    FROM state"""

        cursor.execute(query)

        for row in cursor:
            result.append(State(row["id"], row["name"], row["lat"], row["lng"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_edges(anno, shape):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select n.state1, n.state2, z1.numero_avvistamenti as nn1, z2.numero_avvistamenti as nn2
                    from neighbor n,(select st.id as id_stato, st.name as nome_stato, COUNT(*) as numero_avvistamenti
				                    from state st, sighting si
				                    where st.id = si.state and YEAR(si.s_datetime) = %s and si.shape = %s
				                    group by st.id, st.name) as z1,
				                    (select st.id as id_stato, st.name as nome_stato, COUNT(*) as numero_avvistamenti
				                    from state st, sighting si
				                    where st.id = si.state and YEAR(si.s_datetime) = %s and si.shape = %s
				                    group by st.id, st.name) as z2
                    where n.state1 = z1.id_stato and n.state2 = z2.id_stato """

        cursor.execute(query,(anno, shape, anno, shape,))

        for row in cursor:
            result.append([row["state1"], row["state2"], row["nn1"]+row["nn2"]])

        cursor.close()
        conn.close()
        return result

