import os, re, sqlite3
import streamlit as st
import pandas as pd
import numpy as np
import duckdb
from analysis import demo, esc, run_ai, run_manual
from ui_assets import apply_style, ic

st.set_page_config(page_title="AI Data Analyst", layout="wide", initial_sidebar_state="expanded")
apply_style()

# ---------------- DATA ----------------
ss = st.session_state
src = ss.get("src", "Sample dataset")
df, table_name, load_err, fname = None, "uploaded_data", None, "sample_data.csv"
try:
    if src == "Sample dataset":
        df, table_name = demo(), "sample_data"
    elif src == "Upload CSV" and ss.get("csv") is not None:
        ss["csv"].seek(0)
        df, fname = pd.read_csv(ss["csv"]), ss["csv"].name
    elif src == "SQLite Database" and ss.get("dbf") is not None and ss.get("tbl"):
        with open("/tmp/analyst_uploaded.sqlite", "wb") as f:
            f.write(ss["dbf"].getvalue())
        conn = sqlite3.connect("/tmp/analyst_uploaded.sqlite")
        safe = ss["tbl"].replace('"', '""')
        df = pd.read_sql_query(f'SELECT * FROM "{safe}" LIMIT 100000', conn)
        conn.close()
        table_name, fname = ss["tbl"], ss["dbf"].name
except Exception as exc:
    load_err = str(exc)

if df is not None:
    for c in df.columns:
        if df[c].dtype == object and any(w in c.lower() for w in ["date", "time"]):
            conv = pd.to_datetime(df[c], errors="coerce")
            if conv.notna().mean() > 0.8:
                df[c] = conv
date_column_config = {
    c: st.column_config.DateColumn(c, format="YYYY-MM-DD")
    for c in (df.columns if df is not None else [])
    if pd.api.types.is_datetime64_any_dtype(df[c])
}
table_name = re.sub(r"[^A-Za-z0-9_]", "_", table_name) or "data_table"

# ---------------- SIDEBAR ----------------
rows_txt = f"{len(df):,} rows · {len(df.columns)} columns" if df is not None else "No dataset loaded"
with st.sidebar:
    st.markdown(f"""<div class="sb"><div class="brand"><span class="lg">{ic("bar",22)}</span>Arafa&apos;s Analytics Page</div>
<div class="lbl">Data source</div></div>""", unsafe_allow_html=True)
    sel = st.radio(
        "Source",
        ["Sample dataset", "Upload CSV", "SQLite Database"],
        key="src",
        label_visibility="collapsed",
    )
    if sel == "Upload CSV":
        st.file_uploader("CSV file", type=["csv"], key="csv", label_visibility="collapsed")
    elif sel == "SQLite Database":
        st.file_uploader("SQLite database", type=["db", "sqlite", "sqlite3"], key="dbf", label_visibility="collapsed")
        st.text_input("Table name", key="tbl")
    if load_err:
        st.error(f"The data could not be read: {load_err}")
    if df is not None:
        st.markdown(f"""<div class="file">{ic("file",24)}<div><b>{esc(fname)}</b><small>{rows_txt}</small></div><span class="ck">{ic("ck")}</span></div>""", unsafe_allow_html=True)

# ---------------- TOP + HEADER ----------------
st.markdown("""<div class="hd" style="margin-top:36px"><div><h1>AI Data Analyst</h1>
<p>A clearer view of your data. A smarter way to find insights.</p></div></div>""", unsafe_allow_html=True)

if df is None or df.empty or len(df.columns) == 0:
    st.info("Choose a data source in the sidebar to begin." if df is None else "The dataset is empty.")
    st.stop()

con = duckdb.connect(database=":memory:")
con.register(table_name, df)
con.execute("SET enable_external_access=false")
sig = (fname, table_name, len(df), tuple(df.columns))
if ss.get("sig") != sig:
    ss.pop("last", None)
    ss["sig"] = sig

num_cols = df.select_dtypes(include=np.number).columns.tolist()
group_cols = [c for c in df.columns if c not in num_cols] or df.columns.tolist()
preferred_group = next(
    (c for c in group_cols
     if c in df.columns and not np.issubdtype(df[c].dtype, np.datetime64)),
    "None",
)
miss, dup = int(df.isna().sum().sum()), int(df.duplicated().sum())

