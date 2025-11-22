import numpy as np
import random


class AttackProfile:
    def __init__(self):
        self.bot_count = 10000
        self.requests_per_bot = 10
        self.duration = 180
        self.complexity = 2
        self.protocol_power = 1.0
        self.current_pattern = "steady"
        self.attack_type = "HTTP Flood"
        self.protocol = "HTTP"
        self.hurst_parameter = 0.75
        self.traffic_mode = "pps"
        self.channel_bandwidth = 1000
        self.target_utilization = 60
        self.burstiness = 3.0
        self.packet_size = 512
        self.packet_ttl = 64
        self.destination_ports = [80, 443]
        
    def configure_from_custom(self, params, ip_manager=None):
        self.bot_count = params["botnet_size"]
        self.requests_per_bot = params.get("requests_per_bot", 10)
        self.duration = params["attack_duration"]
        self.complexity = params.get("complexity", 2)
        self.protocol_power = params.get("protocol_power", 1.0)
        self.hurst_parameter = params.get("hurst_parameter", 0.75)
        self.traffic_mode = params.get("traffic_intensity_mode", "pps")
        self.channel_bandwidth = params.get("channel_bandwidth", 1000)
        self.target_utilization = params.get("channel_utilization", 60)
        self.burstiness = params.get("burstiness_level", 3.0)
        self.packet_size = params.get("packet_size", 512)
        self.packet_ttl = params.get("ttl", 64)
        self.attack_type = params.get("attack_type", "HTTP Flood")
        self.protocol = params.get("protocol", "HTTP")
        
    def generate_attack_volume(self, time_elapsed):
        base_volume = self.bot_count * self.requests_per_bot
        
        hurst_factor = 1.0 + (self.hurst_parameter - 0.5) * 2.0
        fractal_component = np.sin(time_elapsed * 0.1) * 0.3 * hurst_factor
        
        if time_elapsed < 30:
            progress = time_elapsed / 30
            phase_multiplier = 0.2 + progress * 0.8
        elif time_elapsed < self.duration - 30:
            base_phase = 0.8
            random_variation = random.random() * 0.4
            phase_multiplier = base_phase + random_variation
            
            if time_elapsed % random.randint(20, 40) < 5:
                phase_multiplier *= self.burstiness
        else:
            progress = (self.duration - time_elapsed) / 30
            phase_multiplier = progress * 0.6
        
        complexity_factor = 1 + (self.complexity - 1) * 0.3
        
        protocol_multiplier = self.protocol_power
        
        attack_power = base_volume * (1 + fractal_component) * phase_multiplier * complexity_factor * protocol_multiplier
        
        return {
            "volume": min(attack_power, 500000),
            "fractal_component": fractal_component,
            "phase_multiplier": phase_multiplier,
            "burst_multiplier": self.burstiness if phase_multiplier > 2.0 else 1.0
        }

class DefenseConfiguration:
    def __init__(self, hardware_manager):
        self.hardware_manager = hardware_manager
        self.hardware_profile_id = "soho-i5-11400"
        self.hardware_profile = None
        self.cloudflare_level = 0
        self.waf_level = 0
        self.rate_limiting = 0
        self.behavior_analysis = 0
        self.geo_filtering = False
        self.ip_reputation = False
        self.captcha_enabled = False
        
        self._update_hardware_profile()
        
    def _update_hardware_profile(self):
        self.hardware_profile = self.hardware_manager.get_profile(self.hardware_profile_id)
        
    def configure_from_custom(self, params):
        self.hardware_profile_id = params.get("hardware_profile", "soho-i5-11400")
        self.cloudflare_level = params.get("cloudflare_level", 0)
        self.waf_level = params.get("waf_level", 0)
        self.rate_limiting = params.get("rate_limiting", 0)
        self.behavior_analysis = params.get("behavior_analysis", 0)
        self.geo_filtering = params.get("geo_filtering_enabled", False)
        self.ip_reputation = params.get("ip_reputation_enabled", False)
        self.captcha_enabled = params.get("captcha_enabled", False)
        
        self._update_hardware_profile()
        
    def calculate_defense_efficiency(self, attack_volume):
        if not self.hardware_profile:
            return {"efficiency": 0.3, "bottlenecks": ["unknown"]}
            
        max_capacity = self.hardware_profile.calculate_max_pps()
        utilization = attack_volume / max_capacity
        
        if utilization < 0.7:
            base_efficiency = 0.3
        elif utilization < 1.0:
            base_efficiency = 0.5
        else:
            base_efficiency = 0.2
            
        total_efficiency = base_efficiency
        
        if self.cloudflare_level > 0:
            cloudflare_efficiency = 0.3 + (self.cloudflare_level - 1) * 0.2
            total_efficiency += cloudflare_efficiency
            
        if self.waf_level > 0:
            waf_efficiency = 0.15 + (self.waf_level - 1) * 0.1
            total_efficiency += waf_efficiency
            
        if self.rate_limiting > 0:
            rate_efficiency = 0.1 + (self.rate_limiting - 1) * 0.05
            total_efficiency += rate_efficiency
            
        if self.behavior_analysis > 0:
            behavior_efficiency = 0.08
            total_efficiency += behavior_efficiency
            
        if self.geo_filtering:
            total_efficiency += 0.1
            
        if self.ip_reputation:
            total_efficiency += 0.07
            
        if self.captcha_enabled:
            total_efficiency += 0.05
            
        bottlenecks = []
        cpu_util = min(100, (attack_volume / max_capacity) * 100)
        
        if cpu_util > 80:
            bottlenecks.append("CPU")
            
        nic_util = min(100, (attack_volume / (self.hardware_profile.calculate_network_capacity() * 100000)) * 100)
        if nic_util > 80:
            bottlenecks.append("NIC")
            
        memory_pressure = (attack_volume * 1500 * 100) / (self.hardware_profile.ram_GB * 1024 * 1024 * 1024) * 100
        if memory_pressure > 70:
            bottlenecks.append("Memory")
            
        return {
            "efficiency": min(total_efficiency, 0.95),
            "bottlenecks": bottlenecks,
            "cpu_utilization": cpu_util,
            "nic_utilization": nic_util,
            "memory_pressure": memory_pressure,
            "hardware_profile": self.hardware_profile.model if self.hardware_profile else "Unknown"
        }

