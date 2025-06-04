import datetime

import cianparser
import pandas as pd

CSV_PATH = "data/raw/dataset_{n_rooms}_{time}.csv"
PAGE_COUNT = 10


class Parser:
    """
    A class to parse real estate listings from Cian for a specified number of rooms.
    """

    def __init__(self) -> None:
        self.parser = cianparser.CianParser(location="Москва")

    def parse_cian(self, n_rooms: int):
        """
        Parses Cian for listings with a specified number of rooms and saves the results to a CSV file.
        """

        t = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        csv_path = CSV_PATH.format(n_rooms=n_rooms, time=t)

        data = self.parser.get_flats(
            deal_type="sale",
            rooms=(n_rooms,),
            with_saving_csv=False,
            additional_settings={
                "start_page": 1,
                "end_page": PAGE_COUNT,
                "object_type": "secondary"
            })

        df = pd.DataFrame(data)

        df.to_csv(csv_path,
                encoding='utf-8',
                index=False)

def main():
    parser = Parser()

    for n_rooms in range(1,4):
        parser.parse_cian(n_rooms)


if __name__ == '__main__':
    main()
