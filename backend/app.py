# -*- coding: utf-8 -*-
"""中学物理创新实验方案 AI 生成与分析平台后端。"""
import os
import sqlite3

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB = os.getenv("DB_PATH", "plans.db")
AI_API_URL = os.getenv("AI_API_URL", "https://api.deepseek.com/v1/chat/completions")
AI_API_KEY = os.getenv("AI_API_KEY", "")
AI_MODEL = os.getenv("AI_MODEL", "deepseek-chat")


def init_db():
    con = sqlite3.connect(DB)
    con.execute(
        """CREATE TABLE IF NOT EXISTS plans(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        plan TEXT DEFAULT '',
        analysis TEXT DEFAULT '',
        improved TEXT DEFAULT '',
        version INTEGER DEFAULT 0,
        created TEXT DEFAULT (datetime('now','localtime'))
    )"""
    )
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
    if "INSERT" in sql.upper():
        return last_id
    return (rows[0] if rows else None) if one else rows


def call_ai(prompt, sys="你是一位经验丰富的中学物理教研专家，擅长设计适合中学生小组完成的创新实验。"):
    if not AI_API_KEY:
        return "请先在后端平台环境变量中配置 AI_API_KEY。"

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
        return f"API 返回异常：{data}"
    except Exception as e:
        return f"调用失败：{e}（请检查网络、后端环境变量和 API Key）"


P_GEN = """请围绕主题「{topic}」，为中学生小组设计一份创新物理实验方案，用Markdown格式输出：

## 实验名称
（突出创新点）
## 实验目的
## 涉及物理原理
## 创新点说明
（与传统实验相比的创新之处）
## 器材清单
（尽量使用生活中廉价易得的材料，列出清单）
## 实验步骤
（编号分步，清晰可操作）
## 数据记录表
（用表格设计，体现控制变量法）
## 安全注意事项
## 小组分工建议
（操作员/记录员/计时员/汇报员等）"""

P_ANA = """请以中学物理教研专家身份，分析下面这份实验方案，用Markdown输出：

## 创新性评分
（1-10分，并说明理由）
## 可行性评估
（器材易得性、操作难度、耗时）
## 科学性检查
（物理原理是否正确、有无逻辑漏洞）
## 安全性提示
## 三条具体改进建议
（每条都要可操作，适合中学生实施）

【待分析方案】
{plan}"""

P_IMP = """请根据下面的「原方案」和「分析意见」，输出一份**改进升级版**实验方案，
保持原Markdown结构（实验名称/目的/原理/创新点/器材/步骤/数据表/安全/分工），
重点落实分析意见中的改进建议，让方案更科学、更有创新性、更易实施。

【原方案】
{plan}

【分析意见】
{analysis}"""


@app.route("/")
def index():
    return jsonify({"ok": True, "name": "physicsexperiment backend"})


@app.route("/api/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json(silent=True) or {}
        topic = data.get("topic", "").strip()

        if not topic:
            return jsonify({"ok": False, "msg": "请输入实验主题"})

        plan = call_ai(P_GEN.format(topic=topic))
        pid = db("INSERT INTO plans(topic, plan) VALUES(?,?)", (topic, plan))

        return jsonify({"ok": True, "id": pid, "plan": plan})
    except Exception as e:
        return jsonify({"ok": False, "msg": "后端出错：" + str(e)})


@app.route("/api/analyze/<int:pid>", methods=["POST"])
def analyze(pid):
    r = db("SELECT * FROM plans WHERE id=?", (pid,), one=True)
    if not r:
        return jsonify({"ok": False, "msg": "方案不存在"})
    base = r["improved"] or r["plan"]
    ana = call_ai(P_ANA.format(plan=base))
    db("UPDATE plans SET analysis=? WHERE id=?", (ana, pid))
    return jsonify({"ok": True, "analysis": ana})


@app.route("/api/improve/<int:pid>", methods=["POST"])
def improve(pid):
    r = db("SELECT * FROM plans WHERE id=?", (pid,), one=True)
    if not r:
        return jsonify({"ok": False, "msg": "方案不存在"})
    base = r["improved"] or r["plan"]
    ana = r["analysis"] or call_ai(P_ANA.format(plan=base))
    imp = call_ai(P_IMP.format(plan=base, analysis=ana))
    db(
        "UPDATE plans SET improved=?, analysis=?, version=version+1 WHERE id=?",
        (imp, ana, pid),
    )
    r = db("SELECT version FROM plans WHERE id=?", (pid,), one=True)
    return jsonify({"ok": True, "improved": imp, "version": r["version"]})


@app.route("/api/list")
def list_plans():
    rows = db(
        "SELECT id,topic,version,created,(analysis!='') a,(improved!='') i "
        "FROM plans ORDER BY id DESC"
    )
    return jsonify([dict(x) for x in rows])


@app.route("/api/get/<int:pid>")
def get_plan(pid):
    r = db("SELECT * FROM plans WHERE id=?", (pid,), one=True)
    return jsonify(dict(r) if r else {})


@app.route("/api/delete/<int:pid>", methods=["POST"])
def delete(pid):
    db("DELETE FROM plans WHERE id=?", (pid,))
    return jsonify({"ok": True})


init_db()

if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", "5000")))
