from .utils import compute_graph_hash

from gerrychain import Partition
from typing import Iterable
import time
import json
import multiprocessing
import getpass
import os
import git
import requests

import subprocess


class Record:
    def __init__(
        self,
        chain: Iterable[Partition],
        filename,
        executable: str = "pcompress",
        # executable="pv",
        threads: int = None,
        extreme: bool = True,
        metadata: dict = {},
        cloud: bool = False,
        cloud_url: str = "http://127.0.0.1:5000",
        api_key: str = None
    ):
        self.chain = iter(chain)
        self.filename = filename
        self.extreme = extreme
        self.executable = executable
        self.cloud = cloud
        self.cloud_url = cloud_url
        self.metadata = metadata
        self.start_time = int(time.time())

        if not api_key:
            self.api_key = os.environ.get("GERRYCHAIN_API_KEY")
        else:
            self.api_key = api_key

        if not threads:
            self.threads = multiprocessing.cpu_count()
        else:
            self.threads = threads

        if self.extreme:
            if self.executable == "pcompress":
                self.executable = "pcompress -e"

            self.child = subprocess.Popen(
                f"{self.executable} | xz -e -T {self.threads} > {self.filename}",
                # f"{self.executable} | xz --lzma2=preset=9e,lp=1,lc=0,pb=0,mf=bt3 -T {self.threads} > {self.filename}",
                shell=True,
                stdin=subprocess.PIPE,
            )
        else:
            self.child = subprocess.Popen(
                f"{self.executable} | xz -T {self.threads} > {self.filename}",
                shell=True,
                stdin=subprocess.PIPE,
            )

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.chain)

    def __next__(self):
        try:
            step = next(self.chain)
            assignment = list(step.assignment.to_series().sort_index().astype(int))
            minimum = min(assignment)
            assignment = [x-minimum for x in assignment]  # GerryChain is sometimes 1-indexed

            state = str(assignment).rstrip() + "\n"
            self.child.stdin.write(state.encode())
            return step

        except StopIteration:  # kill child process
            self.end_time = int(time.time())

            self.child.stdin.close()
            self.child.wait()

            self.child.terminate()
            self.child.wait()

            if self.cloud:
                self.metadata |= {
                    "start_timestamp": self.start_time, 
                    "end_timestamp": self.end_time, 
                    "filename": self.filename, 
                    "graph_hash": compute_graph_hash(self.chain.state.graph),
                    "user": getpass.getuser(),
                    "git_commit": None,
                    "git_repo_clean": None
                    }

                try:
                    repo = git.Repo(".")
                    if repo.index.diff(repo.head.commit) or repo.untracked_files:
                        dirty = True
                        self.metadata["git_repo_clean"] = False
                    else:
                        self.metadata["git_repo_clean"] = True

                    self.metadata["commit"] = str(repo.head.commit)
                except (git.exc.InvalidGitRepositoryError, ValueError) as e:
                    pass

                upload_status = requests.post(self.cloud_url, files={
                    "pcompress": open(self.filename, "rb")
                }, data = self.metadata, headers= {
                    "GERRYCHAIN-API-KEY": self.api_key
                })

                if upload_status.status_code == 200:
                    print("Chain object uploaded as:", upload_status.text)  
                elif upload_status.status_code == 401:
                    print("Access denied. Upload failed.")
                else:
                    print("Server error. Upload failed.")

            raise
