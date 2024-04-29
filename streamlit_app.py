import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

def get_database(username):
    if not firebase_admin._apps:
        # Initialize Firebase Admin SDK with service account credentials
        cred = credentials.Certificate("database/allwheelchair-firebase-adminsdk-rjisr-e43646aa27.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://allwheelchair-default-rtdb.asia-southeast1.firebasedatabase.app/'
        })

    # Get a reference to the Firebase Realtime Database
    ref = db.reference('/')

    data = ref.child("users/%s" % username).get()

    return data

def stream(data):
    st.write("Hello World")
    # st.write(data)
    for json in data:
        st.write(json)
        st.dataframe(data[json])

if __name__ == '__main__':
    data = get_database("Ton")
    stream(data)
