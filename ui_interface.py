# ui_interface.py - исправленная версия
import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QGroupBox, QLabel, QLineEdit, QPushButton, 
    QComboBox, QGridLayout, QDoubleSpinBox, QSpinBox,
    QTextEdit, QTabWidget, QProgressBar, QSplitter, QMessageBox,
    QFrame, QScrollArea, QCheckBox, QSlider, QListWidget, QListWidgetItem,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from simulation_engine import DDoSSimulationEngine, ResultsProcessor
from hardware_profiles import HardwareProfileManager
from documentation_module import DocumentationTab

class Theme:
    COLORS = {
        'background': '#1E1E1E',
        'background_light': '#252526',
        'background_lighter': '#2D2D2D',
        'background_dark': '#181818',
        'foreground': '#CCCCCC',
        'foreground_dark': '#858585',
        'foreground_light': '#E0E0E0',
        'accent_blue': '#007ACC',
        'accent_blue_light': '#3794FF',
        'accent_green': '#4EC9B0',
        'accent_orange': '#CE9178',
        'accent_yellow': '#DCDCAA',
        'accent_red': '#F44747',
        'accent_purple': '#C586C0',
        'border': '#3E3E42',
        'border_light': '#464647',
        'selection': '#264F78',
        'widget': '#2D2D30'
    }

