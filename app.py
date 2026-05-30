import streamlit as st
import pandas as pd
from datetime import datetime
import os
import requests

file_name = "客戶資料.xlsx"
CHANNEL_ACCESS_TOKEN = "PPyeoC/nW8ClZRBUsSbbVyAiXlFvBRp8McEYp3NxLpoG9MrONrYOr7m3d74koKYUoGdz7okw50mQL9BCNQ3Ngu3iyJq2sKbHynG89uQ/PbWm3M4Qn5jSLIuUvtOdm2ZJIc3MgC6vaXNd6EbidAbbiwdB04t89/1O/w1cDnyilFU="
USER_ID = "U05b51b528fc8e762de5537a63ac92aaf"

def send_line_message(text):
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "to": USER_ID,
        "messages": [
            {
                "type": "text",
                "text": text
            }
        ]
    }

    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers=headers,
        json=data
    )
st.title("SAP油壓美睫(AI預約)")
page = st.selectbox(
    "選擇頁面",
    ["客人頁面", "老闆頁面"]
)
if page == "客人頁面":

    industry = st.selectbox(
        "選擇服務",
        ["美容店", "美甲", "美睫", "油壓按摩"]
    )
    name = st.text_input("客戶姓名")
    phone = st.text_input("客戶電話")

    booking_date = st.date_input("預約日期")
    booking_time = st.time_input("預約時間")

    question = st.text_input("請輸入客人的問題")
    answer = ""
     if os.path.exists(file_name):
        old_df = pd.read_excel(file_name)
    else:
        old_df = pd.DataFrame()

    if st.button("送出"):

        if not old_df.empty:
        same_time = old_df[
            (old_df["預約日期"].astype(str) == str(booking_date))
            &
            (old_df["預約時間"].astype(str) == str(booking_time))
        ]

            if len(same_time) > 0:
            st.error("這個時間已經有人預約")
            st.stop()

        if name == "":
            st.error("請輸入客戶姓名")
            st.stop()

        if phone == "":
            st.error("請輸入客戶電話")
            st.stop()

        if question == "":
            st.error("請輸入客人的問題")
            st.stop()

        customer_level = "⭐ 普通客戶"
        deal_rate = "30%"
        action_suggestion = "先觀察客戶需求，可以用 LINE 或電話簡單追蹤。"

        if "預約" in question or "明天" in question or "今天" in question or "看房" in question or "電話" in question:
            customer_level = "🔥 高意願客戶"
            deal_rate = "90%"
            action_suggestion = "建議 5 分鐘內聯絡客戶，優先安排預約。"

        elif "價格" in question or "多少錢" in question or "費用" in question:
            customer_level = "💰 價格詢問客戶"
            deal_rate = "60%"
            action_suggestion = "建議提供方案價格，並引導客戶預約時間。"
            answer = "請輸入問題"
        if industry in ["美容店", "美甲", "美睫", "油壓按摩"]:

            if "美甲" in question:
                answer = "我們提供美甲服務，請私訊款式照片，我們會提供報價。"

            elif "美睫" in question or "睫毛" in question or "補睫毛" in question:
                answer = "我們提供自然款、濃密款等美睫服務，歡迎預約諮詢。"

            elif "油壓" in question or "按摩" in question:
                answer = "油壓按摩採預約制，請提供想預約的日期與時間。"

            elif "價格" in question or "多少錢" in question:
                answer = "價格依服務項目不同而有所差異，請告訴我們想做的項目。"

            elif "預約" in question:
                answer = "請提供姓名、電話、日期與時間，我們會協助安排預約。"

            else:
                answer = "您好，我們提供美甲、美睫與油壓按摩服務，歡迎詢問。"
        elif industry == "搬家公司":
            if "價格" in question:
                answer = "搬家費用會依距離、樓層、物品數量計算。"
            elif "估價" in question:
                answer = "可以傳照片給我們，我們會協助初步估價。"
            elif "預約" in question:
                answer = "請提供搬家日期、出發地、目的地和是否有電梯。"
            else:
                answer = "您好，請提供搬家資訊，我們會協助報價。"

        elif industry == "水電行":
            if "價格" in question:
                answer = "水電維修價格會依問題狀況不同，基本檢修費用約800元起。"
            elif "漏水" in question:
                answer = "請先關閉水源，並拍照傳給我們判斷狀況。"
            elif "到府" in question:
                answer = "我們有提供到府維修服務，請提供地址與問題照片。"
            else:
                answer = "您好，請描述水電問題，我們會協助安排維修。"

        elif industry == "餐廳":
            if "營業" in question:
                answer = "我們營業時間是上午11點到晚上9點。"
            elif "訂位" in question:
                answer = "可以私訊訂位，請提供日期、時間、人數和姓名。"
            elif "菜單" in question:
                answer = "可以私訊我們索取最新菜單。"
            else:
                answer = "您好，歡迎詢問訂位、菜單或營業時間。"

        elif industry == "房仲":
            if "租金" in question or "價格" in question:
                answer = "房屋價格會依地點、坪數、屋況不同，請提供需求。"
            elif "看房" in question:
                answer = "可以預約看房，請提供方便的日期和時間。"
            elif "地點" in question:
                answer = "請告訴我們想找的區域，我們會推薦適合物件。"
            else:
                answer = "您好，請提供預算、地點、房型需求，我們協助配對。"

        st.write("客戶資料")
        st.write("姓名", name)
        st.write("電話", phone)
        st.write("已收到客戶資料")

        new_data = {
                "時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "行業": industry,
                "客戶等級": customer_level,
                "姓名": name,
                "電話": str(phone),
                "預約日期": booking_date,
                "預約時間": booking_time,
                "問題": question,
                "AI回答": answer
            }

        file_name = "客戶資料.xlsx"

        if os.path.exists(file_name):
            old_data = pd.read_excel(file_name)
            df = pd.concat([old_data, pd.DataFrame([new_data])], ignore_index=True)
        else:
            df = pd.DataFrame([new_data])
            
        df.to_excel(file_name, index=False)
        today = datetime.now().strftime("%Y-%m-%d")
        st.success("客戶資料已自動保存 Excel")
        line_message = f"""
        📢 新客戶預約

        姓名：{name}
        電話：{phone}
        服務：{industry}
        日期：{booking_date}
        時間：{booking_time}

        問題：{question}

        AI回答：{answer}
        """

        send_line_message(line_message)

        st.write("AI回答 : ")
        st.write(answer)

    file_name = "客戶資料.xlsx"

