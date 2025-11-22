import random
import json
from typing import List, Dict, Any

class IPPool:
    def __init__(self, pool_config: Dict[str, Any]):
        self.pool_id = pool_config.get("pool_id", "")
        self.name = pool_config.get("name", "")
        self.address_ranges = pool_config.get("address_ranges", [])
        self.tags = pool_config.get("tags", [])
        self.mode = pool_config.get("mode", "static")
        self.rotation_interval = pool_config.get("rotation_interval_sec", 300)
        self.max_reuse_count = pool_config.get("max_reuse_count", 3)
        self.allow_spoofing = pool_config.get("allow_spoofing", False)
        self.seed = pool_config.get("seed", 42)
        
        self.geo_distribution = pool_config.get("geo_distribution", [
            {"region": "EU", "percent": 40},
            {"region": "NA", "percent": 30},
            {"region": "AS", "percent": 20},
            {"region": "OTHER", "percent": 10}
        ])
        
        self.asn_distribution = pool_config.get("asn_distribution", [])
        
        random.seed(self.seed)
        self.generated_ips = self._generate_ips_with_metadata()
        self.ip_usage_count = {}
        self.ip_quarantine = {}
        self.bot_ip_mapping = {}
        
    def _generate_ips_with_metadata(self) -> List[Dict[str, Any]]:
        ips_with_metadata = []
        
        for range_str in self.address_ranges:
            if '/' in range_str:
                base_ips = self._generate_ips_from_cidr(range_str)
            else:
                base_ips = [range_str]
                
            for ip in base_ips:
                metadata = self._generate_ip_metadata(ip)
                ips_with_metadata.append({
                    "ip": ip,
                    "geo": metadata["geo"],
                    "asn": metadata["asn"],
                    "org": metadata["org"]
                })
                
        return ips_with_metadata
    
    def _generate_ips_from_cidr(self, cidr: str) -> List[str]:
        base_ip, mask = cidr.split('/')
        mask = int(mask)
        
        if mask >= 24:
            base_parts = list(map(int, base_ip.split('.')))
            network_size = 2 ** (32 - mask)
            ips = []
            
            for i in range(1, network_size - 1):
                new_ip = f"{base_parts[0]}.{base_parts[1]}.{base_parts[2]}.{base_parts[3] + i}"
                ips.append(new_ip)
                
            return ips
        else:
            return [base_ip]
    
    def _generate_ip_metadata(self, ip: str) -> Dict[str, Any]:
        region_roll = random.random() * 100
        current_percent = 0
        
        for geo in self.geo_distribution:
            current_percent += geo["percent"]
            if region_roll <= current_percent:
                region = geo["region"]
                break
        else:
            region = "OTHER"
            
        asn_org_map = {
            "EU": {"asn_range": (3209, 3299), "orgs": ["Deutsche Telekom", "Orange", "Telefonica"]},
            "NA": {"asn_range": (7018, 7099), "orgs": ["AT&T", "Verizon", "Comcast"]},
            "AS": {"asn_range": (4760, 4799), "orgs": ["China Telecom", "NTT", "SingTel"]},
            "OTHER": {"asn_range": (9000, 9099), "orgs": ["Global Network", "Regional ISP"]}
        }
        
        region_info = asn_org_map.get(region, asn_org_map["OTHER"])
        asn = random.randint(*region_info["asn_range"])
        org = random.choice(region_info["orgs"])
        
        return {
            "geo": {"region": region, "country": self._get_random_country(region)},
            "asn": asn,
            "org": org
        }
    
    def _get_random_country(self, region: str) -> str:
        countries = {
            "EU": ["DE", "FR", "GB", "IT", "ES", "NL", "PL"],
            "NA": ["US", "CA", "MX"],
            "AS": ["CN", "JP", "KR", "SG", "IN"],
            "OTHER": ["AU", "BR", "ZA", "RU"]
        }
        return random.choice(countries.get(region, ["US"]))
    
    def get_ip_for_bot(self, bot_id: str, current_time: int) -> Dict[str, Any]:
        if self.mode == "static":
            ip_data = self._get_static_ip(bot_id)
        elif self.mode == "rotating":
            ip_data = self._get_rotating_ip(bot_id, current_time)
        elif self.mode == "random":
            ip_data = self._get_random_ip(bot_id)
        elif self.mode == "spoofed":
            ip_data = self._get_spoofed_ip(bot_id)
        else:
            ip_data = self._get_static_ip(bot_id)
            
        self.bot_ip_mapping[bot_id] = ip_data
        return ip_data
    
    def _get_static_ip(self, bot_id: str) -> Dict[str, Any]:
        if bot_id not in self.ip_usage_count:
            ip_index = hash(bot_id) % len(self.generated_ips)
            ip_data = self.generated_ips[ip_index].copy()
            self.ip_usage_count[bot_id] = {"ip_data": ip_data, "count": 1}
        return self.ip_usage_count[bot_id]["ip_data"]
    
    def _get_rotating_ip(self, bot_id: str, current_time: int) -> Dict[str, Any]:
        if (bot_id not in self.ip_usage_count or 
            current_time - self.ip_usage_count[bot_id].get("last_rotation", 0) >= self.rotation_interval):
            
            available_ips = [ip for ip in self.generated_ips 
                           if ip["ip"] not in self.ip_quarantine or 
                           current_time - self.ip_quarantine[ip["ip"]] > self.rotation_interval]
            
            if available_ips:
                new_ip_data = random.choice(available_ips).copy()
                self.ip_usage_count[bot_id] = {
                    "ip_data": new_ip_data, 
                    "count": self.ip_usage_count.get(bot_id, {}).get("count", 0) + 1,
                    "last_rotation": current_time
                }
                
                old_ip = self.ip_usage_count.get(bot_id, {}).get("ip_data", {}).get("ip")
                if old_ip and self.ip_usage_count[bot_id]["count"] > self.max_reuse_count:
                    self.ip_quarantine[old_ip] = current_time
                    
        return self.ip_usage_count[bot_id]["ip_data"]
    
    def _get_random_ip(self, bot_id: str) -> Dict[str, Any]:
        return random.choice(self.generated_ips).copy()
    
    def _get_spoofed_ip(self, bot_id: str) -> Dict[str, Any]:
        ip_data = random.choice(self.generated_ips).copy()
        ip_data["spoofed"] = True
        return ip_data

class IPManager:
    def __init__(self):
        self.pools = {}
        self.bot_pool_mapping = {}
        
    def create_pool(self, pool_config: Dict[str, Any]):
        pool = IPPool(pool_config)
        self.pools[pool.pool_id] = pool
        return pool
    
    def assign_pool_to_bots(self, pool_id: str, bot_ids: List[str]):
        for bot_id in bot_ids:
            self.bot_pool_mapping[bot_id] = pool_id
    
    def get_bot_ip(self, bot_id: str, current_time: int) -> Dict[str, Any]:
        pool_id = self.bot_pool_mapping.get(bot_id)
        if pool_id and pool_id in self.pools:
            return self.pools[pool_id].get_ip_for_bot(bot_id, current_time)
        else:
            return {
                "ip": f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}",
                "geo": {"region": "OTHER", "country": "US"},
                "asn": 65534,
                "org": "Generic ISP"
            }
    
    def get_pool_statistics(self, pool_id: str) -> Dict[str, Any]:
        if pool_id not in self.pools:
            return {}
            
        pool = self.pools[pool_id]
        return {
            "total_ips": len(pool.generated_ips),
            "active_bots": len(pool.bot_ip_mapping),
            "quarantined_ips": len(pool.ip_quarantine),
            "geo_distribution": pool.geo_distribution
        }