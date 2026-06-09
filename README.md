# physicsexperiment · 高中物理震撼实验馆

一组可交互、可离线运行的高中物理演示实验。每个实验都包含：

- 网页模拟器 `index.html`（纯前端、零依赖，双击即可离线运行）
- 可打印实验讲义 `handout.md`（实验目标 / 原理 / 器材 / 步骤 / 可探究问题 / 安全提示）
- 原理示意图 `diagram.svg`

## 实验画廊

打开 [`experiments/index.html`](experiments/index.html) 进入导航首页，或直接进入各实验：

| # | 实验 | 关键物理 |
| --- | --- | --- |
| 01 | [克拉尼图形](experiments/01-chladni/) | 二维驻波 / 节线，频率 ∝ √(m²+n²) |
| 02 | [双缝干涉](experiments/02-double-slit/) | I = I0·cos²(πd·sinθ/λ)，测波长、缺级 |
| 03 | [多普勒效应](experiments/03-doppler/) | f' = f·(v±vo)/(v∓vs)，马赫锥 |
| 04 | [李萨如图形](experiments/04-lissajous/) | 垂直简谐振动合成，频率比判定 |
| 05 | [涡流制动](experiments/05-eddy-brake/) | 楞次定律，v_term = m·g/k |
| 06 | [猎人射猴](experiments/06-monkey-hunter/) | 抛体运动的独立性，重力同步 |
| 07 | [受迫振动与共振](experiments/07-resonance/) | A = F/√((ω₀²−ω²)²+(2βω)²) |
| 08 | [弦上驻波](experiments/08-standing-wave/) | λ = 2L/n，f_n = n·v/(2L) |
| 09 | [气体动理论](experiments/09-gas-kinetics/) | 麦克斯韦分布，P·V = N·k·T |
| 10 | [牛顿摆](experiments/10-newtons-cradle/) | 动量与动能双守恒 |

> 另有「摆动波 Pendulum Wave」实验位于仓库根目录的 `web/` 与 `scripts/`（见 PR #1）。

## 设计特色

- 每个模拟器都做了创意交互：沙粒沉降动画、白光彩色条纹、马赫锥/声爆提示、示波器荧光余晖、并排对比下落、命中特效、共振情景预设、可拨虚拟琴弦、瞬间加热冷却、恢复系数衰减等。
- 把经典考点"实验化"：测波长 λ=d·Δy/L、缺级预测、火车鸣笛求 Δf、共振危险频率、为何牛顿摆不会"一球双速弹出"等，均设计为可动手探究的环节，并写入各 handout 的"可探究问题"。

## 运行方式

直接用浏览器打开任意 `index.html` 即可，无需联网或安装依赖。也可在仓库根目录启动本地服务：

```bash
python3 -m http.server 8000   # 然后访问 http://localhost:8000/experiments/
```
