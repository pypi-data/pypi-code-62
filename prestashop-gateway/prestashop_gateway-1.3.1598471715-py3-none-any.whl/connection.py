import requests
import xmltodict
import tempfile
from requests.auth import HTTPBasicAuth
from .exception import PrestashopWebServicesException, PrestashopGatewayException
import logging

logger = logging.getLogger(__name__)


class Connection:
    VERSION = "1.0.0"
    XML = "XML"
    JSON = "JSON"
    IO_FORMATS = ((XML, "xml"), (JSON, "json"))
    OUTPUT_FORMATS = ((XML, "xml"), (JSON, "json"))
    HTTP_SCHEME = "http"
    HTTPS_SCHEME = "https"
    SCHEMES = ((HTTP_SCHEME, "http"), (HTTPS_SCHEME, "https"))
    HTTPS_DEFAULT_PORT = 443
    __EXCEPTION_MESSAGES = {1: "resource is mandatory", 2: "identifier is mandatory"}

    def __init__(
            self,
            host: str,
            api_key: str,
            scheme: str = HTTPS_SCHEME,
            port: int = HTTPS_DEFAULT_PORT,
            io_format: str = XML,
            output_format: str = XML,
            debug: bool = False,
            init: bool = False,
    ) -> None:
        super().__init__()
        self.temp_folder = tempfile.mkdtemp()
        self.host = host
        self.api_key = api_key
        self.scheme = scheme
        self.port = port
        self.io_format = io_format
        self.output_format = output_format
        self.url = f"{self.scheme}://{self.host}:{self.port}/api"
        self.headers = {
            "Io-Format": self.io_format,
            "Output-Format": self.output_format,
        }
        if init:
            response = requests.get(
                url=self.url, headers=self.headers, auth=HTTPBasicAuth(self.api_key, "")
            )
            self.__check_status_code(response.status_code)
            content = xmltodict.parse(response.content)
            with open(f"{self.temp_folder}/schema.xml", "w") as file1:
                file1.write(response.content.decode("utf-8"))
            for element in content["prestashop"]["api"]:
                if not str(element).startswith("@"):
                    logger.debug(f"get resource schema to {str(element)}")
                    if (
                            content["prestashop"]["api"][str(element)].get("schema", None)
                            is not None
                    ):
                        for type_schema in content["prestashop"]["api"][str(element)][
                            "schema"
                        ]:
                            if type_schema["@type"] == "synopsis":
                                response = requests.get(
                                    type_schema["@xlink:href"],
                                    headers=self.headers,
                                    auth=HTTPBasicAuth(self.api_key, ""),
                                )
                                self.__check_status_code(response.status_code)
                                with open(
                                        f"{self.temp_folder}/{str(element)}.xml",
                                        "w",
                                ) as f:
                                    f.write(response.content.decode("utf-8"))

    def __check_status_code(self, status_code: int, obj: str = ""):
        if status_code not in [200, 201]:
            raise PrestashopWebServicesException(status_code)

    def get_version(self):
        return self.VERSION

    def hack_fix(self, content):
        # Hack to fix "XML or text declaration not at start of entity".
        # Sometimes prestashop response has a new line at the beginning so to fix this
        # we strip new lines from the start of the response
        i = -1
        for c in content:
            # if c == '\r' or c == '\n'
            if c == 13 or c == 10:
                i += 1
            else:
                break
        content = content[i + 1:]
        return content

    def add(self, **kwargs):
        resource = kwargs.get("resource", None)
        if resource is not None:
            url = f"{self.url}/{resource}"
            id_shop = kwargs.get("id_shop", None)
            id_group_shop = kwargs.get("id_group_shop", None)
            data = kwargs.get("data", None)
            params = {}
            if id_shop is not None:
                params.update({"id_shop": id_shop})
            if id_group_shop is not None:
                params.update({"id_group_shop": id_group_shop})
            response = requests.post(
                url=url,
                params=params,
                headers=self.headers,
                data=data,
                auth=HTTPBasicAuth(self.api_key, ""),
            )
            self.__check_status_code(response.status_code, url)
            return self.hack_fix(response.content)
        else:
            raise PrestashopGatewayException(self.__EXCEPTION_MESSAGES.get(1))

    def get(self, **kwargs):

        resource = kwargs.get("resource", None)
        schema = kwargs.get("schema", None)
        identifier = kwargs.get("identifier", None)

        params = {}
        options = ["filter", "display", "sort", "limit", "id_shop", "id_group_shop"]
        for option in options:
            opt_value = kwargs.get(option, None)
            if opt_value is not None:
                if option == "filter":
                    for field_name, field_value in opt_value.items():
                        params.update({f"{option}[{field_name}]": field_value})
                elif option == "id_shop":
                    params.update({f"filter[{option}]": opt_value})
                elif option == "id_group_shop":
                    params.update({f"filter[{option}]": opt_value})
                elif option == "display":
                    if opt_value == "full":
                        params.update({option: opt_value})
                    else:
                        item_result = ""
                        for item in opt_value:
                            item_result = f"{item_result}{item},"
                        if item_result.endswith(","):
                            item_r = str(item_result[:-1])
                            item_result = item_r
                        item_result = f"[{item_result}]"
                        params.update({"display": item_result})
                elif option == "sort":
                    for field_name, field_value in opt_value:
                        params.update({option: f"{field_name}_{field_value}"})
                        break
                else:
                    params.update({option: opt_value})

        if resource is not None:
            url = f"{self.url}/{resource}"
            if schema in ["synopsis", "blank"]:
                response = requests.get(
                    url=url,
                    params={"schema": schema},
                    headers=self.headers,
                    auth=HTTPBasicAuth(self.api_key, ""),
                )
                self.__check_status_code(response.status_code, url)
                return self.hack_fix(response.content)
            else:
                if identifier is not None:
                    response = requests.get(
                        url=f"{url}/{identifier}",
                        headers=self.headers,
                        auth=HTTPBasicAuth(self.api_key, ""),
                    )
                    self.__check_status_code(
                        response.status_code, f"{url}/{identifier}"
                    )
                    return self.hack_fix(response.content)
                else:
                    response = requests.get(
                        url=url,
                        params=params,
                        headers=self.headers,
                        auth=HTTPBasicAuth(self.api_key, ""),
                    )
                    self.__check_status_code(response.status_code, url)
                    return self.hack_fix(response.content)

    def head(self, **kwargs):
        resource = kwargs.get("resource", None)
        identifier = kwargs.get("identifier", None)
        params = {}
        options = ["filter", "display", "sort", "limit"]
        for option in options:
            opt_value = kwargs.get(option, None)
            if opt_value is not None:
                if option == "filter":
                    for field_name, field_value in opt_value.items():
                        params.update({f"{option}[{field_name}]": field_value})
                elif option == "display":
                    if opt_value == "full":
                        params.update({option: opt_value})
                    else:
                        item_result = ""
                        for item in opt_value:
                            item_result = f"{item_result}{item},"
                        if item_result.endswith(","):
                            item_r = str(item_result[:-1])
                            item_result = item_r
                        item_result = f"{item_result}]"
                        params.update({"display": item_result})
                elif option == "sort":
                    for field_name, field_value in opt_value:
                        params.update({option: f"{field_name}_{field_value}"})
                        break
                else:
                    params.update({option: opt_value})
        if resource is not None:
            url = f"{self.url}/{resource}"
            if identifier is not None:
                response = requests.head(
                    url=f"{url}/{identifier}",
                    headers=self.headers,
                    auth=HTTPBasicAuth(self.api_key, ""),
                )
                self.__check_status_code(response.status_code, f"{url}/{identifier}")
                return self.hack_fix(response.content)
            else:
                response = requests.head(
                    url=url,
                    params=params,
                    headers=self.headers,
                    auth=HTTPBasicAuth(self.api_key, ""),
                )
                self.__check_status_code(response.status_code, url)
                return self.hack_fix(response.content)

    def edit(self, **kwargs):
        resource = kwargs.get("resource", None)
        if resource is not None:
            url = f"{self.url}/{resource}"
            identifier = kwargs.get("identifier", None)
            id_shop = kwargs.get("id_shop", None)
            id_group_shop = kwargs.get("id_group_shop", None)
            data = kwargs.get("data", None)
            params = {}
            if id_shop is not None:
                params.update({"id_shop": id_shop})
            if id_group_shop is not None:
                params.update({"id_group_shop": id_group_shop})
            if identifier is not None:
                response = requests.put(
                    url=f"{url}/{identifier}",
                    params=params,
                    headers=self.headers,
                    data=data,
                    auth=HTTPBasicAuth(self.api_key, ""),
                )
                self.__check_status_code(response.status_code)
                return self.hack_fix(response.content)
            else:
                raise PrestashopGatewayException(self.__EXCEPTION_MESSAGES.get(2))

        else:
            raise PrestashopGatewayException(self.__EXCEPTION_MESSAGES.get(1))

    def delete(self, **kwargs):
        resource = kwargs.get("resource", None)
        if resource is not None:
            url = f"{self.url}/{resource}"
            identifier = kwargs.get("identifier", None)
            id_shop = kwargs.get("id_shop", None)
            id_group_shop = kwargs.get("id_group_shop", None)
            params = {}
            if id_shop is not None:
                params.update({"id_shop": id_shop})
            if id_group_shop is not None:
                params.update({"id_group_shop": id_group_shop})
            if identifier is not None:
                response = requests.delete(
                    url=f"{url}/{identifier}",
                    params=params,
                    headers=self.headers,
                    auth=HTTPBasicAuth(self.api_key, ""),
                )
                self.__check_status_code(response.status_code)
                return self.hack_fix(response.content)
            else:
                raise PrestashopGatewayException(self.__EXCEPTION_MESSAGES.get(2))

        else:
            raise PrestashopGatewayException(self.__EXCEPTION_MESSAGES.get(1))
