# -*- coding: utf-8 -*-
"""中学物理创新实验方案 AI 生成、分析、排名与版本管理后端。"""

import base64
import json
import os
import re
import sqlite3
from datetime import datetime, timezone

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB = os.getenv("DB_PATH", "plans.db")

AI_API_URL = os.getenv("AI_API_URL", "https://api.deepseek.com/v1/chat/completions")
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "deepseek-chat")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "caimingye78/physicsexperiment")
GITHUB_BRANCH = os.getenv("GITHUB_BRANCH", "main")
GITHUB_SAVE_PATH = os.getenv("GITHUB_SAVE_PATH", "ai-saved-plans")


def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS plans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        plan TEXT DEFAULT '',
        analysis TEXT DEFAULT '',
        improved TEXT DEFAULT '',
        version INTEGER DEFAULT 0,
        score INTEGER DEFAULT 0,
        versions TEXT DEFAULT '[]',
        created TEXT DEFAULT (datetime('now','localtime'))
    )"""
    )
    cur.execute("PRAGMA table_info(plans)")
    existing = {row[1] for row in cur.fetchall()}
    migrations = {
        "score": "ALTER TABLE plans ADD COLUMN score INTEGER DEFAULT 0",
        "versions": "ALTER TABLE plans ADD COLUMN versions TEXT DEFAULT '[]'",
    }
    for column, sql in migrations.items():
        if column not in existing:
            cur.execute(sql)

    cur.execute("SELECT id, plan, versions FROM plans")
    for pid, plan, versions in cur.fetchall():
        if not versions or versions == "[]":
            initial_versions = json.dumps(
                [{"v": 0, "type": "初始方案", "content": plan or ""}],
                ensure_ascii=False,
            )
            cur.execute("UPDATE plans SET versions=? WHERE id=?", (initial_versions, pid))
    con.commit()
    con.close()


def db(sql, args=(), one=False):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    cur = con.execute(sql, args)
    rows = cur.fetchall()
    last_id = cur.lastrowid
    con.commit()
    con.close()
    if sql.strip().upper().startswith("INSERT"):
        return last_id
    return (rows[0] if rows else None) if one else rows


SYS = "你是一位经验丰富的中学物理教研专家，擅长设计适合中学生小组完成的创新实验。"


def call_ai(prompt, sys=SYS):
    if not AI_API_KEY:
        return "⚠️ 服务器未配置 AI_API_KEY，请在部署平台的环境变量中设置。"

    try:
        r = requests.post(
            AI_API_URL,
            headers={
                "Authorization": f"Bearer {AI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": AI_MODEL,
                "messages": [
                    {"role": "system", "content": sys},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.7,
            },
            timeout=120,
        )
        data = r.json()
        if "choices" in data:
            return data["choices"][0]["message"]["content"]
        return f"⚠️ API返回异常：{data}"
    except Exception as e:
        return f"⚠️ 调用失败：{e}"


def extract_score(text):
    """从分析文本提取创新性评分，返回 0-10。"""
    match = re.search(r"创新性评分[^\d]*?(\d{1,2})", text or "")
    if not match:
        match = re.search(r"(\d{1,2})\s*[/／分]", text or "")
    if not match:
        return 0
    return max(0, min(int(match.group(1)), 10))


def slugify_topic(topic):
    slug = re.sub(r"[^A-Za-z0-9\u4e00-\u9fff]+", "-", topic).strip("-")
    return slug[:48] or "physics-plan"


def github_file_path(plan):
    return f"{GITHUB_SAVE_PATH}/{plan['id']:04d}-{slugify_topic(plan['topic'])}.md"


def github_headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def build_plan_markdown(plan):
    saved_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    versions = json.loads(plan["versions"] or "[]")
    parts = [
        f"# {plan['topic']}",
        "",
        f"- 方案 ID：{plan['id']}",
        f"- 保存时间：{saved_at}",
        f"- 版本：{plan['version']}",
        f"- 创新性评分：{plan['score'] or 0}",
        "",
        "## AI 生成方案",
        "",
        plan["plan"] or "暂无",
    ]
    if plan["analysis"]:
        parts.extend(["", "## AI 分析报告", "", plan["analysis"]])
    if plan["improved"]:
        parts.extend(["", f"## 改进版方案（第 {plan['version']} 次迭代）", "", plan["improved"]])
    if len(versions) > 1:
        parts.extend(["", "## 历史版本"])
        for item in versions:
            parts.extend(["", f"### {item.get('type', '版本')} v{item.get('v', '')}", "", item.get("content", "")])
    return "\n".join(parts).rstrip() + "\n"


def save_plan_to_github(pid, reason):
    if not GITHUB_TOKEN:
        return {"ok": False, "skipped": True, "msg": "未配置 GITHUB_TOKEN"}

    plan = db("SELECT * FROM plans WHERE id=?", (pid,), one=True)
    if not plan:
        return {"ok": False, "msg": "方案不存在，无法保存到 GitHub"}

    path = github_file_path(plan)
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}"
    sha = None

    existing = requests.get(url, headers=github_headers(), params={"ref": GITHUB_BRANCH}, timeout=30)
    if existing.status_code == 200:
        sha = existing.json().get("sha")
    elif existing.status_code != 404:
        return {"ok": False, "msg": f"读取 GitHub 文件失败：{existing.status_code} {existing.text[:200]}"}

    content = base64.b64encode(build_plan_markdown(plan).encode("utf-8")).decode("ascii")
    payload = {
        "message": f"{reason}: {plan['topic']}",
        "content": content,
        "branch": GITHUB_BRANCH,
    }
    if sha:
        payload["sha"] = sha

    saved = requests.put(url, headers=github_headers(), json=payload, timeout=60)
    if saved.status_code not in (200, 201):
        return {"ok": False, "msg": f"保存到 GitHub 失败：{saved.status_code} {saved.text[:200]}"}

    data = saved.json().get("content", {})
    return {"ok": True, "path": path, "url": data.get("html_url")}


P_GEN = """请围绕主题「{topic}」，为中学生小组设计一份创新物理实验方案，用Markdown格式输出：
## 实验名称
（突出创新点）
## 实验目的
## 涉及物理原理
## 创新点说明
## 器材清单
（尽量使用生活中廉价易得的材料）
## 实验步骤
（编号分步，清晰可操作）
## 数据记录表
（用Markdown表格，体现控制变量法）
## 安全注意事项
## 小组分工建议
（操作员/记录员/计时员/汇报员等）"""

P_ANA = """请以中学物理教研专家身份分析下面这份实验方案，用Markdown输出，
其中第一项务必写成「创新性评分：X/10」的格式（X为1-10整数）：
## 创新性评分
（写成「创新性评分：X/10」并说明理由）
## 可行性评估
## 科学性检查
## 安全性提示
## 三条具体改进建议
【待分析方案】
{plan}"""

P_IMP = """请根据「原方案」和「分析意见」，输出一份改进升级版实验方案，
保持原Markdown结构，重点落实改进建议，让方案更科学、更创新、更易实施。
【原方案】
{plan}
【分析意见】
{analysis}"""


@app.route("/")
def home():
    return jsonify({"ok": True, "msg": "Physics AI backend is running."})


@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        topic = (request.get_json(silent=True) or {}).get("topic", "").strip()
        if not topic:
            return jsonify({"ok": False, "msg": "请输入实验主题"})

        plan = call_ai(P_GEN.format(topic=topic))
        versions = json.dumps([{"v": 0, "type": "初始方案", "content": plan}], ensure_ascii=False)
        pid = db("INSERT INTO plans(topic, plan, versions) VALUES(?,?,?)", (topic, plan, versions))
        github = save_plan_to_github(pid, "Save generated physics plan")
        return jsonify({"ok": True, "id": pid, "plan": plan, "github": github})
    except Exception as e:
        return jsonify({"ok": False, "msg": "后端出错：" + str(e)})


@app.route("/api/analyze/<int:pid>", methods=["POST"])
def analyze(pid):
    plan = db("SELECT * FROM plans WHERE id=?", (pid,), one=True)
    if not plan:
        return jsonify({"ok": False, "msg": "方案不存在"})

    base = plan["improved"] or plan["plan"]
    analysis = call_ai(P_ANA.format(plan=base))
    score = extract_score(analysis)
    db("UPDATE plans SET analysis=?, score=? WHERE id=?", (analysis, score, pid))
    github = save_plan_to_github(pid, "Save physics plan analysis")
    return jsonify({"ok": True, "analysis": analysis, "score": score, "github": github})


@app.route("/api/improve/<int:pid>", methods=["POST"])
def improve(pid):
    plan = db("SELECT * FROM plans WHERE id=?", (pid,), one=True)
    if not plan:
        return jsonify({"ok": False, "msg": "方案不存在"})

    base = plan["improved"] or plan["plan"]
    analysis = plan["analysis"] or call_ai(P_ANA.format(plan=base))
    improved = call_ai(P_IMP.format(plan=base, analysis=analysis))
    new_version = plan["version"] + 1
    score = extract_score(analysis)
    versions = json.loads(plan["versions"] or "[]")
    versions.append({"v": new_version, "type": f"改进v{new_version}", "content": improved})

    db(
        "UPDATE plans SET improved=?, analysis=?, version=?, score=?, versions=? WHERE id=?",
        (improved, analysis, new_version, score, json.dumps(versions, ensure_ascii=False), pid),
    )
    github = save_plan_to_github(pid, "Save improved physics plan")
    return jsonify({"ok": True, "improved": improved, "version": new_version, "github": github})


@app.route("/api/list")
def list_plans():
    rows = db(
        "SELECT id,topic,version,score,created,(analysis!='') a,(improved!='') i "
        "FROM plans ORDER BY id DESC"
    )
    return jsonify([dict(row) for row in rows])


@app.route("/api/rank")
def rank():
    rows = db(
        "SELECT id,topic,version,score,created FROM plans "
        "WHERE score>0 ORDER BY score DESC, version DESC, id DESC"
    )
    return jsonify([dict(row) for row in rows])


@app.route("/api/get/<int:pid>")
def get_plan(pid):
    plan = db("SELECT * FROM plans WHERE id=?", (pid,), one=True)
    if not plan:
        return jsonify({})
    data = dict(plan)
    data["versions"] = json.loads(data.get("versions") or "[]")
    return jsonify(data)


@app.route("/api/delete/<int:pid>", methods=["POST"])
def delete(pid):
    db("DELETE FROM plans WHERE id=?", (pid,))
    return jsonify({"ok": True})


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
