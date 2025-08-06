from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash", 
    temperature=0.5, 
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

prompt = PromptTemplate(
    input_variables=["requirements"],
    template="""
You're an expert email copywriter. Based on the following product idea, write a compelling cold email to attract potential customers.

Product:
{requirements}
"""
)

email_chain = prompt | gemini

def email_agent(requirements: str) -> str:
    """Returns a cold email based on product idea."""
    result = email_chain.invoke({"requirements": requirements})
    return result["text"].strip()
