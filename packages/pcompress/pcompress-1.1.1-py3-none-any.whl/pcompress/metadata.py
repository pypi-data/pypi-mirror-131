from typing import Optional
import pydantic

class ChainMetadata(pydantic.BaseModel):
    filename: str  # absolute path
    start_timestamp: int  # unix epoch of end time
    end_timestamp: int  # unix epoch of end time
    graph_hash: str  # sha256
    user: str

    git_commit: Optional[str]
    git_repo_clean: Optional[bool]

    ip: Optional[str]
    server_timestamp: Optional[int]
    user_agent: Optional[str]
    identifier: Optional[str]

    class Config:  # allow arbitrary user attributes
        extra = "allow"