import streamlit as st
import os
import hashlib
import anthropic
import logging
from pathlib import Path
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader, TextLoader
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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
                },
                {
                    "id": "LY-1863",
                    "title": "Source System Health Monitoring",
                    "status": "Code Review",
                    "points": 5,
                    "acceptance_criteria": [
                        "Real-time monitoring of all source systems",
                        "Automated alerts for system degradation",
                        "Dashboard shows system health status"
                    ],
                    "tasks": [
                        {"task": "Set up monitoring endpoints", "status": "Complete"},
                        {"task": "Configure alerting rules", "status": "Complete"},
                        {"task": "Create health dashboard", "status": "In Review"}
                    ],
                    "description": "Monitor health and availability of external data sources"
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
                        "Zero data loss during migration",
                        "Performance matches or exceeds current batch processing"
                    ],
                    "tasks": [
                        {"task": "Analyze current Top of Funnel logic", "status": "Complete"},
                        {"task": "Design Kafka event structure", "status": "Complete"},
                        {"task": "Implement event processors", "status": "In Progress"}
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
                        "Database connection pooling optimized",
                        "Parallel processing implemented safely"
                    ],
                    "tasks": [
                        {"task": "Profile current migration performance", "status": "Complete"},
                        {"task": "Implement parallel processing", "status": "In Progress"},
                        {"task": "Optimize database queries", "status": "In Progress"}
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
                "steps_taken": ["Verified database connectivity", "Checked Kafka consumer lag", "Reviewed error logs"],
                "next_actions": ["Contact upstream team", "Implement temporary workaround", "Schedule fix deployment"]
            },
            {
                "id": "INC0012901", 
                "title": "Dual eligibility conflict for UHC123456", 
                "priority": "P3", 
                "status": "Resolved",
                "description": "Member showing conflicting eligibility status between UHC and Optum systems",
                "steps_taken": ["Investigated member data", "Applied eligibility fix", "Verified resolution"],
                "next_actions": ["Monitor for recurrence", "Update documentation"]
            }
        ],
        "on_call_schedule": [
            {"week": "Current", "engineer": "Scott Forsmann", "phone": "612-555-0134"},
            {"week": "Next", "engineer": "Ravali Botta", "phone": "612-555-0178"},
            {"week": "Following", "engineer": "Michael Joyce", "phone": "612-555-0189"}
        ]
    },
    "engineering_manager": {
        "direct_reports": [
            {"name": "Rishab Bhat", "team": "Taj Mahal", "role": "Associate SWE", "current_sprint_load": "80%", "performance": "Meeting Expectations"},
            {"name": "Britney Duratinsky", "team": "Taj Mahal", "role": "Associate SWE", "current_sprint_load": "95%", "performance": "Exceeds Expectations"},
            {"name": "Scott Forsmann", "team": "Taj Mahal", "role": "Associate SWE", "current_sprint_load": "85%", "performance": "Meeting Expectations"},
            {"name": "Michael Joyce", "team": "Machu Picchu", "role": "Senior SWE", "current_sprint_load": "90%", "performance": "Exceeds Expectations"},
            {"name": "Sofia Khan", "team": "Machu Picchu", "role": "Associate SWE", "current_sprint_load": "75%", "performance": "Meeting Expectations"},
            {"name": "Ravali Botta", "team": "Machu Picchu", "role": "Software Engineer", "current_sprint_load": "100%", "performance": "Exceeds Expectations"}
        ],
        "team_performance": {
            "taj_mahal": {"velocity": 42, "target": 45, "efficiency": "93%", "satisfaction": 4.1, "issues": 1},
            "machu_picchu": {"velocity": 38, "target": 40, "efficiency": "95%", "satisfaction": 4.3, "issues": 2}
        },
        "upcoming_reviews": [
            {"employee": "Rishab Bhat", "type": "Quarterly Review", "date": "2025-02-15", "status": "Scheduled"},
            {"employee": "Michael Joyce", "type": "Promotion Discussion", "date": "2025-02-20", "status": "Prep Needed"},
            {"employee": "Sofia Khan", "type": "Career Planning", "date": "2025-02-25", "status": "Scheduled"}
        ],
        "budget_overview": {
            "team_salary_budget": {"used": 2.1, "allocated": 2.3, "percentage": 91},
            "contractor_budget": {"used": 0.8, "allocated": 1.0, "percentage": 80},
            "training_budget": {"used": 15000, "allocated": 25000, "percentage": 60}
        },
        "hiring_pipeline": [
            {"position": "Senior Software Engineer", "team": "Taj Mahal", "candidates": 3, "stage": "Final Interviews"},
            {"position": "Associate Software Engineer", "team": "Machu Picchu", "candidates": 2, "stage": "Technical Screen"}
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
            {"name": "Ravali Botta", "role": "Software Engineer", "current_task": "LY-1852 - Eligibility rule migration framework"},
            {"name": "Shasikumar Bommineni", "role": "Contractor", "current_task": "LY-1853 - User-friendly error messages"}
        ],
        "code_reviews": [
            {"pr": "PR #234", "author": "Sofia Khan", "title": "Add device sync retry logic", "status": "Needs Review"},
            {"pr": "PR #236", "author": "Ravali Botta", "title": "Eligibility rule refactor", "status": "Changes Requested"}
        ],
        "architecture_decisions": [
            {"topic": "Kafka Topic Partitioning Strategy", "status": "Under Review", "owner": "Michael Joyce"},
            {"topic": "Database Connection Pool Sizing", "status": "Approved", "owner": "Ravali Botta"}
        ]
    },
    "director": {
        "team_burndown": {
            "taj_mahal": {"planned": 42, "completed": 28, "remaining": 14, "velocity": "On Track"},
            "machu_picchu": {"planned": 38, "completed": 31, "remaining": 7, "velocity": "Ahead"},
            "acropolis": {"planned": 35, "completed": 22, "remaining": 13, "velocity": "At Risk"},
            "pyramids": {"planned": 30, "completed": 26, "remaining": 4, "velocity": "Ahead"}
        },
        "quarterly_metrics": {
            "deployment_frequency": {"current": 12, "target": 15, "trend": "improving"},
            "incident_rate": {"current": 2.3, "target": 2.0, "trend": "stable"},
            "team_satisfaction": {"current": 4.2, "target": 4.0, "trend": "improving"}
        }
    },
    "product_manager": {
        "active_epics": [
            {"epic": "EPIC-101", "title": "Kafka Migration Initiative", "progress": 65, "target_date": "2025-03-15", "status": "On Track"},
            {"epic": "EPIC-102", "title": "Mobile App Integration", "progress": 30, "target_date": "2025-04-30", "status": "At Risk"},
            {"epic": "EPIC-103", "title": "Advanced Analytics Dashboard", "progress": 85, "target_date": "2025-02-28", "status": "Ahead"}
        ],
        "feature_requests": [
            {"id": "FR-445", "title": "Biometric device integration", "votes": 23, "business_value": "High"},
            {"id": "FR-446", "title": "Family plan optimization", "votes": 18, "business_value": "Medium"},
            {"id": "FR-447", "title": "Personalized health goals", "votes": 31, "business_value": "High"}
        ]
    },
    "scrum_master": {
        "team_health": {
            "taj_mahal": {"velocity_trend": "stable", "blockers": 1, "satisfaction": 4.1, "capacity": "80%"},
            "machu_picchu": {"velocity_trend": "improving", "blockers": 2, "satisfaction": 4.3, "capacity": "95%"},
            "acropolis": {"velocity_trend": "declining", "blockers": 3, "satisfaction": 3.7, "capacity": "70%"},
            "pyramids": {"velocity_trend": "stable", "blockers": 0, "satisfaction": 4.0, "capacity": "85%"}
        },
        "upcoming_ceremonies": [
            {"ceremony": "Sprint Planning", "team": "Taj Mahal", "date": "2025-01-29", "duration": "2 hours"},
            {"ceremony": "Retrospective", "team": "Machu Picchu", "date": "2025-01-30", "duration": "1 hour"},
            {"ceremony": "Backlog Refinement", "team": "All Teams", "date": "2025-02-01", "duration": "1.5 hours"}
        ],
        "impediments": [
            {"team": "Taj Mahal", "impediment": "Waiting for platform team Kafka setup", "days_open": 3, "severity": "High"},
            {"team": "Machu Picchu", "impediment": "Database migration approval pending", "days_open": 7, "severity": "Medium"},
            {"team": "Acropolis", "impediment": "Resource allocation conflicts", "days_open": 12, "severity": "High"}
        ]
    }
}

