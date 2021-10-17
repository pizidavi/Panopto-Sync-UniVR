from tqdm import tqdm

from utils.logger import get_logger

logger = get_logger(__name__)


class ProgressBar:

    def __init__(self, options: dict):
        self.__bar = None

    def on_download_started(self, course: dict, lesson: dict) -> None:
        self.__bar = tqdm(total=100)

    def on_download(self, course: dict, lesson: dict, progress: int) -> None:
        if self.__bar:
            self.__bar.n = progress
            self.__bar.refresh()

    def on_download_completed(self, course: dict, lesson: dict, output: str) -> None:
        self._close_bar()

    def on_download_error(self, course: dict, lesson: dict, error: Exception) -> None:
        self._close_bar()

    def _close_bar(self) -> None:
        if self.__bar:
            self.__bar.close()
            print()
