from loguru import logger

@logger.catch
def convert_tweets_file_content_to_list(content: list) -> list:
    texts = list()
    for el in content:
        for el2 in el["data"]:
            texts.append(el2["text"])
    return texts



if __name__ == "__main__":
    raise NotImplementedError("Use as package")