class DDoSSimulationEngine:
    def __init__(self):
        from hardware_profiles import HardwareProfileManager
        
        self.hardware_manager = HardwareProfileManager()
        self.attack_profile = AttackProfile()
        self.defense_config = DefenseConfiguration(self.hardware_manager)
        self.business_calc = BusinessImpactCalculator()
        
        self.time_records = []
        self.attack_volume_records = []
        self.server_load_records = []
        self.financial_impact_records = []
        self.defense_efficiency_records = []
        self.bottleneck_records = []
        self.channel_utilization_records = []
        self.fractal_component_records = []
        
        self.current_time = 0
        self.attack_active = False
        self.simulation_complete = False
        self.cumulative_financial_impact = 0
        
        self.learning_points = []
        
    def configure_custom_scenario(self, attack_params, defense_params, business_type, ip_pool_config=None):
        self.attack_profile.configure_from_custom(attack_params)
        self.defense_config.configure_from_custom(defense_params)
        self.business_calc.current_business = business_type
        
    def start_simulation(self):
        self.attack_active = True
        self.simulation_complete = False
        self.current_time = 0
        self.cumulative_financial_impact = 0
        self.learning_points = []
        
        self.time_records.clear()
        self.attack_volume_records.clear()
        self.server_load_records.clear()
        self.financial_impact_records.clear()
        self.defense_efficiency_records.clear()
        self.bottleneck_records.clear()
        self.channel_utilization_records.clear()
        self.fractal_component_records.clear()
    
    def execute_simulation_step(self):
        if not self.attack_active:
            return
            
        self.current_time += 1
        self.time_records.append(self.current_time)
        
        attack_data = self.attack_profile.generate_attack_volume(self.current_time)
        attack_volume = attack_data["volume"]
        self.attack_volume_records.append(attack_volume)
        self.fractal_component_records.append(attack_data["fractal_component"])
        
        max_channel_capacity = self.attack_profile.channel_bandwidth * 1000
        current_utilization = min(100, (attack_volume * 1500 * 8) / (max_channel_capacity * 1000000) * 100)
        self.channel_utilization_records.append(current_utilization)
        
        defense_data = self.defense_config.calculate_defense_efficiency(attack_volume)
        defense_efficiency = defense_data["efficiency"]
        self.defense_efficiency_records.append(defense_efficiency)
        self.bottleneck_records.append(defense_data["bottlenecks"])
        
        blocked_volume = attack_volume * defense_efficiency
        effective_attack = attack_volume - blocked_volume
        
        max_capacity = self.defense_config.hardware_profile.calculate_max_pps() if self.defense_config.hardware_profile else 30000
        server_load = min(100, (effective_attack / max_capacity) * 100)
        self.server_load_records.append(server_load)
        
        current_impact = self.business_calc.calculate_financial_impact(
            server_load, attack_volume, 1/60
        )
        self.cumulative_financial_impact += current_impact
        self.financial_impact_records.append(self.cumulative_financial_impact)
        
        self._generate_advanced_learning_points(server_load, defense_data, attack_volume)
        
        if self.current_time >= self.attack_profile.duration:
            self.attack_active = False
            self.simulation_complete = True
    
    def _generate_advanced_learning_points(self, server_load, defense_data, attack_volume):
        points = []
        
        bottlenecks = defense_data.get("bottlenecks", [])
        hardware_model = defense_data.get("hardware_profile", "")
        
        if "CPU" in bottlenecks and "cpu_bottleneck" not in self.learning_points:
            points.append(f"💻 Нехватка CPU на {hardware_model}! Увеличьте число ядер или тактовую частоту")
            
        if "NIC" in bottlenecks and "nic_bottleneck" not in self.learning_points:
            points.append(f"🌐 Нехватка NIC на {hardware_model}! Рассмотрите апгрейд сетевой карты")
            
        if "Memory" in bottlenecks and "memory_bottleneck" not in self.learning_points:
            points.append(f"💾 Нехватка Memory на {hardware_model}! Увеличьте объем RAM")
        
        if (server_load > 90 and "underpowered_hw" not in self.learning_points and 
            "edge" in hardware_model.lower()):
            points.append("🚨 Аппаратный профиль слишком слабый для такой нагрузки! Выберите серверный профиль")
            
        if (defense_data["efficiency"] < 0.3 and "fractal_inefficient" not in self.learning_points and
            self.attack_profile.hurst_parameter > 0.8):
            points.append("🎲 Высокий параметр Хёрста требует специализированной защиты от фрактальных атак")
            
        if (server_load > 80 and "need_cloudflare" not in self.learning_points and 
            self.defense_config.cloudflare_level == 0):
            points.append("☁️ Высокая нагрузка! Cloudflare снизит нагрузку на 70-80%")
            
        if (attack_volume > 50000 and "need_waf" not in self.learning_points and 
            self.defense_config.waf_level == 0):
            points.append("🔥 Мощная атака! WAF необходим для фильтрации вредоносных запросов")
        
        for point in points:
            if point not in self.learning_points:
                self.learning_points.append(point)

