#!/usr/bin/env python3
"""
Builds the V3 self-contained offline HTML 3D Studio + downloadable V3 STL ZIP package + README
in /home/antigravity/mac-rs30-dock/web/ for Preview Pane, GitHub Pages, and local offline viewing.
"""

from __future__ import annotations

import pathlib
import re
import shutil
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent
STL_DIR = ROOT / "stl"
WEB_DIR = ROOT / "web"
ARTIFACT_STUDIO = pathlib.Path(
    "/home/antigravity/.gemini/jetski/brain/v1/default/jetski_remote_agents_3p/"
    "c73c746c-cc16-4946-84df-2e9c7bd2bf5f/mac_rs30_duodock_studio.html"
)

ORDER_README = """========================================================================
StudioBeam DuoDock V3.2 (全真线缆仿真 + 208mm极米电源舱 + 4×M4防掀刚性锁紧版) — M5 Mac Studio × 极米 RS30 交付说明
========================================================================

一、V3.2 五大核心工程升级与实装原理
------------------------------------------------------------------------
1. 【专属极米 RS30 300W 巨型外置电源舱（208×48×94 mm 净腔 + 双端 31mm 通顶 U 型出线槽）】：
   - M5 Mac Studio 采用内置 370W–480W 电源（仅一根直插机身的编织品字 AC 线，无外置电源砖）。
   - 3 号侧挂舱 100% 专为极米 RS30 的巨型外置 DC 适配器（最高达 200×90×40 mm、重 ~1.1 kg）设计！
   - V3.2 将内腔升级至 208×48×94 mm（外壁 220×60×102 mm，仍完美装入 256mm 拓竹热床），并在前后两端开设 31mm 宽直通顶部的 U 型卡槽：先把 C13 交流电源线与圆口 DC 线插好，连砖带防折弯护套直接从上方垂直落入舱内，四角环形护翼稳固抱紧、侧面双风窗对流散热！
2. 【1/4"-20 中心快装螺孔 + 四角 4×M4 防掀起刚性锁紧】：
   - 投影底座锁紧：极米 RS30 的 Ø196mm 底座底面中心自带金属 1/4"-20 三脚架螺母。将 RS30 放在 2 号顶盘 Ø176mm 硅胶垫快装凸台上，从顶盘底面 Ø43→Ø26mm 平底沉孔拧入 1 颗标准相机 1/4"-20 × 14mm D环手拧螺丝（有效咬合 5.5mm），其内置旋转轴承依然可顺畅 360° 水平旋转！
   - 顶盘与底座刚性锁死：2 号顶盘外露四角（R=122.3~126.4mm，完全避开 RS30 的 R=98mm 底盘圆）新增 4 处 M4 内六角沉头通孔，对准 1 号底座立柱顶部的 4 个 24mm 深盲孔（可热熔压入 M4×6×6 滚花铜螺母，或直接拧入 Ø3.8mm PETG-CF 自攻孔），用 4 颗 M4×25mm 螺丝将 M1+M2+RS30 锁成一体刚性框架，仰俯调角度或搬动时顶盘绝不掀起，而正面 Mac Studio 依然随时免拆平抽！
3. 【全真接口坐标避让 + 4 路线缆无干涉走线】：
   - 极米 RS30 接口位于「随云台俯仰摆动的机身背下沿凹槽」（DC IN、HDMI 1 eARC、HDMI 2、2×USB），+90° 投天花板时下摆离顶盘仍有 +47mm 净空。
   - M5 Mac Studio 背板（4×TB5、万兆 RJ45、AC 电源、2×USB-A、HDMI 2.1、电源键）全部裸露于 154.6mm 后大窗中央，零遮挡。
4. 【物理重心防倾覆验算（极限 +95° 仰角稳如磐石）】：
   - 底部 Mac Studio（2.74~3.64kg，重心高 69.5mm）充当天然压舱石；极米 U 型云台转轴紧贴镜头机身质心（偏心 ≤24mm）。
   - 即使在 +95° 极限投射天花板或 -12° 下俯时，整塔 8.72kg 总重心水平偏移仅 Δr ≈ 10.5~14.8mm，距离 216.6mm 底座倾覆边缘（±108.3mm）仍有 >93mm（86%）安全裕度！静态倾覆极限角达 25.3°，抗倾覆重力恢复力矩 8.0 N·m（约为手动调节云台阻尼力矩的 4 倍）。

二、包含的 V3.2 模型文件（单位 mm，全部通过 2-Manifold 水密闭合检测，适配 256×256 mm 拓竹热床）
------------------------------------------------------------------------
1. 01_mac_studio_base_cradle.stl   (216.6 × 216.6 × 139.5 mm | 约 269g PETG)
   - 双层阶梯滑轨底座（Z=6mm 滤网轨 + Z=26mm Mac 植绒滑轨 + 四角 M4 防掀锁紧盲孔）
   - 摆放：底面(Z=0)朝下平铺热床，100% 零支撑直打！

2. 02_rs30_gimbal_upper_deck.stl   (216.6 × 216.6 × 17.0 mm  | 约 357g PETG)
   - Ø176mm 快装凸台承重顶盘（中心 1/4" D环手拧沉孔 + 四角 45° 自支撑榫槽 + 外露四角 4×M4 沉头锁紧孔）
   - 摆放：底面(Z=0)朝下平铺热床，仅开启「仅在打印板上生成支撑」托住中心 Ø26mm 沉孔与四角 M4 小沉台（仅耗材 ~1.5g，一抠即掉）！

3. 03_power_brick_cable_pod.stl    (60.0 × 220.0 × 102.0 mm  | 约 129g PETG)
   - 208×48×94mm 极米 300W 电源散热舱（前后双端 31mm 通顶 U 槽 + 四角环抱护翼 + 双侧散热窗）
   - 摆放：底面(Z=0)朝下平铺热床，100% 零支撑直打！

4. 04_bottom_dust_filter_frame.stl (181.0 × 181.0 × 3.2 mm   | 约 36g PETG)
   - 前抽式防尘滤网框（架在 1 号底座 Z=6mm 实体滑轨台阶上，随时从正面平拉抽出水洗除尘）
   - 摆放：底面(Z=0)朝下平铺热床，100% 零支撑直打！

三、直接发给淘宝/闲鱼「拓竹农场代打」或「嘉立创3D打印」的工艺嘱咐
------------------------------------------------------------------------
- 强烈推荐材料：PETG-CF（碳纤增强，刚度提升 65%、耐热 ~85°C、消光深空灰质感）或 PETG 哑光（耐热 ~75°C）
  * 严禁使用普通 PLA（耐温仅 52-55°C 且在 5.4kg 长期静载下易蠕变下凹）
- 层高：0.20 mm | 壁厚：4 层外壁（≥ 1.6 mm），顶/底实心层各 5 层 | 填充：30% 陀螺仪填充（Gyroid）
- 支撑设置：全部 Z=0 底面朝下平铺；仅 02 顶盘勾选「仅在打印板上生成支撑 (Support on build plate only)」，其余零支撑！

四、配套五金与防刮贴条清单（淘宝合计约 ¥20-30）
------------------------------------------------------------------------
1. 相机快装板 1/4"-20 × 14mm（总长14mm，螺纹+光杆约10-11mm）不锈钢 D环手拧螺丝 × 1 颗（将极米 RS30 锁在 2 号顶盘中心）
2. M4 × 25mm 杯头内六角螺丝 × 4 颗 +（可选）M4×6×6mm 热熔滚花铜螺母 × 4 颗（将 2 号顶盘四角锁死在 1 号底座立柱上；若不烫铜螺母，M4 螺丝也可直接自攻旋入 Ø3.8mm 碳纤 PETG 盲孔）
3. 0.8~1.0mm 厚自粘黑色植绒布胶条 1 卷（贴在 1 号底座 Z=26mm 左右滑轨面与立柱内侧，Mac 推拉零划痕）
4. 1.5~2.0mm 厚硅胶防滑垫贴（必贴于 1 号底座四角底面防桌面打滑 + 贴于 2 号顶盘 Ø176mm 凸台顶面防滑减振）
5. Ø170mm PC 机箱尼龙防尘网片 × 1 片（嵌入 4 号抽拉滤网框）
"""

