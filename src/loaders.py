from langchain_community.document_loaders import WebBaseLoader, CSVLoader


def web_loader(url):
    return WebBaseLoader(web_paths=(url,))
