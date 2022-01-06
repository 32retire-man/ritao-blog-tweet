import pandas as pd
import streamlit as st
import plotly.express as px

st.title('リタおの日時別ツイート分析')

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
df_time = tweet_df.set_index('時間')

year_list = tweet_df["時間"].dt.strftime('%m月%d日%H時%M分')
option_year = st.selectbox('時間', (year_list))

st.text('【ツイートのURL】')
url = tweet_df[(tweet_df['時間'].dt.strftime('%m月%d日%H時%M分') == option_year)]["ツイートの固定リンク"].iloc[0]
st.markdown(url, unsafe_allow_html=True)

st.text('【ツイート本文】')
txt = tweet_df[(tweet_df['時間'].dt.strftime('%m月%d日%H時%M分') == option_year)]["ツイート本文"].iloc[0]
st.write(txt)

imp = tweet_df[(tweet_df['時間'].dt.strftime('%m月%d日%H時%M分') == option_year)]["インプレッション"].iloc[0]
click = tweet_df[(tweet_df['時間'].dt.strftime('%m月%d日%H時%M分') == option_year)]["URLクリック数"].iloc[0]
good = tweet_df[(tweet_df['時間'].dt.strftime('%m月%d日%H時%M分') == option_year)]["いいね"].iloc[0]

st.text('【インプレッション(Twitterが見られた回数)】')
st.subheader(imp)
st.text('【URLクリック数(Twitterからブログ記事をクリックした回数)】')
st.subheader(click)
st.text('【いいね】')
st.subheader(good)
time_array = tweet_df.iloc[:,3]

fig = px.bar(tweet_df, x=[tweet_df['インプレッション'], tweet_df['URLクリック数'], tweet_df['いいね']], y=tweet_df["時間"], range_x=[0,800], orientation='h', width=800, height=3000)
fig.update_layout(
    yaxis = dict(
        tickmode = 'array',
        tickvals = time_array
    ),
    yaxis_tickformat = '%m月%d日%H時'
)
st.plotly_chart(fig)

st.text('出典：Twitterアナリティクス')
st.text('本結果はTwitterアナリティクスのデータを加工して作成')
