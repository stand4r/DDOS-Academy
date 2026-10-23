import numpy as np
import random
from typing import Dict, List, Any

class FractalTrafficGenerator:
    def __init__(self, hurst_parameter: float = 0.75, intensity_base: float = 1000):
        self.H = max(0.5, min(0.99, hurst_parameter))
        self.intensity_base = intensity_base
        self.time_series = []
        self.burst_profile = {"peak_mean_ratio": 3.0, "burst_duration_mean": 5, "burst_duration_std": 2}
        
    def generate_fractal_traffic(self, duration: int, time_elapsed: int, 
                               traffic_mode: str = "pps") -> Dict[str, floЫat]:
        if not self.time_series:
            self._generate_advanced_fractal_series(duration)
        
        if time_elapsed < len(self.time_series):
            fractal_component = self.time_series[time_elapsed]
        else:
            fractal_component = random.gauss(0, 0.2)
            
        hurst_factor = 1.0 + (self.H - 0.5) * 2.0
        
        base_intensity = self.intensity_base * (1 + fractal_component * 0.3 * hurst_factor)
        
        if random.random() < 0.15:
            burst_multiplier = 1.0 + random.random() * (self.burst_profile["peak_mean_ratio"] - 1.0)
            burst_duration = max(1, int(random.gauss(
                self.burst_profile["burst_duration_mean"], 
                self.burst_profile["burst_duration_std"]
            )))
        else:
            burst_multiplier = 1.0
            burst_duration = 1
            
        intensity = base_intensity * burst_multiplier
        
        if traffic_mode == "mbps":
            packet_size_bytes = 750
            intensity = (intensity * packet_size_bytes * 8) / 1_000_000
        elif traffic_mode == "gbps":
            packet_size_bytes = 750
            intensity = (intensity * packet_size_bytes * 8) / 1_000_000_000
            
        return {
            "intensity": max(intensity * 0.1, intensity),
            "burst_multiplier": burst_multiplier,
            "burst_duration": burst_duration,
            "hurst_component": fractal_component
        }
    
    def _generate_advanced_fractal_series(self, duration: int):
        series = np.random.normal(0, 0.1, duration)
        
        for i in range(1, duration):
            series[i] = series[i-1] * self.H + series[i] * (1 - self.H)
            
        self.time_series = series.tolist()

    def set_burst_profile(self, peak_mean_ratio: float, duration_mean: float, duration_std: float):
        self.burst_profile = {
            "peak_mean_ratio": peak_mean_ratio,
            "burst_duration_mean": duration_mean,
            "burst_duration_std": duration_std
        }
            
   def set_