import html
import json
import re
import urllib.parse
import urllib.request

import numpy as np
import pandas as pd
import plotly.express as px
from openai import OpenAI


def esc(value):
    return html.escape(str(value))


def demo():
    np.random.seed(42)
    dates = pd.date_range("2025-01-01", periods=365, freq="D")
    return pd.DataFrame({
        "date": np.random.choice(dates, 500),
        "region": np.random.choice(["Seattle", "New York", "Chicago", "Los Angeles"], 500),
        "product": np.random.choice(["Laptop", "Phone", "Tablet", "Monitor"], 500),
        "units": np.random.randint(1, 20, 500),
        "sales": np.random.uniform(100, 2000, 500).round(2),
        "profit": np.random.uniform(10, 500, 500).round(2),
    })


def fmt(value):
    return value.strftime("%Y-%m-%d") if hasattr(value, "strftime") else value


BLUES = ["#1565D8", "#2399E0", "#5FB4CE", "#A3C6E0", "#7A9CC6", "#4A6B8A"]


def style_fig(fig, bars=False):
    fig.update_layout(
        template="simple_white",
        font=dict(family="Inter, sans-serif", color="#16202E", size=12),
        margin=dict(l=8, r=8, t=16, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        colorway=BLUES,
        showlegend=False,
        title=None,
    )
    fig.update_xaxes(
        showgrid=False,
        linecolor="#E6E9EE",
        title=None,
        tickfont=dict(color="#657285", size=11),
        tickformat="%Y-%m-%d",
        tickangle=-45,
    )
    fig.update_yaxes(
        gridcolor="#E6E9EE",
        griddash="dot",
        zeroline=False,
        title=None,
        tickfont=dict(color="#657285", size=11),
    )
    if bars:
        fig.update_traces(
            marker_color=[BLUES[i % len(BLUES)] for i in range(len(fig.data[0].x))],
            marker_cornerradius=3,
        )
    return fig


def build_chart(kind, res, x, y, title, base=None, metric=None, sx=None, sy=None):
    if kind == "bar" and x in res and y in res:
        return style_fig(px.bar(res, x=x, y=y), True)
    if kind == "line" and x in res and y in res:
        return style_fig(px.line(res, x=x, y=y))
    if kind == "pie" and x in res and y in res:
        fig = px.pie(res, names=x, values=y)
        fig.update_layout(margin=dict(t=8, b=8), colorway=BLUES)
        return fig
    if kind == "histogram" and base is not None and metric:
        return style_fig(px.histogram(base, x=metric))
    if kind == "histogram" and x in res:
        return style_fig(px.histogram(res, x=x))
    if kind == "scatter" and sx and sy:
        return style_fig(px.scatter(base, x=sx, y=sy))
    if kind == "scatter" and x in res and y in res:
        return style_fig(px.scatter(res, x=x, y=y))
    return None


def run_manual(df, table_name, op, gb, metric, kind, sx=None, sy=None):
    name = op.lower()
    if op == "Count":
        res = (
            pd.DataFrame({"count": [len(df)]})
            if gb == "None"
            else df.groupby(gb, dropna=False).size().reset_index(name="count")
        )
        y = "count"
    else:
        fn = {"Sum": "sum", "Average": "mean", "Minimum": "min", "Maximum": "max"}[op]
        if gb == "None":
            res = pd.DataFrame({name: [getattr(df[metric], fn)()]})
        else:
            res = (
                getattr(df.groupby(gb, dropna=False)[metric], fn)()
                .reset_index()
                .rename(columns={metric: name})
            )
        y = name

    x = None if gb == "None" else gb
    agg = {"Sum": "SUM", "Average": "AVG", "Minimum": "MIN", "Maximum": "MAX", "Count": "COUNT"}[op]
    arg = "*" if op == "Count" else f'"{metric}"'
    sql = (
        f"SELECT {agg}({arg}) AS {y}\nFROM {table_name}"
        if gb == "None"
        else f'SELECT "{gb}", {agg}({arg}) AS {y}\nFROM {table_name}\nGROUP BY "{gb}"'
    )
    if op == "Count":
        py = "result = len(df)" if gb == "None" else f'result = df.groupby("{gb}").size()'
    else:
        py = (
            f'result = df["{metric}"].{fn}()'
            if gb == "None"
            else f'result = df.groupby("{gb}")["{metric}"].{fn}()'
        )

    chart_kind = {
        "Bar chart": "bar",
        "Line chart": "line",
        "Pie chart": "pie",
        "Histogram": "histogram",
        "Scatter plot": "scatter",
    }.get(kind)
    if chart_kind in ("bar", "line", "pie") and not x:
        chart_kind = None
    fig = build_chart(chart_kind, res, x, y, "", df, metric, sx, sy) if chart_kind else None
    insight = None
    if x and op in ("Sum", "Count") and len(res) > 1 and res[y].sum():
        top = res.sort_values(y, ascending=False).iloc[0]
        insight = (
            f"{esc(fmt(top[x]))} leads with <strong>{top[y]:,.2f}</strong> {name} "
            f"{esc(metric or 'rows')}, representing {top[y] / res[y].sum():.1%} of the total."
        )
    title = f"{op} of {metric or 'rows'}" + (f" by {gb}" if gb != "None" else "")
    return dict(
        res=res,
        sql=sql,
        py=py,
        fig=fig,
        title=title,
        sub=f"{len(res)} groups · {kind}",
        ins=insight,
        extra=[],
        series=metric or "count",
    )


SYSTEM_PROMPT = """You are a professional data analyst.

Return valid JSON with these keys:

sql:
One DuckDB SELECT query.

python:
A short pandas analysis snippet.

chart:
Object with type:
bar, line, scatter, histogram, pie, or none.
Include x, y, title.

answer:
A direct answer to the user.

insights:
Array of useful observations.

Rules:
- Only use the supplied table and columns.
- Use SELECT or WITH SELECT only.
- No data modification.
- No file access.
- No network access.
- Generated Python is displayed but never executed.
"""


def parse_json_response(text):
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)


