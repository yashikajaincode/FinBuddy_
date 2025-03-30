# FinBuddy - AI Financial Education Platform

FinBuddy is an AI-powered financial education platform designed for students and beginners in India. It helps users learn budgeting, saving, and investing through a gamified, conversational approach.

## Features

- **Interactive Budget Planner**: Track income and expenses with visual breakdowns
- **Savings Coach**: Set and track savings goals with progress visualization
- **Investment Education**: Learn investment basics through interactive modules
- **Financial Health Score**: Get a personalized financial health assessment
- **AI Chat Assistant**: Get personalized financial guidance through conversational AI
- **Achievements & Gamification**: Earn badges and track progress to stay motivated

## Tech Stack

- **Frontend**: React.js with context API for state management
- **Backend**: Node.js with Express.js
- **Database**: PostgreSQL 
- **AI Integration**: LangChain and GPT models for dynamic financial guidance
- **Authentication**: JWT-based user authentication

## Getting Started

### Prerequisites

- Node.js (v16+)
- PostgreSQL database
- OpenAI API key for AI features

### Installation

1. Clone the repository
```bash
git clone https://github.com/yashikajaincode/FinBuddy.git
cd finbuddy
```

2. Install dependencies for both frontend and backend
```bash
# Backend dependencies
cd finbuddy-react/backend
npm install

# Frontend dependencies
cd ../frontend
npm install
```

3. Set up environment variables
Create `.env` files in both frontend and backend directories with the necessary environment variables.

4. Start the development servers
```bash
# Start backend server
cd finbuddy-react/backend
npm run dev

# Start frontend server
cd ../frontend
npm start
```

## Project Structure

- `/finbuddy-react/frontend`: React.js frontend application
- `/finbuddy-react/backend`: Node.js/Express.js backend API
- `/assets`: Shared assets and resources
- `/demo`: Demo applications and examples

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Financial data and educational content adapted for Indian context
- UI design inspired by modern fintech applications