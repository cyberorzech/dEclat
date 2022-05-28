import pandas as pd
from loguru import logger

from src.logger import initialize_logger


def main():
    DATASETS_SIZES = [1000, 5000, 10000, 20000, 35000, 50000]
    dataset1 = pd.read_csv("fixtures/datasource_1.csv", sep=";")
    dataset2 = pd.read_csv("fixtures/datasource_2.csv", sep=";")
    for index, dataset_size in enumerate(DATASETS_SIZES):
        subset1 = dataset1.iloc[0:dataset_size]
        subset2 = dataset2.iloc[0:dataset_size]

        subset1.to_csv(f"fixtures/datasets/dataset1_case{index}")
        subset2.to_csv(f"fixtures/datasets/dataset2_case{index}")
        logger.success(f"Saved case {index}")


if __name__ == "__main__":
    initialize_logger()
    main()