import json
from pydantic import BaseModel, Field
import together
import os

class Product(BaseModel):
    price: str = Field(description="Price of the product")
    name: str = Field(description="Name of the product")
    currency: str = Field(description="Currency of the price in ISO Code e.g. USD, INR, EUR")

client = together.Together(api_key=os.getenv("TOGETHER_API_KEY"))

def process_markdown_with_llm(markdown_content, product, url):
    # Call the LLM with the JSON schema
    extract = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                You are a product data extraction engine for e-commerce markdown. Extract:
                - The **product name** (exact name from the content)
                - The **price** (single numeric price, not a range or estimate)
                - The **currency** (ISO 4217 format like 'INR', 'USD', etc.)

                Normalize price by removing commas and returning as numeric string. Normalize currency symbols (e.g., ₹ = INR, $ = USD). Only include product names that match or are highly similar to the main product mentioned in the content.

                Return JSON array if multiple exact matches are found. Return only highly relevant entries. If price or name is not clearly found, return \"Not Found\".
                Format strictly like:
                ```json
                [{"name": "", "price": "", "currency": ""}]
                """
            },
            {
                "role": "user",
                "content": f"""Extract product name price and currency from this e-commerce page markdown. MARKDOWN: {markdown_content}""",
            },
        ],
        response_format={
            "type": "json_schema",
            "schema": Product.model_json_schema(),
        },
        model=os.getenv("LLM_MODEL", "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free")
    )
    output = json.loads(extract.choices[0].message.content)
    output['url'] = url
    return output
