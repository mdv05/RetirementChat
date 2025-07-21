import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="RetireChat - AI Retirement Planning Coach",
    page_icon="💰",
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
    st.title("💰 RetireChat - AI Retirement Planning Coach")
    st.markdown("---")
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    with st.sidebar:
        st.header("About RetireChat")
        st.write("""
        RetireChat is your AI-powered Retirement Planning Coach that offers:
        
        • Personalized retirement planning advice
        • Goal identification and planning
        • Skills gap analysis
        • Learning opportunity recommendations
        • Step-by-step action plans
        • Professional document generation
        """)
        
        st.header("Suggested Prompts")
        if st.button("🎯 Create retirement development plan"):
            st.session_state.suggested_prompt = "Help me create a detailed retirement development plan based on my current financial situation and future goals."
        
        if st.button("📊 Skill gap analysis"):
            st.session_state.suggested_prompt = "Analyze my current skills and identify any gaps that I need to fill to advance in my career."
        
        if st.button("📚 Learning opportunities"):
            st.session_state.suggested_prompt = "What courses, certifications, or workshops would you recommend for someone in my generation to plan retirement successfully?"
        
        st.markdown("---")
        if st.button("🗑️ Clear Conversation"):
            st.session_state.conversation_history = []
            st.session_state.messages = []
            st.rerun()
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Handle suggested prompts
    suggested_prompt = None
    if "suggested_prompt" in st.session_state:
        suggested_prompt = st.session_state.suggested_prompt
        del st.session_state.suggested_prompt
    
    # Always show the chat input
    chat_prompt = st.chat_input("Ask me about retirement planning, financial goals, or career development...")
    
    # Use suggested prompt if available, otherwise use chat input
    prompt = suggested_prompt or chat_prompt
    
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_ai_response(prompt, st.session_state.conversation_history)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.conversation_history.append({"role": "user", "content": prompt})
        st.session_state.conversation_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()