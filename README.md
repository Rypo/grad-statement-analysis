# grad-statement-analysis
This repository comprises the primary files used to gather and analyze 3,417 Statement of Purpose/Personal Statement/Letter of Intent style documents.

The documents were scraped from a public forum in which a prospective applicant (referred to as 'OP' throughout the analysis) posts their document for other users to review. Nearly all of the statements have at least one response, although some have many more. In total, 11,985 individual text documents were analyzed, consisting of ‘OP’ posts, ‘OP’ self-responses, and critiques.

## File Descriptions
### Notebooks
* [prelim_analysis.ipynb](https://github.com/Rypo/grad-statement-analysis/blob/master/prelim_analysis.ipynb) - The initial, general-purpose notebook used in the analysis. It features basic EDA, sentiment analysis, FastText and Doc2vec embeddings, and LDA, NMF, and LSA models. [[nbviewer](https://nbviewer.jupyter.org/github/Rypo/grad-statement-analysis/blob/master/prelim_analysis.ipynb)]
* [preprocessing.ipynb](https://github.com/Rypo/grad-statement-analysis/blob/master/preprocessing.ipynb) - Demonstrates the multiple approaches taken to preprocess the text into various forms to meet the needs of particular models. [[nbviewer](https://nbviewer.jupyter.org/github/Rypo/grad-statement-analysis/blob/master/preprocessing.ipynb)]
* [kpe_summarization.ipynb](https://github.com/Rypo/grad-statement-analysis/blob/master/kpe_summarization.ipynb) - Applies several forms of Key-phase Extraction and text summarization to user feedback and uses basic heuristics to find commonalities across the documents. [[nbviewer](https://nbviewer.jupyter.org/github/Rypo/grad-statement-analysis/blob/master/kpe_summarization.ipynb)]
* [exploration.ipynb](https://github.com/Rypo/grad-statement-analysis/blob/master/exploration.ipynb) - Supplemental exploratory data analysis that aims to answer questions tangential to main analysis motivations through data visualization [[nbviewer](https://nbviewer.jupyter.org/github/Rypo/grad-statement-analysis/blob/master/exploration.ipynb)]
* [lang_models.ipynb](https://github.com/Rypo/grad-statement-analysis/blob/master/lang_models.ipynb) - Builds ULMFiT language models on the subsets of the corpus. [[nbviewer](https://nbviewer.jupyter.org/github/Rypo/grad-statement-analysis/blob/master/lang_models.ipynb)]

**Note**: The nbextension [Freeze](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/freeze/readme.html) was used liberally throughout each notebook. Without this, notebooks will likely not function sequentially.

### Python Files
* [FaiText.py](https://github.com/Rypo/grad-statement-analysis/blob/master/FaiText.py) - A minimally modified version of [fast.ai’s text transforms](https://github.com/fastai/fastai/blob/master/fastai/text/transform.py). 
* [HTMLutils.py](https://github.com/Rypo/grad-statement-analysis/blob/master/HTMLutils.py) - Custom logic for parsing HTML tags into tokens, meant to be used in concert with FaiText.
#### Scrapy Files
* [grad_scrape/../SopSpider.py](https://github.com/Rypo/grad-statement-analysis/blob/master/grad_scrape/gradsop/spiders/SopSpider.py) - The main scrapping mechanism, a scrapy spider.
* [grad_scrape/../items.py](https://github.com/Rypo/grad-statement-analysis/blob/master/grad_scrape/gradsop/items.py) - Sets up items categories to allow for a cleaner gathering process during the crawl.
* [grad_scrape/../pipelines.py](https://github.com/Rypo/grad-statement-analysis/blob/master/grad_scrape/gradsop/pipelines.py) - Instructs the spider to output the scraped results to a csv or json file rather than writing to console. 
