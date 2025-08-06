# agents/sales_agent.py

from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, google_api_key=os.getenv("GOOGLE_API_KEY"))

sales_prompt = PromptTemplate(
    input_variables=["requirements"],
    template="""
You are the Head of Sales for a new product.

Based on the product idea below, write a strategic sales plan including:
- Target customer personas
- Sales funnel stages
- Lead generation tactics
- Sales channels (inbound & outbound)
- Cold email pitch and call script
- Metrics to measure success

Product idea:
{requirements}
"""
)

sales_agent = sales_prompt | gemini

def run_sales_agent(requirements):
    result = sales_agent.invoke({"requirements": requirements})
    return {"Sales_Strategy": result.content.strip()}
