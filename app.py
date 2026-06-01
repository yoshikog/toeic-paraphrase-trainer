import base64
import html
import json
import random
import re
import zlib

import streamlit as st


st.set_page_config(
    page_title="TOEIC Paraphrase Trainer",
    page_icon="📝",
    layout="centered",
)

# 読み取れた問題データ87問を圧縮して埋め込んでいます。
# 通常はこのまま使えます。
DATA_B64 = """
eNqkvWu3FGW2LvhXsupUDb6sRaNV7l1lf9hDQUuqtXQItT27+0OPyMxYK0MiM3JHRK5lVo8eY13kJiAqgoWogKByUUDxglz/Sy9y
XT6dv9DzmZf3fSMzEpQa45zaCJlvREbM+3zmM/+v/+e3ZZTPx+X/vZjl7d8++9vnesPFaPjbmd+Wnbgb01+srX60tvrN2sqttZWv
1laur60eWlu+trX03fqxj0bnvh29/w3Pru3q9Wf9++Wdu/Oljd25v5+/W6dvVWL0YD5xXw2k9fFhdnlZb+frM27FY2x2vF/fuZ/48
778fmP738/3z8ue//c1/3z7rZ/f5tf3x2+96cZh2+9vF+w9PL+bdn2awGmbURSttkF5zbdP6u+mrpdv6jfjkct8u+hZQeadDJSNJ
6yo2UpenL+W3swHLOvCgsnMynTP/r3/VN2s+V7Z/59/SZZ+9vp6/7xZ9P+yvRz53mf+P58iEDzaFjRCpqRHOVPaLTw7uqxzma1f
JMHPvkw/5c4nB0OY9nzysnLZ/OakZ+OeFn9Mb4Ouz1eb8XiuTExD3FKg/WeoQS3MivI/2z1uPmdv3w5/KoGc7HZvfP5tfL3z4/f
7t//PD1288fnM3XP0PC//C3L369n5yP6Y9enpYzIZuFltuWHP38un//z1S1D/s7tcezs/4r+BLvGweIO/5b/9+PH2J5E/Oj35z9sP
Q3JJuOHzXd83T2HeKcuMAeDI859Hz++KKn4/H5+/gv/358on8f/w90eeHfvLX5+8+bqeF39/8rQ9H9AdNgeNFeH9Ei8Jx1iSSUvH0
ETeY+yCpfoLf4//fBaP5ol3NZBFm49kg9gU/Lr8fIeCDu7nf7j35er4VXDZPxbLTd83wHeFzAVyAitqjSiaKA2OXDApJkWWvNS
HNdEfOA6v1d6un4Wg55NqtF0HH+P5s8jAq2uo2HVufh5eLt5+Of8x+2r/eXPfvef4vfPFgu+S0T3vT3X2no8lnaftX0vb37Lx
58Nbe2a/jo5C3ti2ZZ5OnWhwnwHCCVdG5+FgQ4ePIGKP+ivh0eUdcyE/qJgvEViYB+5hH/c21Npb3q4w9uQTIN6uPhl/gOmQV
WaJmAA+2QTmq20hhxOTeXWp/fmn/54Jlx+uXEJyv/l+k5Mpns0xhJ9iDzZat52O8qXLjRTGb9m9LZK35aJxJszQPD5hYK+t0OI
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
fXzJXw6F4rmYqbm5uTn+J1mxNrc=
"""

QUESTION_DATA = json.loads(
    zlib.decompress(base64.b64decode(DATA_B64)).decode("utf-8")
)


st.markdown("""
<style>
.stApp {
    background-color: #fcfaf7;
    color: #2d2a26;
}
.main-title {
    color: #c2410c;
    font-weight: 800;
}
.toeic-passage-box {
    background-color: #f3ede4;
    border: 2px solid #d97706;
    padding: 24px;
    border-radius: 12px;
    line-height: 1.9;
    font-size: 1.08rem;
    color: #1e1b18;
    white-space: pre-wrap;
    margin: 16px 0 20px 0;
    box-shadow: 0 4px 18px rgba(180, 160, 140, 0.18);
}
.badge {
    background-color: #ea580c;
    color: white;
    padding: 8px 14px;
    border-radius: 6px;
    font-weight: bold;
    display: inline-block;
    margin: 6px 0 12px 0;
}
.pattern-box {
    background-color: #fff7ed;
    border-left: 6px solid #ea580c;
    padding: 14px 16px;
    border-radius: 8px;
    margin: 12px 0;
}
.small-note {
    color: #6b5b4b;
    font-size: 0.92rem;
}
</style>
""", unsafe_allow_html=True)


PHRASAL_VERBS = {
    "sign up", "take part in", "carry out", "set up", "look for",
    "find out", "go over", "turn down", "pick up", "drop off",
    "reach out", "follow up", "check out", "work out", "stand out to",
}

BUSINESS_WORDS = {
    "invoice", "shipment", "department", "division", "policy", "guidelines",
    "procedure", "warranty", "guarantee", "conference", "convention", "budget",
    "authorize", "reimbursement", "deadline", "due date", "vendor", "supplier",
    "representative", "packaging", "property", "extension", "merchandise",
    "assistance", "laboratory", "lease payment", "local office", "market launch",
    "staffing division", "publications supervisor", "internal message",
}