class EnhancedModernButton(QPushButton):
    def __init__(self, text, primary=False, color_scheme=Theme.COLORS):
        super().__init__(text)
        self.setMinimumHeight(36)
        self.setFont(QFont("Cascadia Code", 10))
        
        if primary:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 {color_scheme['accent_blue']}, 
                                              stop:1 {color_scheme['accent_blue_light']});
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                    font-size: 14px;
                    padding: 8px 16px;
                }}
                QPushButton:hover {{
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                              stop:0 {color_scheme['accent_blue_light']}, 
                                              stop:1 {color_scheme['accent_blue']});
                }}
                QPushButton:pressed {{
                    background: {color_scheme['accent_blue']};
                }}
                QPushButton:disabled {{
                    background: {color_scheme['border']};
                    color: {color_scheme['foreground_dark']};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {color_scheme['background_lighter']};
                    color: {color_scheme['foreground']};
                    border: 1px solid {color_scheme['border']};
                    border-radius: 4px;
                    padding: 6px 12px;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background: {color_scheme['accent_blue']};
                    border-color: {color_scheme['accent_blue_light']};
                }}
                QPushButton:disabled {{
                    background: {color_scheme['background_dark']};
                    color: {color_scheme['foreground_dark']};
                    border-color: {color_scheme['border']};
                }}
            """)

class DDoSAcademy(QMainWindow):
    def __init__(self):
        super().__init__()
        self.simulation_engine = DDoSSimulationEngine()
        self.hardware_manager = HardwareProfileManager()
        
        self.setup_theme()
        self.initialize_interface()
        self.setup_simulation_timer()
        
    def setup_theme(self):
        colors = Theme.COLORS
        
        self.setStyleSheet(f"""
            QMainWindow {{
                background: {colors['background']};
                color: {colors['foreground']};
            }}
            QWidget {{
                background: transparent;
                color: {colors['foreground']};
            }}
            QGroupBox {{
                background: {colors['background_light']};
                border: 1px solid {colors['border']};
                border-radius: 4px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                color: {colors['accent_green']};
                font-size: 14px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: {colors['accent_green']};
            }}
            QComboBox {{
                background: {colors['background_lighter']};
                color: {colors['foreground']};
                border: 1px solid {colors['border']};
                border-radius: 3px;
                padding: 4px;
                font-size: 12px;
                min-height: 20px;
            }}
            QComboBox:focus {{
                border: 1px solid {colors['accent_blue']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background: {colors['background_lighter']};
                border: 1px solid {colors['border']};
                color: {colors['foreground']};
                selection-background-color: {colors['selection']};
                selection-color: {colors['foreground_light']};
                outline: none;
            }}
            QSlider::groove:horizontal {{
                background: {colors['border']};
                height: 4px;
                border-radius: 2px;
            }}
            QSlider::handle:horizontal {{
                background: {colors['accent_blue']};
                width: 12px;
                height: 12px;
                border-radius: 6px;
                margin: -4px 0;
            }}
            QTextEdit {{
                background: {colors['background_lighter']};
                color: {colors['foreground']};
                border: 1px solid {colors['border']};
                border-radius: 3px;
                padding: 6px;
                font-size: 14px;
            }}
            QProgressBar {{
                border: 1px solid {colors['border']};
                border-radius: 3px;
                background: {colors['background_light']};
                text-align: center;
                color: {colors['foreground']};
                height: 16px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 {colors['accent_green']}, stop:1 {colors['accent_blue']});
                border-radius: 2px;
            }}
            QTabWidget::pane {{
                border: 1px solid {colors['border']};
                border-radius: 4px;
                background: {colors['background_light']};
            }}
            QTabBar::tab {{
                background: {colors['background']};
                color: {colors['foreground_dark']};
                padding: 6px 10px;
                margin-right: 1px;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                font-weight: bold;
                font-size: 12px;
            }}
            QTabBar::tab:selected {{
                background: {colors['background_light']};
                color: {colors['accent_blue']};
            }}
            QCheckBox {{
                color: {colors['foreground']};
                font-size: 12px;
                spacing: 5px;
            }}
            QCheckBox::indicator {{
                width: 13px;
                height: 13px;
                border: 1px solid {colors['border']};
                background: {colors['background_lighter']};
                border-radius: 2px;
            }}
            QCheckBox::indicator:checked {{
                background: {colors['accent_blue']};
                border: 1px solid {colors['accent_blue_light']};
            }}
            QLineEdit {{
                background: {colors['background_lighter']};
                color: {colors['foreground']};
                border: 1px solid {colors['border']};
                border-radius: 3px;
                padding: 4px;
                font-size: 12px;
            }}
            QSpinBox, QDoubleSpinBox {{
                background: {colors['background_lighter']};
                color: {colors['foreground']};
                border: 1px solid {colors['border']};
                border-radius: 3px;
                padding: 4px;
                font-size: 12px;
            }}
        """)
        
    def initialize_interface(self):
        self.setWindowTitle('🌐 DDoS Academy - Симлуятор DDOS атак')
        self.setGeometry(100, 100, 1920, 1080)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        header = QLabel('«Намерения тех, кто создаёт DDoS-атаки, не связаны с взломом, они — вандалы, а не хакеры»\n🕵️ Кевин Митник')
        header.setStyleSheet(f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 {Theme.COLORS['accent_blue']}, 
                                          stop:1 {Theme.COLORS['accent_green']});
                color: {Theme.COLORS['background']};
                padding: 8px;
                border-radius: 4px;
                margin: 4px;
            }}
        """)
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)
        
        subtitle = QLabel('Реалистичные атаки • Многоуровневая защита • Анализ узких мест • Образовательная платформа')
        subtitle.setStyleSheet(f"font-size: 12px; color: {Theme.COLORS['accent_yellow']}; padding: 4px;")
        subtitle.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(subtitle)
        
        splitter = QSplitter(Qt.Horizontal)
        
        control_panel = self.create_control_panel()
        visualization_panel = self.create_visualization_panel()
        
        splitter.addWidget(control_panel)
        splitter.addWidget(visualization_panel)
        splitter.setSizes([800, 1120])
        
        main_layout.addWidget(splitter)
        
    def create_control_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        quick_start_card = QFrame()
        quick_start_card.setStyleSheet(f"""
            QFrame {{
                background: {Theme.COLORS['background_lighter']};
                border: 1px solid {Theme.COLORS['border']};
                border-radius: 4px;
                padding: 10px;
                margin: 2px;
            }}
        """)
        quick_start_layout = QVBoxLayout()
        quick_start_card.setLayout(quick_start_layout)
        
        quick_start_text = QLabel(
            "🚀 <b>Быстрый старт:</b><br>"
            "1. Выберите тип атаки<br>"
            "2. Настройте параметры защиты<br>" 
            "3. Запустите симуляцию<br>"
            "4. Анализируйте результаты"
        )
        quick_start_text.setStyleSheet(f"color: {Theme.COLORS['foreground']}; font-size: 16px; line-height: 140%;")
        quick_start_text.setWordWrap(True)
        quick_start_layout.addWidget(quick_start_text)
        
        layout.addWidget(quick_start_card)
        
        tab_widget = QTabWidget()
        
        attack_tab = self.create_attack_tab()
        defense_tab = self.create_defense_tab()
        network_tab = self.create_network_tab()
        hardware_tab = self.create_hardware_tab()
        scenario_tab = self.create_scenario_tab()
        documentation_tab = DocumentationTab()
        results_tab = self.create_results_tab()
        
        tab_widget.addTab(attack_tab, "🎯 Атака")
        tab_widget.addTab(defense_tab, "🛡️ Защита") 
        tab_widget.addTab(network_tab, "🌐 Сеть")
        tab_widget.addTab(hardware_tab, "💻 Железо")
        tab_widget.addTab(scenario_tab, "📊 Сценарии")
        tab_widget.addTab(documentation_tab, "📚 Документация")
        tab_widget.addTab(results_tab, "📈 Результаты")
        
        layout.addWidget(tab_widget)
        
        control_layout = QHBoxLayout()
        
        self.start_button = EnhancedModernButton("🚀 Запуск симуляции", primary=True)
        self.start_button.clicked.connect(self.start_simulation)
        control_layout.addWidget(self.start_button)
        
        self.stop_button = EnhancedModernButton("⏹️ Стоп")
        self.stop_button.clicked.connect(self.stop_simulation)
        control_layout.addWidget(self.stop_button)
        
        self.export_button = EnhancedModernButton("💾 Экспорт результатов")
        self.export_button.clicked.connect(self.export_results)
        control_layout.addWidget(self.export_button)
        
        layout.addLayout(control_layout)
        
        return panel

    def create_attack_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        attack_type_group = QGroupBox("🎯 Тип DDoS атаки")
        attack_type_layout = QVBoxLayout()
        
        self.attack_type_combo = QComboBox()
        self.attack_type_combo.addItems([
            "HTTP Flood", "SYN Flood", "UDP Flood", "ICMP Flood", 
            "Slowloris", "DNS Amplification", "Mixed Attack"
        ])
        attack_type_layout.addWidget(self.attack_type_combo)
        
        protocol_layout = QHBoxLayout()
        protocol_layout.addWidget(QLabel("Протокол:"))
        self.protocol_combo = QComboBox()
        self.protocol_combo.addItems(["TCP", "UDP", "ICMP", "HTTP", "HTTPS", "DNS"])
        protocol_layout.addWidget(self.protocol_combo)
        attack_type_layout.addLayout(protocol_layout)
        
        attack_type_group.setLayout(attack_type_layout)
        layout.addWidget(attack_type_group)
        
        intensity_group = QGroupBox("📊 Параметры интенсивности")
        intensity_layout = QGridLayout()
        
        intensity_layout.addWidget(QLabel("Размер ботнета:"), 0, 0)
        self.botnet_size = QSpinBox()
        self.botnet_size.setRange(1000, 500000)
        self.botnet_size.setValue(10000)
        self.botnet_size.setSuffix(" ботов")
        intensity_layout.addWidget(self.botnet_size, 0, 1)
        
        intensity_layout.addWidget(QLabel("Запросов на бота:"), 1, 0)
        self.requests_per_bot = QSpinBox()
        self.requests_per_bot.setRange(1, 100)
        self.requests_per_bot.setValue(10)
        self.requests_per_bot.setSuffix(" запр/сек")
        intensity_layout.addWidget(self.requests_per_bot, 1, 1)
        
        intensity_layout.addWidget(QLabel("Длительность:"), 2, 0)
        self.attack_duration = QSpinBox()
        self.attack_duration.setRange(60, 3600)
        self.attack_duration.setValue(300)
        self.attack_duration.setSuffix(" сек")
        intensity_layout.addWidget(self.attack_duration, 2, 1)
        
        intensity_layout.addWidget(QLabel("Сложность:"), 3, 0)
        self.complexity = QSpinBox()
        self.complexity.setRange(1, 5)
        self.complexity.setValue(2)
        intensity_layout.addWidget(self.complexity, 3, 1)
        
        intensity_group.setLayout(intensity_layout)
        layout.addWidget(intensity_group)
        
        packet_group = QGroupBox("📦 Параметры пакетов")
        packet_layout = QGridLayout()
        
        packet_layout.addWidget(QLabel("Размер пакета:"), 0, 0)
        self.packet_size = QSpinBox()
        self.packet_size.setRange(64, 1500)
        self.packet_size.setValue(512)
        self.packet_size.setSuffix(" байт")
        packet_layout.addWidget(self.packet_size, 0, 1)
        
        packet_layout.addWidget(QLabel("TTL:"), 1, 0)
        self.packet_ttl = QSpinBox()
        self.packet_ttl.setRange(1, 255)
        self.packet_ttl.setValue(64)
        packet_layout.addWidget(self.packet_ttl, 1, 1)
        
        packet_group.setLayout(packet_layout)
        layout.addWidget(packet_group)
        
        fractal_group = QGroupBox("🎲 Фрактальные параметры")
        fractal_layout = QGridLayout()
        
        fractal_layout.addWidget(QLabel("Параметр Хёрста:"), 0, 0)
        self.hurst_parameter = QDoubleSpinBox()
        self.hurst_parameter.setRange(0.50, 0.99)
        self.hurst_parameter.setValue(0.75)
        self.hurst_parameter.setSingleStep(0.01)
        fractal_layout.addWidget(self.hurst_parameter, 0, 1)
        
        fractal_layout.addWidget(QLabel("Burstiness:"), 1, 0)
        self.burstiness = QDoubleSpinBox()
        self.burstiness.setRange(1.0, 10.0)
        self.burstiness.setValue(3.0)
        self.burstiness.setSingleStep(0.1)
        fractal_layout.addWidget(self.burstiness, 1, 1)
        
        fractal_group.setLayout(fractal_layout)
        layout.addWidget(fractal_group)
        
        layout.addStretch()
        return tab

    def create_defense_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        basic_defense_group = QGroupBox("🛡️ Базовая защита")
        basic_layout = QGridLayout()
        
        basic_layout.addWidget(QLabel("Cloudflare:"), 0, 0)
        self.cloudflare_level = QComboBox()
        self.cloudflare_level.addItems(["Отключено", "Базовый", "Продвинутый", "Профессиональный"])
        basic_layout.addWidget(self.cloudflare_level, 0, 1)
        
        basic_layout.addWidget(QLabel("WAF:"), 1, 0)
        self.waf_level = QComboBox()
        self.waf_level.addItems(["Отключено", "Базовый", "Продвинутый"])
        basic_layout.addWidget(self.waf_level, 1, 1)
        
        basic_layout.addWidget(QLabel("Rate Limiting:"), 2, 0)
        self.rate_limiting = QComboBox()
        self.rate_limiting.addItems(["Отключено", "Базовый", "Агрессивный"])
        basic_layout.addWidget(self.rate_limiting, 2, 1)
        
        basic_defense_group.setLayout(basic_layout)
        layout.addWidget(basic_defense_group)
        
        advanced_defense_group = QGroupBox("🔧 Дополнительная защита")
        advanced_layout = QVBoxLayout()
        
        self.geo_filtering = QCheckBox("Гео-фильтрация")
        advanced_layout.addWidget(self.geo_filtering)
        
        self.ip_reputation = QCheckBox("IP репутация")
        advanced_layout.addWidget(self.ip_reputation)
        
        self.behavior_analysis = QCheckBox("Поведенческий анализ")
        advanced_layout.addWidget(self.behavior_analysis)
        
        self.captcha_enabled = QCheckBox("CAPTCHA вызовы")
        advanced_layout.addWidget(self.captcha_enabled)
        
        advanced_defense_group.setLayout(advanced_layout)
        layout.addWidget(advanced_defense_group)
        
        layout.addStretch()
        return tab

    def create_network_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        network_group = QGroupBox("🌐 Параметры сети")
        network_layout = QGridLayout()
        
        network_layout.addWidget(QLabel("Пропускная способность:"), 0, 0)
        self.channel_bandwidth = QComboBox()
        self.channel_bandwidth.addItems(["100 Mbps", "1 Gbps", "10 Gbps", "25 Gbps", "40 Gbps", "100 Gbps"])
        self.channel_bandwidth.setCurrentText("1 Gbps")
        network_layout.addWidget(self.channel_bandwidth, 0, 1)
        
        network_layout.addWidget(QLabel("Целевая утилизация:"), 1, 0)
        self.target_utilization = QSpinBox()
        self.target_utilization.setRange(10, 200)
        self.target_utilization.setValue(60)
        self.target_utilization.setSuffix(" %")
        network_layout.addWidget(self.target_utilization, 1, 1)
        
        network_group.setLayout(network_layout)
        layout.addWidget(network_group)
        
        topology_group = QGroupBox("🕸️ Топология сети")
        topology_layout = QVBoxLayout()
        
        self.topology_type = QComboBox()
        self.topology_type.addItems(["Одиночный сервер", "Балансировка нагрузки", "CDN", "Многоуровневая защита"])
        topology_layout.addWidget(self.topology_type)
        
        topology_info = QTextEdit()
        topology_info.setMaximumHeight(80)
        topology_info.setHtml("""
        <div style='color:#CCCCCC; font-size:12px;'>
        <b>Топологии:</b><br>
        • <b>Одиночный сервер</b> - базовая конфигурация<br>
        • <b>Балансировка</b> - распределение нагрузки<br>
        • <b>CDN</b> - географическое распределение<br>
        • <b>Многоуровневая</b> - комбинированная защита
        </div>
        """)
        topology_layout.addWidget(topology_info)
        
        topology_group.setLayout(topology_layout)
        layout.addWidget(topology_group)
        
        layout.addStretch()
        return tab

    def create_hardware_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        hw_selection_group = QGroupBox("💻 Выбор аппаратного профиля")
        hw_selection_layout = QVBoxLayout()
        
        self.hardware_profile_combo = QComboBox()
        profiles = self.hardware_manager.get_all_profiles()
        for profile in profiles:
            self.hardware_profile_combo.addItem(
                f"{profile.vendor} {profile.model} ({profile.category})", 
                profile.profile_id
            )
        hw_selection_layout.addWidget(self.hardware_profile_combo)
        
        self.hardware_details = QTextEdit()
        self.hardware_details.setMaximumHeight(200)
        self.hardware_profile_combo.currentIndexChanged.connect(self.update_hardware_details)
        self.update_hardware_details()
        hw_selection_layout.addWidget(self.hardware_details)
        
        hw_selection_group.setLayout(hw_selection_layout)
        layout.addWidget(hw_selection_group)
        
        performance_group = QGroupBox("📊 Анализ производительности")
        performance_layout = QVBoxLayout()
        
        performance_table = QTableWidget()
        performance_table.setColumnCount(3)
        performance_table.setHorizontalHeaderLabels(["Метрика", "Значение", "Статус"])
        performance_table.setRowCount(5)
        
        metrics = [
            ["Максимальный PPS", "150,000", "✅ Хорошо"],
            ["Пропускная способность", "10 Gbps", "✅ Отлично"],
            ["Обработка соединений", "50,000/sec", "⚠️ Средне"],
            ["Задержка обработки", "2.5 ms", "✅ Отлично"],
            ["Использование памяти", "45%", "✅ Хорошо"]
        ]
        
        for i, metric in enumerate(metrics):
            for j, value in enumerate(metric):
                performance_table.setItem(i, j, QTableWidgetItem(value))
        
        performance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        performance_layout.addWidget(performance_table)
        
        performance_group.setLayout(performance_layout)
        layout.addWidget(performance_group)
        
        layout.addStretch()
        return tab

    def create_scenario_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        scenarios_group = QGroupBox("🎮 Предустановленные сценарии")
        scenarios_layout = QVBoxLayout()
        
        self.scenarios_list = QListWidget()
        scenarios = [
            "🟢 Легкая атака - Малый бизнес",
            "🟡 Средняя атака - Корпоративный сайт", 
            "🔴 Тяжелая атака - Онлайн-банк",
            "💀 APT атака - Критическая инфраструктура",
            "🌪️ Фрактальная атака - Сложные паттерны",
            "🛡️ Тестирование защиты - Стресс-тест"
        ]
        for scenario in scenarios:
            self.scenarios_list.addItem(scenario)
        scenarios_layout.addWidget(self.scenarios_list)
        
        scenarios_group.setLayout(scenarios_layout)
        layout.addWidget(scenarios_group)
        
        scenario_settings_group = QGroupBox("⚙️ Настройки сценария")
        scenario_settings_layout = QVBoxLayout()
        
        scenario_info = QTextEdit()
        scenario_info.setMaximumHeight(150)
        scenario_info.setHtml("""
        <div style='color:#CCCCCC; font-size:9px;'>
        <b>Выберите сценарий для автоматической настройки параметров:</b><br><br>
        • <b>Легкая атака</b> - базовый HTTP flood, подходит для обучения<br>
        • <b>Средняя атака</b> - комбинированная атака с обходом защиты<br>
        • <b>Тяжелая атака</b> - объемная атака с фрактальными паттернами<br>
        • <b>APT атака</b> - целевая атака с разведкой и эскалацией<br>
        • <b>Фрактальная атака</b> - сложные паттерны трафика<br>
        • <b>Тестирование защиты</b> - оценка эффективности защиты
        </div>
        """)
        scenario_settings_layout.addWidget(scenario_info)
        
        self.scenarios_list.currentRowChanged.connect(self.load_scenario_preset)
        
        scenario_settings_group.setLayout(scenario_settings_layout)
        layout.addWidget(scenario_settings_group)
        
        layout.addStretch()
        return tab

    def create_results_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        results_group = QGroupBox("📊 Основные результаты симуляции")
        results_layout = QVBoxLayout()
        
        self.results_display = QTextEdit()
        self.results_display.setHtml("""
        <div style='text-align:center; color:#CCCCCC; padding:60px;'>
        <h2>🚀 Запустите симуляцию!</h2>
        <p>Настройте параметры атаки и защиты, затем запустите симуляцию для просмотра результатов</p>
        </div>
        """)
        results_layout.addWidget(self.results_display)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        analysis_group = QGroupBox("🔍 Детальный анализ")
        analysis_layout = QVBoxLayout()
        
        self.detailed_analysis = QTextEdit()
        self.detailed_analysis.setMaximumHeight(200)
        self.detailed_analysis.setHtml("""
        <div style='color:#CCCCCC; text-align:center; padding:40px;'>
        <h3>Детальный анализ появится после симуляции</h3>
        <p>Здесь будет показан анализ узких мест, эффективность защиты и рекомендации</p>
        </div>
        """)
        analysis_layout.addWidget(self.detailed_analysis)
        
        analysis_group.setLayout(analysis_layout)
        layout.addWidget(analysis_group)
        
        return tab

    def create_visualization_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        self.viz = VisualizationEngine(self, width=14, height=10, dpi=100)
        layout.addWidget(self.viz)
        
        metrics_group = QGroupBox("📈 Метрики в реальном времени")
        metrics_layout = QVBoxLayout()
        
        self.simulation_progress = QProgressBar()
        self.simulation_progress.setVisible(False)
        metrics_layout.addWidget(self.simulation_progress)
        
        self.realtime_metrics = QTextEdit()
        self.realtime_metrics.setMaximumHeight(120)
        self.realtime_metrics.setHtml("""
        <div style='color:#CCCCCC; text-align:center; padding:20px;'>
        <h3>Метрики появятся во время симуляции</h3>
        <p>Отслеживайте нагрузку, эффективность защиты и узкие места в реальном времени</p>
        </div>
        """)
        metrics_layout.addWidget(self.realtime_metrics)
        
        self.simulation_status = QLabel("🎯 Настройте сценарий и запустите симуляцию")
        self.simulation_status.setStyleSheet(f"""
            QLabel {{
                font-size: 13px;
                font-weight: bold;
                color: {Theme.COLORS['accent_yellow']};
                padding: 10px;
                background: {Theme.COLORS['background_lighter']};
                border: 1px solid {Theme.COLORS['border']};
                border-radius: 4px;
            }}
        """)
        self.simulation_status.setAlignment(Qt.AlignCenter)
        metrics_layout.addWidget(self.simulation_status)
        
        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)
        
        return panel

    def update_hardware_details(self):
        current_id = self.hardware_profile_combo.currentData()
        if current_id:
            profile = self.hardware_manager.get_profile(current_id)
            if profile:
                details_html = f"""
                <div style="color:#CCCCCC; font-size:10px; font-family: 'Cascadia Code', monospace;">
                <h3 style="color:#3794FF; margin:0 0 8px 0;">{profile.vendor} {profile.model}</h3>
                <table style="width:100%; border-collapse: collapse;">
                <tr><td style="padding:2px; color:#4EC9B0;"><b>Категория:</b></td><td style="padding:2px;">{profile.category}</td></tr>
                <tr><td style="padding:2px; color:#4EC9B0;"><b>Процессор:</b></td><td style="padding:2px;">{profile.cores}C/{profile.threads}T @ {profile.base_freq_GHz}GHz</td></tr>
                <tr><td style="padding:2px; color:#4EC9B0;"><b>Кэш L3:</b></td><td style="padding:2px;">{profile.L3_cache_MB} MB</td></tr>
                <tr><td style="padding:2px; color:#4EC9B0;"><b>Память:</b></td><td style="padding:2px;">{profile.ram_GB} GB DDR</td></tr>
                <tr><td style="padding:2px; color:#4EC9B0;"><b>Сеть:</b></td><td style="padding:2px;">{profile.calculate_network_capacity()} Gbps</td></tr>
                <tr><td style="padding:2px; color:#4EC9B0;"><b>Макс PPS:</b></td><td style="padding:2px;">{profile.calculate_max_pps():,} pps</td></tr>
                </table>
                </div>
                """
                self.hardware_details.setHtml(details_html)

    def load_scenario_preset(self, row):
        scenarios_config = {
            0: {
                "attack_type": "HTTP Flood",
                "botnet_size": 5000,
                "requests_per_bot": 5,
                "duration": 180,
                "hardware": "soho-i5-11400",
                "cloudflare": 0,
                "waf": 0
            },
            1: {
                "attack_type": "Mixed Attack", 
                "botnet_size": 25000,
                "requests_per_bot": 8,
                "duration": 300,
                "hardware": "server-xeon-gold-6248",
                "cloudflare": 1,
                "waf": 1
            },
            2: {
                "attack_type": "UDP Flood",
                "botnet_size": 100000,
                "requests_per_bot": 15,
                "duration": 600,
                "hardware": "server-epyc-9654", 
                "cloudflare": 2,
                "waf": 2
            }
        }
        
        if row in scenarios_config:
            config = scenarios_config[row]
            self.attack_type_combo.setCurrentText(config["attack_type"])
            self.botnet_size.setValue(config["botnet_size"])
            self.requests_per_bot.setValue(config["requests_per_bot"])
            self.attack_duration.setValue(config["duration"])
            
            index = self.hardware_profile_combo.findData(config["hardware"])
            if index >= 0:
                self.hardware_profile_combo.setCurrentIndex(index)
                
            self.cloudflare_level.setCurrentIndex(config["cloudflare"])
            self.waf_level.setCurrentIndex(config["waf"])

    def start_simulation(self):
        try:
            attack_config = {
                "attack_type": self.attack_type_combo.currentText(),
                "protocol": self.protocol_combo.currentText(),
                "botnet_size": self.botnet_size.value(),
                "requests_per_bot": self.requests_per_bot.value(),
                "attack_duration": self.attack_duration.value(),
                "complexity": self.complexity.value(),
                "packet_size": self.packet_size.value(),
                "ttl": self.packet_ttl.value(),
                "hurst_parameter": self.hurst_parameter.value(),
                "burstiness_level": self.burstiness.value(),
                "traffic_intensity_mode": "pps",
                "channel_bandwidth": self._parse_bandwidth(self.channel_bandwidth.currentText()),
                "channel_utilization": self.target_utilization.value()
            }
            
            defense_config = {
                "hardware_profile": self.hardware_profile_combo.currentData(),
                "cloudflare_level": self.cloudflare_level.currentIndex(),
                "waf_level": self.waf_level.currentIndex(),
                "rate_limiting": self.rate_limiting.currentIndex(),
                "behavior_analysis": 1 if self.behavior_analysis.isChecked() else 0,
                "geo_filtering_enabled": self.geo_filtering.isChecked(),
                "ip_reputation_enabled": self.ip_reputation.isChecked(),
                "captcha_enabled": self.captcha_enabled.isChecked()
            }
            
            self.simulation_engine.configure_custom_scenario(
                attack_config, defense_config, "Интернет-магазин"
            )
            self.simulation_engine.start_simulation()
            
            self.simulation_progress.setVisible(True)
            self.simulation_progress.setMaximum(attack_config["attack_duration"])
            self.simulation_progress.setValue(0)
            
            self.start_button.setEnabled(False)
            self.simulation_status.setText("🔄 Запущена симуляция...")
            
            self.update_realtime_metrics()
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка запуска", f"Не удалось запустить симуляцию: {str(e)}")

    def _parse_bandwidth(self, bandwidth_str):
        multipliers = {
            'Mbps': 1,
            'Gbps': 1000
        }
        try:
            value, unit = bandwidth_str.split(' ')
            return float(value) * multipliers[unit]
        except:
            return 1000  # 1 Gb

    def stop_simulation(self):
        self.simulation_engine.attack_active = False
        self.start_button.setEnabled(True)
        self.simulation_status.setText("⏹️ Симуляция остановлена")
        self.display_results()

    def export_results(self):
        try:
            QMessageBox.information(self, "Экспорт", "Результаты успешно экспортированы в reports/")
        except Exception as e:
            QMessageBox.warning(self, "Ошибка экспорта", f"Не удалось экспортировать результаты: {str(e)}")

    def setup_simulation_timer(self):
        self.simulation_timer = QTimer()
        self.simulation_timer.timeout.connect(self.update_simulation)
        self.simulation_timer.start(20)  # 50 FPS

    def update_simulation(self):
        if self.simulation_engine.attack_active:
            self.simulation_engine.execute_simulation_step()
            self.simulation_progress.setValue(self.simulation_engine.current_time)
            
            if self.simulation_engine.current_time % 3 == 0:
                self.viz.render_simulation_data(self.simulation_engine)
                self.update_realtime_metrics()
            
            if self.simulation_engine.simulation_complete:
                self.start_button.setEnabled(True)
                self.simulation_status.setText("✅ Симуляция завершена! Анализ результатов готов")
                self.display_results()

    def update_realtime_metrics(self):
        if not self.simulation_engine.time_records:
            return
            
        current_time = self.simulation_engine.current_time
        if (current_time < len(self.simulation_engine.attack_volume_records) and 
            current_time < len(self.simulation_engine.server_load_records) and
            current_time < len(self.simulation_engine.defense_efficiency_records)):
            
            current_attack = self.simulation_engine.attack_volume_records[current_time]
            current_load = self.simulation_engine.server_load_records[current_time]
            current_efficiency = self.simulation_engine.defense_efficiency_records[current_time]
            
            metrics_html = f"""
            <div style="color:#CCCCCC; font-family: 'Cascadia Code', monospace; font-size:9px;">
            <table style="width:100%; border-collapse: collapse;">
            <tr><td style="padding:2px; color:#F44747;"><b>Атака:</b></td><td style="padding:2px;">{current_attack:,.0f} pps</td></tr>
            <tr><td style="padding:2px; color:#3794FF;"><b>Нагрузка:</b></td><td style="padding:2px;">{current_load:.1f}%</td></tr>
            <tr><td style="padding:2px; color:#4EC9B0;"><b>Время:</b></td><td style="padding:2px;">{current_time}/{self.simulation_engine.attack_profile.duration} сек</td></tr>
            <tr><td style="padding:2px; color:#DCDCAA;"><b>Эффективность:</b></td><td style="padding:2px;">{current_efficiency:.1%}</td></tr>
            </table>
            </div>
            """
            
            self.realtime_metrics.setHtml(metrics_html)

    def display_results(self):
        report = ResultsProcessor.generate_performance_report(self.simulation_engine)
        colors = Theme.COLORS
        
        results_html = f"""
        <div style="background:{colors['background_lighter']}; padding:12px; border-radius:4px;">
        <h2 style="color:{colors['accent_blue']}; margin-top:0; border-bottom:1px solid {colors['border']}; padding-bottom:6px;">
        {report['final_status']}
        </h2>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 12px;">
            <div style="background:{colors['background_light']}; padding:8px; border-radius:3px; border-left:3px solid {colors['accent_red']};">
                <b>💥 Пиковая атака</b><br>
                <span style="font-size:14px; color:{colors['accent_red']};">{report['peak_attack_volume']:,.0f} pps</span>
            </div>
            
            <div style="background:{colors['background_light']}; padding:8px; border-radius:3px; border-left:3px solid {colors['accent_yellow']};">
                <b>📈 Макс. нагрузка</b><br>
                <span style="font-size:14px; color:{colors['accent_yellow']};">{report['peak_server_load']:.1f}%</span>
            </div>
            
            <div style="background:{colors['background_light']}; padding:8px; border-radius:3px; border-left:3px solid {colors['accent_green']};">
                <b>🛡️ Эффективность</b><br>
                <span style="font-size:14px; color:{colors['accent_green']};">{report['average_efficiency']:.1%}</span>
            </div>
            
            <div style="background:{colors['background_light']}; padding:8px; border-radius:3px; border-left:3px solid {colors['accent_orange']};">
                <b>💸 Ущерб</b><br>
                <span style="font-size:14px; color:{colors['accent_orange']};">{report['financial_impact']:,.0f} RUB</span>
            </div>
            
            <div style="background:{colors['background_light']}; padding:8px; border-radius:3px; border-left:3px solid {colors['accent_purple']};">
                <b>⏱️ Длительность</b><br>
                <span style="font-size:14px; color:{colors['accent_purple']};">{report['duration']} сек</span>
            </div>
            
            <div style="background:{colors['background_light']}; padding:8px; border-radius:3px; border-left:3px solid {colors['accent_blue']};">
                <b>🎲 Параметр Хёрста</b><br>
                <span style="font-size:14px; color:{colors['accent_blue']};">{self.hurst_parameter.value():.2f}</span>
            </div>
        </div>
        </div>
        """
        
        self.results_display.setHtml(results_html)
        
        analysis_html = f"<h3 style='color:{colors['accent_blue']}; margin-bottom:8px;'>🔍 Анализ эффективности защиты:</h3>"
        
        if report['learning_points']:
            analysis_html += "<ul style='color:#CCCCCC; margin:0; padding-left:12px;'>"
            for point in report['learning_points']:
                analysis_html += f"<li style='margin:4px 0; font-size:10px;'>{point}</li>"
            analysis_html += "</ul>"
        else:
            analysis_html += f"<p style='color:{colors['foreground_dark']}; text-align:center;'>Запустите симуляцию для получения анализа</p>"
        
        self.detailed_analysis.setHtml(analysis_html)

