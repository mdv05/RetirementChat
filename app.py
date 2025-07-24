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

# Custom CSS for professional styling similar to RetireHub
st.markdown("""
<style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1f4e79 0%, #2980b9 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        color: white !important;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
        color: white !important;
    }
    
    /* Card styling */
    .feature-card {
        background: white;
        border: 1px solid #e1e8ed;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    }
    
    .feature-card h3 {
        color: #1f4e79;
        margin-top: 0;
        font-weight: 600;
    }
    
    /* Form styling */
    .form-container {
        background: white;
        border: 1px solid #e1e8ed;
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .form-section {
        margin-bottom: 2rem;
        padding-bottom: 1.5rem;
        border-bottom: 1px solid #f0f0f0;
    }
    
    .form-section:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }
    
    .form-section h4 {
        color: #1f4e79;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Profile summary styling */
    .profile-summary {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 1px solid #dee2e6;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .profile-item {
        display: flex;
        justify-content: space-between;
        padding: 0.5rem 0;
        border-bottom: 1px solid #dee2e6;
    }
    
    .profile-item:last-child {
        border-bottom: none;
    }
    
    .profile-label {
        font-weight: 600;
        color: #1f4e79;
    }
    
    .profile-value {
        color: #495057;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1f4e79 0%, #2980b9 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(31, 78, 121, 0.3);
    }
    
    /* Chat styling */
    .chat-container {
        background: white;
        border-radius: 12px;
        border: 1px solid #e1e8ed;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* Stats styling */
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Footer styling */
    .footer {
        background-color: #f8f9fa;
        padding: 2rem;
        margin-top: 3rem;
        border-radius: 10px;
        border-top: 3px solid #1f4e79;
        text-align: center;
    }
    
    /* Navigation styling */
    .nav-container {
        background: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        border: 1px solid #e1e8ed;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .nav-logo {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f4e79;
    }
    
    .nav-links {
        display: flex;
        gap: 2rem;
    }
    
    .nav-link {
        color: #1f4e79;
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        transition: background-color 0.2s ease;
    }
    
    .nav-link:hover {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def create_retirement_prompt_with_profile(user_profile):
    """Create a personalized prompt based on user profile data"""
    base_prompt = """You are an expert Retirement Planning Coach providing personalized advice.

USER CONTEXT:"""
    
    if user_profile:
        # Create a more concise profile summary to avoid safety filter issues
        profile_summary = []
        
        if user_profile.get('age'):
            profile_summary.append(f"Age {user_profile['age']}")
        if user_profile.get('career_stage'):
            profile_summary.append(f"Career: {user_profile['career_stage']}")
        if user_profile.get('annual_income'):
            profile_summary.append(f"Income: {user_profile['annual_income']}")
        if user_profile.get('current_savings'):
            profile_summary.append(f"Current savings: {user_profile['current_savings']}")
        if user_profile.get('target_retirement_age'):
            profile_summary.append(f"Target retirement age: {user_profile['target_retirement_age']}")
        if user_profile.get('risk_tolerance'):
            profile_summary.append(f"Risk tolerance: {user_profile['risk_tolerance']}")
        if user_profile.get('primary_goals'):
            goals = user_profile['primary_goals'][:100]  # Limit length
            profile_summary.append(f"Goals: {goals}")
        
        base_prompt += f"\n{', '.join(profile_summary[:6])}"  # Limit to 6 key items
    
    base_prompt += """

INSTRUCTIONS:
- Provide personalized retirement planning advice based on the user context above
- Give specific, actionable recommendations
- Reference their age, income, and goals when relevant
- Be encouraging and professional
- Include credible sources when discussing financial concepts
- Ask clarifying questions if you need more specific information

KNOWLEDGE SOURCES:
- Segal Benefits: https://2025-benefits.segalco.com/
- PSCA News: https://www.psca.org/news/psca-news/
"""
    
    return base_prompt

def get_ai_response(user_input, conversation_history, user_profile):
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Build conversation context with simplified profile
        context = create_retirement_prompt_with_profile(user_profile) + "\n\nCONVERSATION:\n"
        
        # Keep only last 5 messages to avoid token limits
        recent_history = conversation_history[-5:] if conversation_history else []
        for msg in recent_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"{role}: {msg['content'][:200]}...\n"  # Limit message length
        
        context += f"\nUser: {user_input}\nAssistant:"
        
        # Add safety settings to handle potential blocks
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        response = model.generate_content(
            context,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=800,  # Reduced to avoid issues
                temperature=0.7,
            ),
            safety_settings=safety_settings
        )
        
        # Check if response was blocked
        if response.candidates and response.candidates[0].finish_reason == 2:
            return """I apologize, but I need to rephrase my response. Let me provide you with some general retirement planning guidance:

**Personalized Retirement Planning Steps:**

1. **Assessment**: Based on your profile, let's review your current savings rate and timeline.

2. **Goal Setting**: With your target retirement age, we can calculate how much you need to save monthly.

3. **Investment Strategy**: Given your risk tolerance, I can recommend appropriate investment allocations.

4. **Action Plan**: 
   - Immediate: Review and optimize current contributions
   - Next 3 months: Set up automatic savings increases
   - Next 6 months: Diversify investment portfolio
   - Ongoing: Annual reviews and adjustments

Could you ask me about a specific aspect of retirement planning? For example:
- "How much should I save monthly for retirement?"
- "What investment mix is right for my age?"
- "How can I catch up on retirement savings?"

This will help me provide more targeted advice for your situation."""
        
        # Return the response text if available
        if response.text:
            return response.text
        else:
            return "I'm having trouble generating a complete response. Could you try asking about a specific aspect of retirement planning instead?"
            
    except Exception as e:
        # Enhanced error handling with helpful fallback
        if "finish_reason" in str(e) or "safety" in str(e).lower():
            return """I apologize, but I need to approach your question differently. Let me provide some general retirement planning guidance:

**Key Retirement Planning Areas:**

🎯 **Savings Strategy**: Most experts recommend saving 10-15% of your income for retirement.

📊 **Investment Allocation**: Your investment mix should align with your age and risk tolerance.

⏰ **Timeline Planning**: The earlier you start, the more compound interest works in your favor.

💡 **Action Steps**: Start with maximizing any employer 401(k) match, then consider additional savings.

**Let's focus on specifics - what would you like to explore?**
- Savings rate calculations
- Investment strategy for your age
- Debt management while saving
- Social Security planning

This will help me give you more targeted advice for your situation."""
        else:
            return f"I'm experiencing a technical issue connecting to the AI service. Please try refreshing the page or asking your question in a different way. Error details: {str(e)[:100]}"

def show_onboarding_form():
    """Display the onboarding form to collect user profile information"""
    st.markdown("""
    <div class="main-header">
        <h1>Welcome to RetireChat</h1>
        <p>Let's create your personalized retirement planning profile</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="form-container">
        <h3 style="color: #1f4e79; margin-top: 0;">Personal Retirement Assessment</h3>
        <p>Please fill out this form so I can provide you with personalized retirement planning advice. All information is kept confidential and used only to tailor recommendations to your specific situation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("retirement_profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="form-section"><h4>👤 Personal Information</h4>', unsafe_allow_html=True)
            age = st.number_input("Current Age", min_value=18, max_value=100, value=35)
            career_stage = st.selectbox("Career Stage", [
                "Early Career (0-5 years experience)",
                "Mid-Career (5-15 years experience)", 
                "Senior Career (15+ years experience)",
                "Near Retirement (5 years or less)",
                "Already Retired"
            ])
            employment_status = st.selectbox("Employment Status", [
                "Full-time Employee",
                "Part-time Employee",
                "Self-employed/Freelancer",
                "Business Owner",
                "Unemployed",
                "Retired"
            ])
            family_status = st.selectbox("Family Status", [
                "Single, no dependents",
                "Married/Partnered, no children",
                "Married/Partnered with children",
                "Single parent",
                "Supporting elderly parents",
                "Other"
            ])
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-section"><h4>💰 Financial Information</h4>', unsafe_allow_html=True)
            annual_income = st.selectbox("Annual Income", [
                "Under $30,000",
                "$30,000 - $50,000",
                "$50,000 - $75,000",
                "$75,000 - $100,000",
                "$100,000 - $150,000",
                "$150,000 - $250,000",
                "Over $250,000"
            ])
            current_savings = st.selectbox("Current Retirement Savings", [
                "No savings yet",
                "Under $10,000",
                "$10,000 - $50,000",
                "$50,000 - $100,000",
                "$100,000 - $250,000",
                "$250,000 - $500,000",
                "$500,000 - $1,000,000",
                "Over $1,000,000"
            ])
            monthly_contributions = st.selectbox("Monthly Retirement Contributions", [
                "Not contributing yet",
                "Under $200",
                "$200 - $500",
                "$500 - $1,000",
                "$1,000 - $2,000",
                "Over $2,000"
            ])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="form-section"><h4>🎯 Goals & Timeline</h4>', unsafe_allow_html=True)
            target_retirement_age = st.number_input("Target Retirement Age", min_value=50, max_value=80, value=65)
            target_savings = st.selectbox("Target Retirement Savings Goal", [
                "Not sure yet",
                "$500,000 - $1,000,000",
                "$1,000,000 - $2,000,000",
                "$2,000,000 - $5,000,000",
                "Over $5,000,000"
            ])
            primary_goals = st.multiselect("Primary Retirement Goals", [
                "Maintain current lifestyle",
                "Travel extensively",
                "Support family/children",
                "Start a business",
                "Volunteer/charity work",
                "Healthcare security",
                "Leave an inheritance",
                "Early retirement"
            ])
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="form-section"><h4>📊 Experience & Risk</h4>', unsafe_allow_html=True)
            investment_experience = st.selectbox("Investment Experience", [
                "Beginner - little to no experience",
                "Basic - some knowledge of investments",
                "Intermediate - moderate experience",
                "Advanced - extensive experience"
            ])
            risk_tolerance = st.selectbox("Risk Tolerance", [
                "Conservative - prefer stable, low-risk investments",
                "Moderate - willing to accept some risk for potential growth",
                "Aggressive - comfortable with high-risk, high-reward investments"
            ])
            current_debt = st.selectbox("Current Debt Level", [
                "No significant debt",
                "Some credit card debt",
                "Student loans",
                "Mortgage only",
                "Multiple debts (credit cards, loans, etc.)",
                "High debt burden"
            ])
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-section"><h4>🤔 Challenges & Concerns</h4>', unsafe_allow_html=True)
        main_challenges = st.multiselect("Main Retirement Planning Challenges", [
            "Don't know where to start",
            "Not saving enough",
            "Understanding investment options",
            "Balancing current expenses with saving",
            "Managing debt while saving",
            "Healthcare costs in retirement",
            "Social Security uncertainty",
            "Market volatility concerns",
            "Inflation impact",
            "Estate planning"
        ])
        additional_info = st.text_area("Additional Information or Specific Questions", 
                                     placeholder="Any other details about your situation or specific questions you'd like addressed...")
        st.markdown('</div>', unsafe_allow_html=True)
        
        submitted = st.form_submit_button("Create My Retirement Profile", use_container_width=True)
        
        if submitted:
            # Store profile in session state
            st.session_state.user_profile = {
                'age': age,
                'career_stage': career_stage,
                'employment_status': employment_status,
                'family_status': family_status,
                'annual_income': annual_income,
                'current_savings': current_savings,
                'monthly_contributions': monthly_contributions,
                'target_retirement_age': target_retirement_age,
                'target_savings': target_savings,
                'primary_goals': ', '.join(primary_goals) if primary_goals else 'Not specified',
                'investment_experience': investment_experience,
                'risk_tolerance': risk_tolerance,
                'current_debt': current_debt,
                'main_challenges': ', '.join(main_challenges) if main_challenges else 'Not specified',
                'additional_info': additional_info
            }
            st.session_state.profile_complete = True
            st.success("✅ Profile created successfully! You can now start chatting with your AI retirement coach.")
            st.rerun()

def show_profile_summary(user_profile):
    """Display a summary of the user's profile"""
    st.markdown("""
    <div class="profile-summary">
        <h4 style="color: #1f4e79; margin-top: 0;">📋 Your Retirement Profile</h4>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="profile-item">
            <span class="profile-label">Age:</span>
            <span class="profile-value">{user_profile.get('age', 'N/A')}</span>
        </div>
        <div class="profile-item">
            <span class="profile-label">Career Stage:</span>
            <span class="profile-value">{user_profile.get('career_stage', 'N/A')}</span>
        </div>
        <div class="profile-item">
            <span class="profile-label">Current Savings:</span>
            <span class="profile-value">{user_profile.get('current_savings', 'N/A')}</span>
        </div>
        <div class="profile-item">
            <span class="profile-label">Monthly Contributions:</span>
            <span class="profile-value">{user_profile.get('monthly_contributions', 'N/A')}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="profile-item">
            <span class="profile-label">Target Retirement Age:</span>
            <span class="profile-value">{user_profile.get('target_retirement_age', 'N/A')}</span>
        </div>
        <div class="profile-item">
            <span class="profile-label">Target Savings:</span>
            <span class="profile-value">{user_profile.get('target_savings', 'N/A')}</span>
        </div>
        <div class="profile-item">
            <span class="profile-label">Risk Tolerance:</span>
            <span class="profile-value">{user_profile.get('risk_tolerance', 'N/A')}</span>
        </div>
        <div class="profile-item">
            <span class="profile-label">Investment Experience:</span>
            <span class="profile-value">{user_profile.get('investment_experience', 'N/A')}</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Initialize session state
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "profile_complete" not in st.session_state:
        st.session_state.profile_complete = False
    
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}
    
    # Show onboarding form if profile not complete
    if not st.session_state.profile_complete:
        show_onboarding_form()
        return
    
    # Navigation Bar
    st.markdown("""
    <div class="nav-container">
        <div class="nav-logo">💰 RetireChat</div>
        <div class="nav-links">
            <a href="#" class="nav-link">Dashboard</a>
            <a href="#" class="nav-link">Planning Tools</a>
            <a href="#" class="nav-link">Resources</a>
            <a href="#" class="nav-link">Support</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main Header
    st.markdown("""
    <div class="main-header">
        <h1>AI Retirement Planning Coach</h1>
        <p>Delivering personalized advice based on your retirement profile</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Chat Interface
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 AI Retirement Planning Assistant</h3>
            <p>Get personalized answers based on your retirement profile and goals</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        prompt = st.chat_input("Ask me about retirement planning, financial goals, or career development...")
        
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):
                with st.spinner("Analyzing your question based on your profile..."):
                    response = get_ai_response(prompt, st.session_state.conversation_history, st.session_state.user_profile)
                    st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.conversation_history.append({"role": "user", "content": prompt})
            st.session_state.conversation_history.append({"role": "assistant", "content": response})
    
    with col2:
        # Profile Summary
        show_profile_summary(st.session_state.user_profile)
        
        # Update Profile Button
        if st.button("✏️ Update Profile", use_container_width=True):
            st.session_state.profile_complete = False
            st.rerun()
        
        # Quick Actions
        st.markdown("### Quick Start Guides")
        
        if st.button("🎯 Personalized Retirement Plan", use_container_width=True):
            st.session_state.suggested_prompt = "Based on my profile, create a detailed personalized retirement plan with specific action steps."
        
        if st.button("📈 Investment Strategy", use_container_width=True):
            st.session_state.suggested_prompt = "Given my risk tolerance and goals, what investment strategy would you recommend?"
        
        if st.button("💰 Savings Optimization", use_container_width=True):
            st.session_state.suggested_prompt = "How can I optimize my current savings and contributions based on my income and goals?"
        
        if st.button("🔮 Retirement Projections", use_container_width=True):
            st.session_state.suggested_prompt = "Show me projections of my retirement readiness and what adjustments I might need to make."
        
        # Stats
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Your Progress</h3>
            <div class="stat-card">
                <p class="stat-number">{}</p>
                <p class="stat-label">Questions Asked</p>
            </div>
        </div>
        """.format(len([msg for msg in st.session_state.messages if msg["role"] == "user"])), unsafe_allow_html=True)
        
        # Resources
        st.markdown("""
        <div class="feature-card">
            <h3>🔗 Trusted Resources</h3>
            <p><a href="https://2025-benefits.segalco.com/" target="_blank" style="color: #1f4e79;">Segal Benefits Portal</a></p>
            <p><a href="https://www.psca.org/news/psca-news/" target="_blank" style="color: #1f4e79;">PSCA Financial News</a></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.conversation_history = []
            st.session_state.messages = []
            st.rerun()
    
    # Handle suggested prompts
    if "suggested_prompt" in st.session_state:
        prompt = st.session_state.suggested_prompt
        del st.session_state.suggested_prompt
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your question based on your profile..."):
                response = get_ai_response(prompt, st.session_state.conversation_history, st.session_state.user_profile)
                st.markdown(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.conversation_history.append({"role": "user", "content": prompt})
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        <h4>💰 RetireChat</h4>
        <p>Delivering trusted retirement planning advice powered by AI technology.</p>
        <p style="font-size: 0.9rem; opacity: 0.7;">
            © 2025 RetireChat. All rights reserved. | 
            <a href="#" style="color: #1f4e79;">Privacy Policy</a> | 
            <a href="#" style="color: #1f4e79;">Terms of Service</a> | 
            <a href="#" style="color: #1f4e79;">Contact Support</a>
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()