import sqlite3
import pandas as pd
import random
from typing import List, Tuple

class UserDB():

    connection = sqlite3.connect("users_db")
            
    def create_table_if_not_exists(self, table_name, persist_table=False):
        # drop table as default
        if not persist_table:
            self.connection.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.connection.execute(f"CREATE TABLE IF NOT EXISTS {table_name}(FirstName text, LastName text, Country text, Email text, Password text, UserID text)")
        self.connection.commit()
        
    def insert_into_table(self, signup: pd.DataFrame, table_name: str) -> None:
        """
        Assumes signup variable is a pandas series object i.e. JSON dictionary converted to dataframe
        Pandas dataframe has shape(5,) with indices 'firstname', 'lastname', 'country', 'email', 'password'
        """
        # create a UserID, and then hash it for uniqueness
        user_randint = random.randint(0,1000)
        userid = signup["firstname"] + signup["lastname"] + str(user_randint)
        userid = str(hash(userid))
        input = signup.to_list()
        input.append(userid)
        # Insert user
        self.connection.execute(f"INSERT INTO {table_name} VALUES (?,?,?,?,?,?)", tuple(input))
        self.connection.commit()
        
    def select_all_from_table(self, table_name) -> List[Tuple]:
        # output of table with sample SELECT statement
        cursor = self.connection.execute(f"SELECT * FROM {table_name};")
        result = cursor.fetchall()
        print(result)
        return result
    
    
if __name__ == "__main__":
    sample_user = pd.Series({'firstname': 'Hans', 'lastname': 'Keller', 
                                'country': 'Germany', 'email': 'hans.keller@aol.com', 
                                'password': 'dfO24*%@xN!'})
    db = UserDB()
    db.create_table_if_not_exists("users")
    db.insert_into_table(sample_user, "users")
    db.select_all_from_table("users")
       





