# 中学生物理创新实验 · AI生成与分析平台

输入实验主题，AI 自动生成完整实验方案，并支持 AI 分析、迭代改进、打分排名、多版本对比和导出。

## 功能

- AI 生成实验方案：名称、原理、器材、步骤、数据表、分工。
- AI 分析：创新性评分、可行性、科学性、安全提示、改进建议。
- 一键迭代改进：每次都在上一版基础上升级。
- 方案打分排名：按创新性评分排序。
- 多版本对比：初始方案与改进版并排查看。
- 导出 Markdown，或通过浏览器打印为 PDF。
- 可选自动保存到 GitHub：配置 `GITHUB_TOKEN` 后，方案会保存为 Markdown 文件。

## 目录结构

```text
physicsexperiment/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Procfile
├── docs/
│   └── index.html
├── .github/
│   └── workflows/
│       └── pages.yml
├── .gitignore
├── render.yaml
└── README.md
```

## 本地运行

```bash
cd backend
pip install -r requirements.txt
export AI_API_KEY=你的模型服务Key
python app.py
```

本地调试前端时，把 `docs/index.html` 顶部的 `API_BASE` 改成：

```js
const API_BASE = "http://127.0.0.1:5000";
```

然后用浏览器打开 `docs/index.html`。

## 后端部署

Render 手动创建 Web Service：

| 配置项 | 内容 |
| --- | --- |
| Root Directory | `backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |

环境变量：

| 变量名 | 示例 |
| --- | --- |
| `AI_API_URL` | `https://api.deepseek.com/v1/chat/completions` |
| `AI_API_KEY` | 在部署平台环境变量中填写，不要提交到 GitHub |
| `AI_MODEL` | `deepseek-chat` |
| `GITHUB_TOKEN` | 可选，GitHub fine-grained token，授予本仓库 Contents 读写权限 |
| `GITHUB_REPO` | `caimingye78/physicsexperiment` |
| `GITHUB_BRANCH` | `main` |
| `GITHUB_SAVE_PATH` | `ai-saved-plans` |

部署完成后，把 `docs/index.html` 中的 `API_BASE` 改成 Render 后端地址：

```js
const API_BASE = "https://你的后端.onrender.com";
```

## 前端部署

本仓库内置 GitHub Pages 工作流。推送到 `main` 或 `master` 后，在 GitHub 仓库的 Settings -> Pages 中选择 GitHub Actions。

Pages 会部署 `docs/` 目录。

## 注意

API Key 只放在部署平台环境变量里，切勿写进代码上传。