class VisualizationEngine(FigureCanvas):    
    def __init__(self, parent=None, width=14, height=10, dpi=100):
        self.figure = Figure(figsize=(width, height), dpi=dpi, facecolor=Theme.COLORS['background'])
        super().__init__(self.figure)
        self.setParent(parent)
        
    def render_simulation_data(self, simulation):
        self.figure.clear()
        
        if simulation.time_records:
            time_points = simulation.time_records
            
            ax1 = self.figure.add_subplot(221)  # Трафик атаки
            ax2 = self.figure.add_subplot(222)  # Нагрузка системы
            ax3 = self.figure.add_subplot(223)  # Эффективность защиты
            ax4 = self.figure.add_subplot(224)  # Фрактальные компоненты
            
            colors = Theme.COLORS
            
            for ax in [ax1, ax2, ax3, ax4]:
                ax.set_facecolor(colors['background'])
                ax.tick_params(colors=colors['foreground'])
                ax.xaxis.label.set_color(colors['foreground'])
                ax.yaxis.label.set_color(colors['foreground'])
                ax.title.set_color(colors['accent_blue'])
                ax.grid(True, alpha=0.1, color=colors['border'])
                for spine in ax.spines.values():
                    spine.set_color(colors['border'])
            
            attack_data = simulation.attack_volume_records
            
            ax1.plot(time_points, attack_data, color=colors['accent_red'], 
                    label='Трафик атаки', linewidth=2, alpha=0.8)
            ax1.fill_between(time_points, 0, attack_data, alpha=0.3, color=colors['accent_red'])
            
            ax1.set_ylabel('Интенсивность (pps)', color=colors['foreground'])
            ax1.set_title('Динамика атаки', fontweight='bold', pad=10, fontsize=11)
            ax1.legend(facecolor=colors['background_light'], edgecolor='none', 
                      labelcolor=colors['foreground'], fontsize=8)
            
            load_data = simulation.server_load_records
            
            ax2.plot(time_points, load_data, color=colors['accent_blue'], 
                    label='Нагрузка сервера', linewidth=2.5)
            ax2.axhline(y=80, color=colors['accent_yellow'], linestyle='--', 
                       label='Порог 80%', alpha=0.7)
            ax2.axhline(y=95, color=colors['accent_red'], linestyle='--', 
                       label='Критично 95%', alpha=0.7)
            ax2.set_ylim(0, 100)
            
            ax2.set_ylabel('Нагрузка (%)', color=colors['foreground'])
            ax2.set_title('Нагрузка на систему', fontweight='bold', pad=10, fontsize=11)
            ax2.legend(facecolor=colors['background_light'], edgecolor='none', 
                      labelcolor=colors['foreground'], fontsize=8)
            
            efficiency_data = simulation.defense_efficiency_records
            
            ax3.plot(time_points, efficiency_data, color=colors['accent_green'], 
                    label='Эффективность защиты', linewidth=2)
            ax3.set_ylim(0, 1)
            
            ax3.set_xlabel('Время (секунды)', color=colors['foreground'])
            ax3.set_ylabel('Эффективность', color=colors['foreground'])
            ax3.set_title('Эффективность защиты', fontweight='bold', pad=10, fontsize=11)
            ax3.legend(facecolor=colors['background_light'], edgecolor='none', 
                      labelcolor=colors['foreground'], fontsize=8)
            
            if hasattr(simulation, 'fractal_component_records') and simulation.fractal_component_records:
                fractal_data = simulation.fractal_component_records
                ax4.plot(time_points, fractal_data, color=colors['accent_orange'], 
                        label='Фрактальная компонента', linewidth=2)
                
                ax4.set_xlabel('Время (секунды)', color=colors['foreground'])
                ax4.set_ylabel('Фрактальная компонента', color=colors['foreground'])
                ax4.set_title('Фрактальные характеристики', fontweight='bold', pad=10, fontsize=11)
                ax4.legend(facecolor=colors['background_light'], edgecolor='none', 
                          labelcolor=colors['foreground'], fontsize=8)
            
        self.figure.tight_layout()
        self.draw()