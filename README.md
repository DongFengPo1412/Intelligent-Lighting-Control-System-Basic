# 基于 ASRPRO 与 WS2812 矩阵的智能离线语音灯光音乐交互系统（初阶）
# Intelligent Lighting & Audio-Visual Interactive System Based on ASRPRO & WS2812 Matrix (Basic Level)

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![MCU: ASRPRO AI Voice](https://img.shields.io/badge/MCU-ASRPRO%20AI%20Voice%20SoC-red.svg?style=flat-square)](https://www.twen51.com/)
[![LED: WS2812B 16x16](https://img.shields.io/badge/Matrix-WS2812B%2016x16%20RGB-green.svg?style=flat-square)](https://www.world-semi.com/)
[![Wireless: HM-10 BLE](https://img.shields.io/badge/Wireless-HM--10%20BLE%204.0-orange.svg?style=flat-square)](docs/)
[![Platform: Tianwen Block](https://img.shields.io/badge/Platform-Tianwen%20Block-blueviolet.svg?style=flat-square)](src/)
[![Course: UESTC Comprehensive Project](https://img.shields.io/badge/UESTC-Comprehensive%20Curriculum%20Design-blueviolet.svg?style=flat-square)](https://www.uestc.edu.cn/)

[**中文文档**](README.md) | [**English**](README_EN.md) | [**日本語**](README_JA.md)

</div>

---

## 1. 项目背景与学术渊源 (Academic Heritage & Background)

本项目源自**电子科技大学（UESTC）自动化工程学院**核心实践课程——**《综合课程设计（初阶）》**优秀工程设计成果。

在智能家居、情感化人机交互与数字化声光艺术飞速发展的背景下，传统的灯具控制大多局限于单一的机械开关或基于智能手机 App 的冷启动触控，存在**交互维度单一、缺乏人机交互温度、无法在断网工况下工作、灯光表现力匮乏**等痛点。

针对上述挑战，本课题以高集成度、沉浸式声光律动与多模态无线交互为导向，研发了一套**基于 ASRPRO 离线语音与 16×16 WS2812B 全彩矩阵的智能声光交互系统**：
- **边缘离线 AI 语音枢纽**：以 **ASRPRO 高性能离线语音识别芯片**（天问 51 内核 / 神经网络语音处理器 NPU）为核心，内置硬件声学回声消除（AEC）与降噪算法，无需联网即可实现毫秒级快速响应（安静环境下识别准确率高达 $98\%$，典型噪声环境下超 $90\%$）；
- **高密度全彩光矩阵**：将 4 块 8×8 WS2812B 智能外控 RGB 模组精密级联拼接为 **16×16 点阵屏（共 256 颗独立像素）**，通过单线高频归零码协议实现 24 位真彩色（16,777,216 色）细腻渲染；
- **全木质实物集成与沉浸式交互**：自主设计并打磨实木画框与亚克力遮光面板，内置高保真差分麦克风与 8002A 音频功率放大器，支持情感表情动画（微笑道别、伤心流泪）、光立方彩虹渐变律动、低功耗蓝牙（HM-10 BLE 4.0）无线遥控以及交互式掌上贪吃蛇游戏；
- **软硬件协同开发链路**：提供天问 Block（TWenBlock）可视化图形编程积木与底层 Native C++ 算法源码双轨开发支持，软硬件系统高度模块化、高鲁棒性。

---

## 2. 硬件实物与工程架构展示 (Hardware & System Showcase)

### 2.1 木质画框实物与矩阵发光效果 (Physical Hardware Artifacts)

<div align="center">

| 16×16 矩阵木框实物发光与互动游戏状态 | 情感化表情动画（微笑道别/点阵表情）实拍 |
| :---: | :---: |
| <img src="docs/images/demo_hardware_enclosure_active.jpg" width="480" alt="Active Hardware Enclosure"> | <img src="docs/images/demo_led_matrix_smile_face.jpg" width="480" alt="Smile Face LED Matrix"> |
| **实物画框集成**：四象限 WS2812B 拼接屏在精工木框内运行贪吃蛇互动游戏与单点高亮 | **情感表情渲染**：16×16 点阵以紫白高对比度真彩动态输出像素微笑了、哭泣与对话动画 |

| 四象限彩虹渐变光效展示 | 点阵发光与内部走线细节 |
| :---: | :---: |
| <img src="docs/images/demo_hardware_wood_case.jpg" width="480" alt="Rainbow Gradient Glow"> | <img src="docs/images/demo_hardware_matrix_glow.jpg" width="480" alt="Internal Wiring and LEDs"> |
| **四象限彩虹渐变**：蓝紫、翠绿、炽橙、青蓝四色平滑光影律动，营造沉浸式环境光 | **点阵走线工艺**：高集成度 3M 导热胶固定、标准 2.54mm 排针镀锡焊接与防抖排线布局 |

</div>

### 2.2 系统全景拓扑与声光数据流 (System Architecture & Data Flow)

系统整体构建了自声学拾音、离线神经网络语音识别、矩阵驱动到蓝牙遥控的闭环架构：

```mermaid
graph TD
    A[用户语音指令 "你好小天" / "打开灯光"] -->|差分拾音| B[驻极体拾音麦克风 + 前置放大]
    B -->|模拟音频信号| C[ASRPRO 芯片: AEC 回声消除 & 硬件 NPU]
    C -->|神经网络模型匹配| D{识别置信度判决 S > S_th}
    D -->|匹配成功| E[8002A 功放 + 扬声器 语音播报]
    D -->|发送指令 ID| F[主控状态机: 模式 / 动画 / 游戏切换]
    G[智能手机 App / 遥控终端] -->|BLE 4.0 串口透传| H[HM-10 蓝牙模块 (UART)]
    H -->|按键 / 方向控制流| F
    F -->|单线归零码 800kHz 驱动| I[WS2812B 16x16 全彩矩阵 (256 像素)]
    I --> J[动态像素表情 / 四象限彩虹光立方 / 贪吃蛇游戏]
```

1. **声学感知与降噪层 (Acoustic Frontend)**：高灵敏度驻极体麦克风捕捉环境声学信号，硬件电路执行模拟预滤波与偏置调理，送入 ASRPRO 片上 16-bit ADC；
2. **边缘智能语音识别层 (Edge AI Speech Core)**：芯片内置硬件 NPU 提取声学梅尔倒谱特征（MFCC），快速完成词条模板与声学模型打分。识别成功后调用片上音频解码器，经 8002A 功放向喇叭播放自然人声应答；
3. **灯光动画与逻辑引擎 (Matrix Display Engine)**：内置 16×16 位图字模库与蛇形拓扑映射算法，支持静态位图加载、行/列滑动扫描、颜色空间转换与动态帧刷新（刷新率超 100Hz）；
4. **无线蓝牙与游戏交互层 (BLE & Interaction)**：HM-10 模块接收手机蓝牙指令，支持远程调色、开关灯、模式切换以及操控点阵贪吃蛇游戏的上下左右运动。

---

## 3. 硬件电路原理与互连规范 (Hardware & Circuit Design)

<div align="center">

| ASRPRO 核心板官方原理图 (MCU + MIC + SPK + AEC) | WS2812B 单颗级联电路与滤波退耦规范 |
| :---: | :---: |
| <img src="docs/images/hardware_asrpro_schematic.png" width="480" alt="ASRPRO Schematic"> | <img src="docs/images/hardware_ws2812_cascade_schematic.png" width="480" alt="WS2812 Cascade Schematic"> |
| **ASRPRO 核心电路**：TW-ASR-Pro 处理器、回声消除（AEC）、MICBIAS 麦克风偏置及 8002A 功放电路 | **WS2812B 级联原理**：单线信号从 DIN 逐级整形成型输出至 DOUT，各像素独立配置 100nF 旁路滤波电容 |

</div>

### 3.1 ASRPRO 核心板硬件电路架构

ASRPRO 核心模块采用专为离线语音处理研发的 SoC 架构，集成度极高：
- **微处理器内核**：内置高性能天问 51 内核与 32 位专用 DSP 协处理器，片载高容量 SPI Flash 存储词条模型与语音固件；
- **麦克风前端放大电路 (MIC Circuit)**：采用低噪声稳压偏置源 `MICBIAS`（输出纯净参考电压），通过 $C_8, C_9$（$0.1\mu\text{F}$）与 $R_3, R_4, R_7$（$2.2\text{k}\Omega / 10\text{k}\Omega$）构成差分输入拓扑，滤除电源共模噪声；
- **音频功率放大子系统 (SPK / Audio PA)**：选用工业级微型音频功放芯片 **8002A**（SOP-8 封装），在 $5\text{V}$ 供电、负载 $3\Omega$ 扬声器工况下可输出 $3\text{W}$ 额定失真度 $< 10\%$ 的充沛音频功率；
- **回声消除硬件网络 (AEC Network)**：扬声器正极 `SPKL+` 经 $C_{13}$（$100\text{nF}$）与分压衰减电阻 $R_8, R_9$ 回采至主芯片 `MICP_R` 比较引脚，实现本地播放提示音时的声学回声主动抵消，确保播报时仍能精准打断唤醒。

### 3.2 WS2812B 16×16 智能矩阵拼接设计

- **模组拼接与信号拓扑**：由 4 块独立的 $8 \times 8$ 硬板 RGB 矩阵无缝平铺，采用“上左右下”顺序级联；
- **级联走线**：
  - 第一块矩阵的 `DIN` 接 ASRPRO 的 `PA_2` 数字引脚，其 `DOUT` 引出连接至第二块矩阵的 `DIN`；
  - 依次串接至第四块矩阵，构成总长为 256 颗灯珠的超长移位级联链；
- **电源完整性设计**：由于 256 颗 RGB LED 满幅白光点亮（全开 $R=G=B=255$）时瞬间峰值工作电流可达：
  
  $$
  I_{\text{peak}} = 256 \times (20\text{ mA} \times 3) = 15.36\text{ A}
  $$
  
  为避免远端供电线压降（IR-Drop）导致尾端色偏与芯片复位，系统在固件中将最大全局亮度钳位在 $20\% \sim 30\%$（稳态平均功耗 $< 1.5\text{A}$），并在电源母线输入端并联 $1000\mu\text{F}$ 低阻抗铝电解电容，每块子矩阵配备独立加粗的 $5\text{V}$ 与 `GND` 供电总线。

### 3.3 无线蓝牙通信子系统 (HM-10 BLE 4.0)

- **射频规格**：选用基于 TI CC2541 的 HM-10 蓝牙 4.0 低功耗从机模块，工作频段 $2.4\text{GHz}$ ISM 频段，调制方式 GFSK；
- **接口连接**：模块的 `TXD` 和 `RXD` 交叉连接至主控板的硬件串口（波特率 $9600\text{bps}$ 或 $115200\text{bps}$），手机端 App 通过 BLE GATT 协议向特定特征值写入单字节控制指令（如 `'E'` 开启贪吃蛇，`'W'` 切换笑脸，`'R'`/`'G'`/`'B'` 切换纯色）。

---

## 4. 核心数学模型与驱动算法推导 (Mathematical Formulations)

系统在固件与图形化逻辑中构建了严格的纳秒级时序、空间坐标映射与离线语音特征匹配数学模型。

### 4.1 WS2812B 单线归零码（NZR）时序参数与传输方程

WS2812B 数据协议基于精准纳秒级单线归零码（Non-Return-to-Zero, NZR）。每个二进制位传输周期为 $T_{\text{bit}} = 1.25\mu\text{s} \pm 150\text{ns}$：
- **逻辑 0 码**：高电平持续时间 $T_{0\text{H}} = 400\text{ns} \pm 150\text{ns}$，低电平持续时间 $T_{0\text{L}} = 850\text{ns} \pm 150\text{ns}$；
- **逻辑 1 码**：高电平持续时间 $T_{1\text{H}} = 850\text{ns} \pm 150\text{ns}$，低电平持续时间 $T_{1\text{L}} = 400\text{ns} \pm 150\text{ns}$；
- **复位帧锁存电平**：低电平持续时间 $T_{\text{reset}} > 50\mu\text{s}$（固件标准取 $280\mu\text{s}$）。

每个像素包含 24 位色彩数据，严格按 **高位先出（MSB First）** 的 **G-R-B** 顺序发送：

$$
\mathbf{C} = [G_7, G_6, \dots, G_0, R_7, R_6, \dots, R_0, B_7, B_6, \dots, B_0] \in \{0, 1\}^{24}
$$

对级联总数为 $N = 256$ 颗的点阵系统，单帧传输总耗时为：

$$
T_{\text{frame}} = N \cdot 24 \cdot T_{\text{bit}} + T_{\text{reset}} = 256 \times 24 \times 1.25\mu\text{s} + 280\mu\text{s} = 7.68\text{ ms} + 0.28\text{ ms} = 7.96\text{ ms}
$$

系统理论最大无撕裂全彩画面刷新率为：

$$
f_{\text{refresh, max}} = \frac{1}{T_{\text{frame}}} = \frac{1}{7.96 \times 10^{-3}\text{ s}} \approx 125.6\text{ Hz}
$$

该帧率远超人眼视觉暂留频率（$24\text{Hz}$），确保了动态表情与彩虹流动光影毫无频闪与撕裂感。

### 4.2 16×16 点阵蛇形拓扑二维空间直角坐标映射变换方程

在平面显示中，像素点直角坐标定义为 $(x, y)$，其中横坐标 $x \in [0, 15]$（自左向右），纵坐标 $y \in [0, 15]$（自上向下）。

由于物理电路布线采用蛇形（Serpentine）反向折线走线，偶数行与奇数行的物理移位顺序相反。定义空间逻辑坐标 $(x, y)$ 到一维显存线性索引 $\text{Index} \in [0, 255]$ 的非线性映射变换方程为：

$$
\text{Index}(x, y) = 
\begin{cases} 
16 \cdot y + x, & \text{当 } y \equiv 0 \pmod 2 \quad (\text{偶数行，正向顺序}) \\
16 \cdot y + (15 - x), & \text{当 } y \equiv 1 \pmod 2 \quad (\text{奇数行，反向逆序})
\end{cases}
$$

矩阵位图动画渲染时，设某时刻目标表情的 16 位行字模向量为 $\mathbf{W}_y = [b_{15}, b_{14}, \dots, b_0]$。第 $x$ 列像素点的开关与颜色判定满足：

$$
\text{PixelColor}(x, y) = 
\begin{cases} 
(R, G, B), & \text{若 } (W_y \gg (15 - x)) \ \& \ 0x0001 = 1 \\
(0, 0, 0), & \text{若 } (W_y \gg (15 - x)) \ \& \ 0x0001 = 0
\end{cases}
$$

### 4.3 离线语音声学特征提取与贝叶斯最大后验概率匹配

ASRPRO 芯片在端侧运行轻量级隐马尔可夫模型与深度前馈神经网络（HMM-DNN）：
1. **预加重与加窗分帧**：采样率 $f_s = 16\text{kHz}$，帧长 $25\text{ms}$，帧移 $10\text{ms}$，采用汉明窗（Hamming Window）进行时域截断；
2. **美尔倒谱系数 (MFCC)**：通过离散傅里叶变换（DFT）计算功率谱，经 24 通道三角美尔带通滤波器组卷积后进行离散余弦变换（DCT），提取 13 维静态 MFCC 及其一阶、二阶差分，构建 39 维时序声学特征矢量 $\mathbf{O} = [\mathbf{o}_1, \mathbf{o}_2, \dots, \mathbf{o}_T]$；
3. **最大后验概率 (MAP) 模式匹配判决**：在预置的词条集合 $\mathcal{W}$ 中搜索最佳匹配词 $\hat{W}$：

$$
\hat{W} = \arg\max_{W \in \mathcal{W}} P(W | \mathbf{O}) = \arg\max_{W \in \mathcal{W}} \left[ \ln P(\mathbf{O} | W) + \lambda \ln P(W) \right]
$$

当综合打分满足置信度门限 $S(\hat{W}) \ge S_{\text{threshold}} = 0.85$ 时，判定识别有效并向主控状态机分发唯一指令 ID。

---

## 5. 软件工程与图形化/代码化编程系统 (Software Systems)

系统支持天问 Block（TWenBlock）图形化积木拼装与底层 C/C++ 代码级混合编程双轨开发模式。

<div align="center">

| 天问 Block 离线语音识别词条配置界面 | 16×16 矩阵像素图案位图设计与取模工具 |
| :---: | :---: |
| <img src="docs/images/software_tianwen_block_voice_config.png" width="480" alt="Tianwen Block Voice Config"> | <img src="docs/images/software_matrix_pattern_design.png" width="480" alt="Matrix Pattern Design"> |
| **天问 Block 语音配置**：免代码可视化配置唤醒词、识别词条（如“打开灯光”、“显示笑脸”）及 TTS 播报音 | **像素图案矩阵取模**：可视化 16×16 点阵设计器，生成 16 进制 uint16 字模数组，实现像素级动画定义 |

</div>

- **天问 Block 可视化架构**：开发者通过直观拖拽“语音识别”、“WS2812 控制”、“延时与动画”等积木，一键编译生成底层 Keil / GCC 兼容固件并经 Type-C USB 烧录至芯片内置 Flash；
- **底层 C/C++ 核心状态机实现**：工程代码包含完整的动画与表情引擎，详见 [`src/asrpro_firmware/main_asrpro_ws2812.cpp`](file:///C:/workspace/Intelligent-Lighting-Control-System-Basic/src/asrpro_firmware/main_asrpro_ws2812.cpp)：
  ```cpp
  // 核心语音回调状态机
  void ASR_CODE() {
    switch (snid) {
      case 0: displaySpeakingAnimation(); break; // 唤醒时说话动态嘴形
      case 1: displaySmileyAnimation();   break; // 指令1: 显示动态微笑了
      case 2: displaycryAnimation();      break; // 指令2: 显示动态流泪哭泣
      case 3: displaySmileyAnimation();   break; // 指令3: 伴随音律播放笑脸
      case 4:                                   // 指令4: 关机/关灯
        ASR_WS2812_2.pixel_set_all_color(0, 0, 0);
        ASR_WS2812_2.pixel_show();
        break;
    }
  }
  ```

---

## 6. 系统主要技术指标 (System Specifications)

| 子系统维度 | 技术选型与部件 | 详细参数与性能指标 |
| :--- | :--- | :--- |
| **主控芯片 (MCU)** | 天问 51 ASRPRO (TW-ASR-Pro) | 高集成 AI 语音 SoC，内置神经网络推理协处理器，主频高达 240MHz |
| **离线语音识别能力** | 片上轻量级声学模型 (NPU) | 支持多达 150 条离线本地词条，安静环境识别率 $\ge 98\%$，响应延迟 $< 0.2\text{s}$ |
| **声学前端与扬声器** | 差分驻极体话筒 + 8002A 功放 | 硬件回声消除（AEC），板载 3W 功放芯片，支持 8 级动态数字音量调节 |
| **全彩显示矩阵** | WS2812B-V5 智能 RGB LED | 4 块 8×8 平铺拼接为 16×16（共 256 颗），24-bit 1677 万色，刷新率 $> 120\text{Hz}$ |
| **无线通信接口** | HM-10 BLE 4.0 蓝牙从机 | 工作频段 2.4GHz ISM，传输距离空旷处 $> 10\text{m}$，端到端指令通信延迟 $< 50\text{ms}$ |
| **外部结构与工艺** | 实木画框 + 亚克力面板 | 尺寸约 $150 \times 150 \times 40\text{ mm}$，3M 导热胶稳固矩阵，排针镀锡防震走线 |
| **供电系统** | DC 5V 外部稳压电源输入 | 具备防反接与大电容储能滤波，动态工作电流 $0.2\text{A} \sim 2.0\text{A}$（亮度自限流保护） |
| **开发环境与工具链** | 天问 Block (TWenBlock) / GCC | 支持图形化积木拼装及底层 C/C++ 源码编译烧录，Type-C USB 免驱下载 |

---

## 7. 仓库目录结构说明 (Repository Layout)

```text
Intelligent-Lighting-Control-System-Basic/
├── docs/
│   └── images/
│       ├── demo_hardware_enclosure_active.jpg      # 木质画框实物点亮与互动状态图 (4064x3048)
│       ├── demo_led_matrix_smile_face.jpg          # 16x16 矩阵微笑了表情高对比度实拍图 (2448x3264)
│       ├── demo_hardware_wood_case.jpg             # 四象限彩虹流动光影木框成品图 (3048x4064)
│       ├── demo_hardware_matrix_glow.jpg           # 点阵发光与内部走线细节图
│       ├── demo_hardware_internal_wiring.jpg       # 矩阵背面走线与绝缘工艺细节图
│       ├── hardware_asrpro_schematic.png           # ASRPRO 核心板官方完整原理图 (MCU/MIC/SPK/AEC)
│       ├── hardware_ws2812_cascade_schematic.png   # WS2812B 级联与去耦电路原理图
│       ├── hardware_asrpro_module.jpg              # ASRPRO 核心板硬件模块实拍图
│       ├── software_tianwen_block_voice_config.png # 天问 Block 离线语音配置图形化界面图
│       ├── software_matrix_pattern_design.png      # 16x16 像素图案字模矩阵设计器
│       └── software_bluetooth_control_app.png      # 蓝牙手机端无线交互控制界面图
├── src/
│   └── asrpro_firmware/
│       ├── main_asrpro_ws2812.cpp                  # ASRPRO 核心固件源码 (语音中断+WS2812矩阵驱动+表情状态机)
│       └── tianwen_block_projects/
│           ├── 最终版本.hd                         # 天问 Block 初阶完整工程源文件
│           ├── 贪吃蛇.hd                           # 16x16 矩阵点阵贪吃蛇交互游戏工程
│           ├── 蓝牙点灯.hd                         # HM-10 蓝牙通信控制工程
│           ├── RGB.hd                              # 全彩色彩空间平滑渐变算法工程
│           ├── 功能二.hd                           # 模式二功能工程
│           └── 功能三.hd                           # 模式三功能工程
├── LICENSE                                         # MIT 官方开源许可协议
├── README.md                                       # 中文工程技术文档与数学推导
├── README_EN.md                                    # English Comprehensive Engineering Specification
└── README_JA.md                                    # 日本語技術仕様書・学術ポートフォリオ
```

---

## 8. 快速上手与固件烧录指南 (Quick Start Guide)

### 8.1 硬件引脚分配与连线定义 (Pinout Mapping)

| ASRPRO 核心板引脚 | 外部模组 / 连接目标 | 引脚功能与信号定义 |
| :---: | :---: | :---: |
| **5V** | WS2812B 矩阵 $V+$ / 蓝牙 VCC | DC 5V 系统供电输入总线 |
| **GND** | WS2812B 矩阵 $V-$ / 蓝牙 GND | 电源公共参考地 |
| **PA_2** | WS2812B 第一块矩阵 `DIN` | 单线高频归零码数字驱动信号线（800kHz） |
| **TXD (UART0_TX)** | HM-10 蓝牙模块 `RXD` | 串口异步发送信号线（默认波特率 9600） |
| **RXD (UART0_RX)** | HM-10 蓝牙模块 `TXD` | 串口异步接收信号线 |
| **SPKL+ / SPKL-** | 8Ω 2W 微型动圈喇叭 | 8002A 差分桥式音频功放输出端 |
| **MICL+ / MIC-** | 驻极体微型拾音话筒 | 差分音频信号拾音输入端 |

### 8.2 工具链安装与天问 Block 固件编译

1. 从官方渠道下载并安装 **天问 Block 2025（TWenBlock）** 桌面开发套件；
2. 双击打开 `天问 Block`，在界面右上角点击“打开项目”，导入位于 [`src/asrpro_firmware/tianwen_block_projects/最终版本.hd`](file:///C:/workspace/Intelligent-Lighting-Control-System-Basic/src/asrpro_firmware/tianwen_block_projects/最终版本.hd)；
3. 使用 Type-C 数据线将 ASRPRO 核心板连接至电脑 USB 口；
4. 在软件顶部工具栏选择目标板卡型号 `ASRPRO-Core`，选择识别到的 CH340 虚拟串口；
5. 点击 **“编译固件”**，天问 Block 将自动生成机器模型、字模数据与 C++ 源码；
6. 编译通过后点击 **“一键烧录”**，程序通过 USB ISP 写入芯片内置 Flash。

### 8.3 交互测试与控制指令清单

1. **唤醒系统**：对设备呼唤预设唤醒词 **“你好小天”**（或自定义唤醒词）；
   - 扬声器播报应答语音：“*在呢，主人*”；
   - 16×16 点阵矩阵瞬间切换为发声嘴形动画；
2. **表情互动指令**：
   - 说出 **“显示笑脸”**，点阵屏高亮渲染紫白相间的像素微笑了动态；
   - 说出 **“不要哭”**，点阵屏切换为流泪哭泣动画并播报安慰语音；
3. **灯光律动与模式控制**：
   - 说出 **“打开灯光”**，矩阵呈现四象限全彩彩虹流动渐变光影；
   - 说出 **“关闭灯光”**，全屏像素熄灭，系统进入超低功耗待机态；
4. **蓝牙遥控与游戏模式**：
   - 打开手机蓝牙串口 App（如 *BLE SPP* 或 *Blinker*），搜索并连接 `HM-10` 蓝牙模组；
   - 发送指令字符 `'E'`，矩阵加载贪吃蛇游戏引擎，用户可通过方向键控制贪吃蛇移动吃点。

---

## 9. 团队与学术致谢 (Credits & Acknowledgments)

- **开发团队**：电子科技大学自动化工程学院 2023 级本科生卓越工科实践小组
  - 核心成员：学号 2023060904025（刘浩然）、2023060909014 等
- **指导教师**：电子科技大学自动化工程学院《综合课程设计（初阶）》教学团队
- **开源致谢**：特别鸣谢天问 51（TWen51）社区在 ASRPRO 离线语音底层库方面提供的技术支持。

---

## 10. 开源许可证 (License)

本项目代码及工程设计文件均基于 **MIT License** 开放源代码。详细条款请参阅根目录下的 [LICENSE](LICENSE) 文件。
