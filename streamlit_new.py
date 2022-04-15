from inspect import signature
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import base64
import json
import os
import hashlib
import sqlite3 
from itertools import groupby
import datetime





################# STREAMLIT ####################

base_url = 'http://127.0.0.1:8005/weatherviz/'
login_url = 'http://127.0.0.1:8005/users/login'
sign_up_url = 'http://127.0.0.1:8005/users/signup'
users_url = 'http://127.0.0.1:8005/users'

API_URL = "https://7876vqgufg.execute-api.us-east-1.amazonaws.com/dev/ner"

API_URL_SUMMARY = "https://k9kaiop1ll.execute-api.us-east-1.amazonaws.com/dev/summary"

def query(payload):
    response = requests.post(API_URL, json=payload) #headers=headers
    return response.json()

def summary_query(payload):
    response = requests.post(API_URL_SUMMARY, json=payload) #headers=headers
    print(response.json())
    return response.json()




# def query(payload):
# 	response = requests.post(API_URL, json=payload) #headers=headers
# 	return response.json()




    
NOWCAST_HTML_TEMPLATE = """
<div style="width:100%;height:100%;margin:1px;padding:5px;position:relative;border-radius:5px;border-bottom-right-radius: 10px;
box-shadow:0 0 1px 1px #eee; background-color: #31333F;
  border-left: 5px solid #6c6c6c;color:white;">
<h4>{}</h4>
<h4>{}</h4>
<h5>{}</h5>
<h6>{}</h6>
</div>
"""

NOWCAST_DES_HTML_TEMPLATE = """
<div style='color:#fff'>
{}
</div>
"""

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
# conn = sqlite3.connect('data.db')
# c = conn.cursor()
# DB  Functions


# def create dataframe():
#     df = pd.dataframe()
cols = ['Username', 'Password', 'Count', 'Timestamp']
lst = []
def add_userdata(username,password,count,time):
    lst.append([username,password,count,time])
    path = 'new.csv'

    # Check whether the specified path exists or not
    isExist = os.path.exists(path)

    if not isExist:
        df = pd.DataFrame(lst, columns = cols)
        df.to_csv("new.csv", index = False)
    else:
        df = pd.read_csv("new.csv")
        df = df.append(pd.DataFrame(lst, columns = cols), ignore_index=True)
        df.to_csv("new.csv", index = False)
    print(df)
    return df
    
# def add_userdata(username,password,count):
#     df = pd.dataframe(['username', 'password', count], columns = ['username', 'password', 'count'])
    
def login_user(username, password):
    a = pd.read_csv("new.csv")
    b = a.loc[(a['Username'] == username) & (a['Password'] == password)]
    print(b)
    c = b.to_numpy()
    return c

def view_all_users():
    a = pd.read_csv("new.csv")
    return a

def update_count(username):
    a = pd.read_csv("new.csv")
    cond = (a['Username'] == username)
    a.loc[cond,'Count'] = a['Count'] - 1
    a.to_csv("new.csv", index = False)
    
def read_count(username):
    a = pd.read_csv("new.csv")
    c =a.loc[a['Username'] == username, 'Count'].iloc[0]
    return c

def add_location(username,location):
    a = pd.read_csv("new.csv")
    userindex = a.index[a['Username']==username]
    a.loc[userindex, ["Location"]] = location
    a.to_csv("new.csv", index = False)
    
    
    
    
    
    
    
# def create_usertable():
# 	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT, count REAL)')


# def add_userdata(username,password,count):
# 	c.execute('INSERT INTO userstable(username,password,count) VALUES (?,?,?)',(username,password,count))
# 	conn.commit()

# def login_user(username,password):
# 	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
# 	data = c.fetchall()
# 	# print(data)
# 	return data

# def view_all_users():
# 	c.execute('SELECT * FROM userstable')
# 	data = c.fetchall()
# 	print(data)
# 	return data


# def update_count(username):
#     #c.execute('SELECT count FROM userstable WHERE username =? AND password = ?',(username,password))
#     c.execute('UPDATE userstable SET count = count - 1 WHERE username =?',(username,))
#     c.close()

    
    
