# agents/frontend_agent.py

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.4,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

frontend_prompt = PromptTemplate(
    input_variables=["requirements"],
    template="""
You are a senior frontend engineer. Based on the product requirement below, generate clean, production-grade React code using Tailwind CSS.

Requirements:
{requirements}

Make sure:
- Use functional components and hooks
- Handle basic error states
- Do NOT include explanations or markdown
- Output only the full code in one file
    """
)

frontend_chain = LLMChain(llm=gemini, prompt=frontend_prompt)

def generate_frontend_code(requirements: str) -> str:
    """Calls the frontend LLM agent to generate code."""
    result = frontend_chain.invoke({"requirements": requirements})
    return result["text"].strip()


frontend_agent = generate_frontend_code
