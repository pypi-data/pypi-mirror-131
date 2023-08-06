"""Graphql Client responsible for make API requests."""


from typing import Dict, Any
import requests
import aiohttp


MAX_CONCURRENCY = 30


class RBClient:
    """Client to communicate with RedBrick AI GraphQL Server."""

    def __init__(
        self,
        api_key: str,
        url: str,
    ) -> None:
        """Construct RBClient."""
        self.session = requests.Session()
        assert (
            len(api_key) == 43
        ), "Invalid Api Key length, make sure you've copied it correctly"
        self.api_key = api_key
        self.url = url.rstrip("/") + "/graphql/"

    def __del__(self) -> None:
        """Garbage collect and close session."""
        self.session.close()

    def execute_query(self, query: str, variables: Dict[str, Any]) -> Any:
        """Execute a graphql query."""
        headers = {"ApiKey": self.api_key}  # Default: Accept-Encoding = gzip, deflate

        try:
            response = self.session.post(
                self.url, headers=headers, json={"query": query, "variables": variables}
            )
            self._check_status_msg(response.status_code)
            return self._process_json_response(response.json())
        except ValueError as error:
            raise error

    async def execute_query_async(
        self, aio_client: aiohttp.ClientSession, query: str, variables: Dict[str, Any]
    ) -> Any:
        """Execute a graphql query using asyncio."""
        headers = {"ApiKey": self.api_key}  # Default: Accept-Encoding = gzip, deflate

        try:
            async with aio_client.post(
                self.url, headers=headers, json={"query": query, "variables": variables}
            ) as response:
                self._check_status_msg(response.status)
                return self._process_json_response(await response.json())
        except ValueError as error:
            raise error

    @staticmethod
    def _check_status_msg(response_status: int) -> None:
        if response_status == 500:
            raise ValueError(
                "Internal Server Error: You are probably using an invalid API key"
            )
        if response_status == 403:
            raise PermissionError("Problem authenticating with Api Key")

    @staticmethod
    def _process_json_response(response_data: Dict) -> Dict:
        """Process JSON resonse."""
        if "errors" in response_data:
            raise ValueError(response_data["errors"][0]["message"])

        res = {}
        if "data" in response_data:
            res = response_data["data"]
        else:
            res = response_data
        return res
