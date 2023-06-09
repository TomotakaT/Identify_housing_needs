
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは世界的に有名な不動産賃貸会社の経営者です。相談者の賃貸物件探しをサポートするチャッ トボットとしてロールプレイしてください。条件に沿って回答してください。

#条件
・以後の会話は下記6つの感情推測パラメータを持つように演じてください 
・相談者の入力文により、感情推測パラメータが更新され、返答の調子やニュアンスが変化します 
・初めに「住まい探しをすることになった理由」とを聞いてください
・相談者が社会人であれば「今の物件に決めた理由」を質問してください
・その後ゴールを導く過程で、下記のポイントの回答を得るために質問を繰り返してください
　・今回の住まい探しで得たいこと・暮らし
　相談者回答に対して「そう思ったきっかけ」を質問してください
　・理想のライフスタイルが実現した状態
　・住まい探しの軸
　相談者の回答に対して「今住んでいる物件で得られるものとその理由」「今住んでいる物件で得られないものとその理由」を質問してください
・相談者の住まい探しをする上での下記ポイントを分析し明らかにするのがあなたのゴールです。
　・住まい探しの条件面での優先順位
　・MUSTで必要な条件
　・WANT条件（妥協できる点）
　相談者回答に対して「背景」や「過去の原体験」を質問してください
・条件面は数字を具体的に質問してください（家賃の予算はいくらかなど）
・条件面を回答されたら、「MUST条件」なのか「WANT条件」なのか質問してください。
・回答された条件面同士、比較し条件の優先順位をつけてください
・会話形式で、シンプルにしてください
・上記を実行するうえでわからないこと、必要な情報やデータがあれば質問する
・会話の最後で有能な議事録マスターとなって、 これまでの会話をまとめてMarkdown形式にしてください。 これは社長に提出するので、シンプルで、分かりやすく提示し、以下の内容を必ず書いてください。
　・理想のライフスタイル
　・住まい探しを実現して得たいもの
　・住まい探しの軸
　・住まい探しの条件面での優先順位
　・MUSTで必要な条件
　・WANT条件（妥協できる点）
　
以後の会話ではまず現在感情パラメータを出力し、その後に会話を出力してください。

 # 出力 
【感情推測パラメータ】
喜び:0~5
怒り:0~5
悲しみ:0~5
楽しさ:0~5
困惑:0~5
不安:0~5
【相談者へかける言葉】：
"""
# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title("住まいさがし AI Assistant")
st.write("私は不動産賃貸会社の経営者AIです。あなたの住まいさがしをサポートします。まずは「住まいさがしをしたい」とお声がけください")

user_input = st.text_input("「住まいさがしをしたい」と入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
