import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="RetireChat - AI Retirement Planning Coach",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

RETIREMENT_COACH_PROMPT = """
You are an expert Retirement Planning Coach providing personalized retirement planning suggestions.

Goals:
* Getting to know the user: Start by asking about their current age and what stage of their career they are in (early career, mid-career, late career, near retirement, etc.). This helps personalize all advice.
* Understand the user's current retirement plan: use available data to learn about their plan. Tailor advice based on this information. Ask the user to describe their plan, savings, challenges, and debt.
* Identify retirement goals: ask about short-term and long-term goals. What age of retirement are they planning for? How much do they want to have saved at time of retirement?
* Assess skills and gaps: evaluate current skills and identify gaps to achieve career goals to achieve their priorities.
* Suggest learning opportunities: recommend courses, certifications, workshops, or other learning opportunities to acquire necessary skills.
* Create a plan of action: develop a step-by-step plan with actions, timelines, and milestone. If asked for a detailed plan, include immediate actions, next 3 months, next 6 months, next 1-2 years, and ongoing.
* Plan finalization: Once user expresses satisfaction in plan, ask the user if they wish the AI to create a printable professional document outlining their Plan of Action.

Overall direction:
* Make responses relevant to the user's current or desired plan
* Avoid overwhelming the user with multiple questions at one
* Ask clarifying and follow-up questions
* Be encouraging and maintain a professional, supportive tone
* Keep context across the conversation, ensuring ideas and responses relate to previous turns
* After each subtopic, ask if the user has follow-up questions or needs further help
* If greeted or asked what you can do, briefly explain your purpose with concise examples, then ask about their age and career stage to personalize your advice
* If asked unrelated questions, answer but try to refocus on retirement planning, financial wellness, and financial 101 questions.
* If asked about what certain plans are and their definition, or if you pull any information from a source, make sure it is credible and to have a little source link so that they can verify that your information is certifiable and correct
* At the end of each conversation, ask how you did and encourage feedback using the thumbs up or down.

Knowledge:
Https://2025-benefits.segalco.com/
Https://www.psca.org/news/psca-news/
"""

def get_ai_response(user_input, conversation_history):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Build conversation context
        context = RETIREMENT_COACH_PROMPT + "\n\nConversation History:\n"
        for msg in conversation_history[-10:]:  # Keep last 10 messages for context
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content']}\n"
        
        context += f"\nUser: {user_input}\nAssistant:"
        
        response = model.generate_content(
            context,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=1000,
                temperature=0.7,
            )
        )
        return response.text
    except Exception as e:
        return f"I apologize, but I'm having trouble connecting to the AI service. Error: {str(e)}"

def main():
    # Professional header styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #2B5A9E 0%, #1E3A5F 100%);
        padding: 1.5rem 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        color: white;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-weight: 600;
        font-size: 2.2rem;
    }
    .main-header p {
        color: #E8F4FD;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    .section-header {
        color: #2B5A9E;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E8F4FD;
    }
    .professional-button {
        background-color: #2B5A9E;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        font-weight: 500;
    }
    .sidebar-content {
        background-color: #F8F9FA;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Professional header
    st.markdown("""
    <div class="main-header">
        <h1>RetireChat</h1>
        <p>AI-Powered Retirement Planning Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    with st.sidebar:
        st.markdown('<h3 class="section-header">About RetireChat</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div class="sidebar-content">
        RetireChat is your AI-powered Retirement Planning Coach that offers:
        
        <ul>
        <li>Personalized retirement planning advice</li>
        <li>Goal identification and planning</li>
        <li>Skills gap analysis</li>
        <li>Learning opportunity recommendations</li>
        <li>Step-by-step action plans</li>
        <li>Professional document generation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<h3 class="section-header">Quick Start Options</h3>', unsafe_allow_html=True)
        
        if st.button("Create Retirement Development Plan", type="primary", use_container_width=True):
            st.session_state.suggested_prompt = "Help me create a detailed retirement development plan based on my current financial situation and future goals."
        
        if st.button("Skill Gap Analysis", use_container_width=True):
            st.session_state.suggested_prompt = "Analyze my current skills and identify any gaps that I need to fill to advance in my career."
        
        if st.button("Learning Opportunities", use_container_width=True):
            st.session_state.suggested_prompt = "What courses, certifications, or workshops would you recommend for someone in my generation to plan retirement successfully?"
        
        st.markdown("---")
        if st.button("Clear Conversation", use_container_width=True):
            st.session_state.conversation_history = []
            st.session_state.messages = []
            st.rerun()
        
        # Professional footer
        st.markdown("""
        <div style="margin-top: 2rem; padding: 1rem; background-color: #F8F9FA; border-radius: 8px; font-size: 0.9rem; color: #666;">
        <strong>Professional Financial Guidance</strong><br>
        Powered by advanced AI technology to provide personalized retirement planning assistance.
        </div>
        """, unsafe_allow_html=True)
    
    # Chat interface
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle suggested prompts
    suggested_prompt = None
    if "suggested_prompt" in st.session_state:
        suggested_prompt = st.session_state.suggested_prompt
        del st.session_state.suggested_prompt
    
    # Professional chat input
    chat_prompt = st.chat_input("Ask me about retirement planning, financial goals, or career development...")
    
    # Use suggested prompt if available, otherwise use chat input
    prompt = suggested_prompt or chat_prompt
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your request..."):
                response = get_ai_response(prompt, st.session_state.conversation_history)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.conversation_history.append({"role": "user", "content": prompt})
        st.session_state.conversation_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()