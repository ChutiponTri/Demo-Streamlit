import pyrebase
import pandas as pd
import numpy as np
import sqlite3

class FireBase():
    def __init__(self):
        config = {
            "apiKey": "AIzaSyAQFqRqACcmD6rrGZh1I-JYaKBvSy5uMII",
            "authDomain": "allwheelchair.firebaseapp.com",
            "databaseURL": "https://allwheelchair-default-rtdb.asia-southeast1.firebasedatabase.app",
            "projectId": "allwheelchair",
            "storageBucket": "allwheelchair.appspot.com",
            "messagingSenderId": "670260110809",
            "appId": "1:670260110809:web:98e13b334d2149eff065c8",
            'measurementId': "G-575094V1EF"
        }
        firebase = pyrebase.initialize_app(config)

            
        # Get a reference to the Firebase Realtime Database
        self.ref = firebase.database()

    # Function To Get Database From Firebase
    def get_database(self, path):

        data = self.ref.child("%s" % (path)).get()

        return data.val()
    
    # Function To Get Index of Firebase
    def get_latest(self, path):
        # data = ref.child(path).order_by_key().limit_to_last(1).get()
        data = self.ref.child(path).get()
        if data:
            return len(data)
        else:
            return 0
    
    # Function To Update Data To Firebase
    def update_one(self, path, dict, data):
        index = self.get_latest("%s/%s" % (path, dict[0]))
        for i in range(len(dict)):
            self.ref.child("%s/%s" % (path, dict[i])).update({index:data[i]})    
    
    # Function To Update Table To Firebase
    def update_table(self, path, username, tablename, df:pd.DataFrame):
        df_ready = self.preprocess_df(df)
        if len(df_ready.index) < 8000:
            self.ref.child("%s/%s" % (path, username)).update({str(tablename):df_ready.to_dict(orient="list")})
            print(df_ready)
        else:
            # file = "data_2024I03I06_11I12I46"
            # raw = self.get_raw_data("Pang_data", file)
            # print(type(raw))
            # raw = firebase.preprocess_df(raw)
            col = df_ready.columns.tolist()
            for col_name in col:
                self.ref.child("users/%s/%s" % (username, tablename)).update({col_name:df_ready[col_name].tolist()})
                print("ok")

        # Split data into smaller chunks
        # chunk_size = 1000  # Adjust the chunk size as needed
        # chunks = [df_ready[i:i+chunk_size] for i in range(0, len(df_ready), chunk_size)]
        
        # for chunk in chunks:
        #     self.ref.child("%s/%s" % (path, name)).update({str(data): chunk.to_dict(orient="list")})

    # Function To Preprocess Dataframe
    def preprocess_df(self, df):
        try:
            df.replace([np.nan, np.inf, -np.inf], "NA", inplace=True)
            df = df.astype(str).map(lambda x: x[:9] if len(str(x)) > 11 else x)
        except Exception as e:
            print(e)
        return df

    # Function To Update Temporary Data To Firebase
    def update_later(self, path, name, data, df):
        name_list = self.get_table_names(name)
        for i in range(len(name_list)):
            self.ref.child(path).child(name).update({name_list[i]:data[i]})

    # Function To Get SQL Table Names
    def get_table_names(self, file):
        # Connect to database
        conn = sqlite3.connect('database/%s.db' % file)

        # Create Cursor
        c = conn.cursor()

        # Insert
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        data = c.fetchall()
        data = [x[0] for x in data]

        # Commit the command
        conn.commit()

        # Close the connection
        conn.close()

        return data

    # Function To Get Raw Data From Database
    def get_raw_data(self, path, table_name):
        # Connect to database
        conn = sqlite3.connect('database/%s.db' % path)

        # Create Cursor
        c = conn.cursor()

        # Query
        query = "SELECT * FROM %s" % table_name
        data = pd.read_sql(query, conn)

        # Commit the command
        conn.commit()

        # Close the connection
        conn.close()   

        return data
    
    # Function To Get Column names
    def get_col_names(self, file, table_name):
        # Connect to database
        conn = sqlite3.connect('database/%s.db' % file)

        # Create Cursor
        c = conn.cursor()

        # Insert
        query = "PRAGMA table_info(%s)" % table_name
        c.execute(query)
        data = c.fetchall()

        # Commit the command
        conn.commit()

        # Close the connection
        conn.close()

        return data
    
    # Function To Get Highest Score
    def get_highest_score(self, username, game, df):
        return df[(df['Username'] == username) & (df['Game'] == game)]['Score'].max()
    
if __name__ == '__main__':
    firebase = FireBase()

    # firebase.ref.child("storage").delete()

    # Update One
    # firebase.update_one("test",["Username", "Game", "Score", "Start", "Finish", "Accuracy"],["Ton", "Alien", "10", "5", "2", "Great"])
    
    # Update Table
    # user = "ํPang"
    # table = firebase.get_table_names(user + "_data")
    # for name in table:
    #     if name != "overview":
    #         raw = firebase.get_raw_data(user + "_data", name)
    #         print(raw)
    #         try:
    #             firebase.update_table("users", user, name, raw)
    #         except:
    #             pass

    # Update Login
    # table = firebase.get_table_names("login")
    # for name in table:
    #     raw = firebase.get_raw_data("login", name)
    #     firebase.ref.update({"current":raw.to_dict("list")})

    # Update Score (ranking / storage)
    # table = firebase.get_table_names("score")
    # raw = firebase.get_raw_data("score", "storage")
    # firebase.ref.update({"storage": raw.to_dict("list")})
    table = "data_2024I03I06_20I14I30"
    user = "Pang"
    col = firebase.get_col_names(user + "_data", table)
    for _,i,_,_,_,_ in col:
        print("OK")
        firebase.ref.child("users/Pang/%s/%s" % (table, i)).delete()
    # firebase.ref.child("users/Pang/%s" % (table)).delete()






