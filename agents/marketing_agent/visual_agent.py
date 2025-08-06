from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.6, google_api_key=os.getenv("GOOGLE_API_KEY"))

prompt = PromptTemplate(
    input_variables=["requirements"],
    template="""
    You are a creative director. Based on the following product idea, generate a concept description for a visual advertisement (digital banner or social media image). Include the visual theme, elements, tagline, and layout.

    Product:
    {requirements}
    """
)
visual_agent = prompt | gemini
