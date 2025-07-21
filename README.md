# RetireChat - AI Retirement Planning Coach

RetireChat is a Streamlit-based AI-powered retirement planning coach that provides personalized retirement planning advice, goals, and action plans.

Deploy.

## Features

- **Personalized Retirement Planning**: Get customized advice based on your current financial situation
- **Goal Identification**: Define short-term and long-term retirement goals
- **Skills Gap Analysis**: Evaluate current skills and identify areas for improvement
- **Learning Recommendations**: Receive suggestions for courses, certifications, and workshops
- **Action Plans**: Get step-by-step plans with timelines and milestones
- **Professional Documents**: Generate printable retirement plans

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/RetirementChat.git
cd RetirementChat
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create a .env file and add your Google API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Configuration

The application includes Streamlit configuration in `.streamlit/config.toml` for:
- Theme customization
- Server settings
- CORS configuration

## AI Coach Capabilities

The AI retirement coach can help with:

1. **Retirement Assessment**: Understanding your current retirement plan and savings
2. **Goal Setting**: Defining retirement age and savings targets
3. **Career Development**: Identifying skills needed for career advancement
4. **Financial Planning**: Creating actionable financial strategies
5. **Learning Paths**: Recommending educational opportunities

## Suggested Conversation Starters

- "Help me create a detailed retirement development plan"
- "Analyze my current skills and identify gaps"
- "What learning opportunities would you recommend for retirement planning?"

## Knowledge Sources

The AI coach references:
- [Segal Benefits](https://2025-benefits.segalco.com/)
- [PSCA News](https://www.psca.org/news/psca-news/)

## Requirements

- Python 3.7+
- Streamlit
- Google AI API access (Gemini 2.5 Flash)
- Internet connection for AI responses

## Getting Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" to generate your key
4. Add the key to your `.env` file as `GOOGLE_API_KEY`

## License

This project is licensed under the MIT License.# Deployment fixed - Mon Jul 21 12:33:21 EDT 2025
# Permissions fixed - Mon Jul 21 12:36:20 EDT 2025
