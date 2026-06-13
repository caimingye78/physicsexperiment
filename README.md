# physicsexperiment · 物理创新实验平台

本仓库包含两部分：

- `ai/`：GitHub Pages 前端，提供“中学生物理创新实验 · AI 生成与分析平台”。
- `backend/`：Flask 后端，负责调用大模型 API、保存方案、分析和迭代改进。

在线访问（GitHub Pages 部署后）：`https://caimingye78.github.io/physicsexperiment/`
AI 平台访问：`https://caimingye78.github.io/physicsexperiment/ai/`

> 注意：GitHub Pages 只能托管静态网页，不能安全保存或运行 AI API Key。后端请部署到 Render、Railway 或自己的服务器，并把 API Key 放在环境变量中。

## AI 平台目录结构

- `backend/app.py` — Flask API 服务。
- `backend/requirements.txt` — Python 依赖。
- `backend/Procfile` — Render 等平台的启动命令。
- `ai/index.html` — GitHub Pages 上的 AI 平台页面。
- `.github/workflows/pages.yml` — GitHub Pages 自动部署工作流。

## 部署后端

以 Render 为例：

方式一：在 Render 中选择本仓库的 `render.yaml` 作为 Blueprint，然后填写 `AI_API_KEY`。

方式二：手动创建 Web Service：

| 配置项 | 内容 |
| --- | --- |
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |

环境变量：

| 变量名 | 示例 |
| --- | --- |
| `AI_API_URL` | `https://api.deepseek.com/v1/chat/completions` |
| `AI_API_KEY` | 在平台环境变量中填写，不要提交到 GitHub |
| `AI_MODEL` | `deepseek-chat` |

部署完成后，将 `ai/index.html` 中的 `API_BASE` 改成真实后端地址。

## 旧版实验馆

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
