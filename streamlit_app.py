import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
import requests
from demo_stream_text import text, page_background
from demo_database_onfire import FireBase

score_order = ["Username", "Game", "Score", "Start", "Finish", "Accuracy"]
overview_order = ["Timestamp", "TimeUsage", "Rotate1", "Dist1", "MeanVel1", "MaxVel1", "Power1", "Rotate2", "Dist2", "MeanVel2", "MaxVel2", "Power2", "AvgHR", "MaxHR", "Calorie", "Zone"]
raw_data_order = ["Start Time", "Stop Time", "Accel X1", "Accel Y1", "Accel Z1", "Gyro X1", "Gyro Y1", "Gyro Z1",
                  "Accel X2", "Accel Y2", "Accel Z2", "Gyro X2", "Gyro Y2", "Gyro Z2", "Heart Rate"]
tabs = ["Game Ranking", "Recent Score", "Overview Data", "Motion Analysis", "Sign in History"]
game = ["Please Select The Game", "AlienInvasion", "BouncingBall", "LuckyBird"]
view = ["Raw Data", "Graph View"]
accel_x = ["Accel X1", "Accel X2"]
accel_y = ["Accel Y1", "Accel Y2"]
accel_z = ["Accel Z1", "Accel Z2"]
gyro_x = ["Gyro X1", "Gyro X2"]
gyro_y = ["Gyro Y1", "Gyro Y2"]
gyro_z = ["Gyro Z1", "Gyro Z2"]
color = ["#0F52BA", "#FF0800"]

