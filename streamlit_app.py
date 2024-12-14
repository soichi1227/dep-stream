import streamlit as st
import requests
from datetime import datetime, timedelta

# Flask APIのURL
FLASK_API_URL = "http://localhost:5000/sales/register_deal"
# Next.jsのURL（Next.jsがホストされるURLに変更してください）
NEXTJS_BASE_URL = "http://localhost:3000"

# Main layout
st.markdown(
    """
    <style>
    .title {
        color: rgb(145, 198, 222); /* Adjusted to match the 'Tech' color */
        font-size: 36px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title with the new color
st.markdown('<div class="title">IT Trip Navigator</div>', unsafe_allow_html=True)

# フォーム入力
with st.form("deal_form"):
    company_name = st.text_input("企業名", placeholder="例: 株式会社サンプル")
    contact_name = st.text_input("担当者名", placeholder="例: 田中 太郎")
    contact_email = st.text_input("担当者メールアドレス", placeholder="例: tanaka@example.com")
    department = st.text_input("部署名（任意）", placeholder="例: 営業部")
    role_name = st.text_input("役職名（任意）", placeholder="例: 部長")
    sales_rep_name = st.text_input("営業担当者名", placeholder="例: 山田 花子")
    sales_rep_email = st.text_input("営業担当者メールアドレス", placeholder="例: yamada@example.com")
    industry = st.selectbox("業種", ["製造業", "流通・小売業", "建設不動産", "物流・運輸業", "エネルギー資源", "観光サービス", "メディア・エンタメ"])
    revenue = st.selectbox("売上規模", ["-50億円", "50億円~100億円", "100億円～1000億円", "1000億円～5000億円", "5000億~"])
    meeting_type = st.radio("商談形式", ["WEB商談", "対面商談"])
    duration = st.radio("所要時間（分）", [30, 60])

    st.subheader("商談候補日時")
    meeting_times = []
    for i in range(1, 6):
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input(f"商談候補日 {i}", key=f"date_{i}")
        with col2:
            time = st.time_input(f"商談候補時刻 {i}", key=f"time_{i}")
        if date and time:
            meeting_times.append(f"{date} {time}")

    # フォーム送信ボタン
    if st.form_submit_button("登録"):
        if not (company_name and contact_name and contact_email and sales_rep_name and sales_rep_email and meeting_times):
            st.error("必須項目をすべて入力してください。")
        else:
            # APIリクエスト
            payload = {
                "company_name": company_name,
                "contact_name": contact_name,
                "contact_email": contact_email,
                "department": department,
                "role_name": role_name,
                "sales_rep_name": sales_rep_name,
                "sales_rep_email": sales_rep_email,
                "industry": industry,
                "revenue": revenue,
                "meeting_type": meeting_type,
                "duration": duration,
                "dates": meeting_times
            }
            response = requests.post(FLASK_API_URL, json=payload)

            if response.status_code == 200:
                result = response.json()
                link = result.get("link")  # Flaskから返されるリンクを取得
                data = result.get("data")
                print(data)
                
                if link:
                    st.success("商談情報が登録されました！")
                    st.write(f"生成されたリンク: {link}")  # 単にリンクを表示
                else:
                    st.error("Flaskサーバーからのリンクが見つかりませんでした。")
            else:
                st.error(f"エラー: {response.json().get('error', '原因不明のエラーです')}")
