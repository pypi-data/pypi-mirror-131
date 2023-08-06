
class Api_BaseException(Exception):
    pass


class http_errors(Api_BaseException):
    """
    http返回并非200，201等。
    """
    def __init__(self, status_code: int):
        self.status_code: int = status_code
        self.details: str = ""

    def __repr__(self):
        match self.status_code:
            case 403:
                self.details = "APIKEY无效，或无权操作这个API！"
            case 500:
                self.details = "API访问受限!"
            case 502:
                self.details = "远程API执行出错!"
            case 504:
                self.details = "NGINX到API服务器超时!"
            case 444:
                self.details = "访问过于频繁，被远端服务器限制！"
            case 900:
                self.details = "连接超时!"
            case 901:
                self.details = "JSON解析失败!"
            case _:
                self.details = f"未知错误 {self.status_code}"
        return f'<HttpFailed, status_code={self.status_code}, details={self.details}>'

    def __str__(self):
        return self.__repr__()


class api_errors(Api_BaseException):
    """
    http返回201等，
    """
    def __init__(self, Code: int, Error):
        self.code: int = Code
        self.Error: str = str(Error)
        self.solution: str = ""
        self.error_final: str = "暂无解决方案!"
        self.uni_code: int = 0

    def __repr__(self):
        match (self.code, self.Error):
            case 404, "没有找到这个玩家喵!":
                self.error_final = "无法找到该ID对应的玩家"
                self.uni_code = 10404
            case -34501, "找不到这一服务器":
                self.error_final = "该GameId无法找到相对应的服务器!"
                self.uni_code = 10500
            case -1, "找不到任何服务器!":
                self.error_final = "无法搜索到这个服务器!"
                self.uni_code = 10501
            case -1, "not found":
                self.error_final = "该服务器目前未检测到开启，如果确定开, 请尝试调用 .查服务器 指令!"
                self.uni_code = 10600
            case _:
                self.error_final = self.Error
                self.uni_code = self.code
        return f'<ApiError, code={self.code}, Error={self.Error}, error_final={self.error_final}, uni_code={self.uni_code}, ' \
               f'solution={self.solution}>'

    def __str__(self):
        return self.__repr__()



