from nltk import download, pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from loguru import logger

@logger.catch
def convert_tweets_file_content_to_list(content: list) -> list:
    texts = list()
    for el in content:
        for el2 in el["data"]:
            texts.append(el2["text"])
    return texts

@logger.catch
def text_to_list(text: str, separator=" ") -> list:
    return text.split(separator)

@logger.catch
def alpha_lowercase_list(text: list) -> list:
    return [el.lower() for el in [el for el in text if el.isalpha()]]

@logger.catch
def sorted_without_duplicates_list(text: list) -> list:
    return sorted(set(text))

@logger.catch
def download_packages() -> None:
    download("punkt")
    download("stopwords")

@logger.catch
def extract_nouns(text: str) -> list:
    nouns = list()
    sentences = sent_tokenize(text)
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [word for word in words if word not in set(stopwords.words('english'))]
        tagged = pos_tag(words)
        for (word, tag) in tagged:
            # if(tag == 'NN' or tag == 'NNS' or tag == 'NNPS' or tag == 'NNP'):
            if(tag == 'NN' or tag == 'NNS'):
                nouns.append(word)
    return nouns

@logger.catch
def is_noun(text: str) -> bool:
    SPACE = " "
    if SPACE in text:
        raise ValueError("Passed string contains space. It is probably more than one word.")
    nouns = list()
    sentences = sent_tokenize(text)
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [word for word in words if word not in set(stopwords.words('english'))]
        tagged = pos_tag(words)
        for (word, tag) in tagged:
            # if(tag == 'NN' or tag == 'NNS' or tag == 'NNPS' or tag == 'NNP'):
            if(tag == 'NN' or tag == 'NNS'):
                return True
    return False
    


if __name__ == "__main__":
    raise NotImplementedError("Use as package")