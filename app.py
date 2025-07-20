
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import os

# Set page title
st.set_page_config(page_title="Customer Review Analyzer", layout="centered")
st.title("🧠 AI-Powered Customer Review Analyzer")

# Instructions
st.markdown("""
Upload a customer reviews **CSV file** with a **'Review'** column.  
If you don't upload a file, the app will show sample reviews automatically.
""")

# File uploader
uploaded_file = st.file_uploader("📤 Upload CSV file", type=["csv"])

# Load data from upload or default
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully.")
else:
    if os.path.exists("customer_review.csv"):
        df = pd.read_csv("customer_review.csv")
        st.info("📂 No file uploaded — showing sample review data.")
    else:
        st.error("❌ 'customer_review.csv' not found. Please upload a file.")
        st.stop()

# Validate
if "Review" not in df.columns:
    st.error("❌ The file must contain a 'Review' column.")
    st.stop()

# Sentiment Analysis
df["Sentiment Score"] = df["Review"].astype(str).apply(lambda x: TextBlob(x).sentiment.polarity)
df["Sentiment"] = df["Sentiment Score"].apply(
    lambda x: "Positive" if x > 0 else ("Negative" if x < 0 else "Neutral")
)

# Show raw data
with st.expander("📋 Show Raw Data"):
    st.dataframe(df)

# Sentiment Distribution
st.subheader("📊 Sentiment Distribution")
sentiment_counts = df["Sentiment"].value_counts()
st.bar_chart(sentiment_counts)

# Word Cloud
st.subheader("☁️ Word Cloud of Reviews")
text = " ".join(df["Review"].dropna().astype(str))
if text.strip() == "":
    st.warning("⚠️ No text found for word cloud.")
else:
    wordcloud = WordCloud(background_color="white", max_words=100).generate(text)
    fig_wc, ax_wc = plt.subplots()
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)

# Sentiment Score Histogram
st.subheader("📈 Sentiment Score Distribution")
fig_hist, ax_hist = plt.subplots()
ax_hist.hist(df["Sentiment Score"], bins=20, color='skyblue', edgecolor='black')
ax_hist.set_xlabel("Sentiment Score")
ax_hist.set_ylabel("Number of Reviews")
st.pyplot(fig_hist)
