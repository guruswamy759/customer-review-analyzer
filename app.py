
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob

# 🌐 Translations
translations = {
    "English": {
        "title": "🧠 AI-Powered Customer Review Analyzer",
        "about": "This app analyzes customer reviews using AI sentiment analysis. You can upload your own file or use the sample data provided.",
        "upload_label": "📤 Upload your customer review CSV file",
        "default_used": "No file uploaded. Showing sample reviews below 👇",
        "instructions": "Please upload a CSV file with a 'Review' column. The app will perform sentiment analysis, generate a word cloud, and show insights.",
        "raw_data": "📋 Show Raw Data",
        "sentiment_distribution": "📊 Sentiment Distribution",
        "word_cloud": "☁️ Word Cloud of Reviews",
        "score_distribution": "📈 Sentiment Score Distribution",
    },
    "Telugu": {
        "title": "🧠 AI ఆధారిత కస్టమర్ సమీక్ష విశ్లేషణ",
        "about": "ఈ యాప్ కస్టమర్ సమీక్షలను ఎయ్ ఐ సెంటిమెంట్ విశ్లేషణతో విశ్లేషిస్తుంది. మీరు మీ ఫైల్‌ను అప్‌లోడ్ చేయవచ్చు లేదా ఉదాహరణ డేటాను ఉపయోగించవచ్చు.",
        "upload_label": "📤 మీ కస్టమర్ సమీక్ష CSV ఫైల్‌ను అప్‌లోడ్ చేయండి",
        "default_used": "ఫైల్ అప్‌లోడ్ కాలేదు. ఉదాహరణ సమీక్షలు చూపబడుతున్నాయి 👇",
        "instructions": "'Review' కాలమ్ ఉన్న CSV ఫైల్‌ను అప్‌లోడ్ చేయండి. యాప్ సెంటిమెంట్ విశ్లేషణ, వరల్డ్ క్లౌడ్ మరియు గ్రాఫ్‌లను చూపిస్తుంది.",
        "raw_data": "📋 అసలు డేటాను చూపించు",
        "sentiment_distribution": "📊 భావ విశ్లేషణ గراف్",
        "word_cloud": "☁️ సమీక్షల వరల్డ్ క్లౌడ్",
        "score_distribution": "📈 భావ స్కోర్ పంపిణీ",
    },
    "Hindi": {
        "title": "🧠 एआई-आधारित ग्राहक समीक्षा विश्लेषक",
        "about": "यह ऐप ग्राहक समीक्षाओं का विश्लेषण एआई सेंटिमेंट एनालिसिस से करता है। आप अपनी फ़ाइल अपलोड कर सकते हैं या सैंपल डेटा का उपयोग कर सकते हैं।",
        "upload_label": "📤 अपनी ग्राहक समीक्षा CSV फ़ाइल अपलोड करें",
        "default_used": "कोई फ़ाइल अपलोड नहीं की गई। नीचे सैंपल समीक्षाएँ दिखाई जा रही हैं 👇",
        "instructions": "कृपया एक ऐसी CSV फ़ाइल अपलोड करें जिसमें 'Review' कॉलम हो। ऐप भावना विश्लेषण करेगा और चार्ट दिखाएगा।",
        "raw_data": "📋 कच्चा डेटा दिखाएँ",
        "sentiment_distribution": "📊 भावना वितरण",
        "word_cloud": "☁️ समीक्षाओं का वर्ड क्लाउड",
        "score_distribution": "📈 भावना स्कोर वितरण",
    }
}

# 🌐 Choose language
lang = st.sidebar.selectbox("🌐 Choose Language / భాషను ఎంచుకోండి / भाषा चुनें", list(translations.keys()))
t = translations[lang]

# 🔤 App layout
st.set_page_config(page_title=t["title"], layout="centered")
st.title(t["title"])
st.info(t["about"])
st.markdown(f"📝 {t['instructions']}")

# 📤 Upload CSV
uploaded_file = st.file_uploader(t["upload_label"], type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning(t["default_used"])
    df = pd.read_csv("customer_review.csv")

# ✅ Check Review column
if "Review" not in df.columns:
    st.error("❌ The CSV must contain a 'Review' column.")
else:
    df["Sentiment Score"] = df["Review"].apply(lambda x: TextBlob(str(x)).sentiment.polarity)
    df["Sentiment"] = df["Sentiment Score"].apply(
        lambda x: "Positive" if x > 0 else ("Negative" if x < 0 else "Neutral")
    )

    # 📋 Raw Data
    with st.expander(t["raw_data"]):
        st.dataframe(df)

    # 📊 Sentiment Chart
    st.subheader(t["sentiment_distribution"])
    st.bar_chart(df["Sentiment"].value_counts())

    # ☁️ Word Cloud
    st.subheader(t["word_cloud"])
    text = " ".join(df["Review"].dropna())
    wordcloud = WordCloud(background_color="white", max_words=100).generate(text)

    fig_wc, ax_wc = plt.subplots()
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)

    # 📈 Score Distribution
    st.subheader(t["score_distribution"])
    fig_hist, ax_hist = plt.subplots()
    ax_hist.hist(df["Sentiment Score"], bins=20, color='skyblue', edgecolor='black')
    ax_hist.set_xlabel("Sentiment Score")
    ax_hist.set_ylabel("Number of Reviews")
    st.pyplot(fig_hist)

