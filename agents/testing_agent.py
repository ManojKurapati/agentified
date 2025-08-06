from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()


gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, google_api_key=os.getenv("GOOGLE_API_KEY"))

testing_prompt = PromptTemplate(
    input_variables=["code"],
    template="""
    You are a test engineer. Write unit tests using pytest for the following Python code.
    Make sure to cover all edge cases and include meaningful assertions.

    Code:
    {code}
    """
)

testing_agent = testing_prompt | gemini
