from io import StringIO
from typing import Optional, Union

import pandas as pd
import dask.dataframe as dd


class DaskReader:
    @classmethod
    def read_raw_hive_data(
        cls, file_path, sep="\t", dtype=None, partitions: int = 1, limit: Optional[int] = None
    ) -> Union[pd.DataFrame, dd.DataFrame]:
        if limit is None:
            df = dd.read_csv(file_path, sep=sep, dtype=dtype)
        else:
            df_string = ""
            with open(file_path) as f:
                current_count = 0
                while current_count < limit:
                    df_string += f.readline()
                    current_count += 1
            df = dd.from_pandas(
                pd.read_csv(StringIO(df_string), sep=sep, dtype=dtype),
                npartitions=partitions,
            )
        return df
