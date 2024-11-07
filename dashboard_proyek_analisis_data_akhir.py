
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Data Wrangling
pd.options.display.max_columns = None
df_day = pd.read_csv('data/day.csv')
df_hour = pd.read_csv('data/hour.csv')

# Konversi kolom dteday ke datetime
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])


# Fungsi untuk membuat comparison data
def create_comparison(df_day, df_hour):
    daily_data_from_hour = df_hour.groupby(df_hour['dteday'].dt.date).agg({
        'cnt': 'sum',
        'temp': 'mean',
        'atemp': 'mean',
        'hum': 'mean',
        'windspeed': 'mean'
    }).reset_index()
    daily_data_from_hour.columns = ['dteday', 'cnt', 'temp', 'atemp', 'hum', 'windspeed']

    # Konversi dteday di daily_data_from_hour agar sesuai dengan df_day
    daily_data_from_hour['dteday'] = pd.to_datetime(daily_data_from_hour['dteday'])
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])

    # Gabungkan data df_day dan daily_data_from_hour
    comparison = pd.merge(df_day[['dteday', 'cnt']], daily_data_from_hour[['dteday', 'cnt']],
                          on='dteday', suffixes=('_day', '_hour'))
    comparison.columns = ['dteday', 'cnt_day', 'cnt_hour']
    return comparison


# Buat comparison
comparison = create_comparison(df_day, df_hour)

# Streamlit Page Title
st.title("Dashboard Bike Sharing Analysis")

"""## Exploratory Data Analysis (EDA)"""

# Distribusi Total Pengguna Sepeda Harian
st.subheader("Distribusi Total Pengguna Sepeda Harian")
fig, ax = plt.subplots()
sns.histplot(df_day['cnt'], kde=True, ax=ax)
ax.set_title("Distribusi Total Pengguna Sepeda Harian")
ax.set_xlabel("Jumlah Pengguna Sepeda")
st.pyplot(fig)

# Pengaruh Musim Terhadap Jumlah Pengguna Sepeda
st.subheader("Pengaruh Musim Terhadap Jumlah Pengguna Sepeda")
fig, ax = plt.subplots()
sns.boxplot(x='season', y='cnt', data=df_day, ax=ax)
ax.set_title("Pengaruh Musim Terhadap Jumlah Pengguna Sepeda")
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Pengguna Sepeda")
st.pyplot(fig)

# Pengaruh Hari Kerja vs Akhir Pekan Terhadap Penggunaan Sepeda
st.subheader("Pengaruh Hari Kerja vs Akhir Pekan Terhadap Penggunaan Sepeda")
fig, ax = plt.subplots()
sns.boxplot(x='workingday', y='cnt', data=df_day, ax=ax)
ax.set_title("Pengaruh Hari Kerja vs Akhir Pekan Terhadap Penggunaan Sepeda")
ax.set_xlabel("Hari Kerja (1) vs Akhir Pekan (0)")
ax.set_ylabel("Jumlah Pengguna Sepeda")
st.pyplot(fig)

# Matriks Korelasi Variabel Utama
st.subheader("Matriks Korelasi Variabel Utama")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df_day[['cnt', 'temp', 'atemp', 'hum', 'windspeed']].corr(), annot=True, cmap='coolwarm', ax=ax)
ax.set_title("Matriks Korelasi Variabel Utama")
st.pyplot(fig)

# Rata-Rata Penggunaan Sepeda Berdasarkan Hari dalam Seminggu
st.subheader("Penggunaan Sepeda Rata-Rata Berdasarkan Hari dalam Seminggu")
avg_cnt_per_weekday = df_day.groupby('weekday')['cnt'].mean()
fig, ax = plt.subplots()
avg_cnt_per_weekday.plot(kind='line', marker='o', ax=ax)
ax.set_title("Penggunaan Sepeda Rata-Rata Berdasarkan Hari dalam Seminggu")
ax.set_xlabel("Hari dalam Seminggu (0 = Minggu)")
ax.set_ylabel("Rata-rata Jumlah Pengguna Sepeda")
st.pyplot(fig)

# Distribusi Total Pengguna Sepeda per Jam
st.subheader("Distribusi Total Pengguna Sepeda per Jam")
fig, ax = plt.subplots()
sns.histplot(df_hour['cnt'], kde=True, ax=ax)
ax.set_title("Distribusi Total Pengguna Sepeda per Jam")
ax.set_xlabel("Jumlah Pengguna Sepeda")
st.pyplot(fig)

# Rata-Rata Penggunaan Sepeda Berdasarkan Jam
st.subheader("Rata-Rata Penggunaan Sepeda Berdasarkan Jam")
fig, ax = plt.subplots()
avg_cnt_per_hour = df_hour.groupby('hr')['cnt'].mean()
avg_cnt_per_hour.plot(kind='line', marker='o', ax=ax)
ax.set_title("Rata-Rata Penggunaan Sepeda Berdasarkan Jam")
ax.set_xlabel("Jam dalam Sehari (0-23)")
ax.set_ylabel("Rata-Rata Jumlah Pengguna Sepeda")
st.pyplot(fig)

# Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda per Jam
st.subheader("Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda per Jam")
fig, ax = plt.subplots()
sns.boxplot(x='weathersit', y='cnt', data=df_hour, ax=ax)
ax.set_title("Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda per Jam")
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Jumlah Pengguna Sepeda")
st.pyplot(fig)

# Penggunaan Sepeda per Jam pada Hari Kerja vs Akhir Pekan
st.subheader("Penggunaan Sepeda per Jam pada Hari Kerja vs Akhir Pekan")
fig, ax = plt.subplots()
sns.lineplot(x='hr', y='cnt', hue='workingday', data=df_hour, ax=ax)
ax.set_title("Penggunaan Sepeda per Jam pada Hari Kerja vs Akhir Pekan")
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Pengguna Sepeda")
st.pyplot(fig)

# Scatter plot untuk membandingkan `cnt` dari df_day dan daily_data_from_hour
st.subheader("Perbandingan Jumlah Pengguna Harian dari df_day dan Agregasi df_hour")
fig, ax = plt.subplots()
sns.scatterplot(x='cnt_day', y='cnt_hour', data=comparison, ax=ax)
ax.plot([comparison['cnt_day'].min(), comparison['cnt_day'].max()],
        [comparison['cnt_day'].min(), comparison['cnt_day'].max()],
        'r--', linewidth=2)  # Garis diagonal untuk menunjukkan konsistensi
ax.set_xlabel("Jumlah Pengguna (Data Harian - df_day)")
ax.set_ylabel("Jumlah Pengguna (Agregasi dari Data Jam - df_hour)")
ax.set_title("Perbandingan Jumlah Pengguna Harian dari df_day dan Agregasi df_hour")
st.pyplot(fig)