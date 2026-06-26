# 載入需要的套件
import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="個人 AI 投資情報站", page_icon="📈", layout="wide")

st.title("📈 我的專屬 AI 投資情報站")
st.markdown("透過 Python 與 Gemini API，自動聯網搜尋並分析每日市場動態。")

with st.sidebar:
    st.header("⚙️ 系統設定")
    # 使用密碼格式隱藏 API Key
    api_key = st.text_input("請輸入你的 Gemini API Key:", type="password")
    st.markdown("[點此免費獲取 API Key](https://aistudio.google.com/)")

# 這裡就是我們賦予 AI 靈魂的地方
system_instruction = """
你是一位精通美股基本面與總體經濟的資深投資策略師。
請根據使用者要求的日期與關注標的，利用你的網路搜尋能力去抓取最新資訊。

輸出格式必須包含三個 Markdown 區塊：
1.  總體經濟與大盤 (VTI) 衝擊
2.  核心板塊基本面追蹤 (請針對使用者關注的標的提供具體新聞與分析)
3.  關注的標的EPS與相關估值指標
4.  政要動態與異常交易 (搜尋是否有相關國會議員持股異動或重大政策發言)

請保持客觀、專業、數據導向的語氣。
"""

# 預設關注的標的
default_targets = "NVDA , PLTR , ORCL , VTI"

with st.form("analysis_form"):
    st.write("### 📝 設定今日分析條件")
    targets = st.text_input("關注的標的或產業：", value=default_targets)
    
    # 送出按鈕
    submitted = st.form_submit_button("🚀 開始聯網搜尋與分析")

if submitted:
    if not api_key:
        st.error("請先在左側輸入 Gemini API Key！")
    else:
        # 在畫面上顯示讀取中的動畫
        with st.spinner("AI 正在聯網搜尋各方新聞與財報資料，請稍候約 10-20 秒..."):
            try:
                # 1. 初始化 Gemini 客戶端
                client = genai.Client(api_key=api_key)
                
                # 2. 組合我們想問的問題
                prompt = f"請搜尋今天最新的市場資訊，並針對以下標的進行深度分析：{targets}"
                
                # 3. 呼叫 Gemini API (開啟 Google 搜尋功能)
                response = client.models.generate_content(
                    model='gemini-2.5-flash', # 使用快速且支援搜尋的模型
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        # 這裡最關鍵：開啟 Google Search 工具，讓 AI 有能力上網！
                        tools=[{"google_search": {}}],
                        temperature=0.3 # 溫度調低，讓回答更客觀理性
                    )
                )
                
                # 4. 將 AI 的回答顯示在網頁上
                st.success("✅ 分析完成！")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                # 捕捉並顯示錯誤
                st.error(f"發生錯誤：{e}")
