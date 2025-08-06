from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, google_api_key=os.getenv("GOOGLE_API_KEY"))

prompt = PromptTemplate(
    input_variables=["requirements"],
    template="""
    You are a branding expert. Based on the product idea below, generate 3 strong, catchy slogans.

    Product Idea:
    {requirements}
    """
)
slogan_agent = prompt | gemini
