
streamlit_code = '''
import streamlit as st
from langchain_openai import ChatOpenAI
from openai import APIError

st.set_page_config(page_title="मराठी शिक्षक (Marathi Tutor)", page_icon="🇮🇳")
st.title("🇮🇳 मराठी शिक्षक (Marathi Tutor)")

tab1, tab2, tab3 = st.tabs([
    "लेखन सराव (Writing Practice)",
…            st.exception(e)
'''

with open("app.py", "w") as f:
    f.write(streamlit_code)

print("Streamlit code saved to app.py")
!cat app.py
Streamlit code saved to app.py

import streamlit as st
from langchain_openai import ChatOpenAI
from openai import APIError

st.set_page_config(page_title="मराठी शिक्षक (Marathi Tutor)", page_icon="🇮🇳")
st.title("🇮🇳 मराठी शिक्षक (Marathi Tutor)")

tab1, tab2, tab3 = st.tabs([
    "लेखन सराव (Writing Practice)",
    "व्याकरण (Fill-in-the-blanks)",
    "संभाषण सराव (Speaking Simulation)"
])

def get_model():
    openrouter_api_key = st.secrets.get("OPENROUTER_API_KEY")
    if not openrouter_api_key:
        st.error("OPENROUTER_API_KEY Streamlit सिक्रेट्समध्ये सापडले नाही.")
        st.stop()
    return ChatOpenAI(
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=openrouter_api_key,
        temperature=0.3,
        model_name="google/gemma-4-26b-a4b-it"
    )

model = get_model()

# --- Tab 1: Writing correction ---
with tab1:
    st.subheader("लेखन सराव – मजकूर दुरुस्ती")
    user_text = st.text_area(
        "तुमचा मजकूर येथे लिहा (उदा. पत्र, ईमेल, तक्रार):",
        height=150,
        key="writing_input"
    )
    if st.button("दुरुस्त करा आणि मूल्यांकन करा", key="writing_btn"):
        prompt = (
            "तुम्ही मराठी भाषेचे व्यावसायिक शिक्षक आहात. "
            "जेव्हा वापरकर्ता चुका करेल, तेव्हा त्याला दुरुस्त करा. "
            "फक्त मराठीमध्ये उत्तर द्या, सोपे मराठी शब्द वापरा, "
            "व्याकरण चुका सोप्या पद्धतीने समजावून सांगा आणि त्याच्या उत्तरांचे मूल्यांकन करा. "
            "कृपया माझा मजकूर दुरुस्त करा आणि त्याचे मूल्यांकन करा. "
            "शब्दलेखन, व्याकरण, वाक्य रचना आणि शब्दसंग्रह यावर लक्ष द्या. "
            "माझ्या चुका दाखवा आणि त्या सुधारा."
            f"
मजकूर:
{user_text}"
        )
        try:
            response = model.invoke(prompt)
            st.markdown("**अभिप्राय (Feedback):**")
            st.write(response.content)
        except APIError as e:
            st.error(f"API Error: {e}")
            st.exception(e)

# --- Tab 2: Grammar fill-in-the-blanks ---
with tab2:
    st.subheader("व्याकरण – रिकाम्या जागा भरा")
    st.write("रिकाम्या जागा भरा यावर आधारित सराव किंवा व्याकरणाचे स्पष्टीकरण (उदा. काळ, लिंग, वचन) विचारा.")
    grammar_question = st.text_input(
        "व्याकरणाचा विषय सांगा किंवा सरावासाठी मजकूर विचारा:",
        key="grammar_input"
    )
    if st.button("सराव तयार करा", key="grammar_btn"):
        prompt = (
            "तुम्ही मराठी भाषेचे शिक्षक आहात. "
            "रिकाम्या जागा भरा यावर आधारित एक छोटा मजकूर तयार करा आणि उत्तरे दाखवा. "
            "त्यानंतर रिकाम्या जागांसाठीचे व्याकरण नियम सोप्या पद्धतीने समजावून सांगा.

"
            f"सरावाचा विषय: {grammar_question}"
        )
        try:
            response = model.invoke(prompt)
            st.markdown("**सराव आणि स्पष्टीकरण:**")
            st.write(response.content)
        except APIError as e:
            st.error(f"API Error: {e}")
            st.exception(e)

# --- Tab 3: Speaking simulation ---
with tab3:
    st.subheader("संभाषण सराव – परीक्षा अनुकरण")
    st.write("संभाषण परीक्षेचे अनुकरण करा. तुमच्या उत्तरांचे मजकूर स्वरूपात लिहा.")
    speaking_prompt = st.text_input(
        "विषय किंवा परिस्थिती सांगा (उदा. मित्रासोबत सहलीचे नियोजन):",
        key="spoken_input"
    )
    if st.button("अनुकरण सुरू करा", key="speaking_btn"):
        prompt = (
            "तुम्ही संभाषण परीक्षेतील भागीदार आहात. "
            "वास्तववादी परीक्षेत सहभागी म्हणून प्रतिसाद द्या, फक्त मराठीमध्ये उत्तर द्या, "
            "सोपे मराठी शब्द वापरा. "
            "आवश्यक असल्यास दुरुस्त करा आणि मूल्यांकन करा.

"
            f"परिस्थिती: {speaking_prompt}"
        )
        try:
            response = model.invoke(prompt)
            st.markdown("**परीक्षा अनुकरण:**")
            st.write(response.content)
        except APIError as e:
            st.error(f"API Error: {e}")
            st.exception(e)
