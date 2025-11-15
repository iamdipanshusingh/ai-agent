import bs4
from langchain_community.document_loaders import WebBaseLoader, CSVLoader


def web_loader(url):
    return WebBaseLoader(
        web_paths=(url,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
