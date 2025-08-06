from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", temperature=0.4, google_api_key=os.getenv("GOOGLE_API_KEY")
)

prd_prompt = PromptTemplate(
    input_variables=["idea", "target_user", "platform", "pain_point"],
    template="""
You are a seasoned product manager at a top-tier tech company.

Given the following inputs, write a **Product Requirements Document (PRD)** that includes:
- Product Summary
- Target Audience
- Problem Statement
- Goals and Objectives
- Key Features
- Assumptions
- Success Metrics

Inputs:
- Product Idea: {idea}
- Target User: {target_user}
- Platform: {platform}
- Key Pain Point Solved: {pain_point}

Return the document in a structured, markdown-like format suitable for product and engineering teams.
"""
)

prd_agent = prd_prompt | gemini
