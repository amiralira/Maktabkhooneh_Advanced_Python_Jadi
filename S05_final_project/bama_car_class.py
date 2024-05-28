import pandas as pd

from bama_class import Bama


class BamaCar(Bama):
    def __init__(self, page_index: int = 0):
        super().__init__(page_index=page_index)
        self.base_url = 'https://bama.ir/cad/api/search'
        self.url = self.create_url()

    def create_url(self):
        return f'{self.base_url}?pageIndex={self.page_index}'

    async def parse_data(self):
        if "status" in self.json_response:
            if self.json_response["status"] is True:
                if "metadata" in self.json_response:
                    metadata_df = pd.json_normalize(self.json_response["metadata"])
                    # print(metadata_df)
                else:
                    raise Exception(f'metadata not found in response in {self.url}')

                if "data" in self.json_response:
                    data_df = pd.json_normalize(self.json_response["data"], record_path='ads')
                    # print(data_df)
                else:
                    raise Exception(f'data not found in response in {self.url}')

                return metadata_df, data_df

            else:
                raise Exception(f'status is not true in {self.url}')
        else:
            raise Exception(f'status not found in response in {self.url}')