# def return_count(username):
#     c.execute('SELECT * FROM userstable WHERE username =?', (username,))
#     data = c.fetchall()
#     #c.close()
#     print(data)
#     return data[0][2]






menu = ["Home","Login","Signup","Users","About"]
choice = st.sidebar.selectbox("Menu",menu)

# st.title("DevDeeds -Search Jobs")
st.title('Media Nowcasting System')
st.write("")
        

if choice == "Home":
    st.subheader("Home")

    # Nav  Search Form
#     with st.form(key='searchform'):
#         nav1,nav2,nav3 = st.columns([3,2,1])

#         with nav1:
#             location = st.text_input("Enter a Location")  
#         with nav2:
#             show_next_nearest = st.text_input("Show Next Nearest Location? (yes/no)")
#         with nav3:
#             enter_api_token = st.text_input("Enter API Token")
        
#         force_nowcast = st.checkbox("Force nowcast")
        
#         submit_search = st.form_submit_button(label='Go')
#             # clear = st.form_submit_button(label="Reset")

#     st.success("You searched for {} and need next nearest location : {}".format(location,show_next_nearest))



#     # Results
#     col1, col2 = st.columns([2,1])
#     images_path = '../images/'+location.strip().split(',')[0]+'/'
#     count = 0
#     with col1:
#         pics = {}
#         showWarningOnDirectExecution = False
#         if submit_search:
#             # count = count + 1
#             # print(count)
#             # if count <= 2:
#                 # Create Search Query
#             search_url = base_url+location+'?'+'next_nearest='+show_next_nearest
#             # st.write(search_url)
#             res = requests.get(search_url)
#             # print(search_url)
#             #print("RESPONSE", res)
#             #print(res.json())
#             # df = pd.read_csv('../data'+'/'+location.strip().split(',')[0]+'/'+location.strip().split(',')[0]+'_top_5_min_distances.csv')
#             # df1 = df[:1]
#             # print("NEWWWWWWWW")
#             # print(df1['distance'])
#             # if int(df1['distance']) >= 100:
#             #     for i in range(0, 12):
#             #         os.remove(data_model['images_path'] + "test" +  str(i) + '.png')
#             #     os.remove(data_model['images_path'] + "nowcast.gif")
#             #     os.remove(data_model['event_narrative_path'])
#             #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/filtered_data.h5')
#             #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/y_pred.h5')
#             #     st.header("No nearest (location found within 100 kms of your location")
#             # if show_next_nearest.lower() != "no" or show_next_nearest.lower() != "yes":
#             #     for i in range(0, 12):
#             #         os.remove(data_model['images_path'] + "test" +  str(i) + '.png')
#             #     os.remove(data_model['images_path'] + "nowcast.gif")
#             #     os.remove(data_model['event_narrative_path'])
#             #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/filtered_data.h5')
#             #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/y_pred.h5')
#             #     # st.header("No nearest (location found within 100 kms of your location")
#             #     st.header("Please enter yes or no")


#         # if clear:
#         #     for i in range(0, 12):
#         #         os.remove(data_model['images_path'] + "test" +  str(i) + '.png')
#         #     os.remove(data_model['images_path'] + "nowcast.gif")
#         #     os.remove(data_model['event_narrative_path'])
#         #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/filtered_data.h5')
#         #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/y_pred.h5')
#         # if submit_search and show_next_nearest.lower() == "no":
#         #     for i in range(0, 12):
#         #         os.remove(data_model['images_path'] + "test" +  str(i) + '.png')
#         #     os.remove(data_model['images_path'] + "nowcast.gif")
#         #     os.remove(data_model['event_narrative_path'])
#         #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/filtered_data.h5')
#         #     os.remove('/Users/priyankashinde/Desktop/neurips-2020-sevir-master/backend/y_pred.h5')
#         #     st.header("No nearest location found within 100 kms of your location")
#         # elif submit_search and show_next_nearest.lower() == "yes" and :






#             # image_path = data_model['images_path']+"test0.png"
#             # if os.path.exists(image_path):

#         for i in range(0, 12):
#             pics[i] = images_path + "test" +  str(i) + '.png'
#         if len(pics) == 0:
#             st.write("Enter params to get results!")

#         else:

