from agents.prd_agent import prd_agent
from agents.marketing_agent.email_agent import email_agent
from agents.marketing_agent.slogan_agent import slogan_agent
from agents.marketing_agent.socialmedia_agent import socialmedia_agent
from agents.marketing_agent.visual_agent import visual_agent
from agents.frontend_agent import frontend_agent
from agents.backend_agent import backend_agent
from agents.userstories_agent import userstories_agent
from agents.testing_agent import testing_agent
from agents.docs_agent import docs_agent
from agents.marketing_agent import socialmedia_agent
from utils.formatters import clean_output
from utils.hitl import human_approval_step

def run_full_pipeline(requirements: str):
    print("\n📄 Generating Product Requirements Document...")
    
    idea = requirements
    target_user = input("🧑 Who is the target user? (optional): ") or "General users"
    platform = input("💻 Which platform is this for? (optional): ") or "Web"
    pain_point = input("😩 What pain point does it solve? (optional): ") or "N/A"

    prd = clean_output(prd_agent.invoke({
        "idea": idea,
        "target_user": target_user,
        "platform": platform,
        "pain_point": pain_point
    }))
    
    approved = human_approval_step("Product Requirements Document", prd)
    if not approved:
        return "PRD rejected by human."

    marketing_outputs = {
    "Email Copy": email_agent.invoke({"requirements": requirements}),
    "Slogans": slogan_agent.invoke({"requirements": requirements}),
    "Social Media Posts": socialmedia_agent.invoke({"requirements": requirements}),
    "Visual Campaign": visual_agent.invoke({"requirements": requirements}),
    }
    output["Marketing"] = marketing_outputs

    print("\n--- User Stories ---")
    user_stories = clean_output(userstories_agent.invoke({"requirements": requirements}))
    print("\n--- User Stories ---\n")
    print(user_stories)
    if not human_approval_step("User Stories", user_stories):
        exit()

    with open("build/user_stories.md", "w") as f:
        f.write(user_stories)

    frontend_code = clean_output(frontend_agent.invoke({"requirements": requirements}))
    print("\n--- Frontend Code ---\n")
    print(frontend_code)
    if not human_approval_step("Frontend Code", frontend_code):
        exit()

    with open("build/frontend_code.jsx", "w") as f:
        f.write(frontend_code)

    backend_code = clean_output(backend_agent.invoke({"requirements": requirements}))
    print("\n--- Backend Code ---\n")
    print(backend_code)
    if not human_approval_step("Backend Code", backend_code):
        exit()

    with open("build/backend_code.py", "w") as f:
        f.write(backend_code)

    combined_code = f"{frontend_code}\n\n{backend_code}"
    test_code = clean_output(testing_agent.invoke({"code": combined_code}))
    print("\n--- Test Code ---\n")
    print(test_code)
    if not human_approval_step("Test Code", test_code):
        exit()

    with open("build/test_code.py", "w") as f:
        f.write(test_code)

    docs = clean_output(docs_agent.invoke({"frontend": frontend_code, "backend": backend_code}))
    print("\n--- Documentation ---\n")
    print(docs)
    if not human_approval_step("Documentation", docs):
        exit()

    with open("build/documentation.md", "w") as f:
        f.write(docs)

    social_copy = clean_output(socialmedia_agent.invoke({"requirements": requirements}))
    print("\n--- Social Media Copy ---\n")
    print(social_copy)

    with open("build/social_copy.txt", "w") as f:
        f.write(social_copy)

    return {
        "user_stories": user_stories,
        "frontend_code": frontend_code,
        "backend_code": backend_code,
        "test_code": test_code,
        "docs": docs,
        "social_copy": social_copy,
    }
