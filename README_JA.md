# STM32・ESP8266・OneNET クラウド連携型 組み込みスマート調光システム (基礎版)
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

## 1. プロジェクト概要 (Project Overview)

**STM32・ESP8266・OneNET クラウド連携型 組み込みスマート調光システム**は、スマートビルディング、省エネルギー環境制御、および多層IoT通信を志向した高信頼性サイバーフィジカル工学ソリューションです。

システムの中核プロセッサには産業グレードの **STMicroelectronics STM32F103C8T6 (ARM 32ビット Cortex-M3 コア @ 72MHz)** を採用。CdS光導電素子による環境照度センシング、パワーMOSFETによる低損失スイッチング駆動、マルチチャネルハードウェアタイマPWM調光、デュアル非同期シリアル通信（USART）、およびイベント駆動型有限状態機械を高密度に統合しています。スマート照明における局所適応制御、モバイルLAN直結操作、および広域クラウド遠隔監視という複合的な要求に対し、**「エッジ側閉ループ自律適応調光 ＋ 構内 Android 端末リアルタイム制御 ＋ 広域 OneNET IoT クラウドテレメトリ」**という三次元統合制御アーキテクチャを確立しました。

信号処理層では、内蔵12ビット逐次比較型（SAR）ADCと移動平均デジタルフィルタにより環境照度を高精度に定量化し、タイマ TIM3 チャネル2 から $10\text{ kHz}$ の高周波フリッカーフリーPWMを出力。通信層では、ESP8266 Wi-Fi ブリッジを介して EDP（Enhanced Device Protocol）プロトコルに基づくクラウドテレメトリと、透過型 TCP ソケットによるスマートフォン双方向コマンドリンクを同時に提供し、マイクロ秒オーダーの即応性と産業機器レベルの堅牢性を両立しています。

---

## 2. ハードウェア実装とシステム外観 (Visual Showcase)

<div align="center">

| システム全体アーキテクチャ・データフロー | STM32F103C8T6 制御コア基板実物 |
| :---: | :---: |
| <img src="docs/images/system_architecture.png" width="450" alt="System Architecture"> | <img src="docs/images/hardware_stm32.png" width="450" alt="STM32 Board"> |
| **Android モバイル端末操作アプリ UI** | **OneNET 広域 IoT クラウド遠隔テレメトリ画面** |
| <img src="docs/images/demo_android_app.png" width="450" alt="Android App"> | <img src="docs/images/demo_onenet_cloud.png" width="450" alt="OneNET Cloud"> |

</div>

---

## 3. 数理モデルと制御工学的定式化 (Mathematical Formulations)

エッジファームウェアおよび制御ループには、厳密な光電変換理論、離散フィルタリング、ハードウェアPWM変調特性、および適応補償則が実装されています。

### 3.1 光導電素子（CdS）光電変換特性と分圧回路方程式

硫化カドミウム光導電セルの電気抵抗値 $R_{\text{photo}}$ は、入射照度 $E$（単位：$\text{lux}$）に対して非線形べき乗特性に従って減少します。10 lux における基準抵抗を $R_{10}$、光電感度指数を $\gamma$ と定義します：

$$
R_{\text{photo}}(E) = R_{10} \cdot \left( \frac{E}{10} \right)^{-\gamma}
$$

分圧回路は精密基準抵抗 $R_{\text{fixed}}$ との直列接続で構成され、ADC サンプリング端子に入力される瞬時分圧値は以下で与えられます：

$$
V_{\text{in}}(E) = V_{\text{ref}} \cdot \frac{R_{\text{photo}}(E)}{R_{\text{fixed}} + R_{\text{photo}}(E)}
$$

### 3.2 12ビット逐次比較型（SAR）ADC 量子化と移動平均デジタルフィルタ

STM32F103 内蔵の 12ビット SAR ADC は、基準電圧 $V_{\text{ref}} = 3.3\text{ V}$ に対し $2^{12} - 1 = 4095$ 階調の離散量子化を実行します：

$$
\text{ADC}_{\text{raw}} = \left\lfloor \frac{V_{\text{in}}}{V_{\text{ref}}} \cdot 4095 \right\rfloor
$$

商用電源の誘導ノイズや高周波ランダム雑音を除去するため、窓長 $N = 10$ の離散移動平均フィルタを適用します：

$$
\overline{\text{ADC}}_k = \frac{1}{N} \sum_{i=0}^{N-1} \text{ADC}_{k-i}
$$

### 3.3 タイマ TIM3 ハードウェア高周波 PWM 変調出力特性

