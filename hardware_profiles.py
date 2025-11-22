import json
import numpy as np
from typing import List, Dict, Any

class HardwareProfile:
    def __init__(self, profile_data: Dict[str, Any]):
        self.profile_id = profile_data.get("profile_id", "")
        self.vendor = profile_data.get("vendor", "")
        self.model = profile_data.get("model", "")
        self.cores = profile_data.get("cores", 1)
        self.threads = profile_data.get("threads", 1)
        self.base_freq_GHz = profile_data.get("base_freq_GHz", 1.0)
        self.turbo_freq_GHz = profile_data.get("turbo_freq_GHz", 1.0)
        self.L1_cache_kB = profile_data.get("L1_cache_kB", 32)
        self.L2_cache_kB = profile_data.get("L2_cache_kB", 256)
        self.L3_cache_MB = profile_data.get("L3_cache_MB", 1)
        self.microarch = profile_data.get("microarch", "")
        self.simd_width = profile_data.get("simd_width", 128)
        self.hyperthreading = profile_data.get("hyperthreading", False)
        self.aes_instruction = profile_data.get("aes_instruction", False)
        self.memory_channels = profile_data.get("memory_channels", 1)
        self.memory_speed_MHz = profile_data.get("memory_speed_MHz", 2133)
        self.ram_GB = profile_data.get("ram_GB", 4)
        self.nic = profile_data.get("nic", [])
        self.disk = profile_data.get("disk", {})
        self.os = profile_data.get("os", {})
        self.category = profile_data.get("category", "unknown")
        
    def calculate_cpu_power(self, workload_type: str = "network") -> float:
        base_power = self.cores * self.base_freq_GHz
        
        arch_multiplier = 1.0
        if "Ice Lake" in self.microarch or "Zen 3" in self.microarch:
            arch_multiplier = 1.3
        elif "Cortex-A" in self.microarch:
            arch_multiplier = 0.7
            
        # Учет типа нагрузки
        workload_multiplier = 1.0
        if workload_type == "l7_http":
            workload_multiplier = 1.5
        elif workload_type == "crypto":
            workload_multiplier = 2.0 if self.aes_instruction else 3.0
            
        turbo_boost = (self.turbo_freq_GHz - self.base_freq_GHz) / self.base_freq_GHz
        cache_factor = 1 + (self.L3_cache_MB / 32) * 0.2
        
        return base_power * (1 + turbo_boost * 0.3) * cache_factor * arch_multiplier * workload_multiplier
    
    def calculate_max_pps(self, packet_size_bytes: int = 1500, workload_type: str = "network") -> float:
        cpu_pps = self.calculate_cpu_power(workload_type) * 150000
        
        nic_pps_total = 0
        for nic in self.nic:
            nic_speed_gbps = nic.get('speed_Gbps', 0)
            offload_factor = 1.0
            offloads = nic.get('offloads', [])
            if "TSO" in offloads and "GRO" in offloads:
                offload_factor = 0.3
            elif "RSS" in offloads:
                offload_factor = 0.7
                
            nic_pps = (nic_speed_gbps * 1e9) / (packet_size_bytes * 8) * offload_factor
            nic_pps_total += nic_pps
        
        memory_pps = (self.ram_GB * 1024 * 1024 * 1024) / (packet_size_bytes * 100)
        
        return min(cpu_pps, nic_pps_total, memory_pps)
    
    def calculate_network_capacity(self) -> float:
        total_capacity = 0
        for nic in self.nic:
            total_capacity += nic.get('speed_Gbps', 0)
        return total_capacity
    
    def get_bottleneck_analysis(self, current_pps: float) -> Dict[str, Any]:
        bottlenecks = []
        
        cpu_util = min(100, (current_pps / self.calculate_max_pps()) * 100)
        if cpu_util > 80:
            bottlenecks.append("CPU")
            
        nic_util = min(100, (current_pps / self.calculate_max_pps()) * 100)
        if nic_util > 80:
            bottlenecks.append("NIC")
            
        memory_pressure = (current_pps * 1500 * 100) / (self.ram_GB * 1024 * 1024 * 1024) * 100
        if memory_pressure > 70:
            bottlenecks.append("Memory")
            
        return {
            "bottlenecks": bottlenecks,
            "cpu_utilization": cpu_util,
            "nic_utilization": nic_util,
            "memory_pressure": memory_pressure
        }
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "vendor": self.vendor,
            "model": self.model,
            "cores": self.cores,
            "threads": self.threads,
            "base_freq_GHz": self.base_freq_GHz,
            "turbo_freq_GHz": self.turbo_freq_GHz,
            "L1_cache_kB": self.L1_cache_kB,
            "L2_cache_kB": self.L2_cache_kB,
            "L3_cache_MB": self.L3_cache_MB,
            "microarch": self.microarch,
            "simd_width": self.simd_width,
            "hyperthreading": self.hyperthreading,
            "aes_instruction": self.aes_instruction,
            "memory_channels": self.memory_channels,
            "memory_speed_MHz": self.memory_speed_MHz,
            "ram_GB": self.ram_GB,
            "nic": self.nic,
            "disk": self.disk,
            "os": self.os,
            "category": self.category
        }

