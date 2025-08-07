import sys
import os
import streamlit as st
import asyncio

# Add root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


from agents.prd_agent import prd_agent
from agents.frontend_agent import render_ui
from agents.backend_agent import backend_agent
from agents.business_dev_agent import business_dev_agent
from agents.sales_agent import sales_agent
from agents.marketing_agent.email_agent import email_agent
from agents.marketing_agent.slogan_agent import slogan_agent
from agents.marketing_agent.socialmedia_agent import socialmedia_agent
from agents.marketing_agent.visual_agent import visual_agent

st.set_page_config(page_title="Agentified Startup Builder", layout="wide")
st.title("🚀 Agentified Startup Builder")
st.markdown("### Build a business from just an idea, with AI agents acting as your founding team.")

with st.form("product_form"):
    st.subheader("🧠 Enter Your Product Idea")
    idea = st.text_area("Describe your product idea")
    target_user = st.text_input("Who is the target user?")
    platform = st.selectbox("Platform", ["Web", "Mobile", "Desktop", "Cross-platform"])
    pain_point = st.text_area("What key pain point does it solve?")
    submitted = st.form_submit_button("Generate PRD")

if submitted:
    with st.spinner("Generating Product Requirements Document..."):
        st.session_state.idea = idea
        st.session_state.prd = prd_agent.invoke({
            "idea": idea,
            "target_user": target_user,
            "platform": platform,
            "pain_point": pain_point
        })["text"]

    st.success("✅ PRD generated successfully!")
    st.download_button("📄 Download PRD", st.session_state.prd, file_name="PRD.md")

    # Show pipeline choices
    st.markdown("### Choose a pipeline to proceed:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💻 Run Tech Pipeline"):
            with st.spinner("Generating backend and frontend code..."):
                st.session_state.backend = backend_agent(st.session_state.idea)
                st.session_state.frontend_code = render_ui(st.session_state.idea)
            st.success("✅ Tech components generated!")

            st.subheader("🧩 Backend Code")
            st.code(st.session_state.backend, language="python")

            st.subheader("🎨 Frontend UI")
            st.code(st.session_state.frontend_code, language="html")

    with col2:
        if st.button("📈 Run Business + Marketing Pipeline"):

            async def run_all_agents():
                tasks = [
                    asyncio.to_thread(business_dev_agent, st.session_state.idea),
                    asyncio.to_thread(sales_agent, st.session_state.idea),
                    asyncio.to_thread(email_agent, st.session_state.idea),
                    asyncio.to_thread(slogan_agent, st.session_state.idea),
                    asyncio.to_thread(socialmedia_agent, st.session_state.idea),
                    asyncio.to_thread(visual_agent, st.session_state.idea),
                ]
                return await asyncio.gather(*tasks)

            with st.spinner("Generating business strategies and marketing content..."):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                biz, sales, email, slogan, social, visual = loop.run_until_complete(run_all_agents())

                st.session_state.biz = biz
                st.session_state.sales = sales
                st.session_state.email = email
                st.session_state.slogan = slogan
                st.session_state.social = social
                st.session_state.visual = visual

            st.success("✅ Business & Marketing content generated!")

            st.subheader("📊 Business Strategy")
            st.markdown(st.session_state.biz)

            st.subheader("💸 Sales Copy")
            st.markdown(st.session_state.sales)

            st.subheader("✉️ Cold Email")
            st.markdown(st.session_state.email)

            st.subheader("🧠 Slogan")
            st.markdown(f"> _{st.session_state.slogan}_")

            st.subheader("📱 Social Media Post")
            st.markdown(st.session_state.social)

            st.subheader("🎨 Visual Description")
            st.markdown(st.session_state.visual)