STM32 の汎用タイマ TIM3 は 72MHz APB1 バス上に配置され、プリスケーラレジスタ（PSC）および自動再ロードレジスタ（ARR）により高周波キャリアを生成します：

$$
f_{\text{PWM}} = \frac{f_{\text{CLK}}}{(\text{PSC} + 1) \cdot (\text{ARR} + 1)} = \frac{72\text{ MHz}}{(0 + 1) \cdot 7200} = 10\text{ kHz}
$$

有効デューティ比 $D_{\text{PWM}}$ はキャプチャ/比較レジスタ CCR2 により直接制御されます：

$$
D_{\text{PWM}} = \frac{\text{CCR2}}{\text{ARR}} \times 100\% = \frac{\text{CCR2}}{7200} \times 100\%
$$

### 3.4 区分線形逆照度自律適応閉ループ補償則

視覚的快適性を保ち過補償によるハンチングを防止するため、不感帯付き三段階区分適応補償関数を適用します：

$$
D_{\text{target}}(\overline{\text{ADC}}) = \begin{cases} \frac{5000}{7200} \approx 69.4\%, & \overline{\text{ADC}} > 3000 \quad (\text{暗所環境：高出力光補償}) \\ \frac{3000}{7200} \approx 41.7\%, & 2000 < \overline{\text{ADC}} \le 3000 \quad (\text{適正照度：標準補償維持}) \\ \frac{1000}{7200} \approx 13.9\%, & \overline{\text{ADC}} \le 2000 \quad (\text{明所環境：省電力待機調光}) \end{cases}
$$

### 3.5 端雲間 IoT 通信遅延と物理伝送スループット境界

テレメトリパケット（ヘッダ、測定値、チェックサム）のサイズを $B_{\text{packet}} = 64\text{ Bytes}$、USART2 ボーレートを $115200\text{ bps}$ としたとき、シリアル伝送遅延は：

$$
T_{\text{UART}} = \frac{B_{\text{packet}} \times 10}{\text{BaudRate}} = \frac{64 \times 10}{115200} \approx 5.56\text{ ms}
$$

フィルタリング処理、UART 送信、802.11 無線伝送、およびインターネット網遅延を包含した端雲往復遅延特性は以下を満たします：

$$
T_{\text{total}} = T_{\text{filter}} + T_{\text{UART}} + T_{\text{RF}} + T_{\text{cloud}} \le 85\text{ ms}
$$

---

## 4. ハードウェア・ソフトウェア諸元 (System Specifications)

| サブシステム項目 | 採用技術・コンポーネント | 仕様諸元および実装標準 |
| :--- | :--- | :--- |
| **主制御マイコン (MCU)** | STMicroelectronics STM32F103C8T6 | 32ビット ARM Cortex-M3 @ 72MHz, 64KB Flash, 20KB SRAM |
| **無線通信モジュール** | Espressif ESP8266 (ESP-01/12F) | 802.11 b/g/n Wi-Fi, STA/AP 両対応, UART AT ブリッジ |
| **光センサユニット** | 硫化カドミウム (CdS) セルモジュール | 分光感度ピーク $400 \sim 700\text{ nm}$、応答速度 $\le 30\text{ ms}$ |
| **ADC サンプリング** | 内蔵 12-Bit SAR ADC (ADC1_IN1) | 変換速度 $1\text{ MSPS}$、PA1 端子、10回移動平均フィルタ |
| **パワー駆動回路** | Nチャネル パワー MOSFET モジュール | 最大 24V / 5A DC 負荷駆動対応、フォトカプラ絶縁保護 |
| **PWM 出力仕様** | 汎用タイマ TIM3 チャネル 2 (PA7) | キャリア周波数 $10\text{ kHz}$、7200段階高分解能、フリッカーレス |
| **クラウドプロトコル** | 中国移動 OneNET IoT クラウド | EDP 長期接続認証、定期テレメトリ送信周期 $2.0\text{ 秒}$ |
| **モバイル操作端末** | Android ネイティブアプリ (Java) | 透過型 TCP ソケット通信、デューティ比微調整 ($\pm 1000$) |

---

## 5. ディレクトリ構造 (Repository Layout)

