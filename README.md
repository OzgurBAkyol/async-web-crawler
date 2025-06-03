# async-web-crawler
Fast, asynchronous, and customizable web crawler built with aiohttp, asyncio, and BeautifulSoup.

Overview

This project is an asynchronous web crawler designed to fetch the HTML content of any given URL and parse its body into a hierarchical list of HTML elements. It provides an interactive CLI to navigate through the page structure, allowing you to select any element and extract its full HTML and text content, along with its nested descendants.

Features

Asynchronously fetch web pages for faster scraping.
Parse HTML body into a structured list of elements with types (headings, divs, paragraphs, texts, etc.).
Recursive parsing with hierarchical path tracking.
Interactive CLI for browsing and selecting elements.
Export selected element and all nested descendants with full HTML and plain text to a JSON file.
Skips non-visible or irrelevant tags like scripts, styles, meta, etc.
Clean and readable output for terminal and detailed JSON output.