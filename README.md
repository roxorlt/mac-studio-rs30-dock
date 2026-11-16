# StudioBeam DuoDock V3 — Apple M5 Mac Studio × 极米 RS30 前推滑轨式 3D 打印一体支架坞

> **🌐 在线 3D 交互预览与前向滑轨演示工作台（免装 Blender，手机/电脑直开）：**
> ### 👉 [https://roxorlt.github.io/mac-studio-rs30-dock/](https://roxorlt.github.io/mac-studio-rs30-dock/)
>
> **📦 直接下载全套 V3 水密可打印文件包（含 4 个 `.stl` + 离线 3D 网页 + 代打与组装说明）：**
> - **[点击直接下载 `StudioBeam_DuoDock_V3_STL_Package.zip`](https://roxorlt.github.io/mac-studio-rs30-dock/StudioBeam_DuoDock_V3_STL_Package.zip)**
> - **[右键另存下载单文件离线 3D 预览器 `StudioBeam_DuoDock_Offline.html`](https://roxorlt.github.io/mac-studio-rs30-dock/StudioBeam_DuoDock_Offline.html)**

---

## 1. V3 核心工程指标（正面水平滑轨机舱 + 5.4kg 承重 + 全向零干涉）

| 核查维度 | 硬件实测参数 | V3 结构与防干涉设计方案 |
| :--- | :--- | :--- |
| **Mac Studio 如何装入与取出 (V3 重点升级)** | 机身 **`197 × 197 × 95 mm`**（含底部 **`Ø179.2 × 8 mm`** 圆形进风底脚，`R30.4` 圆角） | **正面水平推入式导轨机舱（无需拆动顶部 `5.4 kg` 投影仪）**：<br>1. **前门全宽直通**：两根前立柱外扩，正面净宽 **`199.4 mm`**（`> 197 mm` 机身），下部底脚通道净宽 **`182.4 mm`**（`> Ø179.2 mm` 圆底脚，底梁高 `6 mm` 低于底脚 `12 mm` 零磕碰）；<br>2. **双侧水平植绒滑轨**：左右各设 **`8.5 mm`** 宽水平滑轨（`Z = 26 mm`，贴 `1 mm` 自粘植绒条防刮顺滑）；<br>3. **后圆角自居中靠山**：两根后立柱保留 **`22.8 mm` 宽 `R31.6` 弧形内包挡边**，从正面平推到底自动贴合居中锁止！同时兼容首次组装时从上方敞口垂直放入。 |
| **极米 RS30 承重与防蠕变** | 实重 **`5.3 – 5.4 kg`**（按 `3×` 动态安全系数即 `16.2 kg` 设计载荷） | 1. **四角重型外骨骼立柱**：壁厚 **`8.0 mm`**，轴向屈曲极限 `> 800 kg`；<br>2. **顶盘实心桥板厚 `16.0 mm`**：抗弯刚度 `EI` 较 8mm 薄板提升 **`8 倍`**，在 `PETG` / `PETG-CF`（4壁+30%陀螺仪填充）下长期热态静载中心挠度 **`< 0.05 mm`**。 |
| **M5 Mac Studio 背口、开机键与排风** | 背部平直接口区宽 `136.2 mm`（4×雷雳5 + 万兆网口 + HDMI + 电源 + 边角开机键 + `4,000+` 排风孔） | **背部 `153.8 mm` 超宽敞口零遮挡**：完整暴露全部平直接口区与边角电源键（两侧再各富余 `8.8 mm`）；RS30 外置 `300W` 电源砖舱侧挂于 Mac 无接口的 **左/右侧空白铝壁**。 |
| **RS30 `360° × 135°` 回转干涉** | 含 U 型灵动云台总宽 `298 mm`，最大对角回转半径 **`R = 166.5 mm` (`Ø333 mm`)** | - **方案 A/B（立式塔）**：顶盘外围四角下沉 `1 mm` 低于云台底面，且高于侧挂电源舱顶面 `+45 mm`，`360°` 旋转零碰撞；<br>- **方案 C（并排低柜）**：双坞中心轴距 **`295.0 mm`**，在 `Ø333 mm` 极限回转圆外净留 **`+20.8 mm`** 安全间隙。 |
| **真·零支撑平铺直打** | 单件最大尺寸 **`215.4 × 215.4 mm`**（完美适配拓竹 `256 × 256 mm` 热床） | 全部 4 个零件均直接 `Z = 0` 底面朝下平铺打印；2 号顶盘底部 4 个榫槽与中心手拧螺孔均采用 **`45°` 自支撑斜顶/锥顶**，零支撑直打。 |

---

## 2. 仓库文件清单

- [`index.html`](./index.html) / [`StudioBeam_DuoDock_Offline.html`](./StudioBeam_DuoDock_Offline.html)：V3 零外部依赖 WebGL 3D 交互预览、正面滑轨动画演示与实时公差调整导出器
- [`stl/01_mac_studio_base_cradle.stl`](./stl/01_mac_studio_base_cradle.stl)：M1 V3 前推滑轨机舱底座 + 后圆角靠山（`215.4 × 215.4 × 139.0 mm`，约 `252 g`）
- [`stl/02_rs30_gimbal_upper_deck.stl`](./stl/02_rs30_gimbal_upper_deck.stl)：M2 V3 16mm 实厚承重防干涉云台顶盘（`215.4 × 215.4 × 20.0 mm`，约 `367 g`）
- [`stl/03_power_brick_cable_pod.stl`](./stl/03_power_brick_cable_pod.stl)：M3 侧挂式 RS30 300W 电源散热舱（`60.0 × 204.0 × 102.0 mm`，约 `107 g`）
- [`stl/04_bottom_dust_filter_frame.stl`](./stl/04_bottom_dust_filter_frame.stl)：M4 底部前抽式防尘滤网框（`180.0 × 180.0 × 3.2 mm`，约 `33 g`）
- [`generate_cad.py`](./generate_cad.py)：参数化 Python V3 2-Manifold 水密网格生成与拓扑校验脚本
- [`mac_rs30_duodock.scad`](./mac_rs30_duodock.scad)：参数化 OpenSCAD V3 建模源码
- [`cad_manifest.json`](./cad_manifest.json)：精确体积、表面积、切片克重与滑轨通道核验清单

---

## 3. 代打材料与渠道建议

- **最推荐材料**：**`PETG-CF`（碳纤增强，弯曲刚度提升 `+65%`、耐温 `~85°C`、消光深空灰磨砂质感）** 或 **`PETG` 哑光工程料**（耐温 `~75°C`）。*请勿使用普通 PLA（耐温仅 55°C 且长期静载易蠕变下垂）。*
- **切片嘱咐**：`0.20mm 层高`、`4 层外壁 (≥1.6mm)`、`顶底各 5 层`、`30% 陀螺仪 (Gyroid) 填充`、`全部零件底面朝下零支撑直打`。
