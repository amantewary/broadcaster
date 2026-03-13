import streamlit as st
import os
from broadcaster.core import Broadcaster

st.set_page_config(page_title="Broadcaster 📡", page_icon="📡", layout="centered")

st.title("📡 Broadcaster Engine")
st.markdown("Broadcast your content to Medium, Substack, and LinkedIn simultaneously.")

# Initialize session state for credentials
if "medium_sid" not in st.session_state:
    st.session_state.medium_sid = ""
if "medium_uid" not in st.session_state:
    st.session_state.medium_uid = ""
if "smtp_email" not in st.session_state:
    st.session_state.smtp_email = ""
if "smtp_pass" not in st.session_state:
    st.session_state.smtp_pass = ""
if "substack_draft_email" not in st.session_state:
    st.session_state.substack_draft_email = ""

with st.sidebar:
    st.header("🔑 Credentials")
    
    st.subheader("Medium (Session Injection)")
    st.session_state.medium_sid = st.text_input("Medium 'sid' Cookie", type="password", value=st.session_state.medium_sid)
    st.session_state.medium_uid = st.text_input("Medium 'uid' Cookie", type="password", value=st.session_state.medium_uid)
    
    st.subheader("Substack (Email Gateway)")
    st.session_state.smtp_email = st.text_input("SMTP Email (e.g. Gmail)", value=st.session_state.smtp_email)
    st.session_state.smtp_pass = st.text_input("SMTP App Password", type="password", value=st.session_state.smtp_pass)
    st.session_state.substack_draft_email = st.text_input("Substack Secret Draft Email", value=st.session_state.substack_draft_email)

st.header("📝 Compose Article")
article_title = st.text_input("Article Title", placeholder="The Future of AI Agents")
article_content = st.text_area("Article Content (Markdown)", height=300, placeholder="# Introduction\n\nWrite your article here...")

col1, col2, col3 = st.columns(3)
with col1:
    post_medium = st.checkbox("Medium", value=True)
with col2:
    post_substack = st.checkbox("Substack", value=True)
with col3:
    post_linkedin = st.checkbox("LinkedIn (Coming Soon)", disabled=True)

if st.button("🚀 Broadcast Now", type="primary"):
    if not article_title or not article_content:
        st.error("Please enter both a title and content.")
    else:
        publisher = Broadcaster()
        platforms_to_post = []
        kwargs = {}
        
        # Setup Medium
        if post_medium:
            if st.session_state.medium_sid and st.session_state.medium_uid:
                publisher.setup_adapter("medium", {
                    "sid": st.session_state.medium_sid,
                    "uid": st.session_state.medium_uid
                })
                platforms_to_post.append("medium")
            else:
                st.warning("Skipping Medium: Missing sid/uid cookies.")
                
        # Setup Substack
        if post_substack:
            if st.session_state.smtp_email and st.session_state.smtp_pass and st.session_state.substack_draft_email:
                publisher.setup_adapter("substack", {
                    "email": st.session_state.smtp_email, 
                    "password": st.session_state.smtp_pass
                })
                platforms_to_post.append("substack")
                kwargs["substack"] = {"target_email": st.session_state.substack_draft_email}
            else:
                st.warning("Skipping Substack: Missing SMTP credentials or draft email.")
                
        if platforms_to_post:
            with st.spinner("Broadcasting..."):
                results = publisher.broadcast(
                    title=article_title,
                    content=article_content,
                    platforms=platforms_to_post,
                    **kwargs
                )
                
                st.success("Broadcast Complete!")
                for platform, res in results.items():
                    if res["status"] == "success":
                        st.info(f"✅ **{platform.capitalize()}**: {res.get('url', 'Success/Sent')}")
                    else:
                        st.error(f"❌ **{platform.capitalize()}**: {res.get('message')}")
        else:
            st.error("No valid platforms selected or missing credentials.")
