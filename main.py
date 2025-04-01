import streamlit as st
from scrape import scrape_website, extract_body_content, clean_body_content, split_dom_content
from parse import parse_with_groq

# Streamlit UI
st.set_page_config(page_title="AI Web Scraper", layout="wide")
st.title("🕸️ AI Web Scraper")

# Input URL
url = st.text_input("🌐 Website URL", placeholder="https://example.com")

# Scrape Website
if st.button("🚀 Scrape Website") and url:
    with st.spinner("Scraping the website..."):
        try:
            dom_content = scrape_website(url)
            cleaned_content = clean_body_content(extract_body_content(dom_content))
            st.session_state.dom_content = cleaned_content

            with st.expander("📄 View Scraped Content"):
                st.text_area("DOM Content", cleaned_content, height=300)

            st.success("✅ Website scraped successfully!")
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")

# Parse Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("🧠 What do you want to parse?", placeholder="E.g., Extract all product names")

    if st.button("📊 Parse Content") and parse_description:
        with st.spinner("🔍 Parsing content..."):
            try:
                parsed_result = parse_with_groq(split_dom_content(st.session_state.dom_content), parse_description)
                st.markdown("### 📝 Parsed Results")
                st.code(parsed_result, language="text")
                st.success("✅ Parsing completed!")
            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
