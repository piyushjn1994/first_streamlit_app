import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('Hello Everyone')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)
# Let's put a pick list here so they can pick the fruit they want to include
index = list(my_fruit_list)
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Display the table on the page.
streamlit.dataframe(my_fruit_list)

my_fruit_list = my_fruit_list.set_index('Fruit')
#streamlit.multiselect("Pick some fruits:", list(my_fruit_list.set_index),['Avocado','Apple'])


#New Section to import API fruitvice
#create function
def get_fruityvice_data (this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

#New Section to return API responses
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input("What fruit would you like information about?")
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
                                      
except URLError as e:
       streamlit.error()
                                      
#streamlit.write('The user entered ', fruit_choice)

streamlit.header("View Our Fruit List - Add Your Favorites!")
#Snowflake related function
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()

#Add a button to load fruit
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  my_cnx.close()
  streamlit.dataframe(my_data_rows)

#allow the end user to add another fruit to list
def insert_row_snowflake(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('"+ new_fruit + "')")
    return "Thanks for adding " + new_fruit

add_my_fruit = streamlit.text_input('Would you like to add another fruit?')
if streamlit.button('Add a fruit to the list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  back_from_function = insert_row_snowflake(add_my_fruit)
  streamlit.text(back_from_function)