FORMAL_CASUAL_PAIRS = {
    ("purchase", "buy"),
    ("inform", "tell"),
    ("notify", "tell"),
    ("provide", "give"),
    ("provide", "give us your feedback"),
    ("assist", "help"),
    ("assistance", "help"),
    ("require", "need"),
    ("obtain", "get"),
    ("commence", "start"),
    ("terminate", "end"),
    ("approximately", "about"),
    ("inquire", "ask"),
    ("reserve", "book"),
}


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def classify_paraphrase(target_word: str, paraphrased_word: str):
    target = normalize_text(target_word)
    para = normalize_text(paraphrased_word)

    if para in {normalize_text(x) for x in PHRASAL_VERBS}:
        return (
            "句動詞",
            "動詞＋前置詞・副詞の形で言い換えられています。TOEICでは、設問の1語が本文では句動詞になることがあります。",
        )

    if (target, para) in {(normalize_text(a), normalize_text(b)) for a, b in FORMAL_CASUAL_PAIRS}:
        return (
            "フォーマル⇔カジュアル",
            "設問ではややフォーマルな語、本文では日常的でやさしい語に言い換えられています。",
        )

    if target in {normalize_text(x) for x in BUSINESS_WORDS} or para in {normalize_text(x) for x in BUSINESS_WORDS}:
        return (
            "ビジネス表現",
            "会社・会議・請求・規定・配送など、TOEICのビジネス文書でよく使われる表現です。",
        )

    return (
        "同義語",
        "ほぼ同じ意味を持つ語に言い換えられています。TOEICでは、設問と本文で同じ語が使われないことが多いです。",
    )


def init_state():
    defaults = {
        "started": False,
        "current_score": 400,
        "target_score": 600,
        "correct_count": 0,
        "total_count": 0,
        "answered": False,
        "last_result": None,
        "current_question": None,
        "seen_indices": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def choose_question():
    if len(st.session_state.seen_indices) >= len(QUESTION_DATA):
        st.session_state.seen_indices = []

    available = [i for i in range(len(QUESTION_DATA)) if i not in st.session_state.seen_indices]
    idx = random.choice(available)
    st.session_state.seen_indices.append(idx)
    st.session_state.current_question = QUESTION_DATA[idx]
    st.session_state.answered = False
    st.session_state.last_result = None
    st.session_state.answer_text = ""


init_state()


if not st.session_state.started:
    st.markdown("<h1 class='main-title'>TOEIC Paraphrase Trainer</h1>", unsafe_allow_html=True)
    st.write("TOEIC600点を目指す学習者向けの、言い換え表現を探すトレーニングです。")
    st.markdown(f"<p class='small-note'>現在利用できる問題数：{len(QUESTION_DATA)}問</p>", unsafe_allow_html=True)

    current_score = st.number_input(
        "現在のTOEICスコアを入力してください",
        min_value=0,
        max_value=990,
        value=400,
        step=10,
    )

    target_score = st.selectbox(
        "目標スコアを選択してください",
        [500, 600, 730, 860],
        index=1,
    )

    if st.button("学習を開始する", type="primary"):
        st.session_state.current_score = current_score
        st.session_state.target_score = target_score
        st.session_state.started = True
        st.session_state.correct_count = 0
        st.session_state.total_count = 0
        st.session_state.seen_indices = []
        choose_question()
        st.rerun()

    st.stop()


if st.session_state.current_question is None:
    choose_question()

q = st.session_state.current_question

st.markdown("<h1 class='main-title'>TOEIC Paraphrase Trainer</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
col1.metric("現在スコア", f"{st.session_state.current_score}点")
col2.metric("目標スコア", f"{st.session_state.target_score}点")
col3.metric("正答数", f"{st.session_state.correct_count} / {st.session_state.total_count}")

st.markdown("<div class='badge'>TOEIC600点を目指すレベル</div>", unsafe_allow_html=True)

st.subheader(f"Target Word: {q['target_word']}")
st.caption(f"テーマ：{q.get('theme', 'No theme')}")

if st.session_state.current_score < 500 and not st.session_state.answered:
    first_letter = q["paraphrased_word"][0]
    st.info(
        f"ヒント：本文中に「{first_letter}」から始まる、「{q['target_word']}」と似た意味の表現があります。"
    )

safe_passage = html.escape(q["passage"])
st.markdown(f"<div class='toeic-passage-box'>{safe_passage}</div>", unsafe_allow_html=True)

st.write("### Question")
st.write(q["question"])

answer = st.text_input(
    "本文中の言い換え表現を入力してください",
    key="answer_text",
    disabled=st.session_state.answered,
)

col_a, col_b, col_c = st.columns([1.2, 1.2, 1])

with col_a:
    check_clicked = st.button("答え合わせ", disabled=st.session_state.answered, type="primary")

with col_b:
    next_clicked = st.button("次の問題へ")

with col_c:
    reset_clicked = st.button("最初に戻る")

if check_clicked:
    if not answer.strip():
        st.warning("解答を入力してください。")
    else:
        st.session_state.total_count += 1
        correct_answer = normalize_text(q["paraphrased_word"])
        user_answer = normalize_text(answer)
        is_correct = user_answer == correct_answer

        if is_correct:
            st.session_state.correct_count += 1

        st.session_state.answered = True
        st.session_state.last_result = is_correct
        st.rerun()

if next_clicked:
    choose_question()
    st.rerun()

if reset_clicked:
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

if st.session_state.answered:
    if st.session_state.last_result:
        st.success("正解です！")
    else:
        st.error("不正解です。")

    pattern, pattern_explanation = classify_paraphrase(q["target_word"], q["paraphrased_word"])

    st.write(f"正解：**{q['paraphrased_word']}**")
    st.markdown(
        f"""
        <div class='pattern-box'>
        <strong>言い換えパターン：{html.escape(pattern)}</strong><br>
        {html.escape(pattern_explanation)}
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info(q["explanation"])

st.markdown("---")
st.caption("問題はランダムに表示されます。全問が一巡すると、再びランダム出題されます。")
