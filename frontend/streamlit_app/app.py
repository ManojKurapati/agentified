
import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from agents.prd_agent import prd_agent
from agents.userstories_agent import userstories_agent
from agents.frontend_agent import generate_frontend_code
from agents.backend_agent import generate_backend_code

from agents.marketing_agent.email_agent import email_agent
from agents.marketing_agent.slogan_agent import slogan_agent
from agents.marketing_agent.socialmedia_agent import socialmedia_agent
from agents.marketing_agent.visual_agent import visual_agent

from agents.sales_agent import sales_agent
from agents.business_dev_agent import business_dev_agent


st.set_page_config(page_title="⚙️ Build-a-Startup", layout="wide")
st.title("🚀 AI Startup Builder: Department-Level Orchestration")

st.markdown("### Step 1: Describe your product idea")
requirements = st.text_area("💡 Product Idea", placeholder="e.g. An AI-powered nutrition planner that uses wearable data to generate custom meals...")

run_pipeline = st.button("▶️ Run Full Pipeline")

if run_pipeline and requirements:
    with st.spinner("🤖 Generating Product Requirements Document (PRD)..."):
        prd_inputs = {
    "idea": requirements,  # or parse `requirements` into parts if needed
    "pain_point": "Users find current tools fragmented or hard to use",
    "platform": "Web and Mobile",
    "target_user": "Startups and Solo Builders"
}
    prd = prd_agent.invoke(prd_inputs).content


    st.subheader("📄 Product Requirements Document")
    st.code(prd, language="markdown")

    if st.checkbox("✅ Proceed to User Stories"):
        with st.spinner("🧠 Generating Agile User Stories..."):
            user_stories = userstories_agent.invoke({"requirements": prd}).content
        st.subheader("📝 User Stories")
        st.code(user_stories, language="markdown")

        if st.checkbox("✅ Proceed to Frontend & Backend Code"):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🎨 Frontend Code")
                frontend_code = generate_frontend_code(prd)
                st.code(frontend_code, language="javascript")

            with col2:
                st.markdown("### 🛠️ Backend Code")
                backend_code = generate_backend_code(prd)
                st.code(backend_code, language="python")

    if st.checkbox("✅ Proceed to Business Departments"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 💼 Business Strategy")
            biz = business_dev_agent.invoke({"requirements": requirements}).content
            st.write(biz)

        with col2:
            st.markdown("### 📈 Sales Strategy")
            sales = sales_agent.invoke({"requirements": requirements}).content
            st.write(sales)

        with col3:
            st.markdown("### 📣 Marketing Content")

            with st.expander("Email Copy ✉️"):
                email = email_agent.invoke({"requirements": requirements}).content
                st.write(email)

            with st.expander("Slogan 🧠"):
                slogan = slogan_agent.invoke({"requirements": requirements}).content
                st.write(slogan)

            with st.expander("Social Media Captions 📱"):
                social = socialmedia_agent.invoke({"requirements": requirements}).content
                st.write(social)

            with st.expander("Visual Concepts 🎨"):
                visual = visual_agent.invoke({"requirements": requirements}).content
                st.write(visual)

st.markdown("---")
st.info("💡 Tip: You can pause at any stage, refine the inputs manually, and resume. This is a human-in-the-loop system.")