# Custom CSS for better UI
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
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
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
    
    .clickable-button {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin-top: 0.5rem;
        border-radius: 6px;
        background: rgba(255, 255, 255, 0.2);
        cursor: pointer;
        transition: background 0.2s ease;
    }
    
    .clickable-button:hover {
        background: rgba(255, 255, 255, 0.3);
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

@st.cache_data
def load_documents(directory: str) -> List:
    """Load documents from directory"""
    documents = []
    supported_extensions = {'.txt', '.pdf', '.md', '.py', '.js', '.json', '.csv'}
    
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        return documents
    
    files = list(Path(directory).rglob('*'))
    total_files = len([f for f in files if f.is_file() and f.suffix.lower() in supported_extensions])
    
    if total_files == 0:
        return documents
    
    for file_path in files:
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            try:
                if file_path.suffix.lower() == '.pdf':
                    loader = PyPDFLoader(str(file_path))
                else:
                    loader = TextLoader(str(file_path), encoding='utf-8')
                
                docs = loader.load()
                for doc in docs:
                    doc.metadata['source'] = str(file_path)
                    doc.metadata['filename'] = file_path.name
                    doc.metadata['type'] = file_path.suffix[1:]
                
                documents.extend(docs)
                
            except Exception as e:
                logger.warning(f"Failed to load {file_path}: {e}")
    
    return documents

class SimpleVectorStore:
    """Simple in-memory vector store using cosine similarity"""
    def __init__(self, documents, embeddings):
        self.documents = documents
        self.embeddings = embeddings
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
    
    def similarity_search(self, query, k=3):
        """Find most similar documents to query"""
        if not self.documents:
            return []
        
        try:
            # Get query embedding
            query_embedding = self.embedding_model.embed_query(query)
            query_embedding = np.array(query_embedding).reshape(1, -1)
            
            # Calculate similarities
            similarities = cosine_similarity(query_embedding, self.embeddings)[0]
            
            # Get top k indices
            top_indices = np.argsort(similarities)[::-1][:k]
            
            # Return top documents
            return [self.documents[i] for i in top_indices]
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return self.documents[:k] if len(self.documents) >= k else self.documents

@st.cache_resource
def create_vectorstore(_documents: List):
    """Create and cache vector store"""
    if not _documents:
        return None
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
        length_function=len
    )
    
    chunks = text_splitter.split_documents(_documents)
    
    # Create embeddings
    embeddings_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'}
    )
    
    # Get embeddings for all chunks
    texts = [chunk.page_content for chunk in chunks]
    embeddings = embeddings_model.embed_documents(texts)
    embeddings_array = np.array(embeddings)
    
    # Create simple vector store
    vectorstore = SimpleVectorStore(chunks, embeddings_array)
    
    return vectorstore