class BusinessImpactCalculator:
    def __init__(self):
        self.business_types = {
            "Блог": {"base_revenue": 2000, "risk_multiplier": 1.0},
            "Интернет-магазин": {"base_revenue": 15000, "risk_multiplier": 2.0},
            "Онлайн-банк": {"base_revenue": 50000, "risk_multiplier": 4.0},
            "Стриминговый сервис": {"base_revenue": 25000, "risk_multiplier": 2.5}
        }
        self.current_business = "Интернет-магазин"
        
    def calculate_financial_impact(self, server_load, attack_power, time_elapsed):
        business = self.business_types[self.current_business]
        base_revenue = business["base_revenue"]
        risk_multiplier = business["risk_multiplier"]
        
        if server_load > 95:
            load_multiplier = 3.0
        elif server_load > 80:
            load_multiplier = 2.0
        elif server_load > 50:
            load_multiplier = 1.2
        else:
            load_multiplier = 0.3
            
        attack_multiplier = 1 + (attack_power / 100000) * 0.5
        
        time_minutes = time_elapsed / 60
        
        financial_impact = (base_revenue * load_multiplier * 
                          risk_multiplier * attack_multiplier * time_minutes)
        
        return financial_impact

class ResultsProcessor:
    @staticmethod
    def generate_performance_report(simulation):
        if not simulation.time_records:
            return {
                "learning_points": ["Запустите симуляцию для получения результатов"],
                "final_status": "ОЖИДАНИЕ"
            }
            
        peak_load = max(simulation.server_load_records) if simulation.server_load_records else 0
        avg_efficiency = np.mean(simulation.defense_efficiency_records) if simulation.defense_efficiency_records else 0
        
        if peak_load < 80:
            status = "✅ УСПЕШНАЯ ЗАЩИТА"
            status_color = "green"
        elif peak_load < 95:
            status = "⚠️ ЧАСТИЧНЫЙ СБОЙ" 
            status_color = "orange"
        else:
            status = "💥 КРИТИЧЕСКИЙ СБОЙ"
            status_color = "red"
            
        report = {
            'duration': simulation.current_time,
            'peak_attack_volume': max(simulation.attack_volume_records) if simulation.attack_volume_records else 0,
            'peak_server_load': peak_load,
            'average_efficiency': avg_efficiency,
            'financial_impact': simulation.cumulative_financial_impact,
            'learning_points': simulation.learning_points,
            'final_status': status,
            'status_color': status_color
        }
        
        if not report['learning_points']:
            report['learning_points'] = ["💡 Попробуйте разные комбинации защиты для оптимизации"]
            
        return report