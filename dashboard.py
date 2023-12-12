import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

#Menyiapkan dataframe

day_df = pd.read_csv("anaconda3/envs/SdkEnv2/Submission_Analisis_Bike-sandika_arya/Dashboard/data.csv")

def add_sum_cnt_df(day_df):
    sum_cnt_df = day_df.groupby("weathersit").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_cnt_df

def add_mean_cnt_df(day_df):
    mean_cnt_df = day_df
    return mean_cnt_df

def add_min_cnt_df(day_df):
    min_cnt_df = day_df
    return min_cnt_df

def add_max_cnt_df(day_df):
    max_cnt_df = day_df
    return max_cnt_df

def add_sum_workingday_df(day_df):
    sum_workingday_df = day_df.groupby("cnt").workingday.sum().sort_values(ascending=False).reset_index()
    return sum_workingday_df

def add_sum_holiday_df(day_df):
    sum_holiday_df = day_df.groupby("cnt").holiday.sum().sort_values(ascending=False).reset_index()
    return sum_holiday_df

#Membuat data dteday bertipe datetime
datetime_ubah = ["dteday"]

for column in datetime_ubah:
    day_df[column] = pd.to_datetime(day_df[column])

#Membuat filter berdasarkan waktu
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()
 
with st.sidebar:
    #Menambahkan logo (logo bersumber dari google dengan lisensi creative commons)
    st.image("https://shiftindoorcycling.co.uk/wp-content/uploads/2020/08/SHIFT-small-blue.png")
    
    #Mengambil start_date & end_date
    start_date, end_date = st.date_input(
        label="Time Range",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filter_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

#Membuat agar output berdasarkan hasil filter waktu
sum_cnt_df = add_sum_cnt_df(filter_df)
mean_cnt_df = add_mean_cnt_df(filter_df)
min_cnt_df = add_min_cnt_df(filter_df)
max_cnt_df = add_max_cnt_df(filter_df)
sum_workingday_df = add_sum_workingday_df(filter_df)
sum_holiday_df = add_sum_holiday_df(filter_df)

#Menyiapkan dashboard
st.header("Bike Sharing Rental")

#Menampilkan chart jumlah pengguna berdssarkan kondisi cuaca
st.subheader("Number of Users by Weather Conditions")

col1, col2 = st.columns(2)
 
with col1:
    min_cnt = min_cnt_df.cnt.min()
    st.metric("Lowest Users", value=min_cnt)
 
with col2:
    max_cnt = max_cnt_df.cnt.max()
    st.metric("Highest Users", value=max_cnt)

color_1 = {1: "blue", 2: "orange", 3: "green"}

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=filter_df, x="dteday", y="cnt", hue="weathersit", marker="",  palette=color_1 , ax=ax)
ax.set_title("Number of Users by Weather Conditions")
ax.set_xlabel("")
ax.set_ylabel("")

st.pyplot(fig)

#Menampilkan chart jumlah pengguna berdasarkan hari kerja dan hari libur
st.write("")
st.write("")
st.subheader("Number of Users by Holidays and Working Days")
 
col1, col2 = st.columns(2)
 
with col1:
    total_cnt_workingday = sum_workingday_df.workingday.sum()
    st.metric("Total Users in Workingday", value=total_cnt_workingday)
 
with col2:
    total_cnt_holiday = sum_holiday_df.holiday.sum()
    st.metric("Total Users in Holiday", value=total_cnt_holiday)

color_2 = {"Working Day": "orange", "Holiday": "green"}

def create_multichart():
    filter_df[""] = ["Holiday" if hl == 1 else "Working Day" for hl in filter_df["holiday"]]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x="dteday", y="cnt", hue="", data=filter_df, palette=color_2)
    plt.title("Number of Users by Holidays and Working Days")
    plt.xlabel("")
    plt.ylabel("")
    st.pyplot(fig)

create_multichart()

#Menampilkan chart jumlah pengguna berdasarkan hari kerja dan hari libur (bentuk pie chart)
st.write("")
st.write("")
st.subheader("Number of Users by Holidays and Working Days")

total_working_day = filter_df.loc[filter_df["workingday"] == 1, "cnt"].sum()
total_holiday = filter_df.loc[filter_df["holiday"] == 1, "cnt"].sum()

labels = [f"Working Day\n{total_working_day} users", f"Holiday\n{total_holiday} users"]
sizes = [total_working_day, total_holiday]
color_3 = ["orange", "green"]

circle = plt.Circle((0, 0), 0.6, color="white")
fig, ax = plt.subplots()
ax.pie(sizes, labels=labels, colors=color_3, autopct="%1.1f%%", startangle=90, wedgeprops=dict(width=0.9, edgecolor="w"))
ax.add_artist(circle)

st.pyplot(fig)

#Menampilkan chart jumlah pengguna dalam rentang waktu tertentu
st.write("")
st.write("")
st.subheader("Users Development in the Last 2 Years")
 
col1, col2 = st.columns(2)
 
with col1:
    total_cnt = sum_cnt_df.cnt.sum()
    st.metric("Total Users", value=total_cnt)
 
with col2:
    mean_cnt = mean_cnt_df.cnt.mean()
    st.metric("Average Users", value=mean_cnt)

color_4 = "blue"
def create_line_chart():
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x="dteday", y="cnt", data=filter_df, marker="", color=color_4)
    plt.title("Users Development in the Last 2 Years")
    plt.xlabel("")
    plt.ylabel("")
    st.pyplot(fig)

create_line_chart()