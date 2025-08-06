# agents/frontend_subagents.py

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

fix_prompt = PromptTemplate(
    input_variables=["code"],
    template="""
You're a strict code reviewer and debugger.
Fix any syntax, logic, or Tailwind errors in the following React + Tailwind code.

Only return clean, corrected code with no explanation.

Code:
{code}
"""
)

fix_chain = LLMChain(llm=gemini, prompt=fix_prompt)

def fix_code(code: str) -> str:
    result = fix_chain.invoke({"code": code})
    return result["text"].strip()
