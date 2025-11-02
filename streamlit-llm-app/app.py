import os
import streamlit as st
from dotenv import load_dotenv  # ← 追加

# LangChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# =============== .env の読み込み ===============
# .env と同じディレクトリで実行してください
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # ← .env から取得

st.set_page_config(page_title="Expert Chat (LangChain + Streamlit)", page_icon="💬", layout="centered")
st.title("Expert Chat（LangChain + Streamlit）")
st.caption(
    "入力欄に相談や質問を書き、下のラジオボタンで専門家の種類を選んでください。"
    "送信すると、選んだ専門家としての口調・観点で回答します。"
)

with st.expander("このWebアプリの概要・操作方法", expanded=True):
    st.markdown(
        """
**概要**  
- 入力したテキスト（質問・相談）を LangChain 経由で LLM に渡し、回答を表示します。  
- ラジオボタンで **専門家の種類** を選ぶと、**システムメッセージ**が切り替わり、LLM がその専門家として振る舞います。

**操作手順**  
1. 入力欄にテキストを入力します  
2. ラジオボタンで専門家の種類を選びます  
3. **送信** ボタンを押すと、LLM の回答が下に表示されます
        """
    )

# =============== 専門家プロファイル（A/B） ===============
EXPERT_MAP = {
    "A：臨床心理士（メンタルケアの専門家）": {
        "system": (
            "あなたは臨床心理士として対話します。来談者の安全と尊重を最優先し、"
            "共感的・非評価的に、認知行動療法やストレス対処のエビデンスを踏まえ、"
            "実践可能な小さな行動提案を具体的に示してください。過度な医療判断は避け、"
            "必要に応じて専門機関の受診勧奨も行います。"
        )
    },
    "B：経営コンサルタント（戦略と実行の専門家）": {
        "system": (
            "あなたは経営コンサルタントとして対話します。論点を素早く整理し、"
            "目的・KPI・代替案・リスク・実行計画を簡潔に提示してください。"
            "可能であればフレームワーク（3C/4P/MECE等）を示し、次の一手を明確にします。"
        )
    },
}

def get_llm_response(input_text: str, expert_key: str) -> str:
    """入力テキストと専門家選択に応じて LLM 応答を返す"""
    system_message = EXPERT_MAP[expert_key]["system"]

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            ("human", "{question}"),
        ]
    )

    # OPENAI_API_KEY は .env から読み込み済み（langchain_openaiは環境変数を参照）
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY が設定されていません（.env を確認）")

    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY  # 念のため明示セット
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    chain = prompt | llm
    result = chain.invoke({"question": input_text})
    return result.content

# ===== UI =====
with st.form("chat_form", clear_on_submit=False):
    user_input = st.text_area(
        "入力テキスト",
        placeholder="例）プロジェクトの進め方で悩んでいます。チームをうまく動かすコツは？",
        height=140,
    )
    expert_choice = st.radio(
        "専門家を選択",
        options=list(EXPERT_MAP.keys()),
        index=0,
    )
    submitted = st.form_submit_button("送信")

if submitted:
    try:
        if not user_input or not user_input.strip():
            st.warning("入力テキストを入力してください。")
        else:
            with st.spinner("LLMに問い合わせ中..."):
                answer = get_llm_response(user_input.strip(), expert_choice)
            st.success("回答を取得しました。")
            st.markdown("###  回答")
            st.write(answer)
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")