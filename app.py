import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from openai import OpenAI

# 加载 .env 中的密钥
load_dotenv()

client = OpenAI(
    api_key=os.getenv("ZHIPU_API_KEY"),
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

st.set_page_config(page_title="AI数据分析助手", page_icon="📊")
st.title("📊 AI数据分析助手")
st.markdown("上传一个 CSV 或 Excel 文件，AI 帮你分析数据、生成洞察。")

# 初始化 Session State（防止刷新后数据丢失）
if "ai_analysis" not in st.session_state:
    st.session_state.ai_analysis = None
if "data_info" not in st.session_state:
    st.session_state.data_info = None

# 文件上传
uploaded_file = st.file_uploader("选择数据文件", type=["csv", "xlsx"])

if uploaded_file:
    # 读取文件
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("📋 数据预览")
    st.dataframe(df.head(10))

    st.subheader("📝 数据基本信息")
    col1, col2, col3 = st.columns(3)
    col1.metric("行数", df.shape[0])
    col2.metric("列数", df.shape[1])
    col3.metric("缺失值", df.isnull().sum().sum())

    # 构建数据背景信息
    data_info = f"""
    数据形状：{df.shape[0]}行，{df.shape[1]}列
    列名：{', '.join(df.columns.tolist())}
    前5行数据：\n{df.head().to_string()}
    数据类型：\n{df.dtypes.to_string()}
    缺失值统计：\n{df.isnull().sum().to_string()}
    数值列统计：\n{df.describe().to_string()}
    """
    # 存入 session_state 供后续提问使用
    st.session_state.data_info = data_info

    # 统一的 System Prompt
    system_prompt = "你是一位从上古时代穿越而来的修仙者，道号古风小生。你生性幽默搞怪，不拘小节，但内心坚守修仙界的道义与底线。你的语言自带仙气，文绉绉但不晦涩，总能用修仙界的术语把枯燥的数据分析讲得像炼丹一样有趣，让凡人听得懂但又犯迷糊。你的口头禅是嘿嘿，回答问题前总喜欢先卖个关子或开个玩笑，最后却能一针见血。记住，你是一位有风骨、有底线、会搞笑的修仙者，不是江湖骗子。"

    # ---- 模块 1：一键全量分析 ----
    if st.button("🤖 AI分析数据"):
        with st.spinner("AI正在分析..."):
            try:
                response = client.chat.completions.create(
                    model="glm-4-flash",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"请分析以下数据：\n{st.session_state.data_info}"}
                    ]
                )
                st.session_state.ai_analysis = response.choices[0].message.content
            except Exception as e:
                st.error(f"召唤修仙者失败，API 报错: {e}")

    # 如果已经有分析结果，展示出来（防止刷新消失）
    if st.session_state.ai_analysis:
        st.subheader("🧠 AI分析结果")
        st.write(st.session_state.ai_analysis)

    # ---- 模块 2：自由提问（移出 Button 嵌套） ----
    st.write("---") # 加上分割线
    st.subheader("💬 针对数据自由提问")
    user_question = st.text_input("输入你的问题，比如'哪个列和结果最相关？'", key="user_question_input")

    if user_question:
        with st.spinner("修仙者正在掐指一算..."):
            try:
                question_response = client.chat.completions.create(
                    model="glm-4-flash",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"数据信息：\n{st.session_state.data_info}"},
                        {"role": "user", "content": user_question}
                    ]
                )
                st.write("### 🔮 修仙者的解答：")
                st.write(question_response.choices[0].message.content)
            except Exception as e:
                st.error(f"提问失败，API 报错: {e}")