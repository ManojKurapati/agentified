# agents/business_dev_agent.py

from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.4, google_api_key=os.getenv("GOOGLE_API_KEY"))

bizdev_prompt = PromptTemplate(
    input_variables=["requirements"],
    template="""
You are the Head of Business Development at a startup.

Write a plan that includes:
- Capital requirements and funding strategies
- Fund utilization breakdown
- Potential partnership opportunities (platforms, companies, influencers)
- B2B and B2C growth strategies
- Monetization ideas
- Geographic and market expansion plans
- Timeline of key milestones
- Potential challenges and mitigation strategies
- Metrics for success
- ROI projections


Product idea:
{requirements}
"""
)

business_dev_agent = bizdev_prompt | gemini

def run_business_dev_agent(requirements):
    result = business_dev_agent.invoke({"requirements": requirements})
    return {"Business_Development_Plan": result.content.strip()}
