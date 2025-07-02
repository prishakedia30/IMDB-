import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="IMDB Analyzer", layout="wide")
st.title("🎬 IMDB Top 250 Movie Analyzer")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/itiievskyi/IMDB-Top-250/master/imdb_top_250.csv"
    return pd.read_csv(url)

df = load_data()

if df.empty:
    st.error("❌ Failed to load data.")
    st.stop()

st.success(f"✅ Loaded {len(df)} movies.")
st.dataframe(df)

# Year filter
min_year, max_year = int(df["Year"].min()), int(df["Year"].max())
year_range = st.slider("📅 Filter by Year", min_year, max_year, (2000, 2023))

filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
st.write(f"🎥 Showing movies from {year_range[0]} to {year_range[1]}")
st.dataframe(filtered_df)

# Top 10 movies
st.subheader("🏆 Top 10 Movies")
top_10 = filtered_df.sort_values("Rating", ascending=False).head(10)
st.table(top_10)

# Rating by decade
st.subheader("📊 Average Rating by Decade")
df["Decade"] = (df["Year"] // 10) * 10
avg_by_decade = df.groupby("Decade")["Rating"].mean()

fig, ax = plt.subplots()
avg_by_decade.plot(kind="bar", color="skyblue", ax=ax)
plt.title("Average IMDB Rating by Decade")
plt.xlabel("Decade")
plt.ylabel("Average Rating")
plt.xticks(rotation=45)
st.pyplot(fig)

# Download button
st.download_button(
    label="📥 Download Filtered CSV",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_imdb.csv",
    mime="text/csv"
)
