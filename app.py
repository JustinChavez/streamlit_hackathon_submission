import streamlit as st

from connection import CongressDotGov

st.title("Congress.gov API")
st.markdown("[Documentation](https://github.com/LibraryOfCongress/api.congress.gov/)")
st.write("To start, try out some of these eventID for the house chamber: 116282, 116281")
col1, col2, col3 = st.columns(3)
with col1:
    congress = st.text_input("Congress", help="The congress during which the committee meeting took place. For example, the current congress is 118.", placeholder=118)

with col2:
    chamber = st.text_input("Chamber", help="The chamber name. Value can be house, senate, or nochamber.", placeholder="house")

with col3:
    eventID = st.text_input("eventID", help="The event identifier. For example, the value can be 115538.", placeholder=116282)
with st.expander("Enter your own API Key (Optional)"):
    api_key = st.text_input("api_key (Optional)", type="password")

if st.button("Submit"):
    if api_key:
        conn = st.experimental_connection("congress_dot_gov", type=CongressDotGov, api_key=api_key)
    else:
        conn = st.experimental_connection("congress_dot_gov", type=CongressDotGov)
    event_info = conn.get_committee_meetings_by_congress_chamber_event(congress=congress, chamber=chamber, eventID=eventID)
    if "committeeMeeting" in event_info:
        st.title(event_info["committeeMeeting"]["title"])
    else:
        st.write(event_info)
    if eventID == "116282":
        st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXdxMHpqaXV6eDY3dWo2cWc4ZHZ1eHJnejFma3h2M3p6cjdqd2lodCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/NDJWGU4n74di0/giphy.gif", width=200)
    with st.expander("See entire event information"):
        st.write(event_info)