OFFLINE_CSS_SHIM = """
  <style>
    :root {
      --background: #0b0f19;
      --card: #131a2a;
      --secondary: #1e293b;
      --border: #2a3950;
      --card-border: #2a3950;
      --foreground: #f1f5f9;
      --muted-foreground: #94a3b8;
      --primary: #3b82f6;
      --primary-foreground: #ffffff;
      --success: #10b981;
    }
    html.light {
      --background: #f8fafc;
      --card: #ffffff;
      --secondary: #f1f5f9;
      --border: #cbd5e1;
      --card-border: #cbd5e1;
      --foreground: #0f172a;
      --muted-foreground: #475569;
      --primary: #2563eb;
      --primary-foreground: #ffffff;
      --success: #059669;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
      background: var(--background);
      color: var(--foreground);
      font-size: 13px;
      line-height: 1.5;
    }
    .canvas-stage { min-height: 460px; }
    .max-w-\\[1440px\\] { max-width: 1440px; }
    .max-w-\\[300px\\] { max-width: 300px; }
    .mx-auto { margin-left: auto; margin-right: auto; }
    .mb-1 { margin-bottom: 0.25rem; } .mr-1 { margin-right: 0.25rem; } .mt-0\\.5 { margin-top: 0.125rem; }
    .p-2 { padding: 0.5rem; } .p-2\\.5 { padding: 0.625rem; } .p-3 { padding: 0.75rem; } .p-3\\.5 { padding: 0.875rem; } .p-4 { padding: 1rem; }
    .pl-4 { padding-left: 1rem; }
    .px-2 { padding-left: 0.5rem; padding-right: 0.5rem; }
    .px-2\\.5 { padding-left: 0.625rem; padding-right: 0.625rem; }
    .px-3 { padding-left: 0.75rem; padding-right: 0.75rem; }
    .px-4 { padding-left: 1rem; padding-right: 1rem; }
    .py-1 { padding-top: 0.25rem; padding-bottom: 0.25rem; }
    .py-1\\.5 { padding-top: 0.375rem; padding-bottom: 0.375rem; }
    .py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
    .py-2\\.5 { padding-top: 0.625rem; padding-bottom: 0.625rem; }
    .py-3 { padding-top: 0.75rem; padding-bottom: 0.75rem; }
    .pt-1 { padding-top: 0.25rem; } .pt-2 { padding-top: 0.5rem; }
    .space-y-0\\.5 > * + * { margin-top: 0.125rem; }
    .space-y-1 > * + * { margin-top: 0.25rem; }
    .space-y-1\\.5 > * + * { margin-top: 0.375rem; }
    .space-y-2 > * + * { margin-top: 0.5rem; }
    .space-y-2\\.5 > * + * { margin-top: 0.625rem; }
    .space-y-3 > * + * { margin-top: 0.75rem; }
    .space-y-3\\.5 > * + * { margin-top: 0.875rem; }
    .flex { display: flex; } .inline-block { display: inline-block; } .block { display: block; } .hidden { display: none !important; }
    .flex-col { flex-direction: column; } .flex-wrap { flex-wrap: wrap; }
    .items-center { align-items: center; } .items-start { align-items: flex-start; } .items-baseline { align-items: baseline; }
    .justify-between { justify-content: space-between; } .justify-center { justify-content: center; }
    .gap-1 { gap: 0.25rem; } .gap-1\\.5 { gap: 0.375rem; } .gap-2 { gap: 0.5rem; } .gap-3 { gap: 0.75rem; }
    .gap-x-3 { column-gap: 0.75rem; } .gap-y-1 { row-gap: 0.25rem; }
    .grid { display: grid; }
    .grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
    .grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .list-disc { list-style-type: disc; }
    @media (min-width: 640px) { .sm\\:block { display: block !important; } }
    @media (min-width: 768px) {
      .md\\:p-4 { padding: 1rem; }
      .md\\:h-\\[540px\\] { height: 540px !important; }
      .md\\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
      .md\\:text-base { font-size: 1rem; }
    }
    @media (min-width: 1024px) {
      .lg\\:grid-cols-12 { grid-template-columns: repeat(12, minmax(0, 1fr)); }
      .lg\\:col-span-8 { grid-column: span 8 / span 8; }
      .lg\\:col-span-4 { grid-column: span 4 / span 4; }
    }
    .w-full { width: 100%; } .h-full { height: 100%; } .w-9 { width: 2.25rem; } .h-9 { height: 2.25rem; }
    .w-2\\.5 { width: 0.625rem; } .h-2\\.5 { height: 0.625rem; }
    .h-\\[460px\\] { height: 460px; }
    .max-h-\\[540px\\] { max-height: 540px; }
    .relative { position: relative; } .absolute { position: absolute; } .inset-0 { top: 0; right: 0; bottom: 0; left: 0; }
    .top-3 { top: 0.75rem; } .left-3 { left: 0.75rem; } .bottom-3 { bottom: 0.75rem; }
    .overflow-hidden { overflow: hidden; } .overflow-y-auto { overflow-y: auto; }
    .rounded { border-radius: 0.25rem; } .rounded-md { border-radius: 0.375rem; } .rounded-lg { border-radius: 0.5rem; } .rounded-xl { border-radius: 0.75rem; } .rounded-full { border-radius: 9999px; } .rounded-sm { border-radius: 0.125rem; }
    .border { border: 1px solid var(--border); }
    .border-b { border-bottom: 1px solid var(--border); }
    .border-t { border-top: 1px solid var(--border); }
    .border-b-2 { border-bottom-width: 2px; border-bottom-style: solid; }
    .border-transparent { border-color: transparent; }
    .border-\\[var\\(--primary\\)\\] { border-color: var(--primary) !important; }
    .bg-\\[var\\(--background\\)\\] { background-color: var(--background); }
    .bg-\\[var\\(--card\\)\\] { background-color: var(--card); }
    .bg-\\[var\\(--card\\)\\]\\/90 { background-color: rgba(19, 26, 42, 0.88); }
    html.light .bg-\\[var\\(--card\\)\\]\\/90 { background-color: rgba(255, 255, 255, 0.92); }
    .bg-\\[var\\(--secondary\\)\\] { background-color: var(--secondary); }
    .bg-\\[var\\(--primary\\)\\] { background-color: var(--primary); }
    .text-\\[var\\(--foreground\\)\\] { color: var(--foreground); }
    .text-\\[var\\(--muted-foreground\\)\\] { color: var(--muted-foreground); }
    .text-\\[var\\(--primary\\)\\] { color: var(--primary); }
    .text-\\[var\\(--primary-foreground\\)\\] { color: var(--primary-foreground); }
    .text-\\[var\\(--success\\)\\] { color: var(--success); }
    .text-xs { font-size: 0.75rem; } .text-sm { font-size: 0.875rem; } .text-lg { font-size: 1.125rem; }
    .font-medium { font-weight: 500; } .font-semibold { font-weight: 600; } .font-bold { font-weight: 700; }
    .font-mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; }
    .leading-relaxed { line-height: 1.6; } .leading-snug { line-height: 1.35; }
    .text-left { text-align: left; } .resize-none { resize: none; }
    .cursor-pointer { cursor: pointer; } .pointer-events-none { pointer-events: none; } .shrink-0 { flex-shrink: 0; }
    .hover\\:opacity-90:hover { opacity: 0.9; } .hover\\:bg-\\[var\\(--secondary\\)\\]:hover { background-color: var(--secondary); }
    .hover\\:bg-\\[var\\(--primary\\)\\]:hover { background-color: var(--primary); }
    .hover\\:text-\\[var\\(--primary-foreground\\)\\]:hover { color: var(--primary-foreground); }
    button, select, textarea { font: inherit; color: inherit; background: none; border: none; }
    select, textarea { border: 1px solid var(--border); background: var(--secondary); }
    input[type="range"] { width: 100%; accent-color: var(--primary); }
  </style>
"""


