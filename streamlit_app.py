# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw:  Example Streamlit App :cup_with_straw:")
st.write("choose the fruits that you want in your custom smoothie ")

name_on_order = st.text_input('Name on smoothie :')
st.write('The name on your smoothie wiil be : ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col('Fruit_name'))
#st.dataframe(data= my_dataframe ,use_container_width=True)



ingredients_list = st.multiselect(
    'choose up to 5 ingredients :',
    my_dataframe ,
    max_selections =5
)

if ingredients_list:   
     st.write(ingredients_list)
     st.text(ingredients_list)

     ingredients_string =''

     for fruit_chosen in ingredients_list:
         ingredients_string  += fruit_chosen + ' '
         fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
         fv_df = st.dataframe(data = fruityvice_response.json(),use_container_width = True)

     st.write(ingredients_string)


     my_insert_stmt = """ insert into smoothies.public.orders(ingredients ,name_on_order)
            values ('""" + ingredients_string + """' , '""" + name_on_order + """'  )"""


     #st.write(my_insert_stmt)
     time_to_insert = st.button("submit order")

     if time_to_insert:
      session.sql(my_insert_stmt).collect()
      st.success('Your Smoothie is ordered! {}'.format(name_on_order) , icon="✅")




