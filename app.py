import streamlit as st
from google import genai

API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="AI Learning Buddy",page_icon="🤖",layout="wide")

st.markdown("""
<style>

.stApp{
background: linear-gradient(
135deg,
#667EEA,
#764BA2,
#A78BFA,
#C4B5FD
);
background-attachment: fixed;
}

[data-testid="stSidebar"]{

background:rgba(255,255,255,.12);

backdrop-filter:blur(20px);

border-right:1px solid rgba(255,255,255,.2);

}

.glass{

background:rgba(255,255,255,0.15);

backdrop-filter: blur(25px);

-webkit-backdrop-filter: blur(25px);

border:1px solid rgba(255,255,255,0.25);

border-radius:22px;

padding:25px;

box-shadow:
0 10px 40px rgba(0,0,0,0.25),
0 0 20px rgba(255,255,255,0.05);

transition:0.3s ease;

}

.glass:hover{

transform:translateY(-4px);

box-shadow:
0 15px 50px rgba(0,0,0,.35);

}

.hero{

background:rgba(255,255,255,.12);

backdrop-filter:blur(25px);

padding:35px;

border-radius:25px;

border:1px solid rgba(255,255,255,.2);

box-shadow:0 10px 40px rgba(0,0,0,.25);

color:white;

text-align:center;

margin-bottom:20px;

}

.chat-user{

background:#2563EB;

padding:15px;

border-radius:18px 18px 5px 18px;

color:white;

margin:10px;

margin-left:120px;

}

.chat-ai{

background:rgba(255,255,255,.25);

backdrop-filter:blur(15px);

padding:15px;

border-radius:18px 18px 18px 5px;

margin:10px;

margin-right:120px;

color:white;

}

.stButton>button{

background: linear-gradient(
90deg,
#06B6D4,
#3B82F6,
#6366F1
);

color:black;

font-weight:600;

font-size:18px;

border:none;

border-radius:14px;

height:52px;

transition:0.3s;

}

.stButton>button:hover{

transform:scale(1.03);

box-shadow:0 0 25px rgba(99,102,241,.6);

}



</style>
""",unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history=[]

st.markdown("""
<div class="hero">

<h1>🤖 AI Learning Buddy</h1>

<h3>Your Personal AI Tutor</h3>

<p>Explain • Quiz • Summary • Examples • Interview Questions</p>

</div>
""",unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Settings")
    difficulty=st.selectbox("Difficulty",["Beginner","Intermediate","Advanced"])
    st.divider()
    st.subheader("🕘 Recent Topics")
    for h in st.session_state.history[-8:]:
        st.write("•",h)

left,right=st.columns([1,1])

st.divider()

with st.expander("📖 About AI Learning Buddy", expanded=False):
    st.markdown("""
### 🤖 StudyMate AI

**Role**
- Your personal AI tutor that helps students understand topics in an easy and interactive way.

**Personality**
- Friendly 😊
- Patient 🧑‍🏫
- Encouraging 💡
- Easy-to-understand explanations 📚

**What I Can Do**
- 📖 Explain difficult concepts
- 📝 Summarize notes
- 🎯 Generate quizzes
- 💼 Prepare interview questions
- 🌍 Give real-life examples
- ✅ List advantages & disadvantages
- 🚀 Show practical applications
- 🎉 Share fun facts

**Best For**
- School students
- College students
- Beginners preparing for exams
- Self learners
""")

    with st.expander("💡 Prompt Templates", expanded=False):
        st.markdown("""
### 1️⃣ Explain a Concept
**Template**
> Explain **{Topic}** in simple terms for a **{Difficulty}** learner using headings, examples, and key points.

---

### 2️⃣ Summarize Notes
**Template**
> Summarize **{Topic}** into concise study notes with important concepts and bullet points.

---

### 3️⃣ Generate a Quiz
**Template**
> Create a quiz on **{Topic}** for a **{Difficulty}** learner with multiple-choice questions and correct answers.

---

### 4️⃣ Real-Life Example
**Template**
> Explain **{Topic}** using practical real-world examples that are easy to understand.

---

### 5️⃣ Interview Preparation
**Template**
> Generate interview questions and model answers on **{Topic}** suitable for a **{Difficulty}** learner.
""")

with left:
    st.markdown('<div class="card">',unsafe_allow_html=True)
    topic=st.text_input("📚 Topic",placeholder="e.g. Machine Learning")
    option=st.selectbox("🎯 Learning Mode",["Explanation","Summary","Real-Life Example","Quiz","Interview Questions","Advantages & Disadvantages","Applications","Fun Facts"])
    generate=st.button("✨ Generate",use_container_width=True)
    st.markdown("</div>",unsafe_allow_html=True)

def prompt(t,o,d):
    return f"You are an educational tutor. For a {d} learner, provide a well-formatted {o} about {t}. Use headings, bullet points and examples where appropriate."

with right:
    st.markdown('<div class="card">',unsafe_allow_html=True)
    st.subheader("📄 AI Response")
    if generate:
        if not topic.strip():
            st.warning("Enter a topic.")
        else:
            with st.spinner("Thinking..."):
                try:
                    r=client.models.generate_content(model="gemini-3.1-flash-lite",contents=prompt(topic,option,difficulty))
                    txt=r.text
                    st.session_state.history.append(f"{topic} - {option}")
                    st.success("Generated successfully!")
                    st.markdown(txt)
                    st.download_button("📥 Download",txt,file_name=f"{topic}.txt",mime="text/plain",use_container_width=True)
                except Exception as e:
                    st.error(str(e))
    else:
        st.info("Your generated content will appear here.")
    st.markdown("</div>",unsafe_allow_html=True)

st.markdown("---")
st.caption("🚀 Powered by Streamlit + Google Gemini 3.1 Flash-Lite")
