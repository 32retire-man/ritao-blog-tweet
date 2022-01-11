import pandas as pd
import streamlit as st
import plotly.express as px

st.title('【ツイグラフ】')
st.header('Twitterデータ分析用グラフ化ツール')

november_df = pd.read_csv('./csv_data/tweet.csv')

utctime_df = pd.to_datetime(november_df['時間'], utc=True)
jtime_df = utctime_df.dt.tz_convert('Asia/Tokyo')
november_df['時間'] = jtime_df
time_df = november_df.sort_values(by='時間')

option_check = st.checkbox("ブログ投稿記事のみ")
if option_check == True:
  tweet_df = time_df[time_df['ツイート本文'].str.contains('#ブログ')]
else:
  tweet_df = time_df

index_list = tweet_df["時間"].dt.strftime('%m月%d日%H時%M分')
option_index = st.selectbox('ツイート投稿時間', (index_list))

st.text('【ツイートのURL】')
url = tweet_df[(tweet_df['時間'].dt.strftime('%m月%d日%H時%M分') == option_index)]["ツイートの固定リンク"].iloc[0]
st.markdown(url, unsafe_allow_html=True)

st.text('【ツイート本文】')
txt = tweet_df[(tweet_df['時間'].dt.strftime('%m月%d日%H時%M分') == option_index)]["ツイート本文"].iloc[0]
st.write(txt)

imp = tweet_df[(tweet_df['時間'].dt.strftime('%m月%d日%H時%M分') == option_index)]["インプレッション"].iloc[0]
click = tweet_df[(tweet_df['時間'].dt.strftime('%m月%d日%H時%M分') == option_index)]["URLクリック数"].iloc[0]
good = tweet_df[(tweet_df['時間'].dt.strftime('%m月%d日%H時%M分') == option_index)]["いいね"].iloc[0]

st.text('【インプレッション(Twitterが見られた回数)】')
st.subheader(imp)
st.text('【URLクリック数(Twitterからブログ記事をクリックした回数)】')
st.subheader(click)
st.text('【いいね】')
st.subheader(good)
time_array = tweet_df["時間"].dt.strftime('%m月%d日%H時%M分')

fig = px.bar(tweet_df, x=[tweet_df['インプレッション'], tweet_df['URLクリック数'], tweet_df['いいね']], y=tweet_df.index, orientation='h', width=800, height=3000)
fig.update_layout(
    yaxis = dict(
      title = 'ツイート投稿時間',
      tickmode = 'array',
      tickvals = tweet_df.index,
      ticktext = time_array
    ),
    yaxis_tickformat = '%m月%d日%H時'
)
st.plotly_chart(fig)

st.text('出典：Twitterアナリティクス')
st.text('本結果はTwitterアナリティクスのデータを加工して作成')
