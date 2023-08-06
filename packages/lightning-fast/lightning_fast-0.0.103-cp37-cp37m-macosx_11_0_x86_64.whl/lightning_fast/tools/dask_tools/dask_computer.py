import dask.dataframe as dd
from dask.diagnostics import ProgressBar
from dask.distributed import progress


class DaskComputer:
    @classmethod
    def compute_local_one_thread(cls, *args):
        with ProgressBar():
            return dd.compute(*args)

    @classmethod
    def compute_local_cluster(cls, *args):
        targets = [arg.persist() for arg in args]
        progress(*targets)
        return dd.compute(*targets)
