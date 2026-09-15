# 基于 STM32、ESP8266 与 OneNET 云平台的嵌入式智能灯光控制系统 (基础版)
# Embedded Intelligent Lighting Control System Based on STM32, ESP8266 & OneNET Cloud

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![MCU: STM32F103C8T6](https://img.shields.io/badge/MCU-STM32F103C8T6%20Cortex--M3-red.svg?style=flat-square)](https://www.st.com/)
[![Wireless: ESP8266](https://img.shields.io/badge/Wireless-ESP8266%20Wi--Fi-orange.svg?style=flat-square)](https://www.espressif.com/)
[![Cloud: OneNET IoT](https://img.shields.io/badge/Cloud-OneNET%20EDP%20IoT-blueviolet.svg?style=flat-square)](https://open.iot.10086.cn/)
[![App: Android Studio](https://img.shields.io/badge/Mobile-Android%20TCP%20Client-green.svg?style=flat-square)](src/androidControl/)

[**中文文档**](README.md) | [**English**](README_EN.md) | [**日本語**](README_JA.md)

</div>

---

## 1. 项目概述 (Project Overview)

**基于 STM32、ESP8266 与 OneNET 云平台的嵌入式智能灯光控制系统** 是一套面向智慧建筑、节能照明与多源物联网通信的高集成度端云协同工程方案。

系统以工业级 **STMicroelectronics STM32F103C8T6 (ARM 32-bit Cortex-M3 内核)** 作为主控微处理器，融合光敏传感采集、MOSFET 功率驱动、多通道硬件定时器 PWM 调光、双串口异步收发与嵌入式实时状态机。针对智慧照明对就地调光、移动端局域网直连与广域云端运维的多层次需求，系统创新性地构建了**“端侧闭环自适应调光 + 局域网 Android 移动终端实时控制 + 广域网 OneNET 云平台物联网数据上传”**的三维协同控制拓扑。

在算法与信号调理层，系统通过 12 位高精度逐次逼近型 ADC 与滑动窗口数字滤波算法实时量化环境光照度，驱动定时器 TIM3 通道 2 产生高频脉宽调制信号，实现无频闪的自适应动态照度补偿；在物联网通信层，系统利用 ESP8266 高速 Wi-Fi 模组，构建基于 EDP（Enhanced Device Protocol）协议的云端遥测通道与基于透传 TCP Socket 的移动端双向指令链路，实现了微秒级响应与工业级可靠性的智能照明管控。

---

## 2. 硬件实物与工程架构展示 (Visual Showcase)

<div align="center">

| 系统全景与端云数据流拓扑架构 | STM32F103C8T6 主控最小系统实物 |
| :---: | :---: |
| <img src="docs/images/system_architecture.png" width="450" alt="System Architecture"> | <img src="docs/images/hardware_stm32.png" width="450" alt="STM32 Board"> |
| **Android 移动端局域网控制应用界面** | **OneNET 广域物联网云平台数据流接入看板** |
| <img src="docs/images/demo_android_app.png" width="450" alt="Android App"> | <img src="docs/images/demo_onenet_cloud.png" width="450" alt="OneNET Cloud"> |

</div>

---

## 3. 核心数学模型与控制工程推导 (Mathematical Formulations)

本项目在嵌入式固件与控制逻辑中实现了严格的数学模型，包括光敏光电特性转换、ADC 离散滤波量化、定时器 PWM 调制以及分段自适应照度闭环控制律。

### 3.1 光敏电阻光电特性模型与分压信号调理方程

光敏电阻的电学阻值 $R_{\text{photo}}$ 随入射光照度 $E$（单位：$\text{lux}$）呈非线性幂律衰减。设 10 lux 标准照度下的基准电阻为 $R_{10}$，光电特性指数为 $\gamma$：

$$
R_{\text{photo}}(E) = R_{10} \cdot \left( \frac{E}{10} \right)^{-\gamma}
$$

信号调理电路由光敏电阻与精密分压精密电阻 $R_{\text{fixed}}$ 串联组成，输入微控制器 ADC 采样引脚的瞬时电压方程表示为：

$$
V_{\text{in}}(E) = V_{\text{ref}} \cdot \frac{R_{\text{photo}}(E)}{R_{\text{fixed}} + R_{\text{photo}}(E)}
$$

### 3.2 12 位逐次逼近型 ADC 模数转换与滑动平均滤波算法

STM32F103 内置 12 位逐次逼近型 ADC，其满量程量化电平为 $2^{12} - 1 = 4095$，参考基准电压 $V_{\text{ref}} = 3.3\text{ V}$。瞬时离散采样数值量化公式为：

$$
\text{ADC}_{\text{raw}} = \left\lfloor \frac{V_{\text{in}}}{V_{\text{ref}}} \cdot 4095 \right\rfloor
$$

为有效滤除市电工频电磁干扰及高频白噪声，系统采用长度为 $N = 10$ 的离散滑动均值滤波器：

$$
\overline{\text{ADC}}_k = \frac{1}{N} \sum_{i=0}^{N-1} \text{ADC}_{k-i}
$$

### 3.3 定时器 TIM3 高频 PWM 脉宽调制与光照度输出

STM32 高级/通用定时器挂载于 72MHz APB1 总线上，通过预分频寄存器（PSC）与自动重装载寄存器（ARR）产生无频闪的硬件 PWM：

$$
f_{\text{PWM}} = \frac{f_{\text{CLK}}}{(\text{PSC} + 1) \cdot (\text{ARR} + 1)} = \frac{72\text{ MHz}}{(0 + 1) \cdot 7200} = 10\text{ kHz}
$$

输出 PWM 有效占空比 $D_{\text{PWM}}$ 由捕获/比较寄存器 CCR2 决定：

$$
D_{\text{PWM}} = \frac{\text{CCR2}}{\text{ARR}} \times 100\% = \frac{\text{CCR2}}{7200} \times 100\%
$$

### 3.4 分段自适应反向光照补偿闭环控制律

为实现人眼舒适性照明并避免过度调光引发的光学震荡，控制器构建了具有滞环容限的三段自适应反向补偿转移函数：

$$
D_{\text{target}}(\overline{\text{ADC}}) = \begin{cases} \frac{5000}{7200} \approx 69.4\%, & \overline{\text{ADC}} > 3000 \quad (\text{极暗环境，启动高强补光}) \\ \frac{3000}{7200} \approx 41.7\%, & 2000 < \overline{\text{ADC}} \le 3000 \quad (\text{适中照度，维持中度补光}) \\ \frac{1000}{7200} \approx 13.9\%, & \overline{\text{ADC}} \le 2000 \quad (\text{强光充足，切入微光节能}) \end{cases}
$$

### 3.5 双通道物联网通信延迟与吞吐量力学边界

设遥测数据包包含协议包头、通道号、光照强度与校验和，有效载荷字节数为 $B_{\text{packet}} = 64\text{ Bytes}$。在 USART2 波特率为 $115200\text{ bps}$ 下，物理层串行传输耗时为：

$$
T_{\text{UART}} = \frac{B_{\text{packet}} \times 10}{\text{BaudRate}} = \frac{64 \times 10}{115200} \approx 5.56\text{ ms}
$$

端云整体遥测延迟包含滑动滤波窗口延时、串口调度延时、802.11 射频通信延时与公网传输延时：

$$
T_{\text{total}} = T_{\text{filter}} + T_{\text{UART}} + T_{\text{RF}} + T_{\text{cloud}} \le 85\text{ ms}
$$

---

## 4. 软硬件系统技术指标 (System Specifications)

| 子系统 | 核心选型与组件 | 技术规格与实现指标 |
| :--- | :--- | :--- |
| **主控微处理器 (MCU)** | STMicroelectronics STM32F103C8T6 | 32-bit ARM Cortex-M3 @ 72MHz, 64KB Flash, 20KB SRAM |
| **无线通信模组** | Espressif ESP8266 (ESP-01/12F) | 802.11 b/g/n, 支持 STA/AP 模式, 硬件 UART 透传 |
| **光敏传感单元** | 硫化镉 (CdS) 光敏电阻模块 | 光谱响应范围 $400 \sim 700\text{ nm}$，响应时间 $\le 30\text{ ms}$ |
| **模数转换 (ADC)** | 嵌入式 12-Bit SAR ADC (ADC1_IN1) | 转换速率 $1\text{ MSPS}$，采样引脚 PA1，10 次滑动平均滤波 |
| **功率调光驱动** | 场效应管 (N-MOSFET) 驱动模块 | 支持最高 24V / 5A 外部负载，光耦隔离保护 |
| **PWM 输出特性** | 通用定时器 TIM3 通道 2 (PA7) | 载波频率 $10\text{ kHz}$，分辨率 7200 阶，无视觉可视频闪 |
| **广域云端协议** | 中移物联网 OneNET 开放平台 | 支持 EDP 协议长连接认证，遥测推送周期 $2.0\text{ s}$ |
| **移动端交互** | Android 原生开发 (Java/Socket) | 原生 TCP Socket 通信，无缝调节占空比步进 ($\pm 1000$) |

---

## 5. 目录结构说明 (Repository Layout)

```text
Intelligent-Lighting-Control-System-Basic/
├── docs/
│   └── images/
│       ├── system_architecture.png       # 系统端云协同拓扑架构图
│       ├── hardware_stm32.png            # STM32F103C8T6 最小系统实物图
│       ├── hardware_esp8266.png          # ESP8266 无线通信模块实物图
│       ├── hardware_led_control.png      # 功率驱动与信号调理板实物图
│       ├── hardware_led_power.png        # LED 专用驱动稳压供电模块实物图
│       ├── hardware_stlink.png           # ST-Link V2 硬件仿真调试器实物图
│       ├── hardware_cp2102.png           # CP2102 USB-to-UART 串口桥接器实物图
│       ├── demo_android_app.png          # Android 移动端操作界面截图
│       └── demo_onenet_cloud.png         # OneNET 云端物联网数据接入展示图
├── src/
│   ├── stm32Project/                     # Keil uVision MDK-ARM 嵌入式工程
│   │   ├── CMSIS/                        # ARM Cortex-M3 核心抽象层驱动
│   │   ├── FWLIB/                        # STM32F10x 官方标准外设库
│   │   └── USER/                         # 用户应用层源码
│   │       ├── main.c                    # 主调度轮询与模式切换状态机
│   │       ├── adc.c / adc.h             # 12 位 ADC 采样与均值滤波驱动
│   │       ├── timer.c / timer.h         # TIM3 硬件 PWM 生成驱动
│   │       ├── esp8266.c / esp8266.h     # ESP8266 AT 指令与 TCP 透传引擎
│   │       ├── onenet.c / onenet.h       # OneNET 云平台数据流封包上报
│   │       ├── edpkit.c / edpkit.h       # EDP 协议核心打包与解析协议栈
│   │       ├── key.c / key.h             # 硬件实体按键防抖扫描
│   │       └── usart.c / usart.h         # USART1 调试与 USART2 通信驱动
│   └── androidControl/                   # Android Studio 原生移动端工程
│       ├── app/                          # 移动端业务逻辑与 UI 界面
│       └── gradle/                       # 构建系统脚本与依赖配置
├── .gitignore                            # 编译产物与中间调试文件忽略规则
├── LICENSE                               # 官方 MIT 开源许可证
├── README.md                             # 中文工程技术展示与数学模型说明
├── README_EN.md                          # English Engineering Specification
└── README_JA.md                          # 日本語技術仕様書・学術ポートフォリオ
```

---

## 6. 系统部署与使用指南 (Quick Start)

### 6.1 硬件引脚分配表 (Pin Connections)

| 外设模块 | 引脚标识 | STM32F103C8T6 引脚 | 硬件复用与功能定义 |
| :---: | :---: | :---: | :---: |
| **光敏电阻传感器** | AO (模拟输出) | **PA1** | ADC1_IN1，用于环境照度分压采样 |
| **LED 功率调光驱动** | PWM_IN | **PA7** | TIM3_CH2，产生 10kHz 高频调光信号 |
| **ESP8266 Wi-Fi 模组** | TXD | **PA3** | USART2_RX，接收来自 Wi-Fi 的下行指令 |
| **ESP8266 Wi-Fi 模组** | RXD | **PA2** | USART2_TX，发送上行数据至 Wi-Fi 模组 |
| **串口调试终端** | TXD / RXD | **PA9 / PA10** | USART1_TX / USART1_RX，115200bps 打印 |
| **硬件模式按键** | KEY0 ~ KEY3 | **PB0 ~ PB3** | 触发本地调光、OneNET 模式与 APP 模式 |

### 6.2 嵌入式固件编译与烧写

1. 安装 **Keil uVision5 (MDK-ARM v5.x)**，并安装 `Keil.STM32F1xx_DFP` 芯片支持包。
2. 打开 `src/stm32Project/smartlamp.uvprojx` 工程文件。
3. 连接 **ST-Link V2** 仿真器至开发板 SWD 接口（SWCLK、SWDIO、GND、3V3）。
4. 在 Keil 中点击 **Rebuild**，完成无警告编译后点击 **Download**（F8）将固件烧入芯片。

### 6.3 运行与操作流程

1. **上电启动**：系统默认以分段闭环自适应调光模式运行，根据光敏传感器采样实时调整 LED 亮度。
2. **按键模式切换**：
   - 按下 **KEY3**：进入就地手动调光模式，通过按键步进增减占空比。
   - 按下 **KEY4**：启动 OneNET 云端遥测模式，ESP8266 连接路由器并以 2 秒周期推送照度数据至云平台。
   - 按下 **KEY5**：启动 Android 移动端交互模式，ESP8266 配置为 TCP 透传，等待手机 App 发送调光控制字。

---

## 7. 开源许可证 (License)

本项目基于 **MIT License** 开放源代码。详见项目根目录下的 [LICENSE](LICENSE) 文件。
