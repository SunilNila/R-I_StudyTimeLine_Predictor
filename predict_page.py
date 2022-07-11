import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data['model']
le_CSU = data['le_CSU']
le_description = data['le_description']
le_projectType = data['le_projectType']

def show_predict_page():
    st.title("Study Timeline Prediction")
    st.write("""### We need some study information to predict the timeline """)

    clinical_service_unit = (
        "Oncology",                           
        "Abdominal Medicine and Surgery",      
        "Cardio - Respiratory",
        "Children's",                      
        "Centre for Neurosciences",
        "Women's Hospital",
        "Emergency and Specialty Medicine",                                                            
        "Head and Neck",  
        "Adult Theatres & Anaesthesia",
        "Adult Critical Care",
        "Radiology",
        "Pathology",                                                                                       
        "Trauma & Related Services",           
        "Other"
    )

    description = (
        "Adult",
        "Children"
    )

    project_type = (
    "Non-commercial portfolio",        
    "Commercial portfolio",             
    "Non-commercial non-portfolio",     
    "Academic/student",                 
    "Commercial non-portfolio"    
)

    clinical_service_unit = st.selectbox("CSU", clinical_service_unit)
    description = st.selectbox("Adult or Childrens", description)
    project_type = st.selectbox("Project Type", project_type)

    approvals = st.slider("Number of Approvals", 1, 10, 1)

    ok = st.button("Calculate Timeline")
    if ok:
        X = np.array([[clinical_service_unit, description, project_type, approvals]])
        X[:, 0] = le_CSU.transform(X[:,0])
        X[:, 1] = le_description.transform(X[:,1])
        X[:, 2] = le_projectType.transform(X[:,2])
        X = X.astype(float)

        timeLine = regressor.predict(X)
        st.subheader(f"The estimated timeline is: {timeLine[0]:.0f} days")