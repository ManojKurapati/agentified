from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()


# Create Gemini LLM instance
gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, google_api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt template for social content
social_prompt = PromptTemplate(
    input_variables=["feature"],
    template="""
    You are a social media manager. Write a short LinkedIn and Twitter post announcing the following new product feature.
    Make it engaging, benefit-focused, and clear.

    Feature:
    {feature}
    """
)

# Chain
social_agent = social_prompt | gemini
