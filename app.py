import streamlit as st
import random
import re
import html

st.set_page_config(
    page_title="TOEIC Paraphrase Trainer",
    page_icon="📝",
    layout="centered"
)

QUESTION_DATA = [
    {
        "target_word": "Anyway",
        "theme": "プロジェクトの進捗報告",
        "passage": "To: Project Team\nFrom: Sarah Jenkins\nSubject: Project Update\n\nI am writing to inform you that there has been a slight delay in the design phase due to some technical issues with our software. We are currently working with the IT department to resolve this as quickly as possible. In any case, we are still aiming to complete the prototype by the end of this month.",
        "question": "What is the team planning to do anyway despite the delay?",
        "paraphrased_word": "In any case",
        "explanation": "anyway は、本文では In any case に言い換えられています。"
    },
    {
        "target_word": "Following",
        "theme": "セミナー後の懇親会の案内",
        "passage": "The main presentation will begin at 2:00 P.M. and conclude at 4:30 P.M. After the main session, there will be a networking reception in the lobby area.",
        "question": "What will happen following the main session?",
        "paraphrased_word": "After",
        "explanation": "following は、本文では After に言い換えられています。"
    },
    {
        "target_word": "Available",
        "theme": "会議室の予約確認",
        "passage": "Room C is free between 1:00 P.M. and 3:00 P.M. if that works for your team.",
        "question": "When is the conference room available on Wednesday?",
        "paraphrased_word": "free",
        "explanation": "available は、本文では free に言い換えられています。"
    },
    {
        "target_word": "Purchase",
        "theme": "オンラインショップの確認メール",
        "passage": "You chose to buy a wireless keyboard and a noise-canceling headset.",
        "question": "What items did the customer purchase?",
        "paraphrased_word": "buy",
        "explanation": "purchase は、本文では buy に言い換えられています。"
    },
    {
        "target_word": "Register",
        "theme": "講座の申し込み",
        "passage": "To sign up for the event, please visit the staff portal and complete the online form by this Friday.",
        "question": "How can employees register for the workshop?",
        "paraphrased_word": "sign up",
        "explanation": "register は、本文では sign up に言い換えられています。"
    }
]

st.markdown("""
<style>
.stApp {
    background-color: #fcfaf7;
    color: #2d2a26;
}
.toeic-passage-box {
    background-color: #f3ede4;
    border: 2px solid #d97706;
    padding: 24px;
    border-radius: 12px;
    line-height: 1.8;
    font-size: 1.08rem;
    color: #1e1b18;
    white-space: pre-wrap;
    margin: 16px 0 20px 0;
}
.badge {
    background-color: #ea580c;
    color: white;
    padding: 8px 14px;
    border-radius: 6px;
    font-weight: bold;
    display: inline-block;
    margin-bottom: 12px;
}
.pattern-box {
    background-color: #fff7ed;
    border-left: 6px solid #ea580c;
    padding: 14px 16px;
    border-radius: 8px;
    margin: 12px 0;
}
</style>
""", unsafe_allow_html=True)


def normalize_text(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def classify_paraphrase(target_word, paraphrased_word):
    target = normalize_text(target_word)
    para = normalize_text(paraphrased_word)

    if para in ["sign up", "take part in", "carry out"]:
        return "句動詞", "動詞＋前置詞・副詞の形で言い換えられています。"

    if (target, para) in [
        ("purchase", "buy"),
        ("provide", "give"),
        ("inform", "tell")
    ]:
        return "フォーマル⇔カジュアル", "設問ではややフォーマルな語、本文では日常的な語に言い換えられています。"

    if target in ["available", "register", "purchase"] or para in ["free", "sign up", "buy"]:
        return "TOEIC頻出表現", "TOEICでよく出る基本的な言い換え表現です。"

    return "同義語", "ほぼ同じ意味を持つ語に言い換えられています。"


if "started" not in st.session_state:
    st.session_state.started = False

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0

if "total_count" not in st.session_state:
    st.session_state.total_count = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "last_result" not in st.session_state:
    st.session_state.last_result = None

if "question_id" not in st.session_state:
    st.session_state.question_id = random.randint(100000, 999999)


def choose_question():
    st.session_state.current_question = random.choice(QUESTION_DATA)
    st.session_state.answered = False
    st.session_state.last_result = None
    st.session_state.question_id = random.randint(100000, 999999)


if not st.session_state.started:
    st.title("TOEIC Paraphrase Trainer")
    st.write("TOEIC600点を目指す学習者向けの言い換え表現トレーニングです。")

    current_score = st.number_input(
        "現在のTOEICスコアを入力してください",
        min_value=0,
        max_value=990,
        value=400,
        step=10
    )

    target_score = st.selectbox(
        "目標スコアを選択してください",
        [500, 600, 730, 860],
        index=1
    )

    if st.button("学習を開始する"):
        st.session_state.current_score = current_score
        st.session_state.target_score = target_score
        st.session_state.started = True
        choose_question()
        st.rerun()

    st.stop()


if st.session_state.current_question is None:
    choose_question()

q = st.session_state.current_question

st.title("TOEIC Paraphrase Trainer")

col1, col2, col3 = st.columns(3)
col1.metric("現在スコア", f"{st.session_state.current_score}点")
col2.metric("目標スコア", f"{st.session_state.target_score}点")
col3.metric("正答数", f"{st.session_state.correct_count} / {st.session_state.total_count}")

st.markdown(
    "<div class='badge'>TOEIC600点を目指すレベル</div>",
    unsafe_allow_html=True
)

st.subheader(f"Target Word: {q['target_word']}")
st.caption(f"テーマ：{q['theme']}")

if st.session_state.current_score < 500 and not st.session_state.answered:
    first_letter = q["paraphrased_word"][0]
    st.info(
        f"ヒント：本文中に「{first_letter}」から始まる、"
        f"'{q['target_word']}' と似た意味の表現があります。"
    )

safe_passage = html.escape(q["passage"])
st.markdown(
    f"<div class='toeic-passage-box'>{safe_passage}</div>",
    unsafe_allow_html=True
)

st.write("### Question")
st.write(q["question"])

answer = st.text_input(
    "本文中の言い換え表現を入力してください",
    key=f"answer_text_{st.session_state.question_id}",
    disabled=st.session_state.answered
)

col_a, col_b, col_c = st.columns([1.2, 1.2, 1])

with col_a:
    check_clicked = st.button(
        "答え合わせ",
        disabled=st.session_state.answered
    )

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

    pattern, pattern_explanation = classify_paraphrase(
        q["target_word"],
        q["paraphrased_word"]
    )

    st.write(f"正解：**{q['paraphrased_word']}**")

    st.markdown(
        f"""
        <div class='pattern-box'>
        <strong>言い換えパターン：{html.escape(pattern)}</strong><br>
        {html.escape(pattern_explanation)}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(q["explanation"])

st.markdown("---")
st.caption("問題はランダムに表示されます。")