```text
Intelligent-Lighting-Control-System-Basic/
├── docs/
│   └── images/
│       ├── system_architecture.png       # システム全体アーキテクチャ・データフロー図
│       ├── hardware_stm32.png            # STM32F103C8T6 制御コア基板実写
│       ├── hardware_esp8266.png          # ESP8266 Wi-Fi 通信モジュール実写
│       ├── hardware_led_control.png      # 信号調理・MOSFET パワー駆動基板実写
│       ├── hardware_led_power.png        # LED 駆動用定電圧安定化電源モジュール
│       ├── hardware_stlink.png           # ST-Link V2 SWD デバッガ実写
│       ├── hardware_cp2102.png           # CP2102 USB-UART シリアル変換器
│       ├── demo_android_app.png          # Android 操作画面スクリーンショット
│       └── demo_onenet_cloud.png         # OneNET クラウド遠隔ダッシュボード
├── src/
│   ├── stm32Project/                     # Keil uVision MDK-ARM 組み込みファームウェア
│   │   ├── CMSIS/                        # ARM Cortex-M3 コア依存層
│   │   ├── FWLIB/                        # STM32F10x 公式標準ペリフェラルライブラリ
│   │   └── USER/                         # アプリケーション層ソースコード
│   │       ├── main.c                    # メインループおよびモード遷移状態機械
│   │       ├── adc.c / adc.h             # 12ビット ADC ドライバ・移動平均フィルタ
│   │       ├── timer.c / timer.h         # TIM3 ハードウェア PWM 駆動ドライバ
│   │       ├── esp8266.c / esp8266.h     # ESP8266 AT コマンド・TCP 透過エンジン
│   │       ├── onenet.c / onenet.h       # OneNET クラウドパケットシリアライザ
│   │       ├── edpkit.c / edpkit.h       # EDP プロトコルパッカ・パーサスタック
│   │       ├── key.c / key.h             # タクトスイッチデバウンス・スキャン処理
│   │       └── usart.c / usart.h         # USART1 ログおよび USART2 通信ドライバ
│   └── androidControl/                   # Android Studio ネイティブアプリ
│       ├── app/                          # アプリ UI レイアウトおよびソケット通信
│       └── gradle/                       # Gradle ビルドスクリプト
├── .gitignore                            # Keil MDK・Android ビルド中間生成物除外設定
├── LICENSE                               # 公式 MIT オープンソースライセンス条文
├── README.md                             # 中国語技術解説ドキュメント
├── README_EN.md                          # 英語エンジニアリング仕様書
└── README_JA.md                          # 日本語技術仕様書・学術ポートフォリオ
```

---

## 6. ビルド・書き込みおよび操作手順 (Quick Start)

### 6.1 ピンアサイン定義 (Pin Mapping)

| 接続周辺デバイス | モジュール端子 | STM32 接続ピン | ハードウェア機能定義 |
| :---: | :---: | :---: | :---: |
| **光導電セル（CdS）** | AO (アナログ出力) | **PA1** | ADC1_IN1、環境照度分圧入力 |
| **LED MOSFET ドライバ** | PWM_IN | **PA7** | TIM3_CH2、10kHz 高周波調光ライン |
| **ESP8266 Wi-Fi** | TXD | **PA3** | USART2_RX、下りコマンド受信 |
| **ESP8266 Wi-Fi** | RXD | **PA2** | USART2_TX、上りテレメトリ送信 |
| **デバッグシリアル** | TXD / RXD | **PA9 / PA10** | USART1_TX / USART1_RX、115200bps 出力 |
| **モード切替キー** | KEY0 ~ KEY3 | **PB0 ~ PB3** | 動作モード選択および手動調光入力 |

### 6.2 ファームウェアのビルドとフラッシュ書き込み

1. **Keil uVision5 (MDK-ARM v5.x)** を起動し、`Keil.STM32F1xx_DFP` パックが導入されていることを確認します。
2. プロジェクト `src/stm32Project/smartlamp.uvprojx` を開きます。
3. **ST-Link V2** デバッガを開発基板の SWD ポート（SWCLK、SWDIO、GND、3V3）に接続します。
4. **Rebuild** を実行してエラーおよび警告がないことを確認し、**Download**（F8）キーでチップ内 Flash メモリへ書き込みます。

### 6.3 動作モードと実証フロー

1. **電源投入**：起動後、デフォルトで閉ループ自律適応調光モードが動作し、照度に応じて LED 輝度が自動調節されます。
2. **キーによるモード遷移**：
   - **KEY3** 押下：手動調光モードへ移行し、ボタン操作でデューティ比を段階的に増減。
   - **KEY4** 押下：OneNET クラウドモードへ移行し、ESP8266 がルータ経由で接続し 2 秒周期で照度データをアップロード。
   - **KEY5** 押下：Android 端末直接制御モードへ移行し、ESP8266 が TCP サーバとして待機しアプリからの指示を受信。

---

## 7. ライセンス (License)

本リポジトリは **MIT License** のもとで公開されています。詳細は [LICENSE](LICENSE) をご参照ください。
