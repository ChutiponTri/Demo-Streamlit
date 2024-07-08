import firebase_admin
from firebase_admin import credentials, db

class FireBase():
    def __init__(self):
        if not firebase_admin._apps:
            # Initialize Firebase Admin SDK with service account credentials
            self.cred = credentials.Certificate("database/allwheelchair.json")
            firebase_admin.initialize_app(self.cred, {
                'databaseURL': 'https://allwheelchair-default-rtdb.asia-southeast1.firebasedatabase.app/'
            })
            
        # Get a reference to the Firebase Realtime Database
        self.ref = db.reference('/')

    def get_database(self, path):

        data = self.ref.child("%s" % (path)).get()

        return data
    
    def get_top_5(self, group):
        return group.sort_values(by='Score', ascending=False).head(5)

    def get_highest_score(self, username, game, df):
        return df[(df['Username'] == username) & (df['Game'] == game)]['Score'].max()

if __name__ == '__main__':
    database = FireBase()
 


    
