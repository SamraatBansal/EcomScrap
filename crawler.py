import os
import asyncio
from datetime import datetime
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from markdown_processor import process_markdown_with_llm

async def crawl_streaming(urls, query):
    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        excluded_tags=["form", "header", "footer", "nav"],
        stream=True,  # Enable streaming mode
        markdown_generator=DefaultMarkdownGenerator(
           options={
                "ignore_links": True,
                "ignore_images": True,
                "skip_internal_links": True
            }
        ),
    )
    
    markdowns = [] 
    results_list = []  # Collect outputs here

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result_container = await crawler.arun_many(urls, config=run_config)
        results = []
        if isinstance(result_container, list):
            results = result_container
        else:
            async for res in result_container:
                results.append(res)
        for result in results:
            if result.success:
                markdowns.append((result.markdown, result.url))
                # Write markdown to file if enabled by environment variable
                if os.getenv('SAVE_MARKDOWN_FILES', 'false').lower() == 'true':
                    file_name = f"result_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.md"
                    with open(file_name, 'w', encoding='utf-8') as file:
                        file.write(result.markdown)
                    print(f"Markdown saved to {file_name}")
            else:
                print(f"Failed to crawl {result.url}: {result.error_message}")

    # Process markdowns outside the async loop
    for markdown, url in markdowns:
        try:
            output = process_markdown_with_llm(markdown, query, url)
            results_list.append(output)
            # Check if results_list has reached desired length
            if len(results_list) >= int(os.getenv("DESIRED_RESULT_LENGTH", 5)):
                break
        except Exception as e:
            print(f"Failed to process markdown for {url}: {str(e)}")

    def is_valid_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    sorted_results_list = sorted(
        (item for item in results_list if item.get('price') and is_valid_float(item['price'])),
        key=lambda x: float(x['price'])
    )

    return sorted_results_list
