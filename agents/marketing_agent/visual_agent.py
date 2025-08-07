from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.5, 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

visual_prompt = PromptTemplate(
    input_variables=["requirements"],
    template="""
You are a creative director. Based on the product idea below, describe a visual branding concept including logo style, color palette, and possible imagery.

Product:
{requirements}
"""
)

visual_chain = visual_prompt | gemini

def visual_agent(requirements: str) -> str:
    """Returns a visual concept idea for the product."""
    return visual_chain.invoke({"requirements": requirements})["text"].strip()
