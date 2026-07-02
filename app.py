import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
from openai import OpenAI

# 加载密钥
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = os.getenv("GEMINI_BASE_URL")

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

st.set_page_config(page_title="AI数据分析助手", page_icon="📊")
st.title("📊 AI数据分析助手")
st.markdown("上传一个 CSV 或 Excel 文件，AI 帮你分析数据、生成洞察。")

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

    # AI分析
    if st.button("🤖 AI分析数据"):
        with st.spinner("AI正在分析..."):
            data_info = f"""
            数据形状：{df.shape[0]}行，{df.shape[1]}列
            列名：{', '.join(df.columns.tolist())}
            前5行数据：\n{df.head().to_string()}
            数据类型：\n{df.dtypes.to_string()}
            缺失值统计：\n{df.isnull().sum().to_string()}
            数值列统计：\n{df.describe().to_string()}
            """

            response = client.chat.completions.create(
                model="gemini-2.5-flash",
                messages=[
                    {"role": "system", "content": "你是一个数据分析专家。请用中文分析数据，先给出整体结论，再列出关键发现，最后给出3条具体建议。格式清晰，重点突出。"},
                    {"role": "user", "content": f"请分析以下数据：\n{data_info}"}
                ]
            )

            ai_result = response.choices[0].message.content

            st.subheader("🧠 AI分析结果")
            st.write(ai_result)

            # 自由提问
            st.subheader("💬 针对数据自由提问")
            user_question = st.text_input("输入你的问题，比如'哪个列和结果最相关？'")

            if user_question:
                with st.spinner("AI思考中..."):
                    question_response = client.chat.completions.create(
                        model="gemini-2.5-flash",
                        messages=[
                            {"role": "system", "content": "你是一个数据分析专家。请基于之前分析的数据回答用户的问题。"},
                            {"role": "user", "content": f"数据信息：\n{data_info}"},
                            {"role": "user", "content": user_question}
                        ]
                    )
                    st.write(question_response.choices[0].message.content)