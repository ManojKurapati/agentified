from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini LLM instance
gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Final PromptTemplate for neat, clean Agile-style output
user_stories_prompt = PromptTemplate(
    input_variables=["requirements", "target_users", "industry", "pain_points", "output_style"],
    template="""
You are a professional Agile product manager at a top-tier tech company.

Your job is to convert the following product requirements into **clean, industry-grade Agile user stories** in this format:

• As a [user type], I want to [do something], so that [benefit].

Do not include any headers, explanations, or section titles. Just return 8–10 well-formed user stories as a bulleted list. Each story must:
- Be clear, focused, and realistic.
- Only use input provided — do NOT assume or hallucinate features.
- Incorporate optional context if relevant, but skip it if empty.

---
Requirements: {requirements}
Target Users: {target_users}
Industry: {industry}
User Pain Points: {pain_points}
Preferred Tone/Style: {output_style}
---
Return the final list below:
"""
)

# Updated agent chain
userstories_agent = user_stories_prompt | gemini
