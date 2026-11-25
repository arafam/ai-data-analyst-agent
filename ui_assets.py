import streamlit as st

# ---------------- ICONS ----------------
P = {
 "bar": "M5 20V10M12 20V4M19 20v-7",
 "grid": "M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z",
 "db": "M5 6c0-1.7 3-3 7-3s7 1.3 7 3-3 3-7 3-7-1.3-7-3zM5 6v12c0 1.7 3 3 7 3s7-1.3 7-3V6M5 12c0 1.7 3 3 7 3s7-1.3 7-3",
 "file": "M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8zM14 3v5h5M9 13h6M9 17h6",
 "fold": "M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z",
 "sl": "M4 8h9M17 8h3M4 16h3M11 16h9M15 6v4M9 14v4",
 "sh": "M12 3l7 3v6c0 4-3 7-7 9-4-2-7-5-7-9V6z",
 "tb": "M4 7a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zM4 10h16M10 10v9",
 "co": "M4 7a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2zM10 5v14M15 5v14",
 "se": "M11 5a6 6 0 1 0 0 12 6 6 0 0 0 0-12zM20 20l-4-4",
 "cp": "M9 11a2 2 0 0 1 2-2h7a2 2 0 0 1 2 2v7a2 2 0 0 1-2 2h-7a2 2 0 0 1-2-2zM5 15V6a2 2 0 0 1 2-2h8",
 "bu": "M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z",
 "ck": "m5 12 5 5 9-10",
}
def ic(n, s=18):
    return f'<svg class="i" width="{s}" height="{s}" viewBox="0 0 24 24"><path d="{P[n]}"/></svg>'

