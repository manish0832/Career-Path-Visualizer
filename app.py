from flask import Flask, render_template, request, jsonify
import sqlite3
import json
import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            category TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            avg_salary INTEGER,
            growth_rate REAL,
            required_skills TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS career_map (
            id INTEGER PRIMARY KEY,
            from_role TEXT,
            to_role TEXT,
            transition_time INTEGER,
            difficulty TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS salary_data (
            id INTEGER PRIMARY KEY,
            role TEXT,
            year INTEGER,
            salary INTEGER,
            job_openings INTEGER
        )
    ''')
    
    # Insert sample data
    sample_skills = [
        ('Python', 'Programming'),
        ('JavaScript', 'Programming'),
        ('React', 'Frontend'),
        ('Node.js', 'Backend'),
        ('SQL', 'Database'),
        ('Machine Learning', 'AI/ML'),
        ('Data Analysis', 'Analytics'),
        ('Project Management', 'Management'),
        ('Communication', 'Soft Skills'),
        ('Leadership', 'Soft Skills')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO skills (name, category) VALUES (?, ?)', sample_skills)
    
    sample_roles = [
        ('Frontend Developer', 'Build user interfaces and web applications', 75000, 15.2, 'JavaScript,React,HTML,CSS'),
        ('Backend Developer', 'Develop server-side applications and APIs', 85000, 12.8, 'Python,Node.js,SQL,API Development'),
        ('Full Stack Developer', 'Work on both frontend and backend development', 90000, 18.5, 'JavaScript,Python,React,Node.js,SQL'),
        ('Data Scientist', 'Analyze data and build predictive models', 110000, 22.3, 'Python,Machine Learning,Data Analysis,SQL'),
        ('Product Manager', 'Manage product development and strategy', 120000, 14.7, 'Project Management,Communication,Leadership,Data Analysis'),
        ('DevOps Engineer', 'Manage infrastructure and deployment pipelines', 95000, 20.1, 'Python,Linux,Docker,AWS,CI/CD'),
        ('UI/UX Designer', 'Design user interfaces and experiences', 70000, 13.4, 'Design,Figma,User Research,Prototyping'),
        ('Software Architect', 'Design software systems and architecture', 140000, 8.9, 'System Design,Leadership,Multiple Programming Languages')
    ]
    
    cursor.executemany('INSERT OR IGNORE INTO roles (title, description, avg_salary, growth_rate, required_skills) VALUES (?, ?, ?, ?, ?)', sample_roles)
    
    # Generate salary trend data
    roles = ['Frontend Developer', 'Backend Developer', 'Data Scientist', 'Product Manager']
    current_year = datetime.now().year
    
    for role in roles:
        base_salary = {'Frontend Developer': 65000, 'Backend Developer': 75000, 'Data Scientist': 95000, 'Product Manager': 105000}[role]
        base_openings = {'Frontend Developer': 1200, 'Backend Developer': 1000, 'Data Scientist': 800, 'Product Manager': 600}[role]
        
        for i in range(5):
            year = current_year - 4 + i
            salary = base_salary + (i * 5000) + random.randint(-3000, 3000)
            openings = base_openings + (i * 100) + random.randint(-50, 150)
            cursor.execute('INSERT OR IGNORE INTO salary_data (role, year, salary, job_openings) VALUES (?, ?, ?, ?)', 
                         (role, year, salary, openings))
    
    conn.commit()
    conn.close()

def get_matching_roles(skills, interests):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM roles')
    roles = cursor.fetchall()
    
    matched_roles = []
    for role in roles:
        role_skills = role[5].split(',')
        skill_match = len(set(skills) & set(role_skills)) / len(role_skills)
        
        # Simple interest matching (in real app, this would be more sophisticated)
        interest_match = 0.5  # Default interest match
        
        overall_match = (skill_match * 0.7) + (interest_match * 0.3)
        
        matched_roles.append({
            'title': role[1],
            'description': role[2],
            'avg_salary': role[3],
            'growth_rate': role[4],
            'match_score': round(overall_match * 100, 1),
            'required_skills': role[5].split(',')
        })
    
    # Sort by match score
    matched_roles.sort(key=lambda x: x['match_score'], reverse=True)
    conn.close()
    
    return matched_roles[:5]  # Return top 5 matches

def create_salary_chart(role_title):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query('SELECT * FROM salary_data WHERE role = ?', conn, params=(role_title,))
    conn.close()
    
    if df.empty:
        return None
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['salary'],
        mode='lines+markers',
        name='Average Salary',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title=f'Salary Trend for {role_title}',
        xaxis_title='Year',
        yaxis_title='Salary (USD)',
        template='plotly_white',
        height=400
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_job_openings_chart(role_title):
    conn = sqlite3.connect('database.db')
    df = pd.read_sql_query('SELECT * FROM salary_data WHERE role = ?', conn, params=(role_title,))
    conn.close()
    
    if df.empty:
        return None
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['year'],
        y=df['job_openings'],
        name='Job Openings',
        marker_color='#10b981'
    ))
    
    fig.update_layout(
        title=f'Job Market Trend for {role_title}',
        xaxis_title='Year',
        yaxis_title='Number of Job Openings',
        template='plotly_white',
        height=400
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, category FROM skills ORDER BY category, name')
    skills = cursor.fetchall()
    conn.close()
    
    # Group skills by category
    skills_by_category = {}
    for skill, category in skills:
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)
    
    return render_template('index.html', skills_by_category=skills_by_category)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    skills = data.get('skills', [])
    interests = data.get('interests', [])
    experience = data.get('experience', 'entry')
    
    # Get matching roles
    matched_roles = get_matching_roles(skills, interests)
    
    # Create visualizations for top role
    if matched_roles:
        top_role = matched_roles[0]['title']
        salary_chart = create_salary_chart(top_role)
        job_chart = create_job_openings_chart(top_role)
    else:
        salary_chart = None
        job_chart = None
    
    return jsonify({
        'roles': matched_roles,
        'salary_chart': salary_chart,
        'job_chart': job_chart,
        'user_profile': {
            'skills': skills,
            'interests': interests,
            'experience': experience
        }
    })

@app.route('/role/<role_title>')
def role_details(role_title):
    salary_chart = create_salary_chart(role_title)
    job_chart = create_job_openings_chart(role_title)
    
    return jsonify({
        'salary_chart': salary_chart,
        'job_chart': job_chart
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
