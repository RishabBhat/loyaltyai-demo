import streamlit as st
import os
import hashlib
import anthropic
import logging
from pathlib import Path
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Streamlit page config
st.set_page_config(
    page_title="LoyaltyAI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# User database with hashed passwords and roles
USERS = {
    "rishab.bhat": {
        "password": hashlib.sha256("optum123".encode()).hexdigest(),
        "name": "Rishab Bhat", 
        "role": "Associate Software Engineer",
        "team": "Taj Mahal",
        "manager": "Allesha Fogle",
        "dashboard_type": "individual"
    },
    "britney.duratinsky": {
        "password": hashlib.sha256("optum123".encode()).hexdigest(),
        "name": "Britney Duratinsky",
        "role": "Associate Software Engineer", 
        "team": "Taj Mahal",
        "manager": "Allesha Fogle",
        "dashboard_type": "individual"
    },
    "scott.forsmann": {
        "password": hashlib.sha256("optum123".encode()).hexdigest(),
        "name": "Scott Forsmann",
        "role": "Associate Software Engineer",
        "team": "Taj Mahal", 
        "manager": "Allesha Fogle",
        "dashboard_type": "individual"
    },
    "michael.joyce": {
        "password": hashlib.sha256("optum123".encode()).hexdigest(),
        "name": "Michael Joyce",
        "role": "Senior Software Engineer",
        "team": "Machu Picchu",
        "manager": "Allesha Fogle", 
        "dashboard_type": "senior_engineer"
    },
    "christopher.jimenez": {
        "password": hashlib.sha256("optum123".encode()).hexdigest(),
        "name": "Christopher Jimenez",
        "role": "Engineering Director",
        "team": "Leadership",
        "manager": None,
        "dashboard_type": "director"
    },
    "connie.cavallo": {
        "password": hashlib.sha256("optum123".encode()).hexdigest(),
        "name": "Connie Cavallo",
        "role": "Senior Product Manager",
        "team": "Product",
        "manager": "Christopher Jimenez",
        "dashboard_type": "product_manager"
    },
    "swapna.kolimi": {
        "password": hashlib.sha256("optum123".encode()).hexdigest(),
        "name": "Swapna Kolimi", 
        "role": "Scrum Master",
        "team": "Agile",
        "manager": "Christopher Jimenez",
        "dashboard_type": "scrum_master"
    },
    "allesha.fogle": {
        "password": hashlib.sha256("optum123".encode()).hexdigest(),
        "name": "Allesha Fogle",
        "role": "Engineering Manager",
        "team": "Onshore Teams",
        "manager": "Christopher Jimenez",
        "dashboard_type": "engineering_manager"
    }
}

# Dashboard data
DASHBOARD_DATA = {
    "individual": {
        "rishab": {
            "my_stories": [
                {
                    "id": "LY-1847",
                    "title": "Implement Source System Ranking Algorithm",
                    "status": "In Progress",
                    "points": 8,
                    "acceptance_criteria": [
                        "System can rank member data sources by reliability score",
                        "Algorithm handles conflicts between data sources", 
                        "Performance meets SLA of under 200ms response time",
                        "All edge cases documented and tested"
                    ],
                    "tasks": [
                        {"task": "Design ranking algorithm", "status": "Complete"},
                        {"task": "Implement core logic", "status": "In Progress"},
                        {"task": "Add unit tests", "status": "To Do"},
                        {"task": "Performance testing", "status": "To Do"}
                    ],
                    "description": "Build intelligent ranking system to prioritize member data from multiple sources"
                }
            ]
        },
        "britney": {
            "my_stories": [
                {
                    "id": "LY-1834",
                    "title": "Migrate Top of Funnel Script Logic to Kafka",
                    "status": "In Progress",
                    "points": 13,
                    "acceptance_criteria": [
                        "All Top of Funnel logic converted to event-driven processing",
                        "Zero data loss during migration"
                    ],
                    "tasks": [
                        {"task": "Analyze current Top of Funnel logic", "status": "Complete"},
                        {"task": "Design Kafka event structure", "status": "Complete"}
                    ],
                    "description": "Replace legacy Perl script with modern event-driven processing"
                }
            ]
        },
        "scott": {
            "my_stories": [
                {
                    "id": "LY-1849",
                    "title": "Member Data Migration Performance Optimization",
                    "status": "In Progress",
                    "points": 8,
                    "acceptance_criteria": [
                        "Migration performance improved by 50%",
                        "Database connection pooling optimized"
                    ],
                    "tasks": [
                        {"task": "Profile current migration performance", "status": "Complete"},
                        {"task": "Implement parallel processing", "status": "In Progress"}
                    ],
                    "description": "Optimize large-scale member data migration processes"
                }
            ]
        },
        "my_incidents": [
            {
                "id": "INC0012845", 
                "title": "Member eligibility sync failure", 
                "priority": "P2", 
                "status": "Assigned", 
                "description": "UHC member eligibility data not syncing properly from upstream systems",
                "steps_taken": ["Verified database connectivity", "Checked Kafka consumer lag"],
                "next_actions": ["Contact upstream team", "Implement temporary workaround"]
            }
        ],
        "on_call_schedule": [
            {"week": "Current", "engineer": "Scott Forsmann", "phone": "612-555-0134"},
            {"week": "Next", "engineer": "Ravali Botta", "phone": "612-555-0178"},
            {"week": "Following", "engineer": "Michael Joyce", "phone": "612-555-0189"}
        ]
    },
    "senior_engineer": {
        "team_metrics": {
            "sprint_velocity": 38,
            "code_coverage": 87,
            "bug_escape_rate": 2.1,
            "avg_cycle_time": 4.2
        },
        "team_members": [
            {"name": "Sofia Khan", "role": "Associate SWE", "current_task": "LY-1851 - Device sync reliability improvements"},
            {"name": "Ravali Botta", "role": "Software Engineer", "current_task": "LY-1852 - Eligibility rule migration framework"}
        ],
        "code_reviews": [
            {"pr": "PR #234", "author": "Sofia Khan", "title": "Add device sync retry logic", "status": "Needs Review"}
        ],
        "architecture_decisions": [
            {"topic": "Kafka Topic Partitioning Strategy", "status": "Under Review", "owner": "Michael Joyce"}
        ]
    },
    "director": {
        "team_burndown": {
            "taj_mahal": {"planned": 42, "completed": 28, "velocity": "On Track"},
            "machu_picchu": {"planned": 38, "completed": 31, "velocity": "Ahead"}
        },
        "quarterly_metrics": {
            "deployment_frequency": {"current": 12, "target": 15, "trend": "improving"},
            "team_satisfaction": {"current": 4.2, "target": 4.0, "trend": "improving"}
        }
    },
    "engineering_manager": {
        "direct_reports": [
            {"name": "Rishab Bhat", "team": "Taj Mahal", "role": "Associate SWE", "current_sprint_load": "80%", "performance": "Meeting Expectations"},
            {"name": "Michael Joyce", "team": "Machu Picchu", "role": "Senior SWE", "current_sprint_load": "90%", "performance": "Exceeds Expectations"}
        ],
        "team_performance": {
            "taj_mahal": {"velocity": 42, "target": 45, "efficiency": "93%", "satisfaction": 4.1},
            "machu_picchu": {"velocity": 38, "target": 40, "efficiency": "95%", "satisfaction": 4.3}
        },
        "budget_overview": {
            "team_salary_budget": {"used": 2.1, "allocated": 2.3, "percentage": 91},
            "training_budget": {"used": 15000, "allocated": 25000, "percentage": 60}
        }
    },
    "product_manager": {
        "active_epics": [
            {"epic": "EPIC-101", "title": "Kafka Migration Initiative", "progress": 65, "status": "On Track"}
        ],
        "feature_requests": [
            {"id": "FR-445", "title": "Biometric device integration", "votes": 23, "business_value": "High"}
        ]
    },
    "scrum_master": {
        "team_health": {
            "taj_mahal": {"velocity_trend": "stable", "blockers": 1, "satisfaction": 4.1},
            "machu_picchu": {"velocity_trend": "improving", "blockers": 2, "satisfaction": 4.3}
        },
        "upcoming_ceremonies": [
            {"ceremony": "Sprint Planning", "team": "Taj Mahal", "date": "2025-01-29"}
        ]
    }
}

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    
    .dashboard-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        cursor: pointer;
        transition: transform 0.2s ease;
    }
    
    .dashboard-card:hover {
        transform: translateY(-2px);
    }
    
    .dashboard-card-success {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .dashboard-card-alt {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .dashboard-card-danger {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        color: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 500;
        background: rgba(255, 255, 255, 0.2);
    }
    
    .metric-number {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .login-container {
        max-width: 350px;
        margin: 2rem auto;
        padding: 2rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    if username in USERS:
        if hash_password(password) == USERS[username]["password"]:
            return USERS[username]
    return None

def login_page():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown("## 🔐 LoyaltyAI Login")
    
    username = st.text_input("Username", placeholder="firstname.lastname")
    password = st.text_input("Password", type="password", placeholder="Password")
    
    if st.button("Login", use_container_width=True):
        user = authenticate_user(username, password)
        if user:
            st.session_state.user = user
            st.session_state.username = username
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid username or password")
    
    st.markdown('</div>', unsafe_allow_html=True)

@st.cache_resource
def initialize_ai_client():
    """Initialize AI API client"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        return client
    except Exception as e:
        logger.error(f"Failed to initialize AI client: {e}")
        return None

def get_relevant_context(question: str) -> str:
    """Get context based on question keywords - simple demo version"""
    question_lower = question.lower()
    
    # Simple keyword-based context matching for demo
    if any(word in question_lower for word in ["machu picchu", "team members", "who's on"]):
        return "The Machu Picchu team includes Sofia Khan (Associate SWE), Ravali Botta (Software Engineer), Michael Joyce (Senior SWE), Shasikumar Bommineni (Contractor), Ganesh Nettem (Contractor), Nagarjuna Reddy (Software Engineer), and Ajit Krishnan (Software Engineer). Michael Joyce is the Senior Engineer leading the team."
    
    elif any(word in question_lower for word in ["on call", "oncall", "who's on call"]):
        return "Scott Forsmann is currently on call this week. You can reach him at 612-555-0134. Next week Ravali Botta will be on call (612-555-0178), followed by Michael Joyce (612-555-0189)."
    
    elif any(word in question_lower for word in ["sprint", "goals", "current sprint"]):
        return "Sprint 23 goals include: 1) Kafka Migration Phase 1 - eliminate Top of Funnel script dependencies, 2) Implement automated spouse assignment workflow, 3) Fix dual eligibility conflict resolution, 4) Database performance improvements for member lookup queries. The sprint runs from January 15-29, 2025."
    
    elif any(word in question_lower for word in ["tech stack", "technology", "tools"]):
        return "Our tech stack includes Java Spring Boot for backend services, MySQL for database (on-premises), Kubernetes for container orchestration, Apache Kafka for messaging, Splunk for monitoring and logging, and Capillary Technologies provides our frontend."
    
    elif any(word in question_lower for word in ["database", "db issues", "database problems"]):
        return "For database issues, contact the DBA team at dba-team@optum.com. For urgent database problems, escalate to Maria Garcia or the platform team. Common issues include connection pool exhaustion and query performance problems."
    
    elif any(word in question_lower for word in ["kafka", "migration", "top of funnel"]):
        return "The Kafka migration involves replacing the legacy Top of Funnel Perl script with event-driven processing. This will eliminate daily batch processing delays and enable real-time member eligibility updates. Britney Duratinsky is leading this migration effort."
    
    else:
        return f"Based on team documentation and knowledge about the Optum Loyalty platform, focusing on member eligibility, device integrations, and platform engineering."

def generate_answer_with_ai(question: str, context: str, client, user_info) -> str:
    """Generate answer using AI API or demo responses"""
    if not client:
        # Demo mode responses when no API key
        demo_responses = {
            "who's on call": "Scott Forsmann is on call this week. You can reach him at 612-555-0134.",
            "machu picchu team": "The Machu Picchu team includes Sofia Khan, Ravali Botta, Michael Joyce, Shasikumar Bommineni, Ganesh Nettem, Nagarjuna Reddy, and Ajit Krishnan. Michael Joyce serves as the Senior Engineer.",
            "sprint goals": "Sprint 23 focuses on Kafka migration, eliminating the Top of Funnel script, implementing automated spouse assignment, and fixing dual eligibility conflicts.",
            "tech stack": "Our tech stack uses Java Spring Boot, MySQL, Kubernetes, Apache Kafka, and Splunk, with Capillary Technologies handling the frontend.",
            "database issues": "For database issues, contact dba-team@optum.com or escalate to Maria Garcia for urgent problems."
        }
        
        question_lower = question.lower()
        for key, response in demo_responses.items():
            if any(word in question_lower for word in key.split()):
                return response
        
        return f"Hi {user_info['name']}! In the full version with API access, LoyaltyAI would provide detailed answers based on your team's documents. This demo showcases the UI and role-based dashboards with realistic Optum team data."
    
    # Real AI response with API key
    role_context = f"You are LoyaltyAI, responding to {user_info['name']}, a {user_info['role']} on the {user_info['team']} team."
    
    prompt = f"""{role_context}

Based on the following context about the Optum Loyalty team, answer the user's question. Be helpful, accurate, and concise. Do not mention document sources.

Context: {context}

User question: {question}

Provide a direct, helpful answer."""

    try:
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=800,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        return f"I apologize, but I'm having trouble connecting to the AI service right now. Please try again in a moment."

def render_individual_dashboard(user_info):
    """Render dashboard for individual contributors"""
    st.markdown(f"### 👤 Welcome back, {user_info['name']}")
    
    username = st.session_state.username.split('.')[0]
    user_data = DASHBOARD_DATA["individual"].get(username, DASHBOARD_DATA["individual"]["rishab"])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📋 My Current Stories")
        for i, story in enumerate(user_data["my_stories"]):
            card_class = "dashboard-card-success" if story['status'] == 'Code Review' else "dashboard-card-alt" if story['status'] == 'In Progress' else "dashboard-card"
            
            with st.expander(f"🎯 {story['id']} - {story['title']} ({story['points']} pts)", expanded=False):
                st.markdown(f"**Status:** {story['status']}")
                st.markdown(f"**Description:** {story['description']}")
                
                st.markdown("**Acceptance Criteria:**")
                for criteria in story['acceptance_criteria']:
                    st.markdown(f"• {criteria}")
                
                st.markdown("**Tasks:**")
                for task in story['tasks']:
                    status_emoji = "✅" if task['status'] == 'Complete' else "🔄" if task['status'] == 'In Progress' else "📋"
                    st.markdown(f"{status_emoji} {task['task']} - *{task['status']}*")
            
            st.markdown(f'<div class="{card_class}"><strong>{story["id"]}</strong> - {story["title"]}<br><span class="status-badge">{story["status"]}</span> <span style="float: right; font-size: 1.2em; font-weight: bold;">{story["points"]} pts</span></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📅 On-Call Schedule")
        for schedule in DASHBOARD_DATA["individual"]["on_call_schedule"]:
            card_class = "dashboard-card-danger" if schedule['week'] == 'Current' else "dashboard-card"
            st.markdown(f'<div class="{card_class}"><strong>{schedule["week"]} Week</strong><br>{schedule["engineer"]}<br>📞 {schedule["phone"]}</div>', unsafe_allow_html=True)

def render_senior_engineer_dashboard(user_info):
    """Render dashboard for senior engineers"""
    st.markdown(f"### 👨‍💼 {user_info['name']} - {user_info['team']} Team Lead")
    
    metrics = DASHBOARD_DATA["senior_engineer"]["team_metrics"]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div class="dashboard-card-success"><div class="metric-number">{metrics["sprint_velocity"]}</div><strong>Sprint Velocity</strong></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="dashboard-card-alt"><div class="metric-number">{metrics["code_coverage"]}%</div><strong>Code Coverage</strong></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="dashboard-card"><div class="metric-number">{metrics["bug_escape_rate"]}</div><strong>Bug Escape Rate</strong></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="dashboard-card"><div class="metric-number">{metrics["avg_cycle_time"]}</div><strong>Avg Cycle Time</strong></div>', unsafe_allow_html=True)

def render_director_dashboard(user_info):
    """Render dashboard for director"""
    st.markdown(f"### 🎯 {user_info['name']} - Leadership Dashboard")
    
    for team, data in DASHBOARD_DATA["director"]["team_burndown"].items():
        card_class = "dashboard-card-success" if data['velocity'] == 'Ahead' else "dashboard-card-alt"
        completion_pct = round((data['completed'] / data['planned']) * 100)
        st.markdown(f'<div class="{card_class}"><strong>{team.replace("_", " ").title()}</strong><br>Progress: {data["completed"]}/{data["planned"]} ({completion_pct}%)<br><span class="status-badge">{data["velocity"]}</span></div>', unsafe_allow_html=True)

def render_engineering_manager_dashboard(user_info):
    """Render dashboard for engineering manager"""
    st.markdown(f"### 👩‍💼 {user_info['name']} - Engineering Manager")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 👥 Direct Reports")
        for report in DASHBOARD_DATA["engineering_manager"]["direct_reports"]:
            card_class = "dashboard-card-success" if report['performance'] == 'Exceeds Expectations' else "dashboard-card-alt"
            st.markdown(f'<div class="{card_class}"><strong>{report["name"]}</strong><br>{report["role"]} - {report["team"]}<br><span class="status-badge">{report["performance"]}</span></div>', unsafe_allow_html=True)

def render_product_manager_dashboard(user_info):
    """Render dashboard for product manager"""
    st.markdown(f"### 📊 {user_info['name']} - Product Dashboard")
    
    for epic in DASHBOARD_DATA["product_manager"]["active_epics"]:
        st.markdown(f'<div class="dashboard-card"><strong>{epic["epic"]}</strong> - {epic["title"]}<br>Progress: {epic["progress"]}%<br><span class="status-badge">{epic["status"]}</span></div>', unsafe_allow_html=True)

def render_scrum_master_dashboard(user_info):
    """Render dashboard for scrum master"""
    st.markdown(f"### 🏃‍♀️ {user_info['name']} - Agile Dashboard")
    
    for team, health in DASHBOARD_DATA["scrum_master"]["team_health"].items():
        st.markdown(f'<div class="dashboard-card"><strong>{team.replace("_", " ").title()}</strong><br>Satisfaction: {health["satisfaction"]}/5.0<br>Blockers: {health["blockers"]}</div>', unsafe_allow_html=True)

def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        login_page()
        return
    
    user_info = st.session_state.user
    
    with st.sidebar:
        st.markdown('<h1 class="main-header">🤖 LoyaltyAI</h1>', unsafe_allow_html=True)
        st.markdown(f"**Welcome, {user_info['name']}**")
        st.markdown(f"*{user_info['role']} - {user_info['team']} Team*")
        
        if st.button("🚪 Logout"):
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        
        client = initialize_ai_client()
        if client:
            st.success("✅ LoyaltyAI Connected")
        else:
            st.info("🎭 Demo Mode - Add API key for full AI responses")
    
    tab1, tab2 = st.tabs(["📊 Dashboard", "💬 Ask LoyaltyAI"])
    
    with tab1:
        if user_info['dashboard_type'] == 'individual':
            render_individual_dashboard(user_info)
        elif user_info['dashboard_type'] == 'senior_engineer':
            render_senior_engineer_dashboard(user_info)
        elif user_info['dashboard_type'] == 'director':
            render_director_dashboard(user_info)
        elif user_info['dashboard_type'] == 'product_manager':
            render_product_manager_dashboard(user_info)
        elif user_info['dashboard_type'] == 'scrum_master':
            render_scrum_master_dashboard(user_info)
        elif user_info['dashboard_type'] == 'engineering_manager':
            render_engineering_manager_dashboard(user_info)
    
    with tab2:
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("💬 Ask me anything about your team's work..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
            
            with st.chat_message("assistant", avatar="🤖"):
                context = get_relevant_context(prompt)
                answer = generate_answer_with_ai(prompt, context, client, user_info)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()