from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()


# Create Gemini LLM instance
gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, google_api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt template for user stories
user_stories_prompt = PromptTemplate(
    input_variables=["requirements"],
    template="""
    You are a product manager. Convert the following product requirements into Agile-style user stories.
    Follow the format: 'As a [user], I want to [action], so that [benefit]'.

    Requirements:
    {requirements}
    """
)

# Chain
userstories_agent = user_stories_prompt | gemini
