import numpy as np
import random
from typing import Dict, List, Any
from enum import Enum

class AttackType(Enum):
    HTTP_FLOOD = "HTTP Flood"
    SYN_FLOOD = "SYN Flood" 
    UDP_FLOOD = "UDP Flood"
    ICMP_FLOOD = "ICMP Flood"
    SLOWLORIS = "Slowloris"
    DNS_AMPLIFICATION = "DNS Amplification"
    SSL_RENEGOTIATION = "SSL Renegotiation"
    MIXED_ATTACK = "Mixed Attack"

class ProtocolType(Enum):
    TCP = "TCP"
    UDP = "UDP" 
    ICMP = "ICMP"
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    DNS = "DNS"

class BotnetDistribution:    
    def __init__(self):
        self.distributions = {
            "iot_devices": {
                "percentage": 40,
                "profile": "low_power",
                "characteristics": {
                    "requests_per_second": 2,
                    "connection_rate": 1,
                    "packet_size": 512
                }
            },
            "residential_ips": {
                "percentage": 35, 
                "profile": "medium_power",
                "characteristics": {
                    "requests_per_second": 5,
                    "connection_rate": 3,
                    "packet_size": 1024
                }
            },
            "servers": {
                "percentage": 15,
                "profile": "high_power", 
                "characteristics": {
                    "requests_per_second": 20,
                    "connection_rate": 10,
                    "packet_size": 1500
                }
            },
            "cloud_instances": {
                "percentage": 10,
                "profile": "very_high_power",
                "characteristics": {
                    "requests_per_second": 50,
                    "connection_rate": 25, 
                    "packet_size": 1500
                }
            }
        }

