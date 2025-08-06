# agents/marketing_agent.py

from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()
gemini = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.5, google_api_key=os.getenv("GOOGLE_API_KEY"))

# Main marketing strategy generator
marketing_strategy_prompt = PromptTemplate(
    input_variables=["requirements"],
    template="""
You are a marketing strategist at a tech startup.

Generate a detailed marketing strategy based on the following product idea:
{requirements}

Your output should include:
1. Target audience
2. Value proposition
3. Go-to-market plan
4. Social media strategy
5. Content strategy (with formats, timelines, and themes)
6. Influencer or partnership ideas
7. Budget and measurement KPIs
"""
)

# Sub-agents: digital content creation
slogan_prompt = PromptTemplate(
    input_variables=["requirements"],
    template="Generate a catchy slogan for the product: {requirements}"
)

hashtag_prompt = PromptTemplate(
    input_variables=["requirements"],
    template="Generate 5 viral and relevant hashtags for this product: {requirements}"
)

post_ideas_prompt = PromptTemplate(
    input_variables=["requirements"],
    template="Suggest 3 high-performing digital post ideas (can be multimodal) for this product: {requirements}"
)

# Define agents
marketing_agent = marketing_strategy_prompt | gemini
slogan_agent = slogan_prompt | gemini
hashtag_agent = hashtag_prompt | gemini
post_agent = post_ideas_prompt | gemini

def run_marketing_agents(requirements):
    main_strategy = marketing_agent.invoke({"requirements": requirements})
    slogan = slogan_agent.invoke({"requirements": requirements})
    hashtags = hashtag_agent.invoke({"requirements": requirements})
    post_ideas = post_agent.invoke({"requirements": requirements})

    return {
        "Marketing_Strategy": main_strategy.content.strip(),
        "Slogan": slogan.content.strip(),
        "Hashtags": hashtags.content.strip(),
        "Post_Ideas": post_ideas.content.strip(),
    }
