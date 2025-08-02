from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()


# Create Gemini LLM instance
gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, google_api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt template for backend generation
backend_prompt = PromptTemplate(
    input_variables=["requirements"],
    template="""
    You are a backend engineer. Based on the following product requirement, write a FastAPI backend with clean route definitions and request validation.
    Ensure the code follows best practices, includes proper comments, and is production-ready.

    Requirement:
    {requirements}
    """
)

# Chain
backend_agent = backend_prompt | gemini