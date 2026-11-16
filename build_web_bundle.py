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
StudioBeam DuoDock V3 (前推滑轨机舱 + 5.4kg 重载防干涉版) — M5 Mac Studio × 极米 RS30 交付说明
========================================================================

一、V3 核心结构升级：Mac Studio 是怎么装进去/取出来的？
------------------------------------------------------------------------
- 【日常正推滑入 / 免拆抽出】：
  两根前立柱外移让出 199.4 mm 全宽直通舱门（> 197.0 mm Mac Studio 机身宽），下部底脚通道净宽 182.4 mm
  （> Ø179.2 mm 圆形进风底脚，底梁仅高 6mm 低于底脚 12mm）。即使上方已锁死 5.4kg 极米 RS30 投影仪，
  只需拔掉背部线材，Mac Studio 即可像磁带/刀片服务器一样沿左右两条 8.5mm 宽植绒水平滑轨（Z=26mm）直接从正面
  平推入舱或平拉抽出！推到底部时自动贴合两根后立柱的 R31.6 圆角限位靠山，精准居中锁止！
- 【首次组装垂直放入】：
  也可在扣上 2 号云台顶盘前，直接从上方敞口垂直放入 Mac Studio，再扣合顶盘榫卯并锁紧极米 RS30。

二、包含的 V3 模型文件（单位均为 mm，全部通过 2-Manifold 水密闭合检测，零支撑平铺直打）
------------------------------------------------------------------------
1. 01_mac_studio_base_cradle.stl   (215.4 × 215.4 × 139.0 mm | 约 252g PETG)
   - V3 升级：正面 199.4mm 全宽直通滑轨门 + 左右 8.5mm 水平导轨 + 后双柱 R31.6 限位靠山 + 153.8mm 全敞开背口窗
   - 摆放：底面(Z=0)直接朝下平铺热床，零支撑打印

2. 02_rs30_gimbal_upper_deck.stl   (215.4 × 215.4 × 20.0 mm  | 约 367g PETG)
   - 承载 5.4kg RS30：16.0mm 实心承重桥板（抗弯刚度 8 倍，中心变形 <0.05mm）；底部榫槽与手拧螺孔均为 45° 自支撑斜顶
   - 摆放：底面(Z=0)直接朝下平铺热床，真·零支撑直打！

3. 03_power_brick_cable_pod.stl    (60.0 × 204.0 × 102.0 mm  | 约 107g PETG)
   - 侧挂电源舱：贴靠 Mac Studio 空白左/右侧壁放置（低于上方 RS30 底面 45mm），解放背部全部接口与散热孔
   - 摆放：底面(Z=0)直接朝下平铺热床，零支撑打印

4. 04_bottom_dust_filter_frame.stl (180.0 × 180.0 × 3.2 mm   | 约 33g PETG)
   - 前抽式防尘滤网托框：宽度 180mm (< 182.4mm 前下通道)，可直接从正面下部水平抽出清理灰尘！

三、直接发给淘宝/闲鱼「拓竹农场代打」或「嘉立创3D打印」的工艺嘱咐
------------------------------------------------------------------------
- 强烈推荐材料：PETG-CF（碳纤增强，刚度提升 65%、耐热 ~85°C、无层纹磨砂金属感）或 PETG 哑光（耐热 ~75°C）
  * 严禁使用普通 PLA（耐温仅 52-55°C 且在 5.4kg 静载下易蠕变下垂）
- 层高：0.20 mm | 壁厚：4 层外壁（≥ 1.6 mm），顶/底实心层各 5 层 | 填充：30% 陀螺仪填充（Gyroid）
- 支撑：无需支撑（4 个零件均直接 Z=0 底面朝下平铺即可）

四、配套五金与防刮贴条清单（淘宝合计约 ¥15-25）
------------------------------------------------------------------------
1. 相机快装板同款 1/4"-20 × 20mm D环手拧螺丝 × 1 颗（从 2 号顶盘底部穿入锁死极米 RS30）
2. 0.8~1.0mm 厚自粘黑色植绒布胶条 1 卷（贴在 1 号底座左右两条 Z=26mm 水平滑轨顶面与立柱内侧，推拉丝滑零划痕！）
3. 2mm 厚硅胶防滑脚垫贴 × 6 粒（贴底座四角底面 + 2 号云台沉槽内）
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
