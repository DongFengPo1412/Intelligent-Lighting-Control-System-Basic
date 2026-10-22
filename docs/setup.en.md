# Basic setup and operation

[简体中文](setup.zh-CN.md) · **English** · [日本語](setup.ja.md) · [Project overview](../README_EN.md)

[Hardware](#hardware) · [Programs](#programs) · [Toolchain](#toolchain) · [Operation](#operation) · [Troubleshooting](#troubleshooting)

This guide covers archived feature projects, not an assumed unified release. Read the [outstanding source issues](technical-notes.en.md#implementation-status), identify the version, then build and flash.

<a id="hardware"></a>

## Hardware and connections

| Component/interface | Prototype use and checks |
| :--- | :--- |
| ASRPRO board | Participant-described ASRPRO v2.0 with microphone and external speaker; identify the actual Flash capacity. |
| Four WS2812B panels | 8×8 each, 256 LEDs, logically top-left/top-right/bottom-left/bottom-right. Connect each DOUT to the next DIN and verify internal panel routing. |
| SDK logical Pin 2 | LED data output. Logical numbers are not chip package pins or connector positions. |
| SDK logical Pins 13/14 | UART TX/RX under `SECOND_FUNCTION`, crossed to HM-10 RX/TX, with a shared signal ground. |
| HM-10 | Phone BLE to controller UART bridge. Identify bare module/carrier supply and logic specifications; do not assume all variants accept 5 V at VCC. |
| Computer USB | Actual prototype supply; brightness values do not establish USB capacity, voltage drop, or headroom. |
| Speaker | Connected to the board speaker interface. Amplification is a board feature; verify actual impedance/power. |
| Wooden enclosure | Purchased box, transparent lid, and USB cutout. Lid material and internal level conversion are unconfirmed. |

Use the actual board documentation for connections. No measured whole-system current budget is provided.

<a id="programs"></a>

## Select a feature project

| Goal | File | Key settings |
| :--- | :--- | :--- |
| Standard voice effects | [功能二.hd](../src/asrpro_firmware/tianwen_block_projects/功能二.hd) | 256 LEDs; wake “灯光助手”; red/blue/green, rainbow, flowing effect, off. Configured countdown has no handler. |
| Additional SDK effects | [功能2.hd](../src/asrpro_firmware/tianwen_block_projects/功能2.hd) | 256 LEDs; wake “灯光助手”; twelve commands including breathing/flowing/sparkling. |
| Expressions/RGB art | [最终版本.hd](../src/asrpro_firmware/tianwen_block_projects/最终版本.hd) | 256 LEDs; wake “吃豆人”; five commands. Address delay types, RGB indices, and mapping first. |
| Random bars | [功能三.hd](../src/asrpro_firmware/tianwen_block_projects/功能三.hd) | Wake “语音助手”; play/stop. Configure music audio separately and verify loop exit. |
| Bluetooth game | [贪吃蛇.hd](../src/asrpro_firmware/tianwen_block_projects/贪吃蛇.hd) | 256 LEDs, 115200 bps, no speech entries. |
| Bluetooth light test | [蓝牙点灯.hd](../src/asrpro_firmware/tianwen_block_projects/蓝牙点灯.hd) | 64 LEDs, 9600 bps, on/off strings. |
| Historical comparison | [main_asrpro_ws2812.cpp](../src/asrpro_firmware/main_asrpro_ws2812.cpp), [RGB.hd](../src/asrpro_firmware/tianwen_block_projects/RGB.hd) | Early versions, not a single entry point for all features. |

<a id="toolchain"></a>

## Tools, voice assets, and flashing

1. Install Tianwen Block with ASRPRO support and the appropriate USB serial driver. Identify core/development board, Flash capacity, and download port.
2. Open the selected `.hd`, using graphical mode for XML and code mode for C++ content. The platform provides `asr.h`, `setup.h`, and `myLib/asr_ws2812.h`. This repository is not a standalone CMake, PlatformIO, or Arduino build project.
3. Check wake words, IDs, and replies. Generate voice/model resources after changes; platform configuration does not establish independent acoustic-model training.
4. For music, replace the selected reply asset with a prepared fixed clip. Original demonstration audio and generated resources are not fully distributed.
5. Review known code issues, build, and select the actual board/Flash download configuration. An older instruction mentioning “2M” is not sufficient to identify every board.
6. Restart after flashing and check startup, wake, one effect, serial input, and exit separately. Hardware has not been retested in this documentation pass; retain build logs and any source changes.

<a id="operation"></a>

## Operation by program

### Speech lighting and expressions

Say the selected project's wake word and wait for its fixed reply before issuing a configured command. “最终版本” uses “显示笑脸”, “显示哭脸”, “变脸”, “显示桌宠”, and “关闭灯光”. “功能二/功能2” use a different lighting vocabulary; do not combine command sets across files.

The SDK manual describes a default 15-second no-command timeout, subject to tool version. Speech-only programs do not require Bluetooth pairing. Chip AEC support does not establish interruption at any point in an animation or music loop.

### Phone-controlled Snake

1. Use the game version and match the HM-10 UART rate to 115200 bps before connecting the phone BLE client.
2. Use the original five-button Blinker setup and verify that the controller receives uppercase single characters `E`, `W`, `S`, `A`, `D`. The app configuration is not archived. First test those bytes with a BLE serial tool if needed, then adapt the buttons; extra payload or automatic repeats may affect control.
3. Send `E` while stopped to start. `W/S/A/D` mean up/down/left/right; `E` is ignored during play.
4. Self-collision flashes red, then outputs `Game Over! Your Score: ...` over UART. Text visibility depends on the receiving phone interface. This source has no LED numeric score or voice-start path.

### Phone lighting test

`蓝牙点灯.hd` uses 9600 bps, 64 LEDs, and exact `readString()` comparisons to `on`/`off`. These are multi-byte strings, unlike the game's character protocol. Line endings/timeouts affect matching; do not reuse game settings blindly.

<a id="troubleshooting"></a>

## Reproduction checks and troubleshooting

| Symptom | Check first |
| :--- | :--- |
| Command unrecognized | Project version, wake state, command ID, and whether matching resources/application were flashed. |
| Narrowing error in delays | `uint8_t` cannot hold 300/500; use an appropriate type in a corrected revision and revalidate timing. |
| RGB artwork displaced/corrupt | 1–16 out-of-bounds access, linear/block mapping differences, and physical panel orientation. |
| BLE connected but no control | Transparent-UART setup, baud rate, TX/RX, character case, and actual firmware. |
| on/off does nothing | Wrong game firmware or extra newline/payload characters. |
| Animation/music cannot exit | Long loops and blocking delays; AEC capability does not replace application exit logic. |
| No LED numeric score | Archived code only prints serial; matching digit bitmaps/demo logic are missing. |
| Full-board/rapid-turn issue | Food-generation exit, multiple direction changes per step, and shared state. |

No fully reproduction-tested unified release is claimed. Any code additions/fixes should be committed separately, with build environment recorded before hardware tests.

[Technical notes](technical-notes.en.md) · [Project overview](../README_EN.md)
