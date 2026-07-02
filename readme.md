# 📊 AI数据分析助手

一个基于 Google Gemini 大模型的数据分析网页应用，上传文件即可让 AI 帮你分析数据、生成洞察。

## 功能
- 上传 Excel 或 CSV 文件，自动读取并预览数据
- 展示数据基本信息（行数、列数、缺失值）
- AI 自动分析数据，生成洞察和建议
- 支持针对数据自由提问，AI 基于数据回答

## 技术栈
- Python
- python-dotenv（密钥管理）
- Streamlit（网页界面）
- Pandas（数据处理）
- Google Gemini API（AI 分析）

## 如何运行
1. 克隆仓库：`git clone https://github.com/wanqiu-cloud/ai_data_analyzer.git`
2. 安装依赖：`pip install -r requirements.txt`
3. 创建 `.env` 文件并配置密钥（见下方）
4. 运行应用：`streamlit run app.py`

## 环境变量配置（.env）
在项目根目录创建 `.env` 文件，填入以下内容：

GEMINI_API_KEY=你的Gemini密钥
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1/

## 项目结构
ai_data_analyzer/
├── .env              # 密钥文件（需自行创建）
├── .gitignore        # Git 忽略规则
├── app.py            # 主程序
└── requirements.txt  # 依赖清单