def get_relevant_context(question: str, vectorstore, k: int = 3) -> str:
    """Retrieve relevant context from vector store"""
    if not vectorstore:
        return "No documents available for context."
    
    try:
        docs = vectorstore.similarity_search(question, k=k)
        context_parts = []
        
        for doc in docs:
            context_parts.append(doc.page_content)
        
        context = "\n\n---\n\n".join(context_parts)
        return context
        
    except Exception as e:
        logger.error(f"Error retrieving context: {e}")
        return "Error retrieving context."

def generate_answer_with_ai(question: str, context: str, client, user_info) -> str:
    """Generate answer using AI API"""
    if not client:
        return "❌ AI client not available. Please check your API key."
    
    role_context = f"You are LoyaltyAI, responding to {user_info['name']}, a {user_info['role']} on the {user_info['team']} team."
    
    prompt = f"""{role_context}

Based on the following context from team documents, answer the user's question. Be helpful, accurate, and concise. Do not mention document sources or provide citations. Give direct, actionable answers.

Context from team documents:
{context}

User question: {question}

Provide a concise, direct answer without mentioning sources."""

    try:
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=800,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
        
        return response.content[0].text
        
    except Exception as e:
        logger.error(f"Error calling AI API: {e}")
        return f"❌ Error generating response: {str(e)}"

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
                
                if st.button(f"Open {story['id']} in Rally", key=f"story_btn_{i}"):
                    st.success(f"Opening Rally story {story['id']} in new tab...")
            
            st.markdown(f'<div class="{card_class}"><strong>{story["id"]}</strong> - {story["title"]}<br><span class="status-badge">{story["status"]}</span> <span style="float: right; font-size: 1.2em; font-weight: bold;">{story["points"]} pts</span></div>', unsafe_allow_html=True)
        
        st.markdown("#### 🚨 My Incidents")
        for i, incident in enumerate(DASHBOARD_DATA["individual"]["my_incidents"]):
            card_class = "dashboard-card-danger" if incident['priority'] == 'P1' else "dashboard-card" if incident['priority'] == 'P2' else "dashboard-card-success"
            
            with st.expander(f"🚨 {incident['id']} - {incident['title']}", expanded=False):
                st.markdown(f"**Priority:** {incident['priority']}")
                st.markdown(f"**Status:** {incident['status']}")
                st.markdown(f"**Description:** {incident['description']}")
                
                st.markdown("**Steps Taken:**")
                for step in incident['steps_taken']:
                    st.markdown(f"• {step}")
                
                st.markdown("**Next Actions:**")
                for action in incident['next_actions']:
                    st.markdown(f"• {action}")
                
                if st.button(f"Update {incident['id']}", key=f"incident_btn_{i}"):
                    st.success(f"Opening ServiceNow incident {incident['id']} for update...")
            
            st.markdown(f'<div class="{card_class}"><strong>{incident["id"]}</strong> - {incident["title"]}<br><span class="status-badge">{incident["priority"]}</span> <span style="float: right; font-weight: bold;">{incident["status"]}</span></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📅 On-Call Schedule")
        for schedule in DASHBOARD_DATA["individual"]["on_call_schedule"]:
            card_class = "dashboard-card-danger" if schedule['week'] == 'Current' else "dashboard-card"
            st.markdown(f'<div class="{card_class}"><strong>{schedule["week"]} Week</strong><br>{schedule["engineer"]}<br><div class="clickable-button">📞 {schedule["phone"]}</div></div>', unsafe_allow_html=True)

def render_senior_engineer_dashboard(user_info):
    """Render dashboard for senior engineers"""
    st.markdown(f"### 👨‍💼 {user_info['name']} - {user_info['team']} Team Lead")
    
    metrics = DASHBOARD_DATA["senior_engineer"]["team_metrics"]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div class="dashboard-card-success"><div class="metric-number">{metrics["sprint_velocity"]}</div><strong>Sprint Velocity</strong><br><small>Story Points</small></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="dashboard-card-alt"><div class="metric-number">{metrics["code_coverage"]}%</div><strong>Code Coverage</strong><br><small>Target: 85%</small></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<div class="dashboard-card"><div class="metric-number">{metrics["bug_escape_rate"]}</div><strong>Bug Escape Rate</strong><br><small>Target: under 2%</small></div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'<div class="dashboard-card"><div class="metric-number">{metrics["avg_cycle_time"]}</div><strong>Avg Cycle Time</strong><br><small>Days</small></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👥 Team Members & Current Tasks")
        for i, member in enumerate(DASHBOARD_DATA["senior_engineer"]["team_members"]):
            if st.button(f"Message {member['name']}", key=f"member_{i}"):
                st.info(f"Opening Slack DM with {member['name']}...")
            st.markdown(f'<div class="dashboard-card"><strong>{member["name"]}</strong> - {member["role"]}<br><small>{member["current_task"]}</small><br><div class="clickable-button">💬 Slack</div></div>', unsafe_allow_html=True)
        
        st.markdown("#### 🔍 Code Reviews Pending")
        for i, pr in enumerate(DASHBOARD_DATA["senior_engineer"]["code_reviews"]):
            card_class = "dashboard-card-success" if pr['status'] == 'Approved' else "dashboard-card" if pr['status'] == 'Needs Review' else "dashboard-card-danger"
            if st.button(f"Review {pr['pr']}", key=f"pr_{i}"):
                st.info(f"Opening {pr['pr']} in GitHub...")
            st.markdown(f'<div class="{card_class}"><strong>{pr["pr"]}</strong> by {pr["author"]}<br>{pr["title"]}<br><span class="status-badge">{pr["status"]}</span></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🏗️ Architecture Decisions")
        for i, decision in enumerate(DASHBOARD_DATA["senior_engineer"]["architecture_decisions"]):
            card_class = "dashboard-card-success" if decision['status'] == 'Approved' else "dashboard-card-alt" if decision['status'] == 'Under Review' else "dashboard-card"
            if st.button(f"Edit Decision", key=f"decision_{i}"):
                st.info(f"Opening architecture decision: {decision['topic']}")
            st.markdown(f'<div class="{card_class}"><strong>{decision["topic"]}</strong><br>Owner: {decision["owner"]}<br><span class="status-badge">{decision["status"]}</span></div>', unsafe_allow_html=True)

def render_engineering_manager_dashboard(user_info):
    """Render dashboard for engineering manager"""
    st.markdown(f"### 👩‍💼 {user_info['name']} - Engineering Manager")
    
    # Team performance overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="dashboard-card-success"><div class="metric-number">12</div><strong>Direct Reports</strong><br><small>Onshore Teams</small></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="dashboard-card-alt"><div class="metric-number">4.2</div><strong>Avg Team Satisfaction</strong><br><small>Target: 4.0</small></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="dashboard-card"><div class="metric-number">94%</div><strong>Team Efficiency</strong><br><small>Sprint Completion</small></div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="dashboard-card-success"><div class="metric-number">5</div><strong>Open Positions</strong><br><small>Hiring Pipeline</small></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👥 Direct Reports Performance")
        for i, report in enumerate(DASHBOARD_DATA["engineering_manager"]["direct_reports"]):
            card_class = "dashboard-card-success" if report['performance'] == 'Exceeds Expectations' else "dashboard-card-alt" if report['performance'] == 'Meeting Expectations' else "dashboard-card"
            
            if st.button(f"1:1 with {report['name']}", key=f"report_{i}"):
                st.info(f"Scheduling 1:1 meeting with {report['name']}...")
            
            st.markdown(f'<div class="{card_class}"><strong>{report["name"]}</strong> - {report["team"]}<br>{report["role"]} | Load: {report["current_sprint_load"]}<br><span class="status-badge">{report["performance"]}</span></div>', unsafe_allow_html=True)
        
        st.markdown("#### 📊 Team Performance Metrics")
        for team, performance in DASHBOARD_DATA["engineering_manager"]["team_performance"].items():
            card_class = "dashboard-card-success" if performance['efficiency'] == '95%' else "dashboard-card-alt"
            velocity_pct = round((performance['velocity'] / performance['target']) * 100)
            
            st.markdown(f'<div class="{card_class}"><strong>{team.replace("_", " ").title()} Team</strong><br>Velocity: {performance["velocity"]}/{performance["target"]} ({velocity_pct}%)<br>Satisfaction: {performance["satisfaction"]}/5.0 | Issues: {performance["issues"]}<br><span class="status-badge">{performance["efficiency"]} Efficiency</span></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📅 Upcoming Reviews")
        for i, review in enumerate(DASHBOARD_DATA["engineering_manager"]["upcoming_reviews"]):
            card_class = "dashboard-card-danger" if review['status'] == 'Prep Needed' else "dashboard-card"
            
            if st.button(f"Prepare {review['type']}", key=f"review_{i}"):
                st.info(f"Opening preparation notes for {review['employee']} {review['type']}...")
            
            st.markdown(f'<div class="{card_class}"><strong>{review["employee"]}</strong><br>{review["type"]}<br>📅 {review["date"]}<br><span class="status-badge">{review["status"]}</span></div>', unsafe_allow_html=True)
        
        st.markdown("#### 💰 Budget Overview")
        budget = DASHBOARD_DATA["engineering_manager"]["budget_overview"]
        
        for budget_type, data in budget.items():
            card_class = "dashboard-card-success" if data['percentage'] < 85 else "dashboard-card" if data['percentage'] < 95 else "dashboard-card-danger"
            budget_name = budget_type.replace('_', ' ').title()
            
            if budget_type == "training_budget":
                st.markdown(f'<div class="{card_class}"><strong>{budget_name}</strong><br>${data["used"]:,} / ${data["allocated"]:,}<br><span class="status-badge">{data["percentage"]}% Used</span></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="{card_class}"><strong>{budget_name}</strong><br>${data["used"]}M / ${data["allocated"]}M<br><span class="status-badge">{data["percentage"]}% Used</span></div>', unsafe_allow_html=True)
        
        st.markdown("#### 🎯 Active Hiring")
        for i, hire in enumerate(DASHBOARD_DATA["engineering_manager"]["hiring_pipeline"]):
            if st.button(f"Review {hire['position']} Candidates", key=f"hire_{i}"):
                st.info(f"Opening candidate pipeline for {hire['position']}...")
            
            st.markdown(f'<div class="dashboard-card-alt"><strong>{hire["position"]}</strong><br>Team: {hire["team"]}<br>Candidates: {hire["candidates"]} | Stage: {hire["stage"]}<br><div class="clickable-button">👥 Review Pipeline</div></div>', unsafe_allow_html=True)

def render_product_manager_dashboard(user_info):
    """Render dashboard for product manager"""
    st.markdown(f"### 📊 {user_info['name']} - Product Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Active Epics")
        for i, epic in enumerate(DASHBOARD_DATA["product_manager"]["active_epics"]):
            card_class = "dashboard-card-success" if epic['status'] == 'Ahead' else "dashboard-card" if epic['status'] == 'On Track' else "dashboard-card-danger"
            
            if st.button(f"View {epic['epic']} Details", key=f"epic_{i}"):
                st.info(f"Opening epic {epic['epic']} roadmap...")
            
            progress_bar = f'<div style="background-color: rgba(255,255,255,0.2); border-radius: 10px; padding: 5px; margin: 5px 0;"><div style="background-color: #10b981; height: 10px; width: {epic["progress"]}%; border-radius: 5px;"></div></div>'
            st.markdown(f'<div class="{card_class}"><strong>{epic["epic"]}</strong> - {epic["title"]}<br>{progress_bar}{epic["progress"]}% Complete | Due: {epic["target_date"]}<br><span class="status-badge">{epic["status"]}</span></div>', unsafe_allow_html=True)
        
        st.markdown("#### 📝 Top Feature Requests")
        for i, request in enumerate(DASHBOARD_DATA["product_manager"]["feature_requests"]):
            card_class = "dashboard-card-alt" if request['business_value'] == 'High' else "dashboard-card"
            if st.button(f"Review {request['id']}", key=f"feature_{i}"):
                st.info(f"Opening feature request {request['id']}...")
            st.markdown(f'<div class="{card_class}"><strong>{request["id"]}</strong> - {request["title"]}<br><span class="status-badge">👥 {request["votes"]} votes</span><span style="float: right; font-weight: bold;">{request["business_value"]} Value</span></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📈 User Feedback Overview")
        st.markdown('<div class="dashboard-card-success"><strong>App Performance</strong><br>Rating: 4.2/5.0<br><span class="status-badge">📈 Improving</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-card"><strong>Feature Usability</strong><br>Rating: 3.8/5.0<br><span class="status-badge">📊 Stable</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="dashboard-card-success"><strong>Reward System</strong><br>Rating: 4.5/5.0<br><span class="status-badge">📈 Improving</span></div>', unsafe_allow_html=True)

def render_scrum_master_dashboard(user_info):
    """Render dashboard for scrum master"""
    st.markdown(f"### 🏃‍♀️ {user_info['name']} - Agile Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏥 Team Health Overview")
        health_data = DASHBOARD_DATA["scrum_master"]["team_health"]
        
        for i, (team, health) in enumerate(health_data.items()):
            card_class = "dashboard-card-success" if health['satisfaction'] > 4.0 else "dashboard-card" if health['satisfaction'] > 3.5 else "dashboard-card-danger"
            trend_icon = "📈" if health['velocity_trend'] == 'improving' else "📉" if health['velocity_trend'] == 'declining' else "📊"
            
            if st.button(f"Team Retrospective - {team.title()}", key=f"retro_{i}"):
                st.info(f"Scheduling retrospective for {team.replace('_', ' ').title()} team...")
            
            st.markdown(f'<div class="{card_class}"><strong>{team.replace("_", " ").title()}</strong><br>Satisfaction: {health["satisfaction"]}/5.0 | Capacity: {health["capacity"]}<br>Blockers: {health["blockers"]} | {trend_icon} {health["velocity_trend"]}<br><div class="clickable-button">🔄 Retrospective</div></div>', unsafe_allow_html=True)
        
        st.markdown("#### 🚧 Active Impediments")
        for i, impediment in enumerate(DASHBOARD_DATA["scrum_master"]["impediments"]):
            card_class = "dashboard-card-danger" if impediment['severity'] == 'High' else "dashboard-card"
            if st.button(f"Resolve Impediment", key=f"impediment_{i}"):
                st.info(f"Working to resolve: {impediment['impediment']}")
            st.markdown(f'<div class="{card_class}"><strong>{impediment["team"]}</strong><br>{impediment["impediment"]}<br><span class="status-badge">{impediment["severity"]}</span><small style="float: right;">{impediment["days_open"]} days open</small></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📅 Upcoming Ceremonies")
        for i, ceremony in enumerate(DASHBOARD_DATA["scrum_master"]["upcoming_ceremonies"]):
            if st.button(f"Join {ceremony['ceremony']}", key=f"ceremony_{i}"):
                st.info(f"Joining {ceremony['ceremony']} for {ceremony['team']}...")
            st.markdown(f'<div class="dashboard-card-alt"><strong>{ceremony["ceremony"]}</strong><br>Team: {ceremony["team"]}<br>📅 {ceremony["date"]} | ⏱️ {ceremony["duration"]}<br><div class="clickable-button">🔗 Join Meeting</div></div>', unsafe_allow_html=True)
    """Render dashboard for director"""
    st.markdown(f"### 🎯 {user_info['name']} - Leadership Dashboard")
    
    st.markdown("#### 📊 Team Sprint Burndown")
    for team, data in DASHBOARD_DATA["director"]["team_burndown"].items():
        card_class = "dashboard-card-success" if data['velocity'] == 'Ahead' else "dashboard-card-alt" if data['velocity'] == 'On Track' else "dashboard-card-danger"
        completion_pct = round((data['completed'] / data['planned']) * 100)
        team_name = team.replace('_', ' ').title()
        st.markdown(f'<div class="{card_class}"><strong>{team_name}</strong><br>Progress: {data["completed"]}/{data["planned"]} ({completion_pct}%)<br><span class="status-badge">{data["velocity"]}</span><div class="clickable-button">📈 Details</div></div>', unsafe_allow_html=True)
    
    st.markdown("#### 📈 Quarterly Metrics")
    for metric_name, metric_data in DASHBOARD_DATA["director"]["quarterly_metrics"].items():
        display_name = metric_name.replace('_', ' ').title()
        trend_text = metric_data['trend'].title()
        st.markdown(f'<div class="dashboard-card"><strong>{display_name}</strong><br>Current: {metric_data["current"]} | Target: {metric_data["target"]}<br>Trend: {trend_text}</div>', unsafe_allow_html=True)

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
            st.error("❌ LoyaltyAI Not Connected")
        
        st.markdown("---")
        
        docs_directory = st.text_input("📁 Documents Directory", value="./docs")
        
        if st.button("🔄 Refresh Documents"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.rerun()
    
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
        documents = load_documents(docs_directory)
        vectorstore = create_vectorstore(documents)
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"], avatar="🤖" if message["role"] == "assistant" else "👤"):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("💬 Ask me anything about your team's work..."):
            if not client:
                st.error("❌ Please configure your LoyaltyAI API key first!")
                return
            
            if not documents:
                st.error("❌ No documents found. Please add documents to the specified directory.")
                return
            
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("user", avatar="👤"):
                st.markdown(prompt)
            
            with st.chat_message("assistant", avatar="🤖"):
                context = get_relevant_context(prompt, vectorstore, k=3)
                answer = generate_answer_with_ai(prompt, context, client, user_info)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()
