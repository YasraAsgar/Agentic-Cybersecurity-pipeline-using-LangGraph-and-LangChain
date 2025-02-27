import re

class ScopeEnforcer:
    def __init__(self, allowed_domains, allowed_ips):
        self.allowed_domains = allowed_domains
        self.allowed_ips = allowed_ips

    def is_in_scope(self, target):
        for domain in self.allowed_domains:
            if target.endswith(domain):
                return True
        for ip in self.allowed_ips:
            if re.match(ip, target):
                return True
        return False
