import streamlit as st
import pandas as pd
from helper.stats import keyword_popularity, top_users, top_time, vocabulary, active_time, convo_by_users, most_active_users, run_custom_query

user = st.session_state['user']

st.sidebar.markdown("Analytics")

st.title("Analytics")
st.write("See the Reports for")

options = ["word","user", "User Activity", "Custom Query"]

element = st.selectbox("Select option", options, label_visibility="collapsed")
if element == options[0]:
    keyword = st.text_input("enter the word")

    if keyword:
        
        word_frequency = float(keyword_popularity(keyword)[0]['poplularity'])
        st.write(f"# Popularity: {word_frequency}" )

        st.write(f"# Top user with the frequency of the word '{keyword}'" )
        user_list = top_users(keyword)
        df = pd.DataFrame(user_list)
        df.set_index('user_id', inplace=True)
        st.bar_chart(df, x_label="User ID", y_label="Total Words Used")
        
        st.write(f"# Top timeframe with frequency of the word '{keyword}'" )
        time_list = top_time(keyword)
        df = pd.DataFrame(time_list)
        df.set_index('hour', inplace=True)
        st.bar_chart(df, x_label="hour", y_label=f"occurences of {keyword}")

        st.write(f"# Top user that have used the word '{keyword}'")
        user_keyword_occurrence = convo_by_users(keyword)
        data = convo_by_users(keyword)
        df = pd.DataFrame(data)
        df['occurrences'] = pd.to_numeric(df['occurrences'])
        df = df.sort_values(by='occurrences', ascending=False)
        df.set_index('user_id', inplace=True)
        # st.bar_chart(df,x_label="User Id",y_label="Occurrence")
        st.dataframe(df)


if element == options[1]:
    user = st.text_input("enter the user")

    if user:
        
        st.write(f"# Vocabulary of the user {user}")
        vocab = vocabulary(user)
        stopwords = ['the', 'and', 'is', 'of', 'to', 'a', 'in', 'it', 'i', 'you', 'for', 'or', 'id']
        limit = st.slider(label="how many words you want",min_value=0,max_value=(vocab.__len__()-len(stopwords))) 
        df = pd.DataFrame(vocab)
        df = df[~df['word'].str.lower().isin(stopwords)]
        df['occurrences'] = pd.to_numeric(df['occurrences'], errors='coerce')
        df = df.dropna()
        df = df.sort_values(by="occurrences", ascending=False)
        top_n = 10 if limit == 0 else limit
        df = df.head(top_n)
        df = df.set_index("word")
        if limit == 0:
            st.bar_chart(df, x_label="words", y_label="frequency", sort=False)
        else:
            st.bar_chart(df, x_label="words", y_label="frequency")
        
        st.write(f"# Hours in which user {user} is most active")
        data = active_time(user)
        df = pd.DataFrame(data)

        df['hour'] = df['hour'].astype(int)
        df['occurrences'] = pd.to_numeric(df['occurrences'])

        df = df.sort_values(by="hour")
        df.set_index("hour", inplace=True)
        st.bar_chart(df,x_label="hours")

if element == options[2]:
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        from_date = st.date_input("From")

    with col2:
        to_date = st.date_input("To")
    
    with col3:
        top_k = st.input("Number of outputs:")

    with col4:
        load = st.button("Load Data")

    if load and from_date and to_date:
        st.markdown("## Most active users")
        df = pd.DataFrame(most_active_users(from_date, to_date, int(top_k), activity="most"))
        st.dataframe(df)
        
        st.markdown("## Least Active users")
        df=pd.DataFrame(most_active_users(from_date, to_date, int(top_k), activity="least"))
        st.dataframe(df)

if element == options[3]:
    st.markdown("## Run your custom query on the database")
    query = st.text_area("Enter your custom Query:")
    run = st.button("Run Query")

    if run and query:
        df = pd.DataFrame(run_custom_query(query))
        st.markdown("## Output:")
        st.dataframe(df)