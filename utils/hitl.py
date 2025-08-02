# File: utils/hitl.py

def human_approval_step(title: str, content: str) -> bool:
    """
    Displays the LLM-generated output to a human and asks for approval via terminal.
    Returns True if approved, False if rejected.
    """
    print(f"\n--- {title} ---\n")
    print(content)
    decision = input("\n✅ Approve this output? (y/n): ").strip().lower()
    return decision == "y"