class AttackEngine:    
    def __init__(self):
        self.attack_type = AttackType.HTTP_FLOOD
        self.protocol = ProtocolType.HTTP
        self.botnet_distribution = BotnetDistribution()
        self.attack_parameters = {}
        
    def configure_attack(self, attack_config: Dict[str, Any]):
        self.attack_type = AttackType(attack_config.get("attack_type", "HTTP Flood"))
        self.protocol = ProtocolType(attack_config.get("protocol", "HTTP"))
        
        self.attack_parameters = {
            "packet_size": attack_config.get("packet_size", 1500),
            "ttl": attack_config.get("ttl", 64),
            "source_ports": attack_config.get("source_ports", "random"),
            "destination_ports": attack_config.get("destination_ports", [80, 443]),
            "http_methods": attack_config.get("http_methods", ["GET", "POST"]),
            "user_agents": attack_config.get("user_agents", []),
            "referrers": attack_config.get("referrers", []),
            "encryption_level": attack_config.get("encryption_level", 0)  # 0-3
        }
        
    def generate_attack_pattern(self, time_elapsed: int, total_duration: int) -> Dict[str, Any]:
        
        base_pattern = self._get_base_pattern()
        phase_multiplier = self._get_phase_multiplier(time_elapsed, total_duration)
        burst_multiplier = self._get_burst_multiplier(time_elapsed)
        
        total_intensity = base_pattern["base_intensity"] * phase_multiplier * burst_multiplier
        
        distributed_attack = self._distribute_by_botnet_type(total_intensity)
        
        return {
            **distributed_attack,
            "attack_type": self.attack_type.value,
            "protocol": self.protocol.value,
            "phase_multiplier": phase_multiplier,
            "burst_multiplier": burst_multiplier,
            "packet_characteristics": self._get_packet_characteristics()
        }
    
    def _get_base_pattern(self) -> Dict[str, Any]:
        patterns = {
            AttackType.HTTP_FLOOD: {
                "base_intensity": 10000,
                "connections_per_second": 5000,
                "requests_per_connection": 2,
                "pattern": "steady"
            },
            AttackType.SYN_FLOOD: {
                "base_intensity": 50000, 
                "connections_per_second": 25000,
                "requests_per_connection": 1,
                "pattern": "bursty"
            },
            AttackType.UDP_FLOOD: {
                "base_intensity": 75000,
                "connections_per_second": 0,
                "requests_per_connection": 1, 
                "pattern": "volumetric"
            },
            AttackType.SLOWLORIS: {
                "base_intensity": 1000,
                "connections_per_second": 800,
                "requests_per_connection": 0.1,
                "pattern": "slow"
            }
        }
        return patterns.get(self.attack_type, patterns[AttackType.HTTP_FLOOD])
    
    def _get_phase_multiplier(self, time_elapsed: int, total_duration: int) -> float:
        progress = time_elapsed / total_duration
        
        if progress < 0.1:
            return 0.1 + progress * 0.9
        elif progress < 0.3:
            return 1.0 + (progress - 0.1) * 2.0
        elif progress < 0.7:
            return 1.8 + random.random() * 0.4
        elif progress < 0.9:
            return 2.5 + random.random() * 0.5
        else:
            return (1.0 - (progress - 0.9) * 10) * 2.0
    
    def _get_burst_multiplier(self, time_elapsed: int) -> float:
        if time_elapsed % random.randint(30, 60) < 10:
            return 2.0 + random.random() * 3.0
        return 1.0
    
    def _distribute_by_botnet_type(self, total_intensity: float) -> Dict[str, Any]:
        distribution = self.botnet_distribution.distributions
        result = {
            "total_intensity": total_intensity,
            "components": {}
        }
        
        for bot_type, config in distribution.items():
            percentage = config["percentage"] / 100.0
            characteristics = config["characteristics"]
            
            component_intensity = total_intensity * percentage
            result["components"][bot_type] = {
                "intensity": component_intensity,
                "requests_per_second": characteristics["requests_per_second"],
                "connection_rate": characteristics["connection_rate"],
                "packet_size": characteristics["packet_size"]
            }
            
        return result
    
    def _get_packet_characteristics(self) -> Dict[str, Any]:
        return {
            "size_variation": random.randint(
                max(64, self.attack_parameters["packet_size"] - 100),
                self.attack_parameters["packet_size"] + 100
            ),
            "ttl_variation": max(1, self.attack_parameters["ttl"] - random.randint(0, 10)),
            "protocol_specific": self._get_protocol_specific_headers()
        }
    
    def _get_protocol_specific_headers(self) -> Dict[str, Any]:
        if self.protocol in [ProtocolType.HTTP, ProtocolType.HTTPS]:
            return {
                "method": random.choice(self.attack_parameters["http_methods"]),
                "user_agent": self._get_random_user_agent(),
                "referrer": random.choice(self.attack_parameters["referrers"]) if self.attack_parameters["referrers"] else "",
                "accept_encoding": "gzip, deflate",
                "accept_language": "en-US,en;q=0.9"
            }
        elif self.protocol == ProtocolType.TCP:
            return {
                "flags": "SYN",
                "window_size": random.randint(1024, 65535),
                "mss": 1460
            }
        return {}
    
    def _get_random_user_agent(self) -> str:
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/537.36"
        ]
        return random.choice(user_agents)

