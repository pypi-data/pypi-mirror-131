import multiprocessing
import pathlib
import re
import socket

import dask
import psutil

from dask.distributed import LocalCluster, Client


class DaskConfigController:
    @classmethod
    def set_local_one_thread_config(cls):
        dask.config.set({"scheduler": "single-threaded"})

    @classmethod
    def set_local_cluster_config(
        cls, tmp_directory: pathlib.Path, worker_count=None, dashboard_port=5000
    ):
        if worker_count is None:
            worker_count = (
                16 if multiprocessing.cpu_count() > 16 else multiprocessing.cpu_count()
            )
        else:
            worker_count = worker_count
        valid_memory_mb = psutil.virtual_memory().available >> 20
        memory_limit = int(valid_memory_mb / worker_count)
        dask.config.set(
            {
                "temporary-directory": str(tmp_directory / "dask-worker-space"),
                "memory-limit": f"{memory_limit} MB",
            }
        )
        cluster = LocalCluster(
            n_workers=worker_count, dashboard_address=f":{dashboard_port}"
        )
        Client(cluster)
        try:
            origin_ip = socket.gethostbyname(socket.gethostname())
            # noinspection HttpUrlsUsage
            origin_hostname = re.sub(
                r"^.*:", "http://" + origin_ip + ":", cluster.dashboard_link
            )
            print(
                f"\033[1;32;43m dashboard_address(origin): {origin_hostname} \033[0m!"
            )
            print(
                f"\033[1;32;43m dashboard_address(local): {cluster.dashboard_link} \033[0m!"
            )
        except socket.gaierror:
            print(
                f"\033[1;32;43m dashboard_address(local): {socket.gethostname()} \033[0m!"
            )
