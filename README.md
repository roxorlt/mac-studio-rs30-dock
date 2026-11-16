# StudioBeam DuoDock V3.1 — Apple M5 Mac Studio × 极米 RS30 双层前推滑轨 + Ø176 快装凸台一体支架坞

> **🌐 在线 3D 交互预览与前向滑轨演示工作台（V3.1 已修复视角居中、顺手旋转与平移限位）：**
> ### 👉 [https://roxorlt.github.io/mac-studio-rs30-dock/](https://roxorlt.github.io/mac-studio-rs30-dock/)
>
> **📦 直接下载全套 V3.1 水密可打印文件包（含 4 个 `.stl` + 离线 3D 网页 + 代打与组装说明）：**
> - **[点击直接下载 `StudioBeam_DuoDock_V3_STL_Package.zip`](https://roxorlt.github.io/mac-studio-rs30-dock/StudioBeam_DuoDock_V3_STL_Package.zip)**
> - **[右键另存下载单文件离线 3D 预览器 `StudioBeam_DuoDock_Offline.html`](https://roxorlt.github.io/mac-studio-rs30-dock/StudioBeam_DuoDock_Offline.html)**

---

## 1. V3.1 全面工程自检升级清单（解决全部真实物理安装与日常使用隐患）

| 核查维度 | 硬件实测参数 | V3.1 结构与防呆设计方案 |
| :--- | :--- | :--- |
| **1. 贴植绒条后前门顺滑入舱 + 抠手位** | M5 Mac Studio 机身 **`197 × 197 × 95 mm`**（`R30.4` 圆角） | 裸舱门放宽至 **`200.6 mm`**；贴完左右各 `1.0 mm` 防刮植绒布后净留 **`198.6 mm`**（单边 `0.8 mm` 顺滑游隙，绝不因贴绒而卡死）；前下 `32 × 20 mm` 悬空区可直接伸入双指平拉抽出，推到底贴合后立柱 `R32.2` 圆角靠山自动居中。 |
| **2. 双层物理阶梯导轨（防滤网掉桌底）** | 底部进风圆脚 **`Ø179.2 × 8 mm`**；防尘滤网框 **`181 × 181 × 3.2 mm`** | `Z = 0..6 mm` 为 `174 mm` 底座内孔，在 **`Z = 6.0 mm`** 向外阶梯扩至 `183 mm` 形成 **`3.5 mm` 宽实体滤网托轨**（彻底解决滤网受重力掉到桌面被前梁挡死的问题）；**`Z = 26.0 mm`** 再扩至 `200.6 mm` 形成 Mac 水平滑轨，全程向上阶梯零支撑。 |
| **3. Ø176mm 快装凸台（防刮擦 U 型云台臂）** | 极米 RS30 实重 **`5.3 – 5.4 kg`**，U 型灵动云台总宽 `298 mm`（回转圆 **`Ø333 mm`**） | 取消易刮擦 U 型摆臂的外圈凹杯沿，改为中心 **`Ø176.0 × 17.0 mm` 实心抬升快装台**，外围一圈向下阶梯避让 **`-3.0 mm`**（厚 `14 mm`），兼容任意转盘直径且 `360°` 旋转零刮擦；方案 C 双坞轴距扩至 **`296.0 mm`**（净留 `+21.2 mm`）。 |
| **4. Ø43→Ø26mm 平底手拧沉孔** | 标准相机快装板 `1/4"-20 × 14 mm` D环手拧螺丝 | 顶盘底面设 `Ø43 mm` 双指拧转斜口 + **`Z = 8.5 mm` 处 `Ø26 mm` 平底沉台**（夹持实厚 `8.5 mm`）：螺丝有效旋入 RS30 约 `5.5 mm`，平底受力不劈裂层纹，D环折叠后内藏于沉孔内（方案 C 放桌面绝对平整不晃动）。 |
| **5. 154.6mm 全敞背窗 + 50mm 宽电源舱** | 背部平直接口区宽 `136.2 mm` + 边角开机键；外置电源砖 `240W–330W` | 背窗净宽 **`154.6 mm`** 零遮挡接口与电源键；侧挂电源舱内槽扩至 **`50.0 mm`**；若需 RS30 **`+90°` 垂直投天花板**，建议配 **L 型 `90°` 弯头或超短头细线径 HDMI 2.1 线**；整体搬移桌面时请托住 1 号底座搬运。 |

---

## 2. 仓库文件清单（全部通过 2-Manifold 水密闭合检测，适配 `256 × 256 mm` 拓竹热床）

- [`index.html`](./index.html) / [`StudioBeam_DuoDock_Offline.html`](./StudioBeam_DuoDock_Offline.html)：V3.1 零外部依赖 WebGL 3D 交互工作台（含 `⟳ 居中归位`、双击复位、防丢限位平移与正面滑轨动画）
- [`stl/01_mac_studio_base_cradle.stl`](./stl/01_mac_studio_base_cradle.stl)：M1 V3.1 双层阶梯滑轨底座（`216.6 × 216.6 × 139.5 mm`，约 `267 g`，零支撑直打）
- [`stl/02_rs30_gimbal_upper_deck.stl`](./stl/02_rs30_gimbal_upper_deck.stl)：M2 V3.1 `Ø176mm` 快装凸台顶盘（`216.6 × 216.6 × 17.0 mm`，约 `358 g`，仅中心圆沉孔开启打印板支撑 `~1g`）
- [`stl/03_power_brick_cable_pod.stl`](./stl/03_power_brick_cable_pod.stl)：M3 `50mm` 宽槽侧挂电源散热舱（`62.0 × 204.0 × 102.0 mm`，约 `110 g`，零支撑直打）
- [`stl/04_bottom_dust_filter_frame.stl`](./stl/04_bottom_dust_filter_frame.stl)：M4 `181mm` 前抽式防尘滤网框（`181.0 × 181.0 × 3.2 mm`，约 `36 g`，零支撑直打）
- [`generate_cad.py`](./generate_cad.py) / [`mac_rs30_duodock.scad`](./mac_rs30_duodock.scad) / [`cad_manifest.json`](./cad_manifest.json)：参数化 Python & OpenSCAD V3.1 源码与水密核验清单

---

## 3. 代打材料与切片建议

- **最推荐材料**：**`PETG-CF`（碳纤增强，弯曲刚度提升 `+65%`、耐温 `~85°C`、消光深空灰磨砂质感）** 或 **`PETG` 哑光工程料**（耐温 `~75°C`）。*请勿使用普通 PLA（耐温仅 55°C 且长期静载易蠕变下凹）。*
- **切片嘱咐**：`0.20mm 层高`、`4 层外壁 (≥1.6mm)`、`顶底各 5 层`、`30% 陀螺仪 (Gyroid) 填充`；全部 `Z=0` 底面朝下平铺，仅 `02` 顶盘勾选「仅在打印板上生成支撑」（托住中心 `Ø26mm` 平底沉孔，耗材仅 `~1g`），其余全部零支撑直打。
