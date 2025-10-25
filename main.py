import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import report

st.title("Traffic Analysis")

uploaded_file = st.file_uploader("Upload your csv file", type=["csv"])
if not uploaded_file:
    st.info("Please upload the Dataset  to view charts.")
    st.stop()

def streamlit_config():

    # page configuration
    st.set_page_config(page_title='Forecast', layout="wide")

    # page header transparent color
    page_background_color = """
    <style>

    [data-testid="stHeader"] 
    {
    background: rgba(215, 144, 183, 0.8);
    }

    </style>
    """
    st.markdown(page_background_color, unsafe_allow_html=True)

# custom style for submit button - color and width

def style_submit_button():

    st.markdown("""
                    <style>
                    div.stButton > button:first-child {
                                                        background-color: #367F89;
                                                        color: white;
                                                        width: 70%}
                    </style>
                """, unsafe_allow_html=True)


# custom style for prediction result text - color and position

def style_prediction():

    st.markdown(
        """
            <style>
            .center-text {
                text-align: center;
                color: #20CA0C
            }
            </style>
            """,
        unsafe_allow_html=True
    )


df = pd.read_csv('data.csv',header=3)
# print(df.columns.tolist())
df.columns = df.columns.str.strip()
df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
print("Columns in the CSV file:")
# for i, col in enumerate(df.columns):
#     print(f"{i}: '{col}'")
for col in df.columns:
    if col not in ['date', 'unnamed:_0']: 
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.strip(), errors='coerce')

if 'ivt' in df.columns:
    df['app_category'] = np.where(df['ivt']==1,'Flagged','clean')
else:
    df['app_category'] = "Unknown"
print(df.head())
print(df.info())
st.write("File loaded. First 5 rows:")
st.dataframe(df.head())
print(df.describe())
print(df.isna().sum())
print(df.drop_duplicates())

# doing feature engineering baased on the description providded in the asssignment
df['requests_per_idfa'] = df['total_requests']/df['unique_idfas'].replace(0,np.nan) ## replacing 0 with NaN because it should not give error while dividing from zero
df['impressions_per_idfa'] = df['impressions']/df['unique_idfas'].replace(0,np.nan)
df['idfa_ip_ratio'] = df['unique_idfas']/df['unique_ips'].replace(0,np.nan)
df['idfa_ua_ratio'] = df['unique_idfas']/df['unique_uas'].replace(0,np.nan)
df['impression_rate'] = df['impressions']/df['total_requests'].replace(0,np.nan)
df['ua_entropy_rate'] = df['unique_uas']/df['unique_idfas'].replace(0,np.nan)
df['requests_log'] = np.log1p(df['total_requests'])

# Performing EDA
# aggregating the data so it is easy to anlayze
app_summary = df.groupby('unnamed:_0').agg({
    'total_requests':['sum','mean','median'],
    'unique_idfas':['sum','mean'],
    'unique_ips':'mean',
    'unique_uas':'mean',
    'requests_per_idfa':['mean','median'],
    'impression_rate':'mean',
    'idfa_ip_ratio':'mean',
    'idfa_ua_ratio':'mean'
})
# print(f"app_summary:{app_summary}")
# 1. Correlational Matrix
cols = ['unique_idfas', 'unique_ips', 'unique_uas', 'total_requests','requests_per_idfa','impressions_per_idfa','impression_rate','idfa_ip_ratio','idfa_ua_ratio']
corr = df[cols].corr()
fig = plt.figure(figsize=(12,10))
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title("Correlational Matrix Of Key Metrics")
plt.grid(True)
st.pyplot(fig)

#2. Line Chart for time series visual
# Keep only rows that contain "to" (i.e., valid date ranges)
date_mask = df['date'].notna() & df['date'].str.contains(' to ')
df_dates = df.loc[date_mask].copy()
# the above code is solution for error of parsing because date column consists of additional words
start = pd.to_datetime(df_dates['date'].str.split(' to ').str[0] + ' 2025', format='%d %b %Y')
end = pd.to_datetime(df_dates['date'].str.split(' to ').str[1] + ' 2025', format='%d %b %Y')
df_dates['mid_date'] = start + (end - start)/2
# we use mid_date for proper time series analysis also could get error from start and end date
metrics = ['total_requests','requests_per_idfa','idfa_ip_ratio','idfa_ua_ratio','impression_rate','ivt']
fig1 = plt.figure(figsize=(15,8))
colors = ['red','blue','green','yellow','purple','olive']
for col, color in zip(metrics, colors):
    plt.plot(df_dates['mid_date'], df_dates[col], marker='o', label=col, color=color)
plt.title("Time Series Visual Of Key Metrics")
plt.xlabel("Date")
plt.ylabel("Metrics Value")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
st.pyplot(fig1)

# 3. Scatter plot of idfa_ua_ratio and idfa_ip_ratio
fig2 = plt.figure(figsize=(10,8))
sns.scatterplot(data=df, x='idfa_ua_ratio', y='idfa_ip_ratio', hue='ivt')
plt.title('Scatter plot of IDFA-UA vs IDFA-IP Ratio')
plt.grid(True)
st.pyplot(fig2)

# Histogram of idfa_ua_ratio
fig3 = plt.figure(figsize=(10,8))
sns.histplot(data=df,x='idfa_ua_ratio',bins=30,kde=True,hue='ivt',multiple='stack')
plt.title("Histogram Of IDFA-UA Ratio")
plt.xlabel("IDFA-UA Ratio")
plt.ylabel("Frequency")
plt.legend()
plt.grid(True)
st.pyplot(fig3)

# Now we will use boxplots for comparison Of IDFA-UA Ratio And IDFA-IP Ratio across App categories 
# this comparison will help in understanding the change in ivt as asked
fig4 = plt.figure(figsize=(10,8))
sns.boxplot(data=df,x='app_category',y='idfa_ua_ratio',palette='Set2')
plt.title("IDFA-UA Ratio across App Categories")
plt.legend()
plt.grid(True)
st.pyplot(fig4)

#  similarly,we perform for IDFA-IP ratio
fig5 = plt.figure(figsize=(10,8))
sns.boxplot(data=df,x='app_category',y='idfa_ip_ratio',palette='Set3')
plt.title("IDFA-ip Ratio across App Categories")
plt.legend()
plt.grid(True)
st.pyplot(fig5)

# report 
report.show_report()