class DefenseEngine:    
    def __init__(self):
        self.defense_mechanisms = {}
        self.defense_config = {}
        
    def configure_defense(self, defense_config: Dict[str, Any]):
        self.defense_config = defense_config
        
        self.defense_mechanisms = {
            "rate_limiting": {
                "enabled": defense_config.get("rate_limiting_enabled", False),
                "requests_per_second": defense_config.get("rate_limit_rps", 100),
                "connections_per_second": defense_config.get("rate_limit_cps", 50),
                "burst_size": defense_config.get("rate_limit_burst", 200)
            },
            "geo_filtering": {
                "enabled": defense_config.get("geo_filtering_enabled", False),
                "allowed_regions": defense_config.get("allowed_regions", ["EU", "NA"]),
                "blocked_countries": defense_config.get("blocked_countries", [])
            },
            "ip_reputation": {
                "enabled": defense_config.get("ip_reputation_enabled", False),
                "blacklist": defense_config.get("ip_blacklist", []),
                "whitelist": defense_config.get("ip_whitelist", []),
                "asn_blocking": defense_config.get("asn_blocking", [])
            },
            "behavioral_analysis": {
                "enabled": defense_config.get("behavioral_analysis_enabled", False),
                "anomaly_detection": defense_config.get("anomaly_detection", True),
                "learning_period": defense_config.get("learning_period", 300)
            },
            "waf_rules": {
                "enabled": defense_config.get("waf_enabled", False),
                "sql_injection": defense_config.get("waf_sql_injection", True),
                "xss_protection": defense_config.get("waf_xss", True),
                "path_traversal": defense_config.get("waf_path_traversal", True)
            },
            "captcha_challenge": {
                "enabled": defense_config.get("captcha_enabled", False),
                "threshold": defense_config.get("captcha_threshold", 100),
                "difficulty": defense_config.get("captcha_difficulty", "medium")
            }
        }
    
    def analyze_traffic(self, traffic_data: Dict[str, Any], current_time: int) -> Dict[str, Any]:
        
        analysis_result = {
            "blocked_traffic": 0,
            "allowed_traffic": 0,
            "challenged_traffic": 0,
            "block_reasons": [],
            "defense_metrics": {}
        }
        
        total_intensity = traffic_data["total_intensity"]
        
        if self.defense_mechanisms["geo_filtering"]["enabled"]:
            geo_blocked = self._apply_geo_filtering(traffic_data, total_intensity)
            total_intensity -= geo_blocked
            analysis_result["blocked_traffic"] += geo_blocked
            if geo_blocked > 0:
                analysis_result["block_reasons"].append("Geo-filtering")
        
        if self.defense_mechanisms["ip_reputation"]["enabled"]:
            reputation_blocked = self._apply_ip_reputation(traffic_data, total_intensity)
            total_intensity -= reputation_blocked
            analysis_result["blocked_traffic"] += reputation_blocked
            if reputation_blocked > 0:
                analysis_result["block_reasons"].append("IP Reputation")
        
        if self.defense_mechanisms["rate_limiting"]["enabled"]:
            rate_limited = self._apply_rate_limiting(traffic_data, total_intensity)
            total_intensity -= rate_limited
            analysis_result["blocked_traffic"] += rate_limited
            if rate_limited > 0:
                analysis_result["block_reasons"].append("Rate Limiting")
        
        if self.defense_mechanisms["behavioral_analysis"]["enabled"]:
            behavioral_blocked = self._apply_behavioral_analysis(traffic_data, total_intensity, current_time)
            total_intensity -= behavioral_blocked
            analysis_result["blocked_traffic"] += behavioral_blocked
            if behavioral_blocked > 0:
                analysis_result["block_reasons"].append("Behavioral Analysis")
        
        if self.defense_mechanisms["waf_rules"]["enabled"]:
            waf_blocked = self._apply_waf_rules(traffic_data, total_intensity)
            total_intensity -= waf_blocked
            analysis_result["blocked_traffic"] += waf_blocked
            if waf_blocked > 0:
                analysis_result["block_reasons"].append("WAF Rules")
        
        if self.defense_mechanisms["captcha_challenge"]["enabled"]:
            captcha_traffic = self._apply_captcha_challenge(traffic_data, total_intensity)
            analysis_result["challenged_traffic"] = captcha_traffic
            total_intensity -= captcha_traffic * 0.8
        
        analysis_result["allowed_traffic"] = max(0, total_intensity)
        
        analysis_result["defense_metrics"] = self._calculate_defense_metrics(analysis_result)
        
        return analysis_result
    
    def _apply_geo_filtering(self, traffic_data: Dict[str, Any], intensity: float) -> float:
        allowed_regions = self.defense_mechanisms["geo_filtering"]["allowed_regions"]
        blocked_percentage = 0.2 if len(allowed_regions) < 3 else 0.05
        return intensity * blocked_percentage
    
    def _apply_ip_reputation(self, traffic_data: Dict[str, Any], intensity: float) -> float:
        reputation_blocked = 0.0
        
        if self.defense_mechanisms["ip_reputation"]["blacklist"]:
            reputation_blocked += intensity * 0.15
        
        if self.defense_mechanisms["ip_reputation"]["asn_blocking"]:
            reputation_blocked += intensity * 0.10
            
        return min(intensity, reputation_blocked)
    
    def _apply_rate_limiting(self, traffic_data: Dict[str, Any], intensity: float) -> float:
        rate_limit = self.defense_mechanisms["rate_limiting"]["requests_per_second"]
        
        if intensity <= rate_limit:
            return 0.0
        
        excess_traffic = intensity - rate_limit
        burst_allowance = self.defense_mechanisms["rate_limiting"]["burst_size"]
        
        if excess_traffic <= burst_allowance:
            return excess_traffic * 0.5
        else:
            return burst_allowance * 0.5 + (excess_traffic - burst_allowance) * 0.8
    
    def _apply_behavioral_analysis(self, traffic_data: Dict[str, Any], intensity: float, current_time: int) -> float:
        if current_time < self.defense_mechanisms["behavioral_analysis"]["learning_period"]:
            return 0.0
        
        behavioral_indicators = self._analyze_behavioral_indicators(traffic_data)
        
        anomaly_score = sum(behavioral_indicators.values()) / len(behavioral_indicators)
        return intensity * min(anomaly_score, 0.6)
    
    def _analyze_behavioral_indicators(self, traffic_data: Dict[str, Any]) -> Dict[str, float]:
        indicators = {
            "request_regularity": random.uniform(0.1, 0.8),  # Регулярность запросов
            "connection_persistence": random.uniform(0.1, 0.9),  # Постоянство соединений
            "geographic_dispersion": random.uniform(0.2, 0.7),  # Географическая дисперсия
            "user_agent_diversity": random.uniform(0.3, 0.9),  # Разнообразие User-Agent
            "request_entropy": random.uniform(0.1, 0.6)  # Энтропия запросов
        }
        return indicators
    
    def _apply_waf_rules(self, traffic_data: Dict[str, Any], intensity: float) -> float:
        waf_blocked = 0.0
        
        if self.defense_mechanisms["waf_rules"]["sql_injection"]:
            waf_blocked += intensity * 0.08
        
        if self.defense_mechanisms["waf_rules"]["xss_protection"]:
            waf_blocked += intensity * 0.05
            
        if self.defense_mechanisms["waf_rules"]["path_traversal"]:
            waf_blocked += intensity * 0.03
            
        return min(intensity, waf_blocked)
    
    def _apply_captcha_challenge(self, traffic_data: Dict[str, Any], intensity: float) -> float:
        threshold = self.defense_mechanisms["captcha_challenge"]["threshold"]
        
        if intensity > threshold:
            excess_traffic = intensity - threshold
            return min(excess_traffic, intensity * 0.3)
        
        return 0.0
    
    def _calculate_defense_metrics(self, analysis_result: Dict[str, Any]) -> Dict[str, float]:
        total_traffic = (analysis_result["blocked_traffic"] + 
                        analysis_result["allowed_traffic"] + 
                        analysis_result["challenged_traffic"])
        
        if total_traffic == 0:
            return {
                "block_rate": 0.0,
                "challenge_rate": 0.0,
                "false_positive_rate": 0.02,
                "overall_efficiency": 0.0
            }
        
        block_rate = analysis_result["blocked_traffic"] / total_traffic
        challenge_rate = analysis_result["challenged_traffic"] / total_traffic
        
        false_positive_rate = max(0.01, block_rate * 0.1)
        overall_efficiency = block_rate * (1 - false_positive_rate) + challenge_rate * 0.5
        
        return {
            "block_rate": block_rate,
            "challenge_rate": challenge_rate,
            "false_positive_rate": false_positive_rate,
            "overall_efficiency": min(overall_efficiency, 0.95)
        }