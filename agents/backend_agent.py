from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()


gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, google_api_key=os.getenv("GOOGLE_API_KEY"))

backend_prompt = PromptTemplate(
    input_variables=["requirements"],
    template="""
    You are a backend engineer. Based on the following product requirement, write a FastAPI backend with clean route definitions and request validation.
    Ensure the code follows best practices, includes proper comments, and is production-ready.

    Requirement:
    {requirements}
    """
)

backend_agent = backend_prompt | gemini

def generate_backend_code(requirements: str) -> str:
    """Calls the backend agent and returns generated FastAPI code."""
    result = backend_agent.invoke({"requirements": requirements})
    return result.strip()