class HardwareProfileManager:
    def __init__(self):
        self.profiles = {}
        self.load_extended_profiles()
    
    def load_extended_profiles(self):
        extended_profiles = [
            {
                "profile_id": "edge-iot-arm-a53",
                "vendor": "ARM", "model": "Cortex-A53", "category": "edge_iot",
                "cores": 4, "threads": 4, "base_freq_GHz": 1.2, "turbo_freq_GHz": 1.4,
                "L1_cache_kB": 32, "L2_cache_kB": 512, "L3_cache_MB": 1,
                "microarch": "ARMv8-A", "simd_width": 128, "hyperthreading": False, "aes_instruction": True,
                "memory_channels": 1, "memory_speed_MHz": 1066, "ram_GB": 2,
                "nic": [{"vendor": "Generic", "model": "1G NIC", "speed_Gbps": 1, "offloads": []}],
                "disk": {"type": "eMMC", "iops": 1000}, "os": {"kernel": "linux", "version": "5.10"}
            },
            {
                "profile_id": "edge-iot-arm-a72", 
                "vendor": "ARM", "model": "Cortex-A72", "category": "edge_iot",
                "cores": 4, "threads": 4, "base_freq_GHz": 1.8, "turbo_freq_GHz": 2.0,
                "L1_cache_kB": 48, "L2_cache_kB": 1024, "L3_cache_MB": 2,
                "microarch": "ARMv8-A", "simd_width": 128, "hyperthreading": False, "aes_instruction": True,
                "memory_channels": 2, "memory_speed_MHz": 1600, "ram_GB": 4,
                "nic": [{"vendor": "Generic", "model": "1G NIC", "speed_Gbps": 1, "offloads": []}],
                "disk": {"type": "eMMC", "iops": 2000}, "os": {"kernel": "linux", "version": "5.10"}
            },
            {
                "profile_id": "soho-i3-10100",
                "vendor": "Intel", "model": "Core i3-10100", "category": "soho_office", 
                "cores": 4, "threads": 8, "base_freq_GHz": 3.6, "turbo_freq_GHz": 4.3,
                "L1_cache_kB": 256, "L2_cache_kB": 1024, "L3_cache_MB": 6,
                "microarch": "Comet Lake", "simd_width": 256, "hyperthreading": True, "aes_instruction": True,
                "memory_channels": 2, "memory_speed_MHz": 2666, "ram_GB": 16,
                "nic": [{"vendor": "Intel", "model": "I219-V", "speed_Gbps": 1, "offloads": ["TSO", "GRO"]}],
                "disk": {"type": "SATA SSD", "iops": 50000}, "os": {"kernel": "linux", "version": "5.15"}
            },
            {
                "profile_id": "soho-i5-11400",
                "vendor": "Intel", "model": "Core i5-11400", "category": "soho_office",
                "cores": 6, "threads": 12, "base_freq_GHz": 2.6, "turbo_freq_GHz": 4.4,
                "L1_cache_kB": 384, "L2_cache_kB": 3072, "L3_cache_MB": 12,
                "microarch": "Rocket Lake", "simd_width": 256, "hyperthreading": True, "aes_instruction": True,
                "memory_channels": 2, "memory_speed_MHz": 3200, "ram_GB": 32,
                "nic": [{"vendor": "Intel", "model": "I225-V", "speed_Gbps": 2.5, "offloads": ["TSO", "GRO", "RSS"]}],
                "disk": {"type": "NVMe", "iops": 300000}, "os": {"kernel": "linux", "version": "5.15"}
            },
            {
                "profile_id": "server-xeon-gold-6248",
                "vendor": "Intel", "model": "Xeon Gold 6248R", "category": "server",
                "cores": 24, "threads": 48, "base_freq_GHz": 3.0, "turbo_freq_GHz": 4.0,
                "L1_cache_kB": 1536, "L2_cache_kB": 24576, "L3_cache_MB": 35,
                "microarch": "Cascade Lake", "simd_width": 512, "hyperthreading": True, "aes_instruction": True,
                "memory_channels": 6, "memory_speed_MHz": 2933, "ram_GB": 128,
                "nic": [{"vendor": "Intel", "model": "X710", "speed_Gbps": 10, "offloads": ["RSS", "TSO", "GRO", "VXLAN"]}],
                "disk": {"type": "NVMe", "iops": 500000}, "os": {"kernel": "linux", "version": "5.15"}
            },
            {
                "profile_id": "server-epyc-9654",
                "vendor": "AMD", "model": "EPYC 9654", "category": "server",
                "cores": 96, "threads": 192, "base_freq_GHz": 2.4, "turbo_freq_GHz": 3.7,
                "L1_cache_kB": 6144, "L2_cache_kB": 98304, "L3_cache_MB": 384,
                "microarch": "Zen 4", "simd_width": 512, "hyperthreading": True, "aes_instruction": True,
                "memory_channels": 12, "memory_speed_MHz": 4800, "ram_GB": 512,
                "nic": [{"vendor": "Mellanox", "model": "ConnectX-7", "speed_Gbps": 200, "offloads": ["RSS", "TSO", "GRO", "RDMA", "VXLAN"]}],
                "disk": {"type": "NVMe", "iops": 1500000}, "os": {"kernel": "linux", "version": "6.1"}
            },
            {
                "profile_id": "appliance-nvidia-bluefield-2",
                "vendor": "NVIDIA", "model": "BlueField-2", "category": "appliance",
                "cores": 8, "threads": 8, "base_freq_GHz": 2.5, "turbo_freq_GHz": 3.0,
                "L1_cache_kB": 512, "L2_cache_kB": 4096, "L3_cache_MB": 16,
                "microarch": "ARM A72", "simd_width": 128, "hyperthreading": False, "aes_instruction": True,
                "memory_channels": 2, "memory_speed_MHz": 3200, "ram_GB": 16,
                "nic": [{"vendor": "NVIDIA", "model": "ConnectX-6", "speed_Gbps": 100, "offloads": ["RSS", "TSO", "GRO", "RDMA", "VXLAN", "crypto"]}],
                "disk": {"type": "eMMC", "iops": 5000}, "os": {"kernel": "linux", "version": "5.15"}
            }
        ]
        
        additional_categories = [
            "laptop", "workstation", "cloud_vm", "network_appliance", "microcontroller"
        ]
        
        for i, profile_data in enumerate(extended_profiles):
            profile = HardwareProfile(profile_data)
            self.profiles[profile.profile_id] = profile
    
    def get_profiles_by_category(self, category: str) -> List[HardwareProfile]:
        return [p for p in self.profiles.values() if p.category == category]
    
    def get_profile(self, profile_id: str):
        return self.profiles.get(profile_id)
    
    def get_all_profiles(self):
        return list(self.profiles.values())
    
    def add_custom_profile(self, profile_data: Dict[str, Any]):
        profile = HardwareProfile(profile_data)
        self.profiles[profile.profile_id] = profile