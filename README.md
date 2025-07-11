# EcomScrap

## Overview
EcomScrap is a tool designed to scrape e-commerce websites to extract structured product data such as product name, price, currency, and URL. It utilizes the Together API with the `meta-llama/Llama-3.3-70B-Instruct-Turbo` model for accurate data parsing. The tool performs web crawling using `crawl4ai` and integrates with [SerpAPI](https://serpapi.com/) for Google search results.

## Dependencies

EcomScrap relies on several key dependencies:

- **`together` Python SDK**: Used for LLM calls to the Together API.
- **`crawl4ai`**: For asynchronous web crawling.
- **`google-search-results`**: To fetch Google search results (SerpAPI).
- **`pydantic`**: For data validation.
- **`rich`**: For enhanced CLI output.
- **`python-dotenv`**: To manage environment variables.
- **`argparse`**: For parsing CLI arguments.

## Preferred Configurations

The following are the preferred configurations used in the `.env` file:

- **DESIRED_RESULT_LENGTH**: Set to `3` to control the number of results processed.
- **SERPAPI_API_KEY**: Your SerpAPI key for accessing Google search results. ([Get your key here](https://serpapi.com/))
- **TOGETHER_API_KEY**: Your Together API key for LLM processing. ([Get your key here](https://www.together.ai/))
- **SAVE_MARKDOWN_FILES**: Set to `false` to avoid saving markdown files unless needed.
- **LLM_MODEL**: Using `meta-llama/Llama-3.3-70B-Instruct-Turbo` for LLM processing. ([Choose from available models](https://docs.together.ai/docs/json-mode))
- **WEBOUTPUT_FILENAME**: The output filename for search results, default is `webOutput.json`.

These configurations ensure optimal performance and ease of use when running the EcomScrap tool.

## Installation and CLI Guide

### Prerequisites
- Python 3.9+ (Developed with: Python 3.9.6)
- Chromimum should be installed via playwright
- Virtual environment setup (recommended)

### Installation
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd EcomScrap
   ```
2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables in a `.env` file**:
   ```
   DESIRED_RESULT_LENGTH=3
   SERPAPI_API_KEY=<your-serpapi-key>
   TOGETHER_API_KEY=<your-together-api-key>
   SAVE_MARKDOWN_FILES=false
   LLM_MODEL=meta-llama/Llama-3.3-70B-Instruct-Turbo
   WEBOUTPUT_FILENAME=webOutput.json
   ```

### CLI Usage
Run the scraper with the following command:
```bash
python app.py --location "<country-code>" --query "<product-name>"
```

**Example**:
```bash
python app.py --location "JP" --query "matcha powder"
```

## Flow Explanation
1. **Search**: The tool uses SerpAPI to perform a Google search based on the provided location and product query.
2. **Crawling**: It uses `crawl4ai` to crawl the URLs obtained from the search results and extracts markdown content.
3. **Processing**: The markdown content is processed using the Together API to extract product information.
4. **Output**: The extracted data is sorted by price and saved to `result.json`. The console output is styled using `rich` for better readability.

<img width="1301" alt="Screenshot 2025-07-07 at 6 41 35 AM" src="https://github.com/user-attachments/assets/1dbd9046-086f-4259-a486-038d8e997e7e" />


## Example CLI Output

- **Here's an example of the CLI output when running the scraper for "iphone 16 Pro, 128GB":**
   ```bash
   python app.py --location "US" --query "iphone 16 Pro, 128GB"
   ```

   ```
   Scraped Products
   ┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   ┃ Name                ┃  Price ┃ Currency ┃ URL                                                                                                ┃
   ┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
   │ Apple iPhone 16 Pro │ 749.99 │   USD    │ https://www.amazon.com/Apple-iPhone-Version-128GB-Titanium/dp/B0DHJG6JPH                           │
   │ iPhone 16 Pro       │ 999.00 │   USD    │ https://www.apple.com/shop/buy-iphone/iphone-16-pro                                                │
   │ iPhone 16 Pro       │ 999.00 │   USD    │ https://www.apple.com/shop/buy-iphone/iphone-16-pro/6.3-inch-display-128gb-black-titanium-unlocked │
   └─────────────────────┴────────┴──────────┴────────────────────────────────────────────────────────────────────────────────────────────────────┘
   ```

   ![Screenshot](https://github.com/user-attachments/assets/88580837-a36c-4962-b785-6680062df170)

- **Searching for "Ola S1 Pro Electric" in India:**
  ```bash
  python app.py --location "IN" --query "Ola S1 Pro Electric"
  ```
  
  **Output:**
  ```
  Scraped Products
  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ┃ Name                        ┃     Price ┃ Currency ┃ URL                                                             ┃
  ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
  │ OLA S1 Pro Electric Scooter │ 129999.00 │   INR    │ https://www.amazon.in/OLA-S1-Pro-Electric-Scooter/dp/B0DF2XPD8N │
  │ Ola S1 Pro+                 │  148999.0 │   INR    │ https://www.olaelectric.com/s1-pro                              │
  └─────────────────────────────┴───────────┴──────────┴─────────────────────────────────────────────────────────────────┘
  ```
  
   ![Screenshot](https://github.com/user-attachments/assets/5f9dac49-1a79-4390-8917-6c8ca1aafc16)

- **Searching for "matcha powder" in Japan:**
  ```bash
  python app.py --location "JP" --query "matcha powder"
  ```
  **Output:**
  ```
  Performing CLI search for 'matcha powder' in location code 'JP'...
  Results successfully saved to webOutput.json
  Scraped Products
  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ┃ Name                                ┃ Price ┃ Currency ┃ URL                                                                       ┃
  ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
  │ Tsujiri Matcha Milk, 6.7 oz (190 g) │   984 │   JPY    │ https://www.amazon.co.jp/-/en/Green-Tea-Matcha-Powdered-Beverages/s?rh=n… │
  │ New Harvest Matcha 20g Can          │  3000 │   JPY    │ https://global.ippodo-tea.co.jp/collections/matcha                        │
  └─────────────────────────────────────┴───────┴──────────┴───────────────────────────────────────────────────────────────────────────┘
  Sorted results successfully saved to result.json
  ```
