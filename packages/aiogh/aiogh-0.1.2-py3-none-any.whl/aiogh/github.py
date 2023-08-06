import asyncio
import logging
import os
import tarfile
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from io import BytesIO
from tempfile import TemporaryDirectory
from typing import Any, Dict, Optional

import aiohttp

from aiogh.types import Branch

#: Base URL for use of the GitHub API
GITHUB_BASE_URL: str = "https://api.github.com"

MAIN = "main"

logger = logging.getLogger(__name__)


@dataclass
class GitHub:
    """
    Interact with GitHub, optionally as some user via their OAuth token.

    Should be used as an async context manager.
    """

    #: Access token for non-public resources
    token: Optional[str] = None

    #: GitHub API base URL
    base_url: str = GITHUB_BASE_URL

    session: aiohttp.ClientSession = field(
        init=False,
        repr=False,
        hash=False,
        compare=False,
    )

    async def __aenter__(self):
        headers = {"Accept": "application/vnd.github.v3+json"}
        if self.token is not None:
            headers["Authorization"] = f"token {self.token}"

        self.session = aiohttp.ClientSession(
            base_url=self.base_url,
            headers=headers,
        )

        return self

    async def __aexit__(self, *err):
        await self.session.close()

    @asynccontextmanager
    async def download_repo(
        self,
        owner: str,
        repo: str,
        ref=MAIN,
    ):
        """
        Download a repo into a temporary directory, yielding the name of the
        directory containing the extracted repo.
        """
        # Ref https://stackoverflow.com/a/8378458
        target_url = f"/repos/{owner}/{repo}/tarball/{ref}"

        async with self.session.get(target_url) as r:
            repo_tarball = await r.read()
            repo_buffer = BytesIO(repo_tarball)

            tar = tarfile.open(fileobj=repo_buffer)
            with TemporaryDirectory() as tempdir:
                tar.extractall(tempdir)
                (extracted_dir,) = os.listdir(tempdir)
                yield os.path.join(tempdir, extracted_dir)

    async def _page_paginate(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
    ):
        params = params or {}
        page = 1
        while True:
            paginated_params = {**params, "page": page}
            async with self.session.get(url, params=paginated_params) as r:
                logger.debug("Page %s: %s", page, r.status)
                if r.status == 403:
                    content = await r.json()
                    if (
                        "message" in content
                        and "API rate limit exceeded" in content["message"]
                    ):
                        reset_timestamp = r.headers["X-RateLimit-Reset"]
                        reset_time = datetime.fromtimestamp(int(reset_timestamp))
                        delay = reset_time - datetime.now()
                        logger.info(
                            "Rate limit hit. Sleeping for %s seconds",
                            delay.total_seconds(),
                        )
                        await asyncio.sleep(delay=delay.total_seconds())
                        continue
                if r.status != 200:
                    break
                result_json = await r.json()
                yield result_json
                page += 1

    async def list_branches(
        self,
        owner: str,
        repo: str,
        protected: Optional[bool] = None,
    ):
        target_url = f"/repos/{owner}/{repo}/branches"
        params = {"protected": protected} if protected is not None else {}
        async for page in self._page_paginate(target_url, params=params):
            for branch in page:
                yield Branch.parse_obj(branch)
