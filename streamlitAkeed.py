import streamlit as st
import pandas as pd
import pickle
import numpy as np
import datetime


# Load the trained model
model_save_path = "vendorsxgb.pkl"
with open(model_save_path, 'rb') as file:
    loaded_model = pickle.load(file)

st.title('Vendor Recommendation App')
st.markdown('<p style="font-size:20px; font-style: italic;">Discover your next restaurant feast with <strong>Akeed</strong></p>', unsafe_allow_html=True)
st.write("A Restaurant recommendation system by Analytics Alchemy")


# st.subheader('This app Re')

# Background image URL or local path
background_image_url = "https://s.inyourpocket.com/gallery/poznan/2023/04/311779505-5674818599245946-6675073789108808550-n.jpg"
primaryColor="#F63366"
textColor="#262730"
font="sans serif"
base="dark"
# Custom CSS
background_css = f"""
<style>
    .stApp {{
        background: url("{background_image_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
</style>
"""

# Inject the CSS into the Streamlit app
st.markdown(background_css, unsafe_allow_html=True)

# Function to preprocess user inputs and make predictions
def predict_vendorid(vendor_category_en,delivery_charge,serving_distance,is_open,prepration_time,discount_percentage,rank,vendor_rating_x,item_count,grand_total,
                    payment_mode,vendor_discount_amount,is_rated,driver_rating,deliverydistance,location_number):
    
    vendor_id_to_vname = {4: 'Skaboo',13: 'Photobug',20: 'Lajo',23: 'Voonder',28: 'Voomm',33: 'Bubbletube',43: 'Divape',44: 'Reallinks',55: 'Realcube',66: 'Tambee',
                            67: 'Zazio',75:	'Leexo',76:'Fivespan',78:'Meeveo',79:'Jazzy',81:'Topiczoom',82:'Jaxworks',83:'Feedbug',84:'Edgeclub',85:'Jayo',86:'Oyope',
                            90:'Demivee', 92:'Pixope',104:'Babbleset',105:'Mybuzz',106:'Realfire',110:'Thoughtbeat',113:'Voomm',115:'Fiveclub',134:'Katz',145:'Feedmix',
                            148:'Topicware',149:'Voonder',
    154:'Rhyzio',
    157:'Babblestorm',
    159:'Geba',
    160:'Yodo',
    161:'Feedbug',
    176:'Lazzy',
    180:'Feedfish',
    188:'Avaveo',
    189:'Yombu',
    191:'Npath',
    192:'Twitterwire',
    193:'Youbridge',
    195:'Realcube',
    197:'Mynte',
    199:'Buzzster',
    201:'Skidoo',
    203:'Aimbu',
    207:'Yabox',
    216:'Feedmix',
    221:'Kwinu',
    225:'Kimia',
    237:'Jabbersphere',
    250:'Yombu',
    259:'Rhybox',
    265:'Einti',
    271:'Ooba',
    274:'Dablist',
    288:'Einti',
    289:'Quinu',
    294:'Thoughtsphere',
    295:'Divanoodle',
    298:'Dynava',
    299:'Omba',
    300:'Jaxworks',
    303:'Ntag',
    304:'Wordware',
    310:'Snaptags',
    356:'Divavu',
    386:'Twitternation',
    391:'Babblestorm',
    398:'Oyope',
    401:'Realcube',
    419:'Layo',
    459:'Quinu',
    537:'Zoombox',
    547:'Trudeo',
    573:'Buzzbean',
    575:'Yambee',
    577:'Oodoo',
    578:'Roodel',
    582:'Janyx',
    583:'Jamia',
    676:'Voolia',
    679:'Skimia',
    681:'Browsezoom'
    # Add more mappings as per your list
}
    # Assuming label encoding mappings are known

    vendor_category_en_mapping={'Restaurant':0,'Sweet&Bakes':1}
    is_rated_mapping={'Yes':0,'No':1}
    is_rated_mapping_encoded=is_rated_mapping.get(is_rated)
    vendor_category_en_encoded=vendor_category_en_mapping.get(vendor_category_en)
    # Prepare input data as a DataFrame for prediction
    input_data = pd.DataFrame([[vendor_category_en_encoded,is_rated_mapping_encoded,delivery_charge,serving_distance,is_open,int(prepration_time),discount_percentage,
                                rank,vendor_rating_x,item_count,grand_total,payment_mode,vendor_discount_amount,driver_rating,deliverydistance,location_number]],
                              columns=[vendor_category_en,delivery_charge,serving_distance,is_open,prepration_time,discount_percentage,rank,vendor_rating_x,item_count,
                                        grand_total,payment_mode,vendor_discount_amount,is_rated,driver_rating,deliverydistance,location_number])
     # Rename columns to string names
     # Make sure the feature names match the model's expectations
    input_data.columns = ['vendor_category_en','delivery_charge','serving_distance','is_open','prepration_time','discount_percentage','rank','vendor_rating_x',
                            'item_count','grand_total','payment_mode','vendor_discount_amount','is_rated','driver_rating','deliverydistance','location_number']

    # Make prediction
    predicted_price = loaded_model.predict(input_data)[0]
    # predicted_vname = vendor_id_to_vname.get(predicted_price,'Unknown')

    return vendor_id_to_vname.get(predicted_price)

col1,col2,col3= st.columns(3)
with col1:

    is_open= st.toggle('Is Open')
    vendor_category_en=st.selectbox('Vendor Category',['Restaurant','Sweet&Bakes'])
    serving_distance= st.slider('Serving Distance',0,15)
    item_count= st.number_input('Item Count', min_value=0)
    grand_total= st.number_input('Grand Total(R)', min_value=0)
    driver_rating= st.slider('driver_rating',0,5)
    
    
with col2:
    delivery_charge= st.number_input('Delivery Charge(R)', min_value=0)
    location_number= st.number_input('Location Number', step=1)
    rank= st.number_input('Rank', step=1)
    vendor_rating_x= st.slider('vendor_rating_x',0,5)
    deliverydistance= st.number_input('Delivery Distance(KM)', min_value=0)

with col3:
    vendor_discount_amount= st.number_input('Vendor Discount Amount(R)', min_value=0)
    prepration_time= st.selectbox('Prep Time(Mins)',['5','10', '11','12','13','14','15','16','17','18','19','20','21','45'])
    discount_percentage= st.number_input('Discount Percentage', step=0)
    payment_mode= st.number_input('Payment Mode', min_value=0)
    is_rated= st.selectbox('Is Rated',['Yes','No'])

        
# Make prediction
if st.button("Get Recommendation"):
# Call the prediction function
    predicted_vname=predict_vendorid(vendor_category_en,delivery_charge,serving_distance,is_open,prepration_time,discount_percentage,rank,vendor_rating_x,
                                    item_count,grand_total,payment_mode,vendor_discount_amount,is_rated,driver_rating,deliverydistance,location_number)
    st.success('The Recommended Vendor/Restaurant is: ' + predicted_vname)
