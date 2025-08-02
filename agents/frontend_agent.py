from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()


# Create Gemini LLM instance
gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, google_api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt template for frontend generation
frontend_prompt = PromptTemplate(
    input_variables=["requirements"],
    template="""
    You are a frontend engineer. Based on the following product requirement, write clean, modern React code with Tailwind CSS.
    Ensure the output is production-grade, includes basic error handling, and is human-readable.

    Requirement:
    {requirements}
    """
)

# Chain
frontend_agent = frontend_prompt | gemini