def ask_agent(provider, key, model, prompt):
    if provider == "OpenAI":
        response = OpenAI(api_key=key).chat.completions.create(
            model=model,
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return parse_json_response(response.choices[0].message.content)

    if provider == "Gemini":
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{urllib.parse.quote(model, safe='')}:generateContent"
        )
        payload = {
            "systemInstruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0, "responseMimeType": "application/json"},
        }
        request = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "x-goog-api-key": key},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        return parse_json_response(text)

    if provider == "Claude":
        payload = {
            "model": model,
            "max_tokens": 4096,
            "temperature": 0,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": prompt}],
        }
        request = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
        text = "".join(
            part.get("text", "")
            for part in result.get("content", [])
            if part.get("type") == "text"
        )
        return parse_json_response(text)

    raise ValueError(f"Unsupported AI provider: {provider}")


def run_ai(df, con, table_name, question, provider, key, model):
    schema = "\n".join(f"- {column}: {dtype}" for column, dtype in zip(df.columns, df.dtypes.astype(str)))
    prompt = (
        f"Table: {table_name}\n\nColumns:\n{schema}\n\n"
        f"Sample rows:\n{df.head(5).to_csv(index=False)}\n\nQuestion:\n{question}\n"
    )
    plan = ask_agent(provider, key, model, prompt)
    sql = str(plan.get("sql", "")).strip().rstrip(";")
    if not re.match(r"(?is)^(select|with)\b", sql):
        raise ValueError("Only SELECT queries are allowed.")
    scrubbed = re.sub(r"'(?:[^']|'')*'|\"(?:[^\"]|\"\")*\"", "''", sql)
    if ";" in scrubbed:
        raise ValueError("Only a single statement is allowed.")
    if re.search(
        r"(?is)\b(insert|update|delete|drop|alter|create|attach|detach|copy|export|import|install|"
        r"load|pragma|call|set|read_\w+|\w+_scan|glob|getenv)\b",
        scrubbed,
    ):
        raise ValueError("The generated SQL contains a restricted keyword or function.")
    res = con.execute(sql).df()
    chart = plan.get("chart") or {}
    fig = build_chart(chart.get("type", "none"), res, chart.get("x"), chart.get("y"), "")
    insights = plan.get("insights")
    return dict(
        res=res,
        sql=sql,
        py=plan.get("python", ""),
        fig=fig,
        title=chart.get("title") or "Visualization",
        sub=f"{len(res)} rows · AI analysis",
        ins=esc(plan.get("answer", "")),
        extra=[esc(item) for item in insights] if isinstance(insights, list) else [],
        series="result",
    )
