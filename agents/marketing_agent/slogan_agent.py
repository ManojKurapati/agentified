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

slogan_chain = PromptTemplate(
    input_variables=["requirements"],
    template="""
You're a creative copywriter. Given the following product idea, write a catchy product slogan that appeals to modern consumers.

Product:
{requirements}
"""
) | gemini  # this is your RunnableSequence

def slogan_agent(requirements: str) -> str:
    """Generate a product slogan."""
    return slogan_chain.invoke({"requirements": requirements})["text"].strip()