# ---------------- KPIs ----------------
ok = lambda t: f'<small class="ok">{ic("ck",14)}{t}</small>'
st.markdown(f"""<div class="kpis">
<div class="kpi"><div class="t">Total rows{ic("tb")}</div><strong>{len(df):,}</strong><small>Records in your dataset</small></div>
<div class="kpi"><div class="t">Columns{ic("co")}</div><strong>{len(df.columns)}</strong><small>{len(num_cols)} numeric · {len(df.columns)-len(num_cols)} categorical</small></div>
<div class="kpi"><div class="t">Missing values{ic("se")}</div><strong>{miss:,}</strong>{ok("Your dataset is complete") if miss == 0 else "<small>Cells without a value</small>"}</div>
<div class="kpi"><div class="t">Duplicate rows{ic("cp")}</div><strong>{dup:,}</strong>{ok("All records are unique") if dup == 0 else "<small>Repeated records</small>"}</div>
</div>""", unsafe_allow_html=True)

# ---------------- MAIN GRID ----------------
left, right = st.columns([5, 8], gap="large")

with left:
    with st.container(border=True, key="schema"):
        st.markdown(f'<div class="ch">{ic("co")}Dataset schema<span class="hint">{len(df.columns)} columns</span></div>', unsafe_allow_html=True)
        kind_of = lambda c: ("date", "Aa") if np.issubdtype(df[c].dtype, np.datetime64) else (("number", "#") if c in num_cols else ("string", "Aa"))
        st.markdown("".join(f'<div class="sch"><u>{kind_of(c)[1]}</u>{esc(c)}<em>{kind_of(c)[0]}</em></div>' for c in df.columns), unsafe_allow_html=True)

with right:
    with st.container(border=True, key="analyze"):
        st.markdown(f'<div class="ch">{ic("sl")}Analyze your data</div>', unsafe_allow_html=True)
        t_manual, t_ai = st.tabs(["Manual analysis", "AI analysis"])
        with t_manual:
            c1, c2 = st.columns(2)
            op = c1.selectbox("Analysis type", ["Sum", "Average", "Count", "Minimum", "Maximum"])
            group_options = ["None"] + group_cols
            default_group = preferred_group if preferred_group in group_options else "None"
            gb = c2.selectbox("Group by", group_options, index=group_options.index(default_group))
            c3, c4 = st.columns(2)
            metric = c3.selectbox("Numeric column", num_cols, disabled=(op == "Count" or not num_cols)) if num_cols else None
            kind = c4.selectbox("Chart type", ["Bar chart", "Line chart", "Pie chart", "Histogram", "Scatter plot", "Table only"])
            sx = sy = None
            if kind == "Scatter plot" and len(num_cols) >= 2:
                s1, s2 = st.columns(2)
                sx = s1.selectbox("Scatter x-axis", num_cols, key="sx")
                sy = s2.selectbox("Scatter y-axis", num_cols, index=1, key="sy")
            st.markdown('<div class="line"></div>', unsafe_allow_html=True)
            n1, n2 = st.columns([3, 2])
            n1.markdown('<div class="note">No API key required</div>', unsafe_allow_html=True)
            go_manual = n2.button("Analyze dataset", type="primary", icon=":material/auto_awesome:", key="go_m")
        with t_ai:
            provider = st.selectbox("AI provider", ["OpenAI", "Gemini", "Claude"], key="ai_provider")
            k1, k2 = st.columns(2)
            env_key = {
                "OpenAI": "OPENAI_API_KEY",
                "Gemini": "GEMINI_API_KEY",
                "Claude": "ANTHROPIC_API_KEY",
            }[provider]
            default_model = {
                "OpenAI": "gpt-4.1-mini",
                "Gemini": "gemini-2.5-flash",
                "Claude": "claude-sonnet-5-5",
            }[provider]
            env_model = {
                "OpenAI": "OPENAI_MODEL",
                "Gemini": "GEMINI_MODEL",
                "Claude": "ANTHROPIC_MODEL",
            }[provider]
            api_key = k1.text_input("API key", value=os.getenv(env_key, ""), type="password")
            model = k2.text_input("Model", value=os.getenv(env_model, default_model))
            aq = st.text_area("Ask your data analyst", placeholder="e.g. Find the top 5 categories by average revenue.", height=100)
            st.markdown('<div class="line"></div>', unsafe_allow_html=True)
            a1, a2 = st.columns([3, 2])
            a1.markdown(f'<div class="note">Sends the schema and 5 sample rows to AI</div>', unsafe_allow_html=True)
            go_ai = a2.button("Analyze dataset", type="primary", icon=":material/auto_awesome:", key="go_a", disabled=not aq.strip())

    # run
    if go_manual or "last" not in ss:
        try:
            if op != "Count" and metric is None:
                st.error("Select a numeric column to continue.")
            else:
                ss["last"] = run_manual(df, table_name, op, gb, metric, kind, sx, sy)
        except Exception as exc:
            st.error(f"The analysis could not be completed: {exc}")
    if go_ai:
        if not api_key:
            st.error("Enter your API key to continue.")
        else:
            with st.spinner("Analyzing your data..."):
                try:
                    ss["last"] = run_ai(df, con, table_name, aq, provider, api_key, model)
                except Exception as exc:
                    st.error(f"The AI analysis could not be completed: {exc}")