def main() -> None:
    WEB_DIR.mkdir(parents=True, exist_ok=True)
    web_stl_dir = WEB_DIR / "stl"
    web_stl_dir.mkdir(parents=True, exist_ok=True)
    for sf in STL_DIR.glob("*.stl"):
        shutil.copy2(sf, web_stl_dir / sf.name)

    readme_path = WEB_DIR / "00_V3代打工艺与滑轨组装说明.txt"
    readme_path.write_text(ORDER_README, encoding="utf-8")

    src_html = ARTIFACT_STUDIO.read_text(encoding="utf-8")
    offline_html = re.sub(
        r'<script\s+src="https://www\.gstatic\.com/[^"]+"></script>',
        OFFLINE_CSS_SHIM,
        src_html,
    )

    offline_html = offline_html.replace(
        '<button id="btnSaveOfflineHtml"',
        '<button type="button" onclick="document.documentElement.classList.toggle(\'light\')" '
        'class="px-2.5 py-1.5 rounded-md bg-[var(--secondary)] border border-[var(--border)] cursor-pointer">'
        '☀/🌙 主题</button>\n        <button id="btnSaveOfflineHtml"',
        1,
    )

    offline_file = WEB_DIR / "StudioBeam_DuoDock_Offline.html"
    index_file = WEB_DIR / "index.html"
    offline_file.write_text(offline_html, encoding="utf-8")
    index_file.write_text(offline_html, encoding="utf-8")

    zip_v3_path = WEB_DIR / "StudioBeam_DuoDock_V3_STL_Package.zip"
    with zipfile.ZipFile(zip_v3_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(readme_path, arcname="00_V3代打工艺与滑轨组装说明.txt")
        for stl_file in sorted(STL_DIR.glob("*.stl")):
            zf.write(stl_file, arcname=stl_file.name)
        zf.write(ROOT / "mac_rs30_duodock.scad", arcname="mac_rs30_duodock.scad")
        zf.write(ROOT / "generate_cad.py", arcname="generate_cad.py")
        zf.write(ROOT / "cad_manifest.json", arcname="cad_manifest.json")
        zf.write(offline_file, arcname="StudioBeam_DuoDock_V3_离线3D预览器.html")

    # Keep backwards-compatible copies so existing V2/generic links never 404
    shutil.copy2(zip_v3_path, WEB_DIR / "StudioBeam_DuoDock_V2_STL_Package.zip")
    shutil.copy2(zip_v3_path, WEB_DIR / "StudioBeam_DuoDock_STL_Package.zip")

    print(f"Built {index_file} ({index_file.stat().st_size // 1024} KB)")
    print(f"Built {zip_v3_path} ({zip_v3_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
