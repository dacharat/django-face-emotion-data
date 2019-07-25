import psycopg2
from psycopg2.extras import Json, DictCursor
import json

class Database:
  def __init__(self):
    self.conn = psycopg2.connect(
        host='my_postgres',
        port=5432,
        dbname='my_face_data',
        user='postgres',
    )
    self.cur = self.conn.cursor()
    self.TABLENAME = "test_person"

  # create new database
  def create_database(self):
    self.cur.execute("CREATE DATABASE my_face_data;")
    self.conn.commit()

  # create table
  def create_table(self):
    self.cur.execute(
        "CREATE TABLE IF NOT EXISTS {} (id serial PRIMARY KEY, face varchar, emotion_detail text[], face_image text[], face_encoding text[]);".format(self.TABLENAME))
    self.conn.commit()

  # insert new row to database
  def insert(self, face="Jack", emotion_detail=[{"timestamp": "timestamp", "emotion": ["A"]}], image=[], face_encoding=[]):
    self.cur.execute("INSERT INTO {} (face, emotion_detail, face_image, face_encoding) VALUES (%s, %s, %s, %s);".format(
        self.TABLENAME), [face, [Json(i) for i in emotion_detail], image, face_encoding])
    self.conn.commit()

  # show all rows in database
  def show_data(self):
    self.cur.execute("SELECT * FROM {};".format(self.TABLENAME))
    result = self.cur.fetchall()
    print(result)

  # update emotion_detail in database with exist face
  def update(self, face="Jack", new_data=[{"timestamp": "timestamp", "emotion": ["B"]}]):
    self.cur.execute(
        "SELECT emotion_detail FROM {} WHERE face=%s;".format(self.TABLENAME), [face])
    old_data_string_form = self.cur.fetchall()[0][0]
    old_data_json = [json.loads(i) for i in old_data_string_form]
    new_data = old_data_json + new_data
    self.cur.execute("UPDATE {} SET emotion_detail = ARRAY[{}] WHERE face=%s".format(
        self.TABLENAME, ",".join('%s' for x in new_data)), [Json(x) for x in new_data] + [face])
    self.conn.commit()

  # get all rows in face column
  def get_all_face(self):
    self.cur.execute("SELECT face FROM {};".format(self.TABLENAME))
    return [row[0] for row in self.cur.fetchall()]

  # get all rows in emotion_detail column
  def get_emotion_detail(self, face="Jack"):
    self.cur.execute(
        "SELECT emotion_detail FROM {} WHERE face=%s;".format(self.TABLENAME), [face])
    result = [row[0] for row in self.cur.fetchall()][0]
    return [json.loads(i) for i in result]

  # delete row from face
  def delete_row_from_name(self, face):
    self.cur.execute(
        "DELETE FROM {} WHERE face=%s;".format(self.TABLENAME), [face])
    self.conn.commit()

  # delete table
  def drop_database(self):
    self.cur.execute("DROP TABLE {};".format(self.TABLENAME))
    self.conn.commit()

  # check if table is exists or not
  def check_table_exists(self):
    self.cur.execute(
        "SELECT * FROM information_schema.tables WHERE table_name=%s;", [self.TABLENAME])
    return bool(self.cur.rowcount)

  # check database is exists or not
  def check_database_exists(self):
    self.cur.execute("SELECT 1 FROM pg_database WHERE datname='my_face_data';")
    return bool(self.cur.rowcount)

  # get number of rows in database
  def get_number_of_rows(self):
    self.cur.execute("SELECT COUNT(*) FROM {};".format(self.TABLENAME))
    return self.cur.fetchone()[0]

  def get_face_encoding(self):
    self.cur.execute(
        "SELECT face, face_encoding FROM {};".format(self.TABLENAME))
    return self.cur.fetchall()

  def change_face_name(self, face, newFaceName):
    self.cur.execute("UPDATE {} SET face=%s WHERE face=%s".format(
        self.TABLENAME), [newFaceName,face])
    self.conn.commit()

  # close cur and conn
  def close(self):
    self.cur.close()
    self.conn.close()
