# physicsexperiment · 高中物理震撼实验馆

一组可交互、可离线运行的高中物理演示实验。每个实验都包含网页模拟器、可打印讲义与原理示意图，并把经典考点"实验化"成可动手探究的环节。

在线访问（GitHub Pages 部署后）：`https://caimingye78.github.io/physicsexperiment/`
本地访问：直接用浏览器打开根目录的 `index.html`。

## 实验清单

| # | 实验 | 关键物理 | 经典题实验化 |
| --- | --- | --- | --- |
| 00 | [摆动波](web/index.html) | 单摆周期 T = 2π√(L/g) | 由周期反推重力加速度 g |
| 01 | [克拉尼图形](experiments/01-chladni/) | 二维驻波 / 节线 | 频率 ∝ √(m²+n²) |
| 02 | [双缝干涉](experiments/02-double-slit/) | I = I0·cos²(πd·sinθ/λ) | 测波长 λ=d·Δy/L、缺级 |
| 03 | [多普勒效应](experiments/03-doppler/) | f' = f·(v±vo)/(v∓vs) | 火车鸣笛求 Δf、马赫锥 |
| 04 | [李萨如图形](experiments/04-lissajous/) | 垂直简谐振动合成 | 示波器测未知频率 |
| 05 | [涡流制动](experiments/05-eddy-brake/) | 楞次定律 | 终极速度 v=m·g/k |
| 06 | [猎人射猴](experiments/06-monkey-hunter/) | 抛体运动独立性 | 命中与初速无关的证明 |
| 07 | [受迫振动与共振](experiments/07-resonance/) | 共振曲线 | 塔科马大桥/高脚杯危险频率 |
| 08 | [弦上驻波](experiments/08-standing-wave/) | λ = 2L/n，f_n = n·v/(2L) | 弦乐器定音、测声速 |
| 09 | [气体动理论](experiments/09-gas-kinetics/) | 麦克斯韦分布 | P·V = N·k·T 验证 |
| 10 | [牛顿摆](experiments/10-newtons-cradle/) | 动量与动能双守恒 | 为何不能"一球双速"弹出 |

## 目录结构

- `index.html` — 统一首页（实验馆入口，含全部 11 个实验）
- `experiments/` — 10 个实验，每个含 `index.html`（模拟器）、`handout.md`（讲义）、`diagram.svg`（示意图）
- `web/`、`scripts/`、`docs/` — 摆动波实验：模拟器、摆长计算脚本、讲义与数据表
- `.github/workflows/pages.yml` — GitHub Pages 自动部署工作流

## 运行方式

纯前端、无外部依赖，双击任意 `index.html` 即可离线运行。也可启动本地服务：

```bash
python3 -m http.server 8000   # 然后访问 http://localhost:8000/
```

## 在线发布（GitHub Pages）

本仓库已内置部署工作流。合并到 `main` 后，在 GitHub 仓库的 **Settings → Pages → Build and deployment → Source** 选择 **GitHub Actions** 即可，几分钟后即可通过上面的 Pages 网址在线点击访问。
