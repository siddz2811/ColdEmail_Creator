import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
import os
from langchain_core.output_parsers import JsonOutputParser

from chroma_config import get_or_create_portfolio_collection
from prompts import extract_prompt, email_prompt

def main():
    st.set_page_config(
        page_title="Job Scraper & Email Generator",
        page_icon=":mailbox_with_mail:",
        layout="wide"
    )

    st.title(":mailbox_with_mail: Job Scraper & Email Generator(Btech Graduates only)")

    # --- Personal Prompt Template ---
    st.header("👤 About Yourself Prompt Reference")
    st.markdown(
        "Add a short template that describes yourself, your experience, or achievements. This will be used as reference in the generated cold email."
    )
    default_prompt = (
        "Enter your bio,qualifications,experience,etc"
    )
    user_prompt = st.text_area(
        "Your personal prompt", value=default_prompt, height=120
    )
    st.session_state["user_prompt"] = user_prompt

    # --- Load environment variables and LLM ---
    load_dotenv()
    groq_token = os.getenv("GROQ_API_TOKEN")
    llm = ChatGroq(
        temperature=0,
        groq_api_key=groq_token,
        model_name="llama-3.3-70b-versatile"
    )

    job_url = st.text_input("🔗 Enter Career Page URL", "")
    col1, col2 = st.columns([1,1])
    with col1:
        scrape_btn = st.button("🕵️ Scrape Job")
    with col2:
        email_btn = st.button("✉️ Generate Email")

    # --- Portfolio CSV and ChromaDB setup ---
    try:
        collection = get_or_create_portfolio_collection()
    except Exception as e:
        st.error(f"Error setting up portfolio collection: {e}")
        return

    if "job_data" not in st.session_state:
        st.session_state["job_data"] = None
    if "link_list" not in st.session_state:
        st.session_state["link_list"] = None
    if "page_data" not in st.session_state:
        st.session_state["page_data"] = None

    # --- Scrape Job Button ---
    if scrape_btn:
        with st.spinner("🔎 Scraping job page..."):
            loader = WebBaseLoader(job_url)
            try:
                page_data = loader.load().pop().page_content
                st.session_state["page_data"] = page_data
            except Exception as e:
                st.error(f"Error loading web page: {e}")
                return

            st.subheader("📄 Scraped Job Page Content")
            st.text(st.session_state["page_data"][:1500])  # Show first 1500 chars

            # Extract job info using LLM
            chain_extract = extract_prompt | llm
            res = chain_extract.invoke(input={'page_data': st.session_state["page_data"]})
            json_parser = JsonOutputParser()
            try:
                json_res = json_parser.parse(res.content)
                st.session_state["job_data"] = json_res
                st.success("Job info extracted! 🎉")
            except Exception as e:
                st.error(f"Error parsing job info: {e}")
                return

            # Find relevant portfolio links
            skills = st.session_state["job_data"][0]['skills']
            links = collection.query(query_texts=skills, n_results=2).get('metadatas', [])
            st.session_state["link_list"] = links[0] if links else []
            st.success("Portfolio links found! 💡")

    # --- Show job info as a card ---
    if st.session_state["job_data"]:
        job = st.session_state["job_data"][0]
        st.markdown(
            f"""
            <div style="background:#f9f9f9;padding:1em;border-radius:8px;margin-bottom:1em">
            <span style='font-size:1.3em'><b>Role:</b> {job['role']}</span><br>
            <b>Experience:</b> {job['experience'] if job['experience'] else 'Not specified'}<br>
            <b>Skills:</b> {job['skills']}<br>
            <b>Description:</b> {job['description']}
            </div>
            """, unsafe_allow_html=True
        )

    # --- Generate cold email with personal prompt reference ---
    if email_btn and st.session_state["job_data"] is not None and st.session_state["link_list"] is not None:
        chain_email = email_prompt | llm
        email_res = chain_email.invoke({
            "job_description": str(st.session_state["job_data"]),
            "link_list": st.session_state["link_list"],
            "user_prompt": st.session_state["user_prompt"]
        })
        st.markdown("#### :sparkles: Generated Cold Email")
        st.code(email_res.content, language="markdown")
        st.success("Email generated successfully!")

    st.markdown("""---""")


if __name__ == "__main__":
    main()