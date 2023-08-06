from .exceptions import http_errors, api_errors
import httpx
import json

class API(httpx.AsyncClient):
    def __init__(self, apikey: str, custom_url: str = None, http2: bool = False):
        """
        :param apikey: K-0N API的APIKEY
        :param custom_url: 是否自定义K-0N API的URL，默认情况为 https://api.k-0n.org/
        :param http2: 是否启用http2与api进行通讯，默认情况关闭。
        """
        self.http_client = super(API, self).__init__(headers={"apikey": apikey}, http2=http2)
        if custom_url:
            self.baseurl = custom_url
        else:
            self.baseurl = "https://api.k-0n.org/"

    async def do(self, route: str, json_value: dict = None, http_method: str = "POST", **kwargs) -> dict:
        """
        请求API
        :param route: 路径地址
        :param json_value: 是否传递JSON值，默认为否
        :param http_method: 选择HTTP传送方法，默认为POST
        :param kwargs: 其他参数作为路径参数传递.
        :return:
        """
        result = await super(API, self).request(http_method, self.baseurl + route, json=json_value, params=kwargs)
        try:
            if result.status_code not in (200, 201):
                raise http_errors(result.status_code)
            result = result.json()
            if not result["Status"]:
                raise api_errors(result["Data"]["Code"], result["Data"]["Error"])
        except json.JSONDecodeError:
            raise http_errors(901)
        except httpx.TimeoutException:
            raise http_errors(900)
        return result["Data"]

    async def origin_searchUser(self, displayName: str, onlyPersonaId: bool = True) -> int | dict:
        """
        :param displayName: 搜索的用户名
        :param onlyPersonaId: 是否只返回personaId
        :return: onlyPersonaId=True => int类型的personaId, 否则返回dict.
        """
        result = await self.do(f"origin/getPid/{displayName}", http_method="GET", details=True)
        if onlyPersonaId:
            return result["PersonaId"]
        return result



