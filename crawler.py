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
        # Process each URL individually
        for url in urls:
            # Only continue if results_list's length is less than desired result length from env
            if len(markdowns) >= int(os.getenv('DESIRED_RESULT_LENGTH', '5')):
                break
            result = await crawler.arun(
                url=url,
                config=run_config,
                # dispatcher=dispatcher
            )
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
        except Exception as e:
            print(f"Failed to process markdown for {url}: {str(e)}")

    # Sort results_list by ascending order of price
    sorted_results_list = sorted(
        (item for item in results_list if item.get('price') and item['price'].replace('.', '', 1).isdigit()),
        key=lambda x: float(x['price'])
    )

    return sorted_results_list
