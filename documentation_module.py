from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QGroupBox
from PyQt5.QtCore import Qt

class DocumentationModule:    
    @staticmethod
    def get_ddos_tutorial():
        return """
        <div style="color: #CCCCCC; font-family: 'Arial', sans-serif; line-height: 1.6;">
        <h1 style="color: #3794FF; border-bottom: 2px solid #3794FF; padding-bottom: 10px;">📚 Руководство по DDoS атакам и защите</h1>
        
        <div style="background: #2D2D30; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h2 style="color: #4EC9B0; margin-top: 0;">🎯 Введение в проблематику</h2>
        <p><b>DDoS (Distributed Denial of Service)</b> - кибератака, направленная на нарушение доступности информационных систем путем создания чрезмерной нагрузки.</p>
        <p><b>Исторический контекст:</b> Первые DoS атаки зафиксированы в 1999 году, современные DDoS атаки стали масштабируемыми с появлением ботнетов.</p>
        </div>

        <h2 style="color: #4EC9B0;">🔍 Классификация DDoS атак по OSI модели</h2>

        <h3 style="color: #CE9178; background: #2D2D30; padding: 10px; border-radius: 5px;">📡 Сетевой уровень (L3-4) - Volume Attacks</h3>
        <div style="margin-left: 20px;">
        <p><b>UDP Flood</b> - отправка UDP пакетов на случайные порты:</p>
        <ul>
            <li>Цель: исчерпание полосы пропускания</li>
            <li>Характеристики: высокий PPS (packets per second)</li>
            <li>Сложность обнаружения: низкая</li>
        </ul>

        <p><b>ICMP Flood</b> - массовая отправка ping запросов:</p>
        <ul>
            <li>Цель: перегрузка сетевой инфраструктуры</li>
            <li>Особенность: требует ответных ICMP reply пакетов</li>
        </ul>

        <p><b>DNS Amplification</b> - техника усиления через DNS серверы:</p>
        <ul>
            <li>Коэффициент усиления: 50-100x</li>
            <li>Механизм: запросы с поддельным IP отправителя</li>
            <li>Уязвимые службы: открытые рекурсивные DNS резолверы</li>
        </ul>
        </div>

        <h3 style="color: #CE9178; background: #2D2D30; padding: 10px; border-radius: 5px;">⚡ Транспортный уровень (L4) - Protocol Attacks</h3>
        <div style="margin-left: 20px;">
        <p><b>SYN Flood</b> - эксплуатация TCP three-way handshake:</p>
        <ul>
            <li>Механизм: отправка SYN без завершения ACK</li>
            <li>Результат: исчерпание таблицы соединений</li>
            <li>Защита: SYN cookies, увеличение backlog queue</li>
        </ul>

        <p><b>ACK/PUSH Flood</b> - установленные соединения:</p>
        <ul>
            <li>Особенность: требует предварительного установления TCP сессии</li>
            <li>Сложность фильтрации: высокая</li>
        </ul>

        <p><b>UDP Fragmentation</b> - фрагментация пакетов:</p>
        <ul>
            <li>Цель: перегрузка систем сборки пакетов</li>
            <li>Влияние: высокое потребление CPU и памяти</li>
        </ul>
        </div>

        <h3 style="color: #CE9178; background: #2D2D30; padding: 10px; border-radius: 5px;">🌐 Прикладной уровень (L7) - Application Layer</h3>
        <div style="margin-left: 20px;">
        <p><b>HTTP/HTTPS Flood</b> - атаки на веб-приложения:</p>
        <ul>
            <li>GET Flood - массовые запросы статического контента</li>
            <li>POST Flood - отправка данных с высокой нагрузкой на БД</li>
            <li>Slowloris - медленные HTTP запросы с длинными заголовками</li>
            <li>RUDY (R-U-Dead-Yet) - медленная отправка тела POST</li>
        </ul>

        <p><b>SSL/TLS атаки:</b></p>
        <ul>
            <li>SSL Renegotiation - повторное согласование параметров</li>
            <li>THC SSL DoS - эксплуатация вычислительной сложности RSA</li>
        </ul>

        <p><b>DNS Query Flood</b> - атаки на DNS инфраструктуру:</p>
        <ul>
            <li>Цель: перегрузка DNS серверов</li>
            <li>Особенность: сложность отличия от легитимного трафика</li>
        </ul>
        </div>

        <h2 style="color: #4EC9B0;">🛡️ Многоуровневая система защиты</h2>

        <h3 style="color: #DCDCAA;">🏢 Организационные меры</h3>
        <ul>
            <li><b>Политика информационной безопасности</b> - регламенты реагирования на инциденты</li>
            <li><b>Обучение персонала</b> - подготовка к действиям при атаке</li>
            <li><b>Резервные каналы связи</b> - альтернативные маршруты трафика</li>
        </ul>

        <h3 style="color: #DCDCAA;">🔧 Технические решения</h3>

        <p><b>Сетевой уровень защиты:</b></p>
        <ul>
            <li>BGP Flowspec - фильтрация на уровне маршрутизаторов</li>
            <li>ACL (Access Control Lists) - блокировка по IP/портам</li>
            <li>QoS (Quality of Service) - приоритизация трафика</li>
        </ul>

        <p><b>Серверная защита:</b></p>
        <ul>
            <li>Увеличение системных лимитов (backlog, file descriptors)</li>
            <li>Настройка TCP stack параметров (tcp_syncookies, tcp_max_syn_backlog)</li>
            <li>Оптимизация веб-серверов (nginx, Apache)</li>
        </ul>

        <p><b>Облачные решения:</b></p>
        <ul>
            <li>CDN (Cloudflare, Akamai) - географическое распределение</li>
            <li>DDoS Protection as a Service (AWS Shield, Azure DDoS Protection)</li>
            <li>Anycast сеть - распределение атаки по множеству точек</li>
        </ul>

        <h2 style="color: #4EC9B0;">📊 Методы обнаружения и анализа</h2>

        <h3 style="color: #CE9178;">📈 Статистические методы</h3>
        <ul>
            <li><b>Анализ временных рядов</b> - выявление аномалий в трафике</li>
            <li><b>Энтропийный анализ</b> - оценка случайности распределения пакетов</li>
            <li><b>Корреляционный анализ</b> - поиск взаимосвязей в сетевом потоке</li>
        </ul>

        <h3 style="color: #CE9178;">🤖 Машинное обучение в обнаружении DDoS</h3>
        <ul>
            <li><b>Классификация трафика</b> - SVM, Random Forest</li>
            <li><b>Глубокое обучение</b> - RNN, LSTM для анализа последовательностей</li>
            <li><b>Аномалийное обнаружение</b> - Isolation Forest, Autoencoders</li>
        </ul>

        <h3 style="color: #CE9178;">🔍 Сигнатурный анализ</h3>
        <ul>
            <li>Pattern matching - поиск известных сигнатур атак</li>
            <li>Behavioral analysis - анализ поведенческих паттернов</li>
            <li>Protocol compliance - проверка соответствия стандартам</li>
        </ul>

        <h2 style="color: #4EC9B0;">⚖️ Юридические аспекты и нормативная база</h2>

        <div style="background: #2D2D30; padding: 15px; border-radius: 5px;">
        <h3 style="color: #F44747; margin-top: 0;">📜 Международное законодательство</h3>
        <ul>
            <li><b>Будапештская конвенция</b> - международное сотрудничество по киберпреступности</li>
            <li><b>Директива NIS</b> - европейские стандарты сетевой безопасности</li>
            <li><b>FISMA</b> - американские стандарты защиты информации</li>
        </ul>

        <h3 style="color: #F44747;">🇷🇺 Российское законодательство</h3>
        <ul>
            <li>Статья 273 УК РФ - создание и распространение вредоносных программ</li>
            <li>Статья 274 УК РФ - нарушение правил эксплуатации ЭВМ</li>
            <li>Федеральный закон №187-ФЗ - защита критической информационной инфраструктуры</li>
        </ul>
        </div>

        <h2 style="color: #4EC9B0;">🔬 Современные тенденции и будущее DDoS защиты</h2>

        <h3 style="color: #CE9178;">🚀 Технологические тренды</h3>
        <ul>
            <li><b>AI-driven защита</b> - адаптивные системы на основе машинного обучения</li>
            <li><b>Edge computing</b> - распределенная обработка на границе сети</li>
            <li><b>Blockchain</b> - децентрализованные системы защиты</li>
            <li><b>5G security</b> - защита в сетях нового поколения</li>
        </ul>

        <h3 style="color: #CE9178;">📊 Эволюция атакующих методик</h3>
        <ul>
            <li>Multi-vector атаки - комбинация различных техник</li>
            <li>IoT ботнеты - использование уязвимых IoT устройств</li>
            <li>Application-specific атаки - целевые атаки на конкретные приложения</li>
            <li>Low-and-slow атаки - малозаметные длительные воздействия</li>
        </ul>

        <div style="background: #2D2D30; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #F44747;">
        <h3 style="color: #F44747; margin-top: 0;">⚠️ Ответственность и этика</h3>
        <p><b>Важно понимать:</b> Данный симулятор создан исключительно в образовательных и исследовательских целях.</p>
        <p><b>Проведение реальных DDoS атак является уголовно наказуемым преступлением</b> и может привести к:</p>
        <ul>
            <li>Уголовной ответственности по статье 273 УК РФ (до 7 лет лишения свободы)</li>
            <li>Гражданско-правовой ответственности (возмещение ущерба)</li>
            <li>Административной ответственности (крупные штрафы)</li>
        </ul>
        <p><b>Используйте знания исключительно для:</b></p>
        <ul>
            <li>Защиты собственной инфраструктуры</li>
            <li>Проведения легитимных стресс-тестов</li>
            <li>Исследований в области кибербезопасности</li>
            <li>Образовательных целей</li>
        </ul>
        </div>

        <h2 style="color: #4EC9B0;">💡 Практические рекомендации</h2>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
        <div style="background: #2D2D30; padding: 15px; border-radius: 5px;">
        <h4 style="color: #4EC9B0; margin-top: 0;">🛠️ Для администраторов</h4>
        <ul>
            <li>Регулярно обновляйте системы и приложения</li>
            <li>Настройте мониторинг и алертирование</li>
            <li>Проводите регулярные стресс-тесты</li>
            <li>Имейте план реагирования на инциденты</li>
        </ul>
        </div>
        </div>
        </div>

        <div style="background: #2D2D30; padding: 20px; border-radius: 8px; margin-top: 20px; text-align: center;">
        </div>
        </div>
        """
    
    @staticmethod
    def get_hardware_guide():
        return """
        <div style="color: #CCCCCC; font-family: 'Arial', sans-serif; line-height: 1.6;">
        <h2 style="color: #3794FF; border-bottom: 2px solid #3794FF; padding-bottom: 10px;">💻 Аппаратное обеспечение для DDoS защиты</h2>
        
        <div style="background: #2D2D30; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #4EC9B0; margin-top: 0;">🎯 Критические компоненты системы защиты</h3>
        <p>Эффективная защита от DDoS требует сбалансированной аппаратной конфигурации, где каждый компонент играет ключевую роль.</p>
        </div>

        <h3 style="color: #CE9178;">🧠 Центральный процессор (CPU)</h3>
        
        <h4 style="color: #DCDCAA;">Архитектурные особенности</h4>
        <ul>
            <li><b>Ядра и потоки</b> - для параллельной обработки сетевых потоков</li>
            <li><b>Тактовая частота</b> - критична для latency-sensitive операций</li>
            <li><b>Кэш-память</b> - L3 кэш для хранения таблиц состояний</li>
        </ul>

        <h4 style="color: #DCDCAA;">Специализированные инструкции</h4>
        <ul>
            <li><b>AES-NI</b> - аппаратное ускорение шифрования TLS/SSL</li>
            <li><b>AVX-512</b> - векторные операции для анализа трафика</li>
            <li><b>TSX</b> - транзакционная память для конкурентного доступа</li>
        </ul>

        <h4 style="color: #DCDCAA;">Рекомендации по выбору</h4>
        <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
        <tr style="background: #2D2D30;">
            <th style="padding: 10px; border: 1px solid #3E3E42; text-align: left;">Сценарий</th>
            <th style="padding: 10px; border: 1px solid #3E3E42; text-align: left;">Минимальная конфигурация</th>
            <th style="padding: 10px; border: 1px solid #3E3E42; text-align: left;">Рекомендуемая</th>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #3E3E42;">Малый бизнес</td>
            <td style="padding: 10px; border: 1px solid #3E3E42;">4 ядра / 8 потоков</td>
            <td style="padding: 10px; border: 1px solid #3E3E42;">8 ядер / 16 потоков</td>
        </tr>
        <tr style="background: #2D2D30;">
            <td style="padding: 10px; border: 1px solid #3E3E42;">Корпоративный</td>
            <td style="padding: 10px; border: 1px solid #3E3E42;">16 ядер / 32 потока</td>
            <td style="padding: 10px; border: 1px solid #3E3E42;">32 ядра / 64 потока</td>
        </tr>
        <tr>
            <td style="padding: 10px; border: 1px solid #3E3E42;">Провайдер</td>
            <td style="padding: 10px; border: 1px solid #3E3E42;">64 ядра / 128 потоков</td>
            <td style="padding: 10px; border: 1px solid #3E3E42;">96+ ядер / 192+ потока</td>
        </tr>
        </table>

        <h3 style="color: #CE9178;">🌐 Сетевые интерфейсы (NIC)</h3>
        
        <h4 style="color: #DCDCAA;">Ключевые характеристики</h4>
        <ul>
            <li><b>Скорость порта</b> - 1G/10G/25G/40G/100G Ethernet</li>
            <li><b>Количество очередей</b> - RSS (Receive Side Scaling)</li>
            <li><b>Буферная память</b> - обработка burst трафика</li>
        </ul>

        <h4 style="color: #DCDCAA;">Технологии оффлоадинга</h4>
        <ul>
            <li><b>TSO/GSO</b> - TCP Segmentation Offload</li>
            <li><b>LRO/GRO</b> - Large Receive Offload</li>
            <li><b>VXLAN/NVGRE</b> - туннелирование</li>
            <li><b>RSS</b> - распределение по ядрам CPU</li>
        </ul>

        <h3 style="color: #CE9178;">💾 Оперативная память (RAM)</h3>
        
        <h4 style="color: #DCDCAA;">Требования к памяти</h4>
        <ul>
            <li><b>Объем</b> - для хранения connection tracking таблиц</li>
            <li><b>Скорость</b> - DDR4/DDR5 с высокой пропускной способностью</li>
            <li><b>Канальность</b> - dual/quad channel конфигурации</li>
        </ul>

        <h4 style="color: #DCDCAA;">Расчет потребления памяти</h4>
        <div style="background: #2D2D30; padding: 15px; border-radius: 5px; margin: 10px 0;">
        <p><b>Формула оценки:</b> Память = (Количество_соединений × 512 байт) + (PPS × 256 байт)</p>
        <p><b>Пример:</b> 1 млн соединений + 1M PPS = ~768 MB RAM</p>
        </div>

        <h3 style="color: #CE9178;">⚡ Системная архитектура</h3>
        
        <h4 style="color: #DCDCAA;">NUMA архитектура</h4>
        <ul>
            <li><b>Локализация памяти</b> - минимизация межсокетного доступа</li>
            <li><b>Привязка процессов</b> - CPU affinity для сетевых обработчиков</li>
            <li><b>Разделение ресурсов</b> - выделенные NUMA ноды для критичных процессов</li>
        </ul>

        <h4 style="color: #DCDCAA;">Шинная архитектура</h4>
        <ul>
            <li><b>PCIe версия</b> - 4.0/5.0 для высокоскоростных NIC</li>
            <li><b>Количество линий</b> - обеспечение пропускной способности</li>
            <li><b>Topology</b> - оптимальное распределение устройств</li>
        </ul>

        <h3 style="color: #CE9178;">🔧 Оптимизация производительности</h3>
        
        <h4 style="color: #DCDCAA;">Настройка ядра Linux</h4>
        <div style="background: #2D2D30; padding: 15px; border-radius: 5px; margin: 10px 0;">
        <code style="color: #4EC9B0;">
        # Увеличение таблицы соединений<br>
        net.netfilter.nf_conntrack_max = 2000000<br>
        net.ipv4.tcp_max_syn_backlog = 65536<br>
        <br>
        # Оптимизация сетевого стека<br>
        net.core.rmem_max = 134217728<br>
        net.core.wmem_max = 134217728<br>
        net.ipv4.tcp_rmem = 4096 65536 134217728<br>
        </code>
        </div>

        <h4 style="color: #DCDCAA;">Мониторинг производительности</h4>
        <ul>
            <li><b>PPS (Packets Per Second)</b> - общая производительность</li>
            <li><b>CPU utilization</b> - загрузка процессора</li>
            <li><b>Memory pressure</b> - использование памяти</li>
            <li><b>NIC statistics</b> - статистика сетевых карт</li>
        </ul>

        <div style="background: #2D2D30; padding: 20px; border-radius: 8px; margin-top: 20px;">
        <h4 style="color: #4EC9B0; margin-top: 0;">💡 Ключевые выводы</h4>
        <ul>
            <li>Баланс между CPU, памятью и сетью критически важен</li>
            <li>Современные NIC с оффлоадингом снижают нагрузку на CPU</li>
            <li>Правильная настройка ОС может увеличить производительность на 30-50%</li>
            <li>Регулярный мониторинг помогает выявлять узкие места</li>
        </ul>
        </div>
        </div>
        """

class DocumentationTab(QWidget):    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.doc_browser = QTextEdit()
        self.doc_browser.setReadOnly(True)
        self.doc_browser.setHtml(DocumentationModule.get_ddos_tutorial())
        
        layout.addWidget(self.doc_browser)
        self.setLayout(layout)