if os.path.exists(file_name):
    dashboard_df = pd.read_excel(file_name)
else:
    dashboard_df = pd.DataFrame(columns=[
        "時間", "行業", "客戶等級", "姓名", "電話",
        "預約日期", "預約時間", "問題", "AI回答"
    ])
    dashboard_df = dashboard_df.sort_values("時間", ascending=False)
    today_count = len(dashboard_df)

    high_count = len(
        dashboard_df[
            dashboard_df["客戶等級"].astype(str).str.contains("高意願", na=False)
        ]
    )

    price_count = len(
        dashboard_df[
            dashboard_df["客戶等級"].astype(str).str.contains("價格", na=False)
        ]
    )
if page == "老闆頁面":
    password = st.text_input("請輸入老闆密碼", type="password")

    if password != "1234":
        st.warning("請輸入正確密碼")
        st.stop()
    st.title("📊 老闆管理系統")

    file_name = "客戶資料.xlsx"
    if os.path.exists(file_name):
        dashboard_df = pd.read_excel(file_name)
    else:
        dashboard_df = pd.DataFrame(columns=[
            "時間", "行業", "客戶等級", "姓名", "電話",
            "預約日期", "預約時間", "問題", "AI回答"
            ])
    today_count = len(dashboard_df)
    high_count = len(
        dashboard_df[
            dashboard_df["客戶等級"].astype(str).str.contains("高意願", na=False)
        ]
    )

    price_count = len(
        dashboard_df[
            dashboard_df["客戶等級"].astype(str).str.contains("價格", na=False)
        ]
     )

    st.metric("今日客戶", today_count)
    st.metric("高意願客戶", high_count)
    st.metric("價格詢問", price_count)
    
    dashboard_df["排序時間"] = pd.to_datetime(
        dashboard_df["預約日期"].astype(str) + " " + dashboard_df["預約時間"].astype(str),
        errors="coerce"
    )

    dashboard_df = dashboard_df.sort_values("排序時間", ascending=True)

    dashboard_df = dashboard_df.drop(columns=["排序時間"])

    dashboard_df["電話"] = dashboard_df["電話"].astype(str)

    st.subheader("預約名單")

    st.dataframe(dashboard_df)
