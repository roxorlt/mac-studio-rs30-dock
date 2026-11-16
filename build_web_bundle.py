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
StudioBeam DuoDock V3.1 (全面工程自检版：双层阶梯滑轨 + Ø176快装凸台) — M5 Mac Studio × 极米 RS30 交付说明
========================================================================

一、V3.1 全面实装自检升级亮点（解决五大真实物理使用细节）
------------------------------------------------------------------------
1. 【200.6 mm 植绒专用滑轨门 + 前下双指抠手位】：
   裸舱门净宽放宽至 200.6 mm；在左右立柱内侧与滑轨面贴上 1.0 mm 厚自粘防刮植绒胶条后，净余 198.6 mm
   （单边各留 0.8 mm 丝滑运行游隙，绝不因贴绒而卡紧 197.0 mm 的 Mac Studio！）。无需搬动上方 5.4 kg 极米 RS30，
   伸入前下 32×20 mm 悬空区即可轻松平拉抽出或平推入舱，推到底自动贴合后立柱 R32.2 圆角靠山居中定位。
2. 【Z=6 mm / Z=26 mm 双层物理阶梯导轨（防滤网掉桌底卡死）】：
   Z=0..6 mm 为 174 mm 内孔底座环，在 Z=6 mm 处向外阶梯扩至 183 mm 形成 3.5 mm 宽实体托架承托 4 号防尘网框
   （181×181×3.2 mm），彻底避免旧版滤网受重力掉到桌面被前横梁挡死；Z=26 mm 再向外扩至 200.6 mm 形成 Mac 滑轨。
3. 【Ø176 mm 抬升快装凸台（消除凹杯刮擦 U 型云台臂）】：
   2 号顶盘取消外圈凸起凹杯，改为中心 Ø176 mm × 17.0 mm 实心抬升快装台，外围一圈向下阶梯避让 -3.0 mm（厚 14 mm），
   兼容任意底盘直径且为极米 RS30 298 mm U 型摆臂 360° 旋转留出充裕净空。
4. 【Ø43→Ø26 mm 平底手拧沉孔（标准 14 mm D环螺丝锁紧不顶桌面）】：
   2 号顶盘底部设 Ø43 mm 双指拧转斜口 + Z=8.5 mm 平底沉台（夹持实厚 8.5 mm），标准相机 1/4"-20 × 14 mm D环手拧螺丝
   拧紧后有效旋入 RS30 底孔 5.5 mm（符合三脚架标准），螺头平整受力不劈裂层纹，折叠后完全藏于沉孔内（方案C放桌面不晃动）。
5. 【50 mm 宽槽电源舱 + 天花板垂直投射接线提示】：
   3 号侧挂电源舱内宽扩至 50 mm 兼容各批次 240W–330W 适配器；若需 RS30 镜头 +90° 垂直朝上投天花板，建议搭配 L 型 90°
   弯头或超短头细线径 HDMI 2.1 线，避免长尾硬直插头在 +90° 极限仰角下触碰顶板。
   * 搬动提醒：1号底座与2号顶盘采用 8.5 mm 重力止口榫卯定位，整体搬移桌面位置时请托住 1 号底座搬运，勿单提投影仪云台。

二、包含的 V3.1 模型文件（单位 mm，全部通过 2-Manifold 水密闭合检测，适配 256×256 mm 拓竹热床）
------------------------------------------------------------------------
1. 01_mac_studio_base_cradle.stl   (216.6 × 216.6 × 139.5 mm | 约 267g PETG)
   - 双层阶梯滑轨底座（Z=6mm 滤网导轨 + Z=26mm Mac 植绒滑轨 + 154.6mm 全敞开背窗）
   - 摆放：底面(Z=0)朝下平铺热床，100% 零支撑直打！

2. 02_rs30_gimbal_upper_deck.stl   (216.6 × 216.6 × 17.0 mm  | 约 358g PETG)
   - Ø176mm 快装凸台承重顶盘（中心实厚 17mm 承载 5.4kg 变形 <0.05mm + 四角 45° 自支撑榫槽 + 中心 Ø26mm 平底沉孔）
   - 摆放：底面(Z=0)朝下平铺热床，仅开启「仅在打印板上生成支撑」托住中心 Ø26mm 平底圆沉孔（仅耗材 ~1g，一抠即掉）！

3. 03_power_brick_cable_pod.stl    (62.0 × 204.0 × 102.0 mm  | 约 110g PETG)
   - 50mm 宽槽侧挂电源散热舱（贴靠 Mac 空白左/右侧壁，低于上方 RS30 底面 45mm 零干涉）
   - 摆放：底面(Z=0)朝下平铺热床，零支撑直打！

4. 04_bottom_dust_filter_frame.stl (181.0 × 181.0 × 3.2 mm   | 约 36g PETG)
   - 前抽式防尘滤网框（架在 1 号底座 Z=6mm 实体滑轨台阶上，随时从正面平拉抽出水洗除尘）
   - 摆放：底面(Z=0)朝下平铺热床，零支撑直打！

三、直接发给淘宝/闲鱼「拓竹农场代打」或「嘉立创3D打印」的工艺嘱咐
------------------------------------------------------------------------
- 强烈推荐材料：PETG-CF（碳纤增强，刚度提升 65%、耐热 ~85°C、消光深空灰质感）或 PETG 哑光（耐热 ~75°C）
  * 严禁使用普通 PLA（耐温仅 52-55°C 且在 5.4kg 长期静载下易蠕变下凹）
- 层高：0.20 mm | 壁厚：4 层外壁（≥ 1.6 mm），顶/底实心层各 5 层 | 填充：30% 陀螺仪填充（Gyroid）
- 支撑设置：全部 Z=0 底面朝下平铺；仅 02 顶盘勾选「仅在打印板上生成支撑 (Support on build plate only)」，其余零支撑！

四、配套五金与防刮贴条清单（淘宝合计约 ¥15-25）
------------------------------------------------------------------------
1. 标准相机快装板 1/4"-20 × 14mm（总长14mm，螺纹/光杆约10-11mm）D环手拧螺丝 × 1 颗
2. 0.8~1.0mm 厚自粘黑色植绒布胶条 1 卷（贴在 1 号底座 Z=26mm 左右水平滑轨顶面与立柱内侧，推拉丝滑零划痕）
3. 1.5~2.0mm 厚硅胶防滑垫贴（贴在 1 号底座四角底面 + 2 号顶盘 Ø176mm 凸台顶面防滑减振）
4. Ø170mm PC 机箱尼龙防尘网片 × 1 片（嵌入 4 号抽拉滤网框）
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
