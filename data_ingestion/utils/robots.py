class RobotsParser:
    """Provides methods to process robots.txt
    """

    from urllib.robotparser import RobotFileParser

    def __init__(self, robots_url):
        self.robots_url = robots_url
        self.user_agent = 'bot'

    def parse_robots_txt(self):
        print(f"Parsing robots.txt at {self.robots_url}")
        self.rp = self.RobotFileParser()
        self.rp.set_url(self.robots_url)
        self.rp.read()
        print("robots.txt parsed")
    
    def is_allowed(self, path) -> bool:
        return self.rp.can_fetch(self.user_agent, path)
    
    def get_delay(self) -> float:
        return self.rp.crawl_delay(self.user_agent)