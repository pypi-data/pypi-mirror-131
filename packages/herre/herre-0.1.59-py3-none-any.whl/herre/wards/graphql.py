from abc import abstractproperty
import json
from typing import Any, Dict
from herre.exceptions import TokenExpired
from herre.wards.base import BaseQuery, BaseWard, WardException
import aiohttp
import logging
import re
from herre.wards.variables import parse_variables
from fakts import Fakts, get_current_fakts, Config

logger = logging.getLogger(__name__)

gqlparsed_with_variables = re.compile(
    r"[\s]*(?P<type>subscription|query|mutation)\s*(?P<operation>[a-zA-Z]*)\((?P<arguments>[^\)]*)\)[\s]*{[\s]*(?P<firstchild>[^\(:]*).*"
)
gqlparser_without_variables = re.compile(
    r"[\s]*(?P<type>subscription|query|mutation)\s*(?P<operation>[a-zA-Z]*)[\s]*{[\s]*(?P<firstchild>[^\(\{\s:]*).*"
)


class GQLException(Exception):
    pass


class ParsedQuery(BaseQuery):
    def __init__(self, query: str) -> None:
        self.query = query
        self.variables = None
        self._type = None
        self.m = gqlparsed_with_variables.match(self.query)
        self.has_variables = True

        if not self.m:
            self.m = gqlparser_without_variables.match(self.query)
            self.has_variables = False

        if not self.m:
            raise GQLException(f"Illformed request {self.query}")

    def get_operation_name_for_datakey(self, key):
        # TODO: Make work
        return key

    def combine(self, variables: dict):
        self.variables = variables
        return {"query": self.query, "variables": self.variables}

    def parsed(self):
        assert (
            self.variables and self.query
        ), "Please specify query and set variables before parsing"
        return {"query": self.query, "variables": self.variables}

    @property
    def firstchild(self):
        return self.m.group("firstchild")

    @property
    def operation_name(self):
        return self.m.group("operation")

    @property
    def type(self):
        return self.m.group("type")

    def extract(self, result: dict):
        assert (
            self.firstchild in result
        ), f"Cannot Access {self.firstchild}: in {result}"
        assert result[self.firstchild] is not None, f"Empty response {result}"
        return result[self.firstchild]


class GraphQLException(WardException):
    pass


class GraphQLQueryException(GraphQLException):
    pass


class GraphQLProtocolException(WardException):
    pass


class GraphQLWardConfig(Config):
    @abstractproperty
    def endpoint(self):
        return NotImplementedError("Please overwrite endpoint")


class GraphQLWard(BaseWard):
    configClass = GraphQLWardConfig
    config: GraphQLWardConfig

    class Meta:
        abstract = True

    async def handle_connect(self):

        self.async_session = aiohttp.ClientSession(headers=self.herre.headers)

    async def handle_disconnect(self):
        await self.async_session.close()
        self.connected = False

    async def handle_run(
        self, gql: ParsedQuery, variables: dict = {}, files: dict = {}, retry=0
    ):
        try:
            assert (
                retry < self.max_retries
            ), f"Retries Exceeded for Request {gql} with {variables}"

            payload = {"query": gql.query}

            if len(files.items()) > 0:
                # We have to uload files

                payload["variables"] = variables

                data = aiohttp.FormData()

                file_map = {str(i): [path] for i, path in enumerate(files)}
                # Enumerate the file streams
                # Will generate something like {'0': <_io.BufferedReader ...>}
                file_streams = {str(i): files[path] for i, path in enumerate(files)}
                operations_str = json.dumps(payload)

                data.add_field(
                    "operations", operations_str, content_type="application/json"
                )
                file_map_str = json.dumps(file_map)
                data.add_field("map", file_map_str, content_type="application/json")

                for k, v in file_streams.items():
                    data.add_field(
                        k,
                        v,
                        filename=getattr(v, "name", k),
                    )

                post_args: Dict[str, Any] = {"data": data}

            else:
                payload["variables"] = variables
                post_args = {"json": payload}

            async with self.async_session.post(
                self.config.endpoint, **post_args
            ) as resp:

                if resp.status == 200:
                    result = await resp.json()
                    logger.debug(f"Received Reply {result}")

                    if "errors" in result:
                        raise GraphQLQueryException(
                            f"Ward {self.config.endpoint}:" + str(result["errors"])
                        )

                    return result["data"]

                if resp.status == 403:
                    logger.error("Auth token is expired trying to refresh")
                    raise TokenExpired("Token Expired Error")

                if resp.status == 400:
                    raise GraphQLProtocolException(await resp.json())

                raise GraphQLProtocolException(
                    f"Unexpected statuscode {resp.status} {resp}"
                )

        except TokenExpired as e:
            await self.herre.arefresh()
            return await self.run(gql, variables, retry=retry + 1)

        except aiohttp.client_exceptions.ClientOSError as e:
            await self.adisconnect()
            raise GraphQLProtocolException("Ward is not reachable") from e
