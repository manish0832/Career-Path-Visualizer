# Career Path Visualizer 🚀

A comprehensive web application that helps users discover their ideal career paths based on their skills, interests, and current market trends.

## Features

- **Skill Assessment**: Interactive skill selection across multiple categories
- **Interest Matching**: Personality and interest-based career recommendations
- **Market Analysis**: Real-time salary trends and job market forecasts
- **Visual Analytics**: Interactive charts showing career growth and opportunities
- **Personalized Recommendations**: AI-powered matching algorithm

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Visualization**: Plotly.js
- **Icons**: Font Awesome

## Installation

1. Clone the repository
2. Install dependencies:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`
3. Run the application:
   \`\`\`bash
   python app.py
   \`\`\`
4. Open http://localhost:5000 in your browser

## Project Structure

\`\`\`
career-path-visualizer/
├── app.py                 # Main Flask application
├── database.db           # SQLite database (auto-generated)
├── templates/
│   ├── base.html         # Base template
│   └── index.html        # Main page
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
\`\`\`

## Database Schema

- **skills**: Available skills categorized by type
- **roles**: Career roles with descriptions and requirements
- **career_map**: Career transition pathways
- **salary_data**: Historical salary and job market data

## API Endpoints

- `GET /`: Main application page
- `POST /analyze`: Analyze user input and return career recommendations
- `GET /role/<role_title>`: Get detailed analytics for specific role

## Hackathon Ready Features

✅ Complete working prototype
✅ Professional UI/UX design
✅ Data visualization and analytics
✅ Scalable database structure
✅ API-ready architecture
✅ Mobile responsive design

## Future Enhancements

- Integration with LinkedIn/Indeed APIs
- Machine learning recommendation engine
- User accounts and progress tracking
- Career roadmap generation
- Skill gap analysis
