from src.db_prep.db import Table

def FILTER_PROMPT(filter_function :str ,details:Table,result:str):
    FILTER_PROMPT = f"""
        You are given a Python filter function and a product's details.

        Filter logic:
        {filter_function}

        Product details:
        - Description: {details.description_product}
        - Price: {details.price}
        - Rating: {details.rating}
        - Reviews: {details.reviews}

        Filter result: {result}

        INSTRUCTIONS:
        - If the product PASSES, return exactly:
        "All conditions are met successfully"

        - If the product FAILS, return ONLY a short reason.
        Examples:
        - "Rating 3.2 is below minimum threshold 3.8"
        - "Review count 45 is less than required minimum 100"
        - "Price 8.99 is below allowed range"

        RULES:
        - Do NOT explain the filter logic.
        - Do NOT include extra text.
        - Do NOT add prefixes like "Reason:".
        - Return only the final reason string.
        """

    
    return FILTER_PROMPT

def KEYWORD_GENERATION_PROMPT(description:str):
    prompt = f"""
You are given a product description.

Description:
{description}

Your task:
Extract concise, search-friendly keywords that would help find similar products.

Guidelines:
- Focus on **product-defining attributes**, such as:
  - material (e.g., stainless steel, plastic)
  - capacity / size (e.g., 32oz, 1 liter)
  - insulation / special features
  - product type (e.g., water bottle, flask)
  - intended use (e.g., sports, hiking, office)
- Exclude marketing words (e.g., "premium", "best", "high-quality").
- Do NOT invent attributes not present in the description.
- Keep keywords short and specific.

Output format:
- Return a **comma-separated list of keywords only**
- No explanations, no extra text

Example output:
stainless steel water bottle, insulated bottle, 32oz capacity, sports bottle
"""

    
    return prompt