#             pic = st.select_slider('Select a Picture', options=list(pics.keys()))
#             st.image(pics[pic], use_column_width=True)
#             # else:
#             #     st.write("You have exceeded the Max. API calls!")



#     with col2:
#         #         if submit_search:
# #             if count <= 2:
#         col2.subheader("Weather Nowcast - Next Hour")
#         data_url = ""
#         gif_path = images_path+'nowcast.gif'

#         if os.path.exists(gif_path):
#             file_ = open(images_path+ "nowcast.gif", "rb")
#             contents = file_.read()
#             data_url = base64.b64encode(contents).decode("utf-8")
#             file_.close()

#         st.markdown(
#             f'<img src="data:image/gif;base64,{data_url}" alt="nowcast gif">',
#             unsafe_allow_html=True,
        
            # else:
            #     st.write("Consider creating a new account!")

    
    # st.header("Event Narrative Nearby Locations")

    # event_narrative_path1 = data_model['event_narrative_path']
    # if os.path.exists(event_narrative_path1):

    #     event_narrative_data = pd.read_csv(event_narrative_path1)
    #     print(event_narrative_data.head(1))
    #     event_narrative_data = event_narrative_data.drop(columns=['Unnamed: 0'])

    #     nearby_locations_list = []
    #     nearby_narrative_list = []
    #     event_type = []
        
    #     for i in range(0, 4):
    #         nearby_locations_list.append(event_narrative_data['LOCATION'][i])
    #         event_type.append(event_narrative_data['EVENT_TYPE'][i])
    #         nearby_narrative_list.append(event_narrative_data['EVENT_NARRATIVE'][i])
            
    #         # nearby_locations_list.append(nearest_loc)
    #     # print("NEARBY LIST __",len(nearby_narrative_list))
    #     select = st.selectbox('STATE', nearby_locations_list)
        
    
    #     for i in range(0, 4):
    #         if select == nearby_locations_list[i]:
    #             st.header("Event Narrative")
    #             st.write(nearby_narrative_list[i])
    #             st.header("Event Type")
    #             st.write(event_type[i])

    #     df = event_narrative_data.filter(['LATITUDE','LONGITUDE','EVENT_TYPE', 'LOCATION', 'STATE'], axis=1)
    #     df = df.rename({'LATITUDE':'lat', 'LONGITUDE' : 'lon'},axis='columns')


    #     st.header("Geo Locations of Nearby Events")


    #     fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="LOCATION", hover_data=["STATE", "EVENT_TYPE"],
    #                             color_discrete_sequence=["fuchsia"], zoom=3, height=300)
    #     fig.update_layout(mapbox_style="open-street-map")
    #     fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    #     st.plotly_chart(fig)

elif choice == 'Signup':
    # st.subheader("Sign Up")
    st.subheader("Create New Account")
    new_user = st.text_input("Username")
    new_password = st.text_input("Password",type='password')

    if st.button("Signup"):
        #create_usertable()
        add_userdata(new_user,make_hashes(new_password), 10, datetime.datetime.now())
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")



    # Nav  Search Form
#     with st.form(key='signupform'):
#         nav1,nav2,nav3,nav4 = st.columns([4,3,2,1])

#         with nav1:
#             fullname = st.text_input("Enter Full Name")
            
#         with nav2:
#             email = st.text_input("Enter Email")
#         with nav3:
#             password = st.text_input("Enter Password")

#         with nav4:
#             submit_signup = st.form_submit_button(label='Sign Up')
#             # clear = st.form_submit_button(label="Reset")

#     st.success("You Signed up as {}".format(fullname))

    # col1 = st.columns([1])

    # with col1:
        # pics = {}
        # showWarningOnDirectExecution = False
    # user = {
    #         "fullname": fullname,
    #         "email": email,
    #         "password": password
    #     }
    # if submit_signup:
    #     # Create Search Query
    #     data = {'fullname':  [fullname],
    #             'email': [email],
    #             'api_count': [2]
    #     }

    #     df = pd.DataFrame(data, columns = ['fullname', 'email', 'api_count'])
    #     df.to_csv('../data/sevir_users.csv')
    #     r = requests.post(url = sign_up_url, json = user)
    #     token = r.json()
    #     print(token)
    #     st.write("Here is your token  {} ".format(token['access token']))
    
        
