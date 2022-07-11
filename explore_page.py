import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

#'Other' function - for CSU's with less than 2 counts
def shorten_categories (categories, cutoff):
  categorical_map = {}
  for i in range(len(categories)):
    if categories.values[i] >= cutoff:
      categorical_map[categories.index[i]] = categories.index[i]
    else:
      categorical_map[categories.index[i]] = 'Other'
  return categorical_map

#where approvals > 10, change to 10
def clean_approvals(x):
  if x >= 10:
    return 10
  return float(x)

@st.cache
def load_data():
    df = pd.read_csv('Data.csv')
    #df = df.dropna(how='any', axis=0)
    csu_map = shorten_categories(df.CSU.value_counts(),2)
    df['CSU'] = df['CSU'].map(csu_map)
    df = df[df['Days_to_open'] <= 300]
    df['Approvals'] = df['Approvals'].apply(clean_approvals)  
    return df  

df = load_data()

def show_explore_page():
    st.title("Explore R&I Opened Studies")
    data = df['CSU'].value_counts()
    
    #pie chart - studies opened by CSU
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%0.0f%%",  startangle=90)
    ax1.axis("equal")
    st.write("""#### Studies Opened by CSU""")
    st.pyplot(fig1)

    #Mean Timeline based on Clincal Service Unit
    st.write("""### Mean Timeline based on Clincal Service Unit""")

    data = df.groupby(['CSU'])['Days_to_open'].mean().sort_values(ascending=True)
    st.bar_chart(data)
    st.write("""### Mean Timeline based on Project Type""")
    data = df.groupby(['Project_type'])['Days_to_open'].mean().sort_values(ascending=True)
    st.line_chart(data)
