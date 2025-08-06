from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, google_api_key=os.getenv("GOOGLE_API_KEY"))

docs_prompt = PromptTemplate(
    input_variables=["code"],
    template="""
    You are a technical writer. Write clear and concise documentation in Markdown format for the following Python code.
    Include function descriptions, usage examples, and parameter explanations.

    Code:
    {code}
    """
)

docs_agent = docs_prompt | gemini