elif choice == 'Login':
    st.subheader("Login")
    
#     if 'count' not in st.session_state:
#         st.session_state.count = 0

#     # def increment_counter():
#     #     st.session_state.count += 1
        
#     def update_counter(val):
#         st.session_state.count += val #st.session_state.increment_value

    username = st.sidebar.text_input("User Name")
    password = st.sidebar.text_input("Password",type='password')
    #count = 0
    if st.sidebar.checkbox("Login"):
        # if password == '12345':
        #create_usertable()
        hashed_pswd = make_hashes(password)
        result = login_user(username,check_hashes(password,hashed_pswd))
        
            
        if len(result):
            
            st.success("Logged In as {}".format(username))
            ctr = read_count(username)
            if ctr > 0:
                with st.form(key='searchform'):
                    nav1,nav2= st.columns([2,1])

                    with nav1:
                        location = st.text_input("Enter a Location")  
                    with nav2:
                        show_next_nearest = st.text_input("Show Next Nearest Location? (yes/no)")
                    # with nav3:
                    #     enter_api_token = st.text_input("Enter API Token")

                    force_nowcast = st.checkbox("Cache")
                    fresh_nowcast = st.checkbox("Fresh")

                    #submit_search1 = st.form_submit_button(label='')
                    #st.number_input('Enter a value', value=0, step=1, key='increment_value')
                    submit_search = st.form_submit_button(label='Go')#, on_click=update_counter(1))
                    #submit_search = st.form_submit_button(label='Cache')
                    
                #submit_search = st.button('Submit', on_click= increment_counter)
                    

                        # clear = st.form_submit_button(label="Reset")

                #st.success("You searched for {} and need next nearest location : {}".format(location,show_next_nearest))


                # Results
                col1, col2 = st.columns([2,1])
                images_path = '../images/'+location.strip().split(',')[0]+'/'
                event_narrative_path = '../data/'+location.strip().split(',')[0]+'/'+location.strip().split(',')[0]+'_top_5_min_distances.csv'
                
                if force_nowcast and submit_search:
                    update_count(username)
                    add_location(username,location)
                    with col1:
                        pics = {}
                        showWarningOnDirectExecution = False
                        col1.subheader("Weather Nowcast - Next Hour")
                        data_url = ""
                        gif_path = images_path+'nowcast.gif'

                        if os.path.exists(gif_path):
                            file_ = open(images_path+ "nowcast.gif", "rb")
                            contents = file_.read()
                            data_url = base64.b64encode(contents).decode("utf-8")
                            file_.close()

                        st.markdown(
                            f'<img src="data:image/gif;base64,{data_url}" alt="nowcast gif">',
                            unsafe_allow_html=True,
                        )
                        
                       
                    with col2:
                        
                        event_narrative_data = pd.read_csv(event_narrative_path)
                        event_narrative_data = event_narrative_data.drop(columns=['Unnamed: 0'])

                        df = event_narrative_data.filter(['LATITUDE','LONGITUDE','EVENT_TYPE', 'LOCATION', 'STATE'], axis=1)
                        df = df.rename({'LATITUDE':'lat', 'LONGITUDE' : 'lon'},axis='columns')
                        
                        col2.subheader("Geo Locations of Nearby Events")
                        fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="LOCATION", hover_data=["STATE", "EVENT_TYPE"],
                                                    color_discrete_sequence=["fuchsia"], zoom=3, width=410, height=350)
                        fig.update_layout(mapbox_style="open-street-map")
                        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                        st.plotly_chart(fig)
                        
                    st.subheader("Named Entity Recog and Summary for Event and Episode Narrative")

                    if os.path.exists(event_narrative_path):

                        event_narrative_data = pd.read_csv(event_narrative_path)
                        print(event_narrative_data.head(1))
                        event_narrative_data = event_narrative_data.drop(columns=['Unnamed: 0'])

                        nearby_locations_list = []
                        nearby_narrative_list = []
                        episode_narrative_list = []

                        for i in range(0, 1):
                            nearby_locations_list.append(event_narrative_data['LOCATION'][i])
                            episode_narrative_list.append(event_narrative_data['EPISODE_NARRATIVE'][i])
                            nearby_narrative_list.append(event_narrative_data['EVENT_NARRATIVE'][i])

                            # nearby_locations_list.append(nearest_loc)
                        # print("NEARBY LIST __",len(nearby_narrative_list))
                        a = nearby_locations_list[0]
                        st.subheader("Nearest Location")
                        st.write(a)
                        


                        # for i in range(0, 1):
                        #     if select == nearby_locations_list[i]:
                        st.subheader("Event Narrative")
                        st.write(nearby_narrative_list[0])
                        output = query({

                            "inputs": nearby_narrative_list,
                        })

                        dict1 = {}
                        # define a fuction for key
                        def key_func(k):
                            return k["entity"]

                        # sort INFO data by 'company' key.
                        INFO = sorted(output['answer'], key=key_func)
                        dict1={}  
                        for key, value in groupby(INFO, key_func):
                            # print(key)
                            # print([val for val in value])
                            dict1[key] = [val["word"] for val in value]

                        data = pd.DataFrame.from_dict(dict1, orient='index')
                        st.subheader("Named Entity Recog")
                        st.dataframe(data)
                        
                        
                        # st.subheader("Summary")
                        output1 = summary_query({

                            "inputs": nearby_narrative_list[0],
                        })
                        st.subheader("Summary")
                        st.write(output1['answer'])
                        
                        
                        st.subheader("Episode Narrative")
                        st.write(episode_narrative_list[0])
                                
                        # def query(payload):
                        #     response = requests.post(API_URL, json=payload) #headers=headers
                        #     return response.json()
                                
                        output = query({

                            "inputs": episode_narrative_list,
                        })

                        dict1 = {}
                        # define a fuction for key
                        def key_func(k):
                            return k["entity"]

                        # sort INFO data by 'company' key.
                        INFO = sorted(output['answer'], key=key_func)
                        dict1={}  
                        for key, value in groupby(INFO, key_func):
                            # print(key)
                            # print([val for val in value])
                            dict1[key] = [val["word"] for val in value]

                        data = pd.DataFrame.from_dict(dict1, orient='index')
                        st.subheader("Named Entity Recog")
                        st.dataframe(data)
                        
                        output1 = summary_query({

                            "inputs": episode_narrative_list[0],
                        })
                        st.subheader("Summary")
                        st.write(output1['answer'])
                            
                        # image = Image.open('key.png')

                        # if Analyze:
                        #     st.dataframe(data)
                        #     st.image(image, caption='bert NER key')
                        
                     
                elif fresh_nowcast and submit_search:
                    update_count(username)
                    with col1:
                        pics = {}
                        showWarningOnDirectExecution = False
                        #if force_nowcast and submit_search:
                            
                        search_url = base_url+location+'?'+'next_nearest='+show_next_nearest

                        res = requests.get(search_url)
                        
                        col1.subheader("Weather Nowcast - Next Hour")
                        data_url = ""
                        gif_path = images_path+'nowcast.gif'

                        if os.path.exists(gif_path):
                            file_ = open(images_path+ "nowcast.gif", "rb")
                            contents = file_.read()
                            data_url = base64.b64encode(contents).decode("utf-8")
                            file_.close()

                        st.markdown(
                            f'<img src="data:image/gif;base64,{data_url}" alt="nowcast gif">',
                            unsafe_allow_html=True,
                        )

                        
                       
                    with col2:
                        event_narrative_data = pd.read_csv(event_narrative_path)
                        event_narrative_data = event_narrative_data.drop(columns=['Unnamed: 0'])

                        df = event_narrative_data.filter(['LATITUDE','LONGITUDE','EVENT_TYPE', 'LOCATION', 'STATE'], axis=1)
                        df = df.rename({'LATITUDE':'lat', 'LONGITUDE' : 'lon'},axis='columns')
                        
                        col2.subheader("Geo Locations of Nearby Events")
                        fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="LOCATION", hover_data=["STATE", "EVENT_TYPE"],
                                                    color_discrete_sequence=["fuchsia"], zoom=3, width=410, height=350)
                        fig.update_layout(mapbox_style="open-street-map")
                        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                        st.plotly_chart(fig)
                        
                    st.subheader("Named Entity Recog for Event and Episode Narrative")

                    if os.path.exists(event_narrative_path):

                        event_narrative_data = pd.read_csv(event_narrative_path)
                        print(event_narrative_data.head(1))
                        event_narrative_data = event_narrative_data.drop(columns=['Unnamed: 0'])

                        nearby_locations_list = []
                        nearby_narrative_list = []
                        episode_narrative_list = []

                        for i in range(0, 1):
                            nearby_locations_list.append(event_narrative_data['LOCATION'][i])
                            episode_narrative_list.append(event_narrative_data['EPISODE_NARRATIVE'][i])
                            nearby_narrative_list.append(event_narrative_data['EVENT_NARRATIVE'][i])

                            # nearby_locations_list.append(nearest_loc)
                        # print("NEARBY LIST __",len(nearby_narrative_list))
                        a = nearby_locations_list[0]
                        st.subheader("Nearest Location")
                        st.write(a)
                        


                        # for i in range(0, 1):
                        #     if select == nearby_locations_list[i]:
                        st.subheader("Event Narrative")
                        st.write(nearby_narrative_list[0])
                        output = query({

                            "inputs": nearby_narrative_list,
                        })

                        dict1 = {}
                        # define a fuction for key
                        def key_func(k):
                            return k["entity"]

                        # sort INFO data by 'company' key.
                        INFO = sorted(output['answer'], key=key_func)
                        dict1={}  
                        for key, value in groupby(INFO, key_func):
                            # print(key)
                            # print([val for val in value])
                            dict1[key] = [val["word"] for val in value]

                        data = pd.DataFrame.from_dict(dict1, orient='index')
                        st.subheader("Named Entity Recog")
                        st.dataframe(data)
                        
                        output1 = summary_query({

                            "inputs": nearby_narrative_list[0],
                        })
                        st.subheader("Summary")
                        st.write(output1['answer'])
                        
                        
                        st.subheader("Episode Narrative")
                        st.write(episode_narrative_list[0])
                                
                        # def query(payload):
                        #     response = requests.post(API_URL, json=payload) #headers=headers
                        #     return response.json()
                                
                        output = query({

                            "inputs": episode_narrative_list,
                        })

                        dict1 = {}
                        # define a fuction for key
                        def key_func(k):
                            return k["entity"]

                        # sort INFO data by 'company' key.
                        INFO = sorted(output['answer'], key=key_func)
                        dict1={}  
                        for key, value in groupby(INFO, key_func):
                            # print(key)
                            # print([val for val in value])
                            dict1[key] = [val["word"] for val in value]

                        data = pd.DataFrame.from_dict(dict1, orient='index')
                        st.subheader("Named Entity Recog")
                        st.dataframe(data)
                        
                        output1 = summary_query({

                            "inputs": episode_narrative_list[0],
                        })
                        st.subheader("Summary")
                        st.write(output1['answer'])

                    
            else:
                st.warning("Limit crossed")
                


        else:
            st.warning("Incorrect Username/Password")

    # Nav  Search Form
    # with st.form(key='loginform'):
    #     nav1,nav2,nav3 = st.columns([3,2,1])

    #     with nav1:
    #         email = st.text_input("Enter Email")
    #     with nav2:
    #         password = st.text_input("Enter Password")

    #     with nav3:
    #         submit_login = st.form_submit_button(label='Login')
    #         # clear = st.form_submit_button(label="Reset")

    # st.success("You Logged in as {}".format(email))

    # # col1 = st.columns([1])

    # # with col1:
    #     # pics = {}
    #     # showWarningOnDirectExecution = False
    # user = {
    #         "email": email,
    #         "password": password
    #     }
    # if submit_login:
    #     # Create Search Query
    #     r = requests.post(url = login_url, json = user)
    #     token = r.json()
    #     st.write("Here is your token  {} ".format(token))
    
    

elif choice == 'Users':
    st.subheader("User Profiles")
    user_result = view_all_users()
    #clean_db = pd.DataFrame(user_result,columns=["Username","Token","count"])
    st.dataframe(user_result)

else:
    st.subheader("About")