L = ss.get("last")
if L:
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    with st.container(border=True, key="results"):
        st.markdown(f'<div class="ch">{ic("bar")}Analysis results<span class="bdg">Completed</span></div>', unsafe_allow_html=True)
        tv, tr, tq, tp = st.tabs(["Visualization", "Results", "SQL", "Python"])
        with tv:
            st.markdown(f'<div class="ct"><div><b>{esc(L["title"])}</b><small>{esc(L["sub"])}</small></div><div class="leg"><i></i>{esc(L["series"])}</div></div>', unsafe_allow_html=True)
            if L["fig"] is not None:
                st.plotly_chart(L["fig"], width="stretch", theme=None)
            else:
                st.info("No chart is available for this selection. Choose a grouping column or a different chart type.")
            if L["ins"]:
                extra = "".join(f"<br>&bull; {i}" for i in L["extra"])
                st.markdown(f'<div class="ins">{ic("bu")}<div><b>Key insight</b><span>{L["ins"]}{extra}</span></div></div>', unsafe_allow_html=True)
        with tr:
            result_date_config = {
                c: st.column_config.DateColumn(c, format="YYYY-MM-DD")
                for c in L["res"].columns
                if pd.api.types.is_datetime64_any_dtype(L["res"][c])
            }
            st.dataframe(L["res"], width="stretch", hide_index=True, column_config=result_date_config)
            st.download_button("Download CSV", L["res"].to_csv(index=False).encode("utf-8"), "analysis_result.csv", "text/csv")
        with tq:
            st.code(L["sql"], language="sql")
        with tp:
            st.code(L["py"], language="python")
            st.caption("Generated Python is displayed for reference and is not executed.")

# ---------------- DATASET OVERVIEW ----------------
st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
with st.container(border=True, key="overview"):
    h1, h2, h3 = st.columns([5, 2.4, 0.8], vertical_alignment="center")
    h1.markdown(f'<div class="ch" style="margin:0;padding:0;border:0">{ic("tb")}Dataset overview</div>', unsafe_allow_html=True)
    q = h2.text_input("Search data", placeholder="Search data...", label_visibility="collapsed")
    h3.download_button("Export", df.to_csv(index=False).encode("utf-8"), "dataset.csv", "text/csv", icon=":material/download:")
    st.markdown('<div class="line" style="margin-top:6px"></div>', unsafe_allow_html=True)
    tp_, ti_ = st.tabs(["Data preview", "Column information"])
    view = df
    if q:
        view = df[df.astype(str).apply(lambda c: c.str.contains(q, case=False, na=False)).any(axis=1)]
    with tp_:
        st.dataframe(view.head(100), width="stretch", height=300, column_config=date_column_config)
        st.caption(f"Showing {min(len(view), 100):,} of {len(view):,} rows")
    with ti_:
        st.dataframe(pd.DataFrame({"Column": df.columns, "Data type": df.dtypes.astype(str).values,
                                   "Missing values": df.isna().sum().values, "Unique values": df.nunique().values}),
                     width="stretch", hide_index=True)
