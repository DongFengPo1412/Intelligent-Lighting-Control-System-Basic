# Basic technical notes

[简体中文](technical-notes.zh-CN.md) · **English** · [日本語](technical-notes.ja.md) · [Project overview](../README_EN.md)

[Source map](#source-map) · [Speech](#speech) · [Graphics](#graphics) · [Music](#music) · [Game/UART](#game) · [Implementation scope](#implementation-status) · [References/media](#references)

These notes distinguish implementation, version differences, and reproduction conditions using archived application code, participant accounts, physical evidence, and platform documentation. Reports and slides are supporting references, not automatic proof of their metrics or architecture claims.

<a id="source-map"></a>

## Features, files, and versions

| File | Type | Features and scope |
| :--- | :--- | :--- |
| [main_asrpro_ws2812.cpp](../src/asrpro_firmware/main_asrpro_ws2812.cpp) | Early C++ expression code | One wake word and four commands; no RGB sprite, Bluetooth game, or nine-frame shutdown animation. |
| [最终版本.hd](../src/asrpro_firmware/tianwen_block_projects/最终版本.hd) | C++ expression/image project | One wake word and five commands; binary expressions, frame animation, a static RGB image, and lights off. |
| [功能二.hd](../src/asrpro_firmware/tianwen_block_projects/功能二.hd) | Graphical XML lighting project | One wake word and seven command entries; handlers cover IDs 1–6, but ID 7 countdown has no matching action. |
| [功能2.hd](../src/asrpro_firmware/tianwen_block_projects/功能2.hd) | Graphical XML multi-effect project | One wake word and twelve commands; SDK effects, solid colors, and off, with an effect-task configuration. |
| [功能三.hd](../src/asrpro_firmware/tianwen_block_projects/功能三.hd) | C++ random-bar experiment | One wake word and two commands; random heights/colors. Replacement audio assets are not distributed. |
| [贪吃蛇.hd](../src/asrpro_firmware/tianwen_block_projects/贪吃蛇.hd) | C++ two-task game | 256 LEDs, 115200 bps, E/W/S/A/D; empty speech callback and serial score output. |
| [蓝牙点灯.hd](../src/asrpro_firmware/tianwen_block_projects/蓝牙点灯.hd) | C++ speech/serial lighting test | One wake word and four commands; 64 LEDs, 9600 bps, on/off strings. |
| [RGB.hd](../src/asrpro_firmware/tianwen_block_projects/RGB.hd) | Early graphical XML test | One wake word and two command entries; entries/handlers are not fully aligned. It is not a complete gradient engine. |

The `.hd` extension covers both graphical XML and C++ text marked as code-mode projects. Vocabulary counts are per file and must not be added together as one firmware's command set. SDK calls, images, and replies depend on the selected version.

The file named “最终版本” does not contain every effect and game. Team recollection of a final combined firmware is uncertain; separate stored files establish archive structure, not that the demonstration necessarily used separate flashing. Voice game-start and LED numeric scoring are participant-reported demonstration features whose archived implementation has not been located.

<a id="speech"></a>

## Offline speech configuration and events

Configure wake words, commands, IDs, and reply audio, generate resources, then build and flash with application code. Resource generation alone is not deployment. Offline refers to device operation; development tools or resource-generation services may need a network connection.

`ASR_CODE` dispatches the SDK's `snid` events. It is an event handler, not evidence of a hardware interrupt service routine. Preset matching is not free conversation or LLM understanding. Speech resources come from the platform; no team-trained acoustic network pipeline is included here.

The ASRPRO programming-mode manual, page 21, describes a default wake timeout of 15 seconds. The archived application does not define one common explicit timeout, so this is documented as a platform default subject to SDK version, not a team-developed timer state machine.

Mouth animation uses preset frames and delays alongside replies, without phoneme extraction, audio-progress tracking, or phase-lock feedback. Whether wake words interrupt long animations or random-bar loops requires SDK/hardware validation; arbitrary mode interruption is not established by this archive.

<a id="graphics"></a>

## Matrix data and coordinate algorithms

### Binary patterns and RGB planes

Each `uint16_t` row stores sixteen pixels. A set bit draws the chosen color. For row mask M_y, code tests `pattern[y] & (1 << (15-x))`:

```math
b(x,y)=\left(M_y\gg(15-x)\right)\mathbin{\&}1,\qquad 0\le x,y<16
```

Here monochrome means that lit pixels share one RGB color within a frame, not that the hardware is limited to black/white. Multiple arrays provide crying/mouth frames. The four-color expression cycle traverses four patterns three times, with `delay(1000)` per frame.

The static character uses separate red, green, and blue 16×16 arrays. Storage is:

```math
S_{\mathrm{binary}}=16\times2=32\ \mathrm{bytes},\qquad S_{\mathrm{RGB}}=3\times16\times16=768\ \mathrm{bytes}
```

![RGB character artwork](images/demo_pixel_desktop_pet.png)

This is static pixel artwork, not a physical photograph or proof of an animated desktop pet.

### Mapping four 8×8 panels

`贪吃蛇.hd:getPixelIndex` uses zero-based coordinates. Panel q follows top-left, top-right, bottom-left, bottom-right; each block is row-indexed. This describes the code's assumption, not a verified wiring pattern for every physical panel.

```math
q=2\left\lfloor\frac{y}{8}\right\rfloor+\left\lfloor\frac{x}{8}\right\rfloor,\qquad
i=64q+8(y\bmod8)+(x\bmod8)
```

For (8,0), block mapping gives 64 while the earlier linear `displayPattern` gives 8. Revised RGB drawing shares the game's zero-based block formula, but monochrome drawing keeps its linear mapping. Check wiring for the selected program.

### Driver and theoretical wire time

Applications call SDK initialization, color setters, and `pixel_show()`. Low-level waveform code and oscilloscope records are not included. Assuming 800 kbit/s and 24 bits per LED, the ideal data-only time for 256 LEDs is:

```math
T_{\mathrm{wire}}=\frac{256\times24}{800000}=7.68\ \mathrm{ms},\qquad
T_{\mathrm{frame}}\ge T_{\mathrm{wire}}+T_{\mathrm{reset}}
```

Reset intervals, processing, library behavior, and scheduling add overhead. Theoretical bandwidth is not measured refresh rate, animation frame rate, or team-developed nanosecond waveform control. Pulse/reset requirements must match the actual WS2812B variant and documentation revision.

<a id="music"></a>

## Music clips with random bars

The participant describes replacing a fixed reply audio asset with a song excerpt; those audio resources are not distributed. `功能三.hd` uses `rand()%17` for heights and `rand()%256` for RGB values, with a 200 ms task delay in the display loop.

There is no audio sampling, FFT, loudness envelope, or beat extraction. The feature is accurately described as music playback accompanied by random lighting or simulated music visualization. A preset excerpt is not streaming playback. A stop-command branch exists, but accepting new events during the long handler loop remains to be verified.

<a id="game"></a>

## Snake and serial tasks

| Mechanism | Implementation and purpose |
| :--- | :--- |
| Initialization | `resetGame()` creates three segments, starts moving right, generates food, and resets the score. |
| Reception | `UART_RX` reads available characters at 115200 bps, with a 2 ms outer-loop delay. |
| Updates | `app` calls `moveSnake()` when started, then delays 300 ms; this is not a strictly fixed 300 ms period. |
| Direction guard | At each game tick, apply the latest request unless it reverses the last committed direction. |
| Boundary wrapping | Coordinates outside 0–15 wrap to the opposite edge, equivalent to the equation below. |
| Food placement | Enumerate unoccupied cells and select one; return completion if none remain. |
| Motion/growth | Segments follow the head; eating appends the old tail position and increments score. |
| End feedback | Self-collision stops play, flashes red three times at 300 ms on/off, then prints the score to serial. |

```math
x'=(x+\Delta x+16)\bmod16,\qquad y'=(y+\Delta y+16)\bmod16
```

Both tasks retain priority 4 and stack-depth arguments of 256, with units defined by the SDK. UART publishes atomic single-slot requests rather than writing dx/dy or resetting the snake. Later direction input can overwrite earlier input. The 300 ms update delay and 2 ms receive polling are not measured response latency.

`E` starts/restarts only while the game is stopped and does not reset active play. Archived `showScore()` uses `Serial.print/println`, with no numeric bitmap drawing. Voice start, LED scoring, and unified mode switching need the matching demonstration code.

<a id="implementation-status"></a>

## Implementation scope, outstanding issues, and validation

| Item | Current evidence | Documentation/reproduction treatment |
| :--- | :--- | :--- |
| Final demonstration firmware | Feature development versions are preserved; a complete combined version is unconfirmed. | Describe files individually; do not promise one project covers every demonstration. |
| Animation delays | `uint16_t frameDelay[]` retains declared 300/500 values. | Correct types do not establish measured frame timing. |
| RGB indices | Arrays use 0–15, preserving panel order. | Physical orientation remains to be checked. |
| Mapping differences | Monochrome linear and RGB/game block mappings coexist. | Verify coordinates per program rather than presenting them as one implementation. |
| Game boundaries | Bounded food selection, full-capacity exit, atomic input slots and game-task-owned state. | Offline boundary tests pass; vendor SDK/task scheduling are untested. |
| Music/mode exit | Long loops and blocking delays exist. | Chip AEC support alone does not prove interruption in every mode. |
| Performance | Course demonstration and subjective feedback, without reproducible controlled test records. | Do not claim 98% recognition, fixed latency, 10 m range, measured refresh, or current figures. |
| Power/brightness | USB power is participant-confirmed; programs contain values such as 5, 50, or graphical configuration 255. | These are not one adjustable-brightness feature and do not establish current, voltage drop, or supply headroom. |

Seven offline cases execute functions extracted from the real .hd source with Clang/WebAssembly: unique pixel mapping, RGB bounds, one/free-no-cell cases, growth to capacity and rapid turns; source delay declarations are also compiled. The complete Tianwen SDK was not built or flashed and hardware was not retested. The target compiler must support GCC/Clang `__atomic` builtins; vendor SDK and task stack behavior remain unverified.

<a id="references"></a>

## Engineering sources and media captions

- Primary evidence is application code, participant accounts of USB power/wooden enclosure/fixed music audio, and physical images; course reports/slides are secondary.
- The [official ASRPRO board specification](https://www.haohaodada.com/jpeguploadfile/twen/ASRPRO/ASRPROV1.1.pdf) describes a 32-bit CPU, neural processor, and audio interfaces. These are platform capabilities, not team-developed speech algorithms. [Official Tianwen resources](https://www.twen51.com/)
- Enclosure, rainbow, and expression photographs show the physical prototype. Static artwork describes a design, not system performance.
- Media names describe their actual content: physical matrix photographs, a WS2812 panel product reference, and a Tianwen resource-layout reference. App, ASRPRO-board, and rear-wiring photographs remain to be supplied.

The following are manufacturer/component connection references, not evidence that the team designed the chip circuitry or that every illustrated capability is implemented in the prototype.

| ASRPRO core-board reference circuit | WS2812B single-pixel connection reference |
| :---: | :---: |
| ![ASRPRO reference circuit](images/hardware_asrpro_schematic.png) | ![WS2812B connection reference](images/hardware_ws2812_cascade_schematic.png) |

[Project overview](../README_EN.md) · [Setup and operation](setup.en.md)
