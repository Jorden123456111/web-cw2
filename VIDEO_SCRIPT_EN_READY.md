# 5-Minute English Presentation Script (Ready to Read)

Use this script for your final recording.  
Target duration: around **4:50 to 4:58**.

## 0:00 - 0:20 Introduction
Hello, this is my coursework 2 submission for COMP/XJCO3011.  
I implemented a command-line search tool in Python for `quotes.toscrape.com`.  
The tool crawls pages, builds an inverted index, stores it, and supports search with four commands: `build`, `load`, `print`, and `find`.

## 0:20 - 2:20 Live Demo
First, I run the `build` command.  
This crawls pages and creates the index file.  
I use a politeness delay of 6 seconds between requests, which is required in the brief.

Now I run `load` to load the saved index from disk.  
The output shows document count, term count, and build timestamp.

Next, I run `print nonsense`.  
This command prints the posting list for one word.  
If the word exists, it shows frequency and token positions per page.

Then I run `find good friends`.  
This demonstrates multi-word query handling.  
My implementation uses AND semantics, so returned pages must contain all query terms.  
Results are ranked using a TF-IDF style score.

Now I quickly show edge cases.  
If I run an empty query, the program returns a clear validation message.  
If I search for a missing word, it returns a clean “no documents found” response.

## 2:20 - 3:50 Code Walkthrough and Design Decisions
My code is split into five modules.

`crawler.py` handles breadth-first crawling, same-domain filtering, URL normalization, and politeness timing.  
It also records crawl errors instead of crashing, so the build remains robust.

`indexer.py` tokenizes text in a case-insensitive way and builds this structure:  
word to document to frequency and positions.

`search.py` handles both `print` and `find` logic.  
For `find`, I intersect posting lists for AND matching, then rank matched documents by score.

`storage.py` saves and loads one JSON index bundle, including metadata, visited pages, errors, document metadata, and the inverted index itself.

`main.py` provides the CLI and command routing.

The main trade-off I made is controlled crawl scope by default for stable timing and reproducible demos, while still supporting broader crawling through configuration.

## 3:50 - 4:20 Testing
Now I run the test suite with `pytest`.  
I wrote tests for crawler behavior, indexing correctness, search behavior, storage round-trip, and CLI flow.  
This includes edge cases like missing terms, empty queries, and crawl failures.

## 4:20 - 4:40 Git Workflow
Here is my Git history.  
I developed incrementally: crawler first, then index/search logic, then CLI, then tests and documentation.  
Commit messages are descriptive and reflect the development steps.

## 4:40 - 5:00 GenAI Critical Evaluation
I used GenAI for scaffolding and test brainstorming.  
It helped me move faster on initial structure, but some suggestions were not fully suitable.  
For example, an early suggestion did not preserve positional statistics in the index, so I redesigned that part manually.  
I validated all AI-assisted code with tests and debugging.  
My conclusion is that GenAI is useful for acceleration, but correctness and final design decisions must stay with the developer.

