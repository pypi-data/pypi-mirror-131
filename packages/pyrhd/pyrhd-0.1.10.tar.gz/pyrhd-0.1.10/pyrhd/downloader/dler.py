import os
import shutil
import time
from threading import BoundedSemaphore
from typing import Optional

import requests
from pyrhd.harvester.hrv8r import BaseHarvester
from pyrhd.utility.cprint import aprint


class BaseDownloader(BaseHarvester):
    def __init__(
        self, ultimatum_path, saving_interval: int = None, default_ultimatum: dict = {}
    ) -> None:
        self.ultimatum_path = ultimatum_path
        super().__init__(ultimatum_path, saving_interval, default_ultimatum)
        # self.getFileData(default_ultimatum)
        # self.life_saver_thr = Thread(target=self.lifeSaver, daemon=True)
        # self.life_saver_thr.start()

    @classmethod
    def downloadAMedia(
        cls,
        url: str,
        dir_: str,
        title: Optional[str] = None,
        sema4: Optional[BoundedSemaphore] = None,
        same_line: bool = False,
        verbose: bool = True,
        err_ver: bool = True,
        add_ver: bool = False,
        header: Optional[dict] = None,
        cookies: Optional[dict] = None,
    ) -> bool:
        """Downloads the content of the media/file/object from the internet to the specified path on the local disk.

        Args:
            url (str): URL of the media to be used to download.
            dir_ (str): directory path in which the file will be saved.
            title (Optional[str], optional): Title/filename of the file. Defaults to None.
            sema4 (Optional[BoundedSemaphore], optional): Bounded Semaphore which is used to release the semaphore after function execution. Defaults to None.
            same_line (bool, optional): Flag indicating whether to print all the info in a same line. Defaults to False.
            verbose (bool, optional): Normal verbose flag. Defaults to True.
            err_ver (bool, optional): Error verbose flag. Defaults to True.
            add_ver (bool, optional): Additional verbose flag. Defaults to False.
            header (Optional[dict], optional): Optional header to be sent in a request. Defaults to None.
            cookies (Optional[dict], optional): Optional cookie header to be sent in a request. Defaults to None.

        Returns:
            bool: Status of the process
        """
        filename, f10sion = os.path.splitext(title or "")
        url_filename, ex10sion = os.path.splitext(url.split("/")[-1])
        ex10sion = ex10sion.split("?")[0] if "?" in ex10sion else ex10sion
        path_ = fr"{dir_}\\{filename or url_filename}{ex10sion or f10sion or ''}"

        # TODO: Add resume functionality for partially downloaded files
        # for now, program just deletes partially downloaded
        # files and tries to download from the beginning
        if os.path.exists(path_ + ".part"):
            os.remove(path_ + ".part")

        downloaded = os.path.exists(path_)
        if downloaded:
            if add_ver:
                msg = [f"⚠️ Existing media ", (252, 225, 0), url, "magenta"]
                aprint(*msg, same_line=same_line)
            sema4.release() if sema4 else None
            return True

        r = None
        try:
            r = requests.get(url, stream=True, headers=header, cookies=cookies)
            if r and r.status_code == 200:
                r.raw.decode_content = True
                with open(path_ + ".part", "wb") as f:
                    shutil.copyfileobj(r.raw, f)
                if verbose:
                    msg = [f"✅ Downloaded media from ", (167, 206, 155), url, "magenta"]
                    aprint(*msg, same_line=same_line)
                time.sleep(0.5)
                os.rename(path_ + ".part", path_)
                downloaded = True
        except Exception as e:
            aprint(e, "red") if err_ver else None

        if not downloaded:
            msg = f"❎ {r.status_code if r else ''} Error while downloading "
            aprint(msg, "red", url, "magenta", same_line=same_line) if verbose else None
        sema4.release() if sema4 else None
        return downloaded
