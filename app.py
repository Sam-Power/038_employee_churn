import streamlit as st 
import pickle
import pandas as pd
import numpy as np


st.sidebar.title("HR Employee Churn")
html_temp = """
<div style="background-color:green;padding:10px">
<h1 style="color:white;text-align:center;">HR Employee Churn App </h1>
</div>"""
st.markdown(html_temp,unsafe_allow_html=True)

satisfaction_level = st.sidebar.slider("satisfaction_level",9,100,33,step=1) /100
last_evaluation = st.sidebar.slider("last_evaluation",36,100,55,step = 1)/100
number_project=st.sidebar.slider("number_project",2,7,3,step = 1)
average_montly_hours=st.sidebar.slider("average_montly_hours", 96,310,150,step = 1)
time_spend_company=st.sidebar.slider("time_spend_company", 2,10,3,step = 1)
Work_accident=st.sidebar.radio("Work_accident", (0, 1))
promotion_last_5years=st.sidebar.radio("promotion_last_5years", (0, 1))
Departments=st.sidebar.selectbox("Departments", ('IT', 'RandD', 'accounting','hr'
	, 'management', 'marketing','product_mng','sales','support', 'technical'))
salary=st.sidebar.radio("salary", ('Low', 'Medium', 'High'))
if salary== 'Low':
	salary=1
elif salary == 'Medium':
	salary=2
elif salary == 'High':
	salary=0

my_dict = { 'satisfaction_level' : satisfaction_level,
'last_evaluation' : last_evaluation,
'number_project' : number_project,
'average_montly_hours' : average_montly_hours,
'time_spend_company' : time_spend_company,
'Work_accident' : Work_accident,
'promotion_last_5years' : promotion_last_5years,
'Departments' : Departments,
'salary' : salary}

df = pd.DataFrame.from_dict([my_dict])
#df = pd.get_dummies(df)
#st.sidebar.table(df)
columns = ['satisfaction_level', 'last_evaluation', 'number_project',
'average_montly_hours', 'time_spend_company', 'Work_accident',
'promotion_last_5years', 'salary', 'Departments_IT',
'Departments_RandD', 'Departments_accounting', 'Departments_hr',
'Departments_management', 'Departments_marketing',
'Departments_product_mng', 'Departments_sales', 'Departments_support',
'Departments_technical']
df = pd.get_dummies(df).reindex(columns=columns, fill_value=0)
#st.title("ssss")
#st.sidebar.table(df.T)

with open('saved_model.pkl', 'rb') as file:  
    model = pickle.load(file)

run = st.sidebar.button("RUN")
if run:
	prediction = model.predict(df)[0]
	if prediction == 1:
		prediction = "Churn Yes !"
		st.sidebar.warning(prediction)
	else:
		prediction = "Churn No"
		st.sidebar.success(prediction)

st.cache()
dfshow = pd.read_csv("df_out.csv",index_col=0)

if st.checkbox('Select Random Employees'):
	text = st.text_input("Enter a number to bring random Employees to be shown")
	if text:
		#num = st.slider("Number of random Customers to be shown",1,dfshow.shape[0],1,step=1)
		selection = dfshow.iloc[np.random.randint(dfshow.shape[0], size=int(text))]
		st.success(f"Churn probability of {text} randomly selected Employees")
		st.table(selection)

#if st.checkbox('click see top 5'):
	#st.table(dfshow.head())

if st.checkbox('Top Employees to Churn'):
	text2 = st.text_input("Number of top Employees to Churn")
	if text2:
		#num_top = st.slider("Number of top customer to Churn",1,dfshow.shape[0],1,step=1)
		selection_top = dfshow.iloc[dfshow['Churn Probability'].sort_values(ascending=False)[:int(text2)].index.values]
		st.warning(f"Top {text2} Employees to Churn")
		st.table(selection_top)

if st.checkbox('Top Employees to Loyal'):
	text3 = st.text_input("Number of top Employees to Loyal")
	#num_top = st.slider("Number of top Employees to Loyal",1,dfshow.shape[0],1,step=1)
	if text3:
		selection_top = dfshow.iloc[dfshow['Churn Probability'].sort_values(ascending=True)[:int(text3)].index.values]
		st.success(f"Top {text3} Employees to Loyal")
		st.table(selection_top)
#"Top Customers to Churn"
#"Top Customers to Loyal"


#st.table(dfshow.head())