STYLE = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
html,body,.stApp,[class*="css"]{font-family:Inter,-apple-system,'Segoe UI',sans-serif;color:#16202E}
.stApp{background:#F7F8FA}
header[data-testid="stHeader"]{background:transparent}
footer{display:none}
button[data-testid="stExpandSidebarButton"]{
    display:flex!important;
    visibility:visible!important;
    opacity:1!important;
    pointer-events:auto!important;
    position:fixed!important;
    top:10px!important;
    left:10px!important;
    z-index:10001!important;
    width:40px!important;
    height:40px!important;
    align-items:center!important;
    justify-content:center!important;
    border:1px solid #C9D1DC!important;
    border-radius:8px!important;
    background:#fff!important;
    color:#1565D8!important;
}
button[data-testid="stExpandSidebarButton"] *{visibility:visible!important;color:#1565D8!important}
.block-container{padding:0 48px 24px;max-width:1400px}
svg.i{fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;flex:none}
/* sidebar */
section[data-testid="stSidebar"]{background:#fff;border-right:1px solid #E6E9EE;width:272px!important;min-width:272px!important}
.sb{padding:0}
.st-key-src [role="radiogroup"]{display:flex;flex-direction:column;gap:10px;width:100%}
.st-key-src [role="radio"]{width:100%;min-height:48px;padding:10px 12px;border:1.5px solid #DDE5F0;border-radius:10px;background:#F9FBFD;box-shadow:0 1px 2px rgba(21,101,216,.04);transition:.15s ease}
.st-key-src [role="radio"]:hover{border-color:#8BB4EF;background:#F3F7FD;transform:translateY(-1px)}
.st-key-src [role="radio"][aria-checked="true"]{border-color:#1565D8;background:#EAF2FE;box-shadow:0 2px 8px rgba(21,101,216,.12)}
.st-key-src [role="radio"] label{width:100%;font-size:14px;font-weight:600;color:#2F4158}
.st-key-src [role="radio"][aria-checked="true"] label{color:#1565D8}
.st-key-src [data-testid="stWidgetLabel"]{display:none}
.brand{display:flex;align-items:center;gap:12px;font-size:22px;font-weight:600;letter-spacing:-.02em;margin:0 0 28px;color:#16202E!important;white-space:nowrap}
.brand .lg{width:40px;height:40px;border-radius:10px;background:#1565D8;color:#fff;display:grid;place-items:center}
.brand b{color:#1565D8}
.lbl{font-size:11.5px;font-weight:600;letter-spacing:.04em;color:#657285;margin:0 0 4px;text-transform:uppercase}
/* top bar and header */
.hd{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;margin-bottom:26px}
.hd h1{font-size:32px;font-weight:600;letter-spacing:-.02em;margin:0 0 6px;padding:0;line-height:1.15}.hd p{color:#657285;font-size:15px;margin:0}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:20px;margin-bottom:12px}
.kpi{background:#fff;border:1px solid #E6E9EE;border-radius:12px;padding:22px 24px}
.kpi .t{display:flex;justify-content:space-between;color:#657285;font-size:14px}
.kpi strong{display:block;font-size:34px;font-weight:600;margin:10px 0 6px;letter-spacing:-.02em;line-height:1.1}
.kpi small{color:#657285;font-size:12.5px;display:flex;align-items:center;gap:6px}.kpi small.ok{color:#0E7A4B}
@media(max-width:1100px){.kpis{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){.block-container{padding:0 16px 24px}.top{margin:0 -16px 24px;padding:0 16px}.hd{flex-direction:column}.hd h1{font-size:26px}.kpi{padding:16px}.kpi strong{font-size:28px}}
/* cards */
[data-testid="stVerticalBlockBorderWrapper"]:has(>div>[data-testid="stVerticalBlock"]>.stElementContainer .ch){background:#fff;border:1px solid #E6E9EE;border-radius:12px;padding:22px 24px;overflow:hidden}
.ch{display:flex;align-items:center;gap:12px;margin:-22px -24px 14px;padding:20px 24px;border-bottom:1px solid #E6E9EE;font-size:17px;font-weight:600}
.ch svg{color:#657285}.ch .hint{margin-left:auto;font-size:12.5px;font-weight:400;color:#657285}
.bdg{background:#E3F4EB;color:#0E7A4B;font-size:12px;font-weight:500;padding:2px 10px;border-radius:6px}
.stSelectbox label p,.stTextInput label p,.stTextArea label p{font-weight:500;font-size:13.5px}
[data-baseweb="select"]>div,.stTextInput input,.stTextArea textarea{border-radius:8px;border-color:#E6E9EE;background:#fff;min-height:46px}
[data-testid="stFileUploaderDropzone"]{border:1.5px dashed #DDE2E9;border-radius:10px;background:#F7F8FA}
.stButton>button,.stDownloadButton>button{border-radius:8px;font-weight:500;border:1px solid #E6E9EE}
.stButton>button[kind="primary"]{background:#1565D8;border-color:#1565D8;color:#fff;padding:.6rem 1.1rem}
.stButton>button[kind="primary"]:hover{background:#0F52B0}
:is(button,input,select,textarea):focus-visible{outline:2px solid #1565D8;outline-offset:2px}
.file{display:flex;align-items:center;gap:14px;border:1px solid #E6E9EE;border-radius:10px;padding:14px 16px;margin-top:6px}
.file>svg{color:#0E7A4B}.file b{display:block;color:#16202E!important;font-weight:500;font-size:13.5px}.file small{color:#657285;font-size:12.5px}.file .ck{margin-left:auto;color:#0E7A4B}
.sch{display:flex;align-items:center;gap:12px;padding:11px 0;font-size:14px}.sch u{text-decoration:none;color:#657285;font-size:12px;width:20px}
.sch em{margin-left:auto;font-style:normal;font-size:11.5px;color:#657285;background:#F3F5F8;padding:2px 9px;border-radius:5px}
.line{border-top:1px solid #E6E9EE;margin:8px -24px 14px}.note{display:flex;align-items:center;gap:8px;color:#657285;font-size:12.5px;padding-top:10px}
/* segmented control (Manual / AI) */
.st-key-analyze [data-baseweb="tab-list"]{background:#F3F5F8;border-radius:8px;padding:4px;gap:0;margin-bottom:20px}
.st-key-analyze [data-baseweb="tab"]{flex:1;justify-content:center;border-radius:6px;height:40px;font-weight:500}
.st-key-analyze [data-baseweb="tab"][aria-selected="true"]{background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.08)}
.st-key-analyze [data-baseweb="tab-highlight"],.st-key-analyze [data-baseweb="tab-border"]{display:none}
/* underline tabs */
.st-key-results [data-baseweb="tab-list"],.st-key-overview [data-baseweb="tab-list"]{gap:26px;margin:-14px -24px 16px;padding:0 24px;border-bottom:1px solid #E6E9EE}
[data-baseweb="tab"]{font-weight:500}
.ct{display:flex;justify-content:space-between;align-items:flex-start}.ct b{font-size:15px}.ct small{display:block;color:#657285;font-size:12.5px;margin-top:2px}
.leg{display:flex;align-items:center;gap:8px;font-size:12.5px;color:#657285}.leg i{width:9px;height:9px;border-radius:50%;background:#1565D8}
.ins{display:flex;gap:14px;background:#F3F5F8;border-top:1px solid #E6E9EE;margin:14px -24px -22px;padding:18px 24px;font-size:13.5px}
.ins svg{color:#1565D8}.ins b{display:block;font-weight:600;margin-bottom:2px}.ins span{color:#657285}.ins strong{color:#16202E}

/* readable text everywhere */
.stApp label,.stApp [data-testid="stWidgetLabel"] p,.stApp [data-testid="stWidgetLabel"]{color:#16202E!important}
[data-baseweb="select"] *,[data-baseweb="popover"] *{color:#16202E!important}
[data-baseweb="popover"] ul,[data-baseweb="menu"]{background:#fff!important}
.stTextInput input,.stTextArea textarea{color:#16202E!important;-webkit-text-fill-color:#16202E!important;background:#fff!important}
::placeholder{color:#7C8797!important;opacity:1!important;-webkit-text-fill-color:#7C8797!important}
[data-baseweb="tab"] p,[data-baseweb="tab"] span{color:#657285!important}
[data-baseweb="tab"][aria-selected="true"] p,[data-baseweb="tab"][aria-selected="true"] span{color:#1565D8!important}
.stApp [role="tab"]{color:#657285!important;background:#F7F8FA!important;font-weight:600!important;opacity:1!important}
.stApp [role="tab"] *{color:#657285!important;opacity:1!important}
.stApp [role="tab"][aria-selected="true"]{color:#1565D8!important;background:#FFFFFF!important}
.stApp [role="tab"][aria-selected="true"] *{color:#1565D8!important}
.st-key-analyze [role="tab"]{padding:0 18px!important}
.st-key-analyze [role="tab"][aria-selected="true"]{box-shadow:0 1px 3px rgba(22,32,46,.10)}
.st-key-results [role="tab"],.st-key-overview [role="tab"]{padding:10px 4px!important}
.st-key-results [role="tab"][aria-selected="true"],.st-key-overview [role="tab"][aria-selected="true"]{border-bottom:2px solid #1565D8!important}
.st-key-analyze [data-baseweb="tab"][aria-selected="true"] p{color:#16202E!important}
.stButton>button,.stDownloadButton>button{background:#fff;color:#16202E!important}
.stButton>button p,.stDownloadButton>button p{color:#16202E!important}
.stButton>button[kind="primary"],.stButton>button[kind="primary"] p{color:#fff!important}
.stButton>button[kind="primary"]{background:#1565D8!important}
.stButton>button:disabled{background:#E6E9EE!important;opacity:1}.stButton>button:disabled p{color:#7C8797!important}
[data-testid="stFileUploaderDropzone"] *{color:#16202E!important}
[data-testid="stFileUploaderDropzone"] small{color:#657285!important}
[data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] *{color:#657285!important}
.stAlert,.stAlert *{color:#16202E!important}

/* explicit backgrounds: independent of light/dark theme */
:root,.stApp{color-scheme:light}
.stApp,[data-testid="stAppViewContainer"],[data-testid="stMain"]{background:#F7F8FA!important}
section[data-testid="stSidebar"],section[data-testid="stSidebar"]>div{background:#fff!important}
.st-key-source,[data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-source),.st-key-schema,[data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-schema),.st-key-analyze,[data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-analyze),.st-key-results,[data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-results),.st-key-overview,[data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-overview){background:#fff!important}
.st-key-analyze [data-baseweb="tab-list"]{background:#F3F5F8!important;border:1px solid #E6E9EE}
.st-key-analyze [data-baseweb="tab"]{background:transparent!important}
.st-key-analyze [data-baseweb="tab"][aria-selected="true"]{background:#fff!important;border:1px solid #DDE2E9}
.st-key-analyze [data-baseweb="tab"]:hover{background:#E9EDF3!important}
[data-baseweb="tab-list"]{background:transparent}
[data-testid="stFileUploaderDropzone"]{background:#F7F8FA!important;border:1.5px dashed #B9C3D0!important}
[data-testid="stFileUploaderDropzone"] button{background:#fff!important;color:#16202E!important;border:1px solid #C9D1DC!important;border-radius:8px}
[data-testid="stFileUploaderDropzone"] button *{color:#16202E!important}
[data-baseweb="select"]>div{background:#fff!important;border:1px solid #C9D1DC!important}
.stSelectbox [data-baseweb="select"],.stSelectbox [data-baseweb="select"]>div,.stSelectbox [data-baseweb="select"] div{background:#fff!important;color:#16202E!important}
.stSelectbox [data-baseweb="select"] span,.stSelectbox [data-baseweb="select"] svg{color:#16202E!important;fill:#657285!important}
[data-testid="stDataFrame"]{background:#fff!important;color:#16202E!important;border:1px solid #E6E9EE;border-radius:8px}
.stTextInput input,.stTextArea textarea{border:1px solid #C9D1DC!important}
.stButton>button,.stDownloadButton>button{border:1px solid #C9D1DC!important}
.stButton>button[kind="primary"]{border-color:#1565D8!important}

/* consistent borders on Streamlit input controls */
.stApp [data-testid="stSelectbox"] [role="group"]{
    min-height:46px!important;
    background:#fff!important;
    border:1px solid #AAB7C7!important;
    border-radius:8px!important;
    box-shadow:inset 0 0 0 1px #AAB7C7!important;
}
.stApp [data-testid="stSelectbox"] [role="group"]:hover{
    border-color:#71839A!important;
    box-shadow:inset 0 0 0 1px #71839A!important;
}
.stApp [data-testid="stSelectbox"] [role="group"]:focus-within{
    border-color:#1565D8!important;
    box-shadow:inset 0 0 0 1px #1565D8!important;
}
.stApp [data-testid="stSelectbox"] input[role="combobox"]{
    min-height:44px!important;
    background:transparent!important;
    border:0!important;
    outline:0!important;
    box-shadow:none!important;
    color:#16202E!important;
    -webkit-text-fill-color:#16202E!important;
}
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div{
    min-height:46px!important;
    background:#fff!important;
    border:1px solid #AAB7C7!important;
    border-radius:8px!important;
    box-shadow:inset 0 0 0 1px #AAB7C7!important;
    outline:1px solid #AAB7C7!important;
    outline-offset:-1px!important;
}
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] > div:hover{
    border-color:#71839A!important;
    box-shadow:inset 0 0 0 1px #71839A!important;
    outline-color:#71839A!important;
}
.stApp [data-testid="stTextInput"] input,
.stApp [data-testid="stTextArea"] textarea{
    min-height:46px!important;
    background:#fff!important;
    border:1px solid #AAB7C7!important;
    border-radius:8px!important;
    box-shadow:inset 0 0 0 1px #AAB7C7!important;
    outline:1px solid #AAB7C7!important;
    outline-offset:-1px!important;
    color:#16202E!important;
    -webkit-text-fill-color:#16202E!important;
}
.stApp [data-testid="stTextInput"] input:focus,
.stApp [data-testid="stTextArea"] textarea:focus{
    border-color:#1565D8!important;
    box-shadow:inset 0 0 0 1px #1565D8!important;
    outline-color:#1565D8!important;
}
.stApp [data-testid="stTextInput"] input::placeholder,
.stApp [data-testid="stTextArea"] textarea::placeholder{
    color:#7C8797!important;
    -webkit-text-fill-color:#7C8797!important;
    opacity:1!important;
}
[data-baseweb="popover"] [role="option"]{background:#fff!important;color:#16202E!important}
[data-baseweb="popover"] [role="option"]:hover,[data-baseweb="popover"] [aria-selected="true"]{background:#EAF2FE!important}
.file b{color:#16202E!important}.file small{color:#657285!important}

</style>
"""


def apply_style():
    st.markdown(STYLE, unsafe_allow_html=True)