class Stream():
    def __init__(self):
        # Initialize Firebase
        self.firebase = FireBase()

        # Initialize Config
        st.set_page_config(page_title="ALL Wheelchair", page_icon="♿")

        # initialize database
        # self.data = Database()
        # account = self.data.check_current_user()
        
        # Check if User is logged in
        # if account[2] != "login":
        #     self.login()
        # else:

        # Create Current Username Label
        self.user_list = list(self.firebase.get_database("customers/Username"))
        self.user = st.selectbox("Users", self.user_list)
        self.path = "database/%s_data.db" % self.user
        st.markdown(f"<h3 style='text-align:right; font-size:24px'>User : {self.user}</h3>", unsafe_allow_html=True)
        self.logout()

        # Create Sidebar 
        self.sidebar()

        # Initialize Database File
        try:
            table_names = "users/%s" % self.user
            self.sheetname_list = list(self.firebase.get_database(table_names).keys())
            self.sheetname_list.insert(0, "Please Select Data")
        except:
            self.sheetname_list = ["Please Select Data"]
        try:
            self.sheetname_list.remove("overview")
        except:
            pass

        # Initialize Tab Widget
        self.game, self.score, self.overview, self.motion, self.record = st.tabs(tabs)

        # Function To Create Tabs
        self.tab1_ui()
        self.tab2_ui()
        self.tab3_ui()
        self.tab4_ui()
        self.tab5_ui()

    def sidebar(self):
        with st.sidebar:
            # Create Select Box
            self.side_select = st.selectbox("Game Selection", options=game, key="GameSelection")
            
            # Create Toggle
            if st.toggle("Background", value=False):
                st.markdown(page_background, unsafe_allow_html=True)

            # Create Chat
            messages = st.container(height=200)
            if prompt := st.button("Share My Score"):
                token = "TtK9sTE06I8itQbl75gFdcwjdYertYmIbQEhTr7V0Mg"
                # token = "chh83xOVBvxqA4IVaFuYQKgYwdWAQanTMBU4WAyf6rC"
                url = "https://notify-api.line.me/api/notify"
                header = {"content-type": "application/x-www-form-urlencoded", "Authorization": "Bearer " + token}
                img = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/900px-Cat03.jpg"
                score = self.data.get_ranking_personal(self.user, self.side_select)
                data = {"message": "%s got highest score of %s %s" % (self.user, self.side_select, score)}

                if self.side_select != "Please Select The Game" and score != None:
                    messages.chat_message("user").write(data["message"])
                    messages.chat_message("assistant").write(f"Message Successfully Sent")
                    session = requests.Session()
                    session.post(url, headers=header, data=data)
                
                elif self.side_select == "Please Select The Game":
                    messages.chat_message("user").write("My Game")
                    messages.chat_message("assistant").write(f"Please Select The Game")

                elif score == None:
                    messages.chat_message("user").write("My Ranking")
                    messages.chat_message("assistant").write(f"Your Ranking Not Exist")
                

    # Function to Create Tab1 UI
    def tab1_ui(self):
        with self.game:
            # Set up Game Selection layout
            if self.side_select != "Please Select The Game":
                st.header(f":rainbow[{self.side_select}]")
                st.subheader(f"Top 5 Scores of {self.side_select} are :", divider="rainbow")
                ranking = self.firebase.get_database("ranking")
                if len(ranking) != 0:
                    df = pd.DataFrame(ranking)[score_order]
                    df['Score'] = pd.to_numeric(df["Score"], errors="coerce")
                    top_5_scores = df.groupby('Game').apply(self.firebase.get_top_5).loc[self.side_select]
                    game = top_5_scores.reset_index(drop=True)
                    game.index += 1
                    st.dataframe(game, width=800)
                else:
                    st.write("## No Data")
            
            # Set up Introduction layout
            else:
                st.header("ALL :blue[Wheelchair]:wheelchair:", divider="rainbow")
                st.video("video/tun.mp4", start_time=0)
                st.write(text)

    # Function to Create Tab2 UI
    def tab2_ui(self):
        with self.score:
            score = self.firebase.get_database("storage")
            score_df = pd.DataFrame(score)[score_order]   
            score_df = score_df[score_df['Username'] == self.user]     
            score_df["Score"] = pd.to_numeric(score_df["Score"], errors="coerce")

            if self.side_select == "Please Select The Game":
                # Header
                st.header("Recent Score Records:balloon:", divider="rainbow")

                # Create Score Table
                if len(score) != 0:
                    # Skip Username Column
                    # score = [(tup[1:]) for tup in score]            
                    # columns = ["Game", "Score", "Start Time", "Finish Time", "Accuracy"]    
                    st.dataframe(score_df, width=800, hide_index=True)
                    average = np.mean(score_df["Score"])
                    st.write(f"Average Score is {average:.2f}")
                else:
                    st.write("## No Data")

            else:
                # Get Emoji
                if self.side_select == "AlienInvasion":
                    emoji = "rocket"
                elif self.side_select == "BouncingBall":
                    emoji = "basketball"
                elif self.side_select == "LuckyBird":
                    emoji = "bird"
                
                # Header
                st.header(f"{self.side_select} Score Records:{emoji}:", divider="rainbow")

                # Create Score Table
                if len(score) != 0:
                    # Skip Username Column
                    game = score_df[score_df['Game'] == self.side_select]
                    st.dataframe(game, width=800, hide_index=True)

                    # Calculate Average Score
                    average = np.mean(game["Score"])
                    st.write(f"Average Score is {average:.2f}")
                else:
                    st.write("## No Data")

    # Function to Create Tab3 UI
    def tab3_ui(self):
        with self.overview:
            # Header
            st.header("Overview Data", divider="rainbow")

            # Get The Overview Data
            try:
                overview_path = "users/%s/overview" % self.user
                overview = self.firebase.get_database(overview_path)
                if len(overview) != 0:
                    # Create DataFrame
                    df = pd.DataFrame(overview)
                    df = df[overview_order]
                    st.dataframe(df, width=800, hide_index=True)
            except:
                st.write("## No Data")

    # Function to Create Tab4 UI
    def tab4_ui(self):
        with self.motion:
            # Header
            st.header("Motion Data 📈", divider="rainbow")

            # Create Column For Data Selection  
            col1, col2 =  st.columns(2)

            # Create Select Box
            choice = col1.selectbox("Please Select View Mode", options=view)
            datasheet = col2.selectbox("Please Select Datasheet", options=self.sheetname_list)

            if datasheet != "Please Select Data":
                # Load Data From Database
                raw_data_path = "users/%s/%s" % (self.user, datasheet)
                data = self.firebase.get_database(raw_data_path)
                df = pd.DataFrame(data)
                df = df[raw_data_order]
                # Create View Mode Condition
                if choice == "Graph View":
                    for column in df.columns:
                        df[column] = pd.to_numeric(df[column], errors="coerce")

                    # Initialize Plot Style
                    plt.style.use("https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle")

                    # Create Accel X Plot
                    st.write("## Accel X")
                    fig1 = plt.figure()
                    plt.plot(df[accel_x], label=accel_x)
                    plt.legend(loc="upper right")
                    plt.xlabel("Data")
                    plt.ylabel("Accel X")
                    st.write(fig1)

                    # Create Accel Y Plot
                    st.write("## Accel Y")
                    fig2 = plt.figure()
                    plt.plot(df[accel_y], label=accel_y)
                    plt.legend(loc="upper right")
                    plt.xlabel("Data")
                    plt.ylabel("Accel Y")
                    st.write(fig2)

                    try:
                        if len(df[accel_z]) > 1:
                            # Create Accel Z Plot
                            st.write("## Accel Z")
                            fig3 = plt.figure()
                            plt.plot(df[accel_z], label=accel_z)
                            plt.legend(loc="upper right")
                            plt.xlabel("Data")
                            plt.ylabel("Accel Z")
                            st.write(fig3)

                            # Create Gyro X Plot
                            st.write("## Gyro X")
                            fig4 = plt.figure()
                            plt.plot(df[gyro_x], label=gyro_y)
                            plt.legend(loc="upper right")
                            plt.xlabel("Data")
                            plt.ylabel("Gyro X")
                            st.write(fig4)

                            # Create Gyro Y Plot
                            st.write("## Gyro Y")
                            fig5 = plt.figure()
                            plt.plot(df[gyro_y], label=gyro_y)
                            plt.legend(loc="upper right")
                            plt.xlabel("Data")
                            plt.ylabel("Gyro Y")
                            st.write(fig5)
                    except:
                        pass

                    # Create Gyro Z Plot
                    st.write("## Gyro Z")
                    fig6 = plt.figure()
                    plt.plot(df[gyro_z], label=gyro_z)
                    plt.legend(loc="upper right")
                    plt.xlabel("Data")
                    plt.ylabel("Gyro Z")
                    st.write(fig6)

                elif choice == "Raw Data":
                    # Create SQL DataFrame
                    df.index += 1
                    st.write("## Raw Data")
                    st.write(f"{len(df)} Data Points")
                    st.dataframe(df, height=800)
    
    # Function to Create Tab5 UI
    def tab5_ui(self):
        with self.record:
            # Header
            st.header("Sign in History", divider="rainbow")

            # Create Record DataFrame 
            record = self.firebase.get_database("current")
            columns = ["Username", "Timestamp", "Status"]
            record_df = pd.DataFrame(record)[columns]
            record_df = record_df[record_df['Username'] == self.user]
            record_df = record_df.reset_index(drop=True)
            record_df.index += 1
            if len(record_df) != 0:
                st.dataframe(record_df, width=800)
            else:
                st.write("## No Data")
    
    # Function To Create Login Page
    # def login(self):
    #     # Header
    #     st.header("ALL :blue[Wheelchair]:wheelchair:", divider="rainbow")
    #     col1, col2, col3 = st.columns([0.2, 0.6, 0.2])
    #     col2.image("icons/Logo.png", use_column_width="always")
    #     with st.form("Form"):
    #         # Create Username, Password Inputs
    #         username = st.text_input("Please Enter Username", placeholder="Please Enter Username")
    #         password = st.text_input("Please Enter Password", placeholder="Please Enter Password", type="password")

    #         # Create Form Submit Button
    #         if st.form_submit_button("Submit"):
    #             if (username == "" or password == ""):
    #                 st.warning("Please Enter Username and Password 😵")
    #                 st.toast("Please Enter Username and Password", icon='🥺')
    #             else:
    #                 if self.data.username_password_lookup(username, password):
    #                     self.data.create_current_user()
    #                     self.data.current_user(username)
    #                     st.success("Found Accout %s 👌🏼" % username)
    #                     st.toast("Log in Successfully !", icon='✅')
    #                     pyautogui.press("F5")
    #                 else:
    #                     st.warning("Invalid Username or Password 🥶")
    #                     st.toast("Invalid Username or Password", icon='😰')

    # Function To Create Logout Button
    def logout(self):
        col1, col2 = st.columns([0.87, 0.13])
        
        button = col2.button("Logout")
        # if button:
        #     self.data.del_current_user(self.user)
        #     st.rerun()

if __name__ == '__main__':
    stream = Stream()
