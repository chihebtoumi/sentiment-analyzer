import os
import streamlit as st
from chains import build_chain

st.set_page_config(page_title="Sentiment Analyzer", page_icon="💬")
st.title("💬 Sentiment Analyzer")
st.caption("Parallel LLM tasks with LangChain + Groq")

if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY is missing. Add it to your .env file.")
    st.stop()


@st.cache_resource
def get_chain():
    return build_chain()


text = st.text_area("Enter your text", height=150,
                    placeholder="I had a fantastic time hiking yesterday.")

if st.button("Analyze", type="primary"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing..."):
            try:
                result = get_chain().invoke(text.strip())
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        st.subheader("Results")
        st.markdown("**Text**")
        st.write(result["statement"])

        col1, col2 = st.columns(2)
        sentiment = result["sentiment"].strip().rstrip(".").lower()
        icon = {"positive": "😊", "negative": "😞", "neutral": "😐"}.get(sentiment, "🤔")
        col1.metric("Sentiment", f"{icon} {sentiment.capitalize()}")
        col2.metric("Topic", result["main_topic"].strip())

        st.markdown("**Follow-up question**")
        st.info(result["followup"].strip())