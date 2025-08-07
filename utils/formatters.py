# File: utils/formatters.py



def clean_output(text: str) -> str:
    """
    Cleans raw LLM output by removing markdown formatting, code fences,
    excess whitespace, and trailing line breaks.
    """
    import re
    if hasattr(text, "content"):
        text = text.content  
    text = text.strip()
    text = re.sub(r"^```(?:\\w+)?", "", text, flags=re.MULTILINE)
    text = re.sub(r"```$", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\s+$", "", text, flags=re.MULTILINE)
    return text.strip()
