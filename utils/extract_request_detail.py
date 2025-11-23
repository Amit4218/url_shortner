from user_agents import parse


class RequestExtractor:

    def __init__(self, requset) -> None:
        self.request = requset
        self.user_agent_string = self.request.headers.get("User-Agent")
        self.user_agent = parse(self.user_agent_string)

    def extract_request_details(self, key=None):
        """extracts information from the request header of the User-Agent"""
        normal_ip = self.request.remote_addr

        if normal_ip == "127.0.0.1" or normal_ip == None:
            normal_ip = self.request.headers.get(
                "X-Forwarded-For", self.request.remote_addr
            )

        info = {
            "browser": self.user_agent.browser.family,
            "os": self.user_agent.os.family,
            "device_type": self.user_agent.device.family,
            "is_mobile": self.user_agent.is_mobile,
            "is_tablet": self.user_agent.is_tablet,
            "is_pc": self.user_agent.is_pc,
            "ip_address": normal_ip,
        }

        if not key:
            return info

        return info[key]

    def get(self, key):
        """returns the value from the request object based on the key"""
        return self.extract_request_details(key=key)
