import multiprocessing
import limits
import limits.storage
import limits.strategies
import limits.aio.storage
import limits.aio.strategies

import flask
import fastapi


SERVER_CONFIGS = {
    "flask": {"module": "flask_app"},
    "fastapi": {"module": "fastapi_app"},
}


class Benchmark:
    def start_storages(self):
        pass

    def start_server(self, server_config: dict[str, dict[str, str]]):
        pass


if __name__ == "__main__":
    benchmark = Benchmark()
    benchmark.perform()
