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

# Dashboard data - Complete and properly structured
DASHBOARD_DATA = {
    "director": {
        "team_burndown": {
            "taj_mahal": {
                "planned": 42, 
                "completed": 28, 
                "remaining": 14,
                "velocity": "On Track",
                "team_lead": "Michael Joyce",
                "focus_areas": ["Source System Ranking", "Top of Funnel Migration", "Database Performance"],
                "blockers": 1,
                "satisfaction": 4.1,
                "recent_achievements": ["Reduced API timeout errors by 60%", "Kafka migration 70% complete"]
            },
            "machu_picchu": {
                "planned": 38, 
                "completed": 31, 
                "remaining": 7,
                "velocity": "Ahead",
                "team_lead": "Michael Joyce", 
                "focus_areas": ["Eligibility Processing", "Device Integrations", "Performance Testing"],
                "blockers": 2,
                "satisfaction": 4.3,
                "recent_achievements": ["Device sync reliability improved 40%", "Load testing automation complete"]
            },
            "acropolis": {
                "planned": 35,
                "completed": 22,
                "remaining": 13, 
                "velocity": "At Risk",
                "team_lead": "Raj Patel",
                "focus_areas": ["Platform Stability", "Monitoring", "Legacy System Maintenance"],
                "blockers": 3,
                "satisfaction": 3.7,
                "recent_achievements": ["Monitoring dashboard deployed", "Reduced incident response time by 25%"]
            },
            "pyramids": {
                "planned": 30,
                "completed": 26,
                "remaining": 4,
                "velocity": "Ahead",
                "team_lead": "Priya Sharma",
                "focus_areas": ["QA Automation", "Testing Infrastructure", "Quality Gates"],
                "blockers": 0,
                "satisfaction": 4.0,
                "recent_achievements": ["Automated test coverage 95%", "Zero production defects last sprint"]
            }
        },
        "quarterly_metrics": {
            "deployment_frequency": {
                "current": 12, 
                "target": 15, 
                "trend": "improving",
                "q4_2024": 8,
                "improvement": "+50%"
            },
            "incident_rate": {
                "current": 2.3, 
                "target": 2.0, 
                "trend": "stable",
                "p1_incidents": 0,
                "p2_incidents": 3,
                "mttr": "45 minutes"
            },
            "team_satisfaction": {
                "current": 4.2, 
                "target": 4.0, 
                "trend": "improving",
                "participation_rate": "94%",
                "key_drivers": ["Work-life balance", "Technical challenges", "Career growth"]
            },
            "velocity_consistency": {
                "current": 85,
                "target": 90,
                "trend": "improving",
                "predictability_score": "High"
            },
            "code_quality": {
                "coverage": "89%",
                "sonar_gate": "Passing",
                "tech_debt_ratio": "12%",
                "security_issues": 0
            }
        },
        "budget_status": {
            "q1_personnel": {"used": 1.2, "allocated": 1.5, "percentage": 80, "forecast": "Under budget"},
            "q1_infrastructure": {"used": 0.3, "allocated": 0.4, "percentage": 75, "trend": "stable"},
            "q2_forecast": {"personnel": 1.8, "infrastructure": 0.5, "training": 0.2, "tools": 0.1}
        },
        "strategic_initiatives": [
            {
                "name": "Platform Modernization",
                "status": "On Track", 
                "completion": 65,
                "owner": "Engineering Teams",
                "key_milestones": ["Kafka Migration (70% complete)", "Database Optimization (40% complete)", "API Modernization (Planning)"],
                "budget": "$2.1M allocated",
                "timeline": "Q1-Q3 2025"
            },
            {
                "name": "Scalability Enhancement", 
                "status": "Planning",
                "completion": 15,
                "owner": "Platform Team",
                "key_milestones": ["Architecture Review (Complete)", "Capacity Planning (In Progress)", "Implementation (Q2)"],
                "budget": "$1.5M allocated",
                "timeline": "Q2-Q4 2025"
            },
            {
                "name": "Developer Experience Improvement",
                "status": "On Track",
                "completion": 45,
                "owner": "All Teams",
                "key_milestones": ["CI/CD Enhancement (80%)", "Testing Automation (90%)", "Documentation Portal (60%)"],
                "budget": "$800K allocated",
                "timeline": "Q1-Q2 2025"
            }
        ],
        "risk_register": [
            {
                "risk": "Kafka Migration Timeline Slip",
                "probability": "Medium",
                "impact": "High", 
                "mitigation": "Additional contractor resources allocated, fallback plan prepared",
                "owner": "Allesha Fogle",
                "status": "Monitoring"
            },
            {
                "risk": "Key Engineer Attrition",
                "probability": "Low",
                "impact": "High",
                "mitigation": "Retention bonuses, career development plans, competitive compensation review",
                "owner": "Christopher Jimenez",
                "status": "Mitigated"
            },
            {
                "risk": "Database Performance Degradation",
                "probability": "Medium",
                "impact": "Medium",
                "mitigation": "Proactive monitoring, performance optimization sprint planned",
                "owner": "Scott Forsmann",
                "status": "In Progress"
            }
        ],
        "hiring_pipeline": [
            {"position": "Senior Software Engineer", "team": "Taj Mahal", "candidates": 3, "stage": "Final Interviews", "hire_date": "2025-02-15"},
            {"position": "DevOps Engineer", "team": "Platform", "candidates": 2, "stage": "Technical Assessment", "hire_date": "2025-03-01"},
            {"position": "Product Manager", "team": "Product", "candidates": 4, "stage": "Offer Extended", "hire_date": "2025-02-01"},
            {"position": "QA Automation Engineer", "team": "Pyramids", "candidates": 1, "stage": "Background Check", "hire_date": "2025-01-30"}
        ],
        "compliance_status": {
            "security_reviews": {"completed": 12, "planned": 15, "overdue": 0},
            "privacy_assessments": {"completed": 8, "planned": 10, "critical": 0},
            "audit_findings": {"open": 2, "closed_this_quarter": 8, "high_priority": 0}
        }
    },
    "individual": {
        "rishab": {
            "my_stories": [
                {
                    "id": "LY-1847",
                    "title": "Implement Source System Ranking Algorithm",
                    "status": "In Progress",
                    "points": 8,
                    "acceptance_criteria": [
                        "System can rank member data sources by reliability score (0-100)",
                        "Algorithm handles conflicts between UHC and Optum data sources", 
                        "Performance meets SLA of under 200ms response time for 10K requests",
                        "All edge cases documented and tested (duplicate members, null values)",
                        "Integration with existing Loyalty-Member service APIs",
                        "Configurable weighting system for different data quality metrics"
                    ],
                    "tasks": [
                        {"task": "Design ranking algorithm with weighted scoring", "status": "Complete"},
                        {"task": "Implement core logic with Spring Boot service", "status": "In Progress"},
                        {"task": "Add comprehensive unit tests (JUnit)", "status": "To Do"},
                        {"task": "Performance testing with 50K member dataset", "status": "To Do"},
                        {"task": "Integration testing with Kafka event streams", "status": "To Do"},
                        {"task": "Documentation and code review", "status": "To Do"}
                    ],
                    "description": "Build intelligent ranking system to prioritize member data from multiple sources (UHC, Optum, EDG) based on data freshness, completeness, and historical accuracy"
                },
                {
                    "id": "LY-1863",
                    "title": "Source System Health Monitoring Dashboard",
                    "status": "Code Review",
                    "points": 5,
                    "acceptance_criteria": [
                        "Real-time monitoring of all 12 external source systems",
                        "Automated alerts for system degradation via Splunk",
                        "Dashboard shows health status with 99.9% uptime SLA tracking",
                        "Integration with existing Kubernetes health checks"
                    ],
                    "tasks": [
                        {"task": "Set up monitoring endpoints for all source systems", "status": "Complete"},
                        {"task": "Configure Splunk alerting rules and thresholds", "status": "Complete"},
                        {"task": "Create React dashboard with real-time updates", "status": "In Review"},
                        {"task": "Add automated failover logic", "status": "In Review"}
                    ],
                    "description": "Monitor health and availability of external data sources including UHC eligibility API, device integration services, and pharmacy systems"
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
                        "All Top of Funnel logic converted to event-driven Kafka processing",
                        "Zero data loss during migration (validated with checksums)",
                        "Performance matches or exceeds current batch processing (4-6 hours)",
                        "Rollback plan validated and tested in stage environment"
                    ],
                    "tasks": [
                        {"task": "Analyze current Top of Funnel Perl script (2000+ lines)", "status": "Complete"},
                        {"task": "Design Kafka event structure and schema", "status": "Complete"},
                        {"task": "Implement Java Spring Boot event processors", "status": "In Progress"},
                        {"task": "Set up Kafka topics with proper partitioning", "status": "In Progress"}
                    ],
                    "description": "Replace legacy Perl script (daily batch processing) with modern event-driven Kafka architecture for real-time member eligibility processing"
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
                        "Migration performance improved by 50% (from 12hrs to 6hrs)",
                        "Database connection pooling optimized for 10M+ member records",
                        "Parallel processing implemented with thread safety guarantees",
                        "Data integrity maintained with checksum validation"
                    ],
                    "tasks": [
                        {"task": "Profile current migration performance bottlenecks", "status": "Complete"},
                        {"task": "Implement parallel processing with ExecutorService", "status": "In Progress"},
                        {"task": "Optimize database queries and connection pooling", "status": "In Progress"}
                    ],
                    "description": "Optimize large-scale member data migration processes for annual enrollment period handling 15M+ member records"
                }
            ]
        },
        "my_incidents": [
            {
                "id": "INC0012845", 
                "title": "Member eligibility sync failure - UHC API timeout", 
                "priority": "P2", 
                "status": "In Progress", 
                "description": "UHC member eligibility API experiencing intermittent timeouts (>30s response time) causing 15% of eligibility checks to fail during peak hours",
                "steps_taken": [
                    "Verified database connectivity - all connections healthy",
                    "Checked Kafka consumer lag - normal processing times",
                    "Reviewed error logs - 500+ timeout errors in last 4 hours",
                    "Contacted UHC API team - investigating on their end",
                    "Implemented temporary retry logic with exponential backoff"
                ],
                "next_actions": [
                    "Escalate to UHC API team lead (John Smith)",
                    "Implement circuit breaker pattern for API calls",
                    "Schedule fix deployment for tonight's maintenance window",
                    "Add enhanced monitoring for API response times"
                ],
                "impact": "Affecting 5,000+ members per hour during peak enrollment",
                "assigned_to": "Rishab Bhat",
                "created_date": "2025-01-20 09:30:00",
                "sla_breach": False
            }
        ],
        "on_call_schedule": [
            {"week": "Current (Jan 20-26)", "engineer": "Scott Forsmann", "phone": "612-555-0134", "backup": "Ravali Botta"},
            {"week": "Next (Jan 27-Feb 2)", "engineer": "Ravali Botta", "phone": "612-555-0178", "backup": "Michael Joyce"},
            {"week": "Following (Feb 3-9)", "engineer": "Michael Joyce", "phone": "612-555-0189", "backup": "Sofia Khan"},
            {"week": "Feb 10-16", "engineer": "Sofia Khan", "phone": "612-555-0167", "backup": "Rishab Bhat"}
        ],
        "recent_deployments": [
            {"version": "v2.1.3", "date": "2025-01-19", "status": "Success", "components": ["loyalty-member", "loyalty-eligibility"]},
            {"version": "v2.1.2", "date": "2025-01-17", "status": "Success", "components": ["loyalty-services"]},
            {"version": "v2.1.1", "date": "2025-01-15", "status": "Rollback", "components": ["loyalty-member"], "reason": "Database migration timeout"}
        ],
        "team_metrics": {
            "sprint_completion": "87%",
            "code_coverage": "92%",
            "avg_cycle_time": "4.2 days",
            "bug_escape_rate": "1.8%"
        }
    },
    "senior_engineer": {
        "team_metrics": {
            "sprint_velocity": 38,
            "velocity_trend": "+12% from last sprint",
            "code_coverage": 87,
            "coverage_trend": "+3% improvement",
            "bug_escape_rate": 2.1,
            "avg_cycle_time": 4.2,
            "team_satisfaction": 4.3,
            "deployment_frequency": "Daily",
            "mttr": "45 minutes"
        },
        "team_members": [
            {
                "name": "Sofia Khan", 
                "role": "Associate SWE", 
                "current_task": "LY-1851 - Device sync reliability improvements",
                "status": "On Track",
                "current_sprint_load": "85%",
                "skills": ["Java", "Spring Boot", "Kafka", "React"],
                "recent_achievements": ["Reduced device sync failures by 40%", "Mentored 2 new contractors"],
                "goals": ["Complete Java certification", "Lead architecture discussions"]
            },
            {
                "name": "Ravali Botta", 
                "role": "Software Engineer", 
                "current_task": "LY-1852 - Eligibility rule migration framework",
                "status": "Ahead",
                "current_sprint_load": "95%",
                "skills": ["Java", "MySQL", "Kubernetes", "Python"],
                "recent_achievements": ["Designed new eligibility framework", "Improved query performance by 30%"],
                "goals": ["Tech lead promotion track", "AWS certification"]
            }
        ],
        "priority_code_reviews": [
            {
                "pr": "PR #234", 
                "author": "Sofia Khan", 
                "title": "Add device sync retry logic with exponential backoff", 
                "status": "Needs Review",
                "complexity": "High",
                "files_changed": 8,
                "urgency": "Critical",
                "description": "Critical fix for device sync failures affecting 15% of Fitbit users",
                "lines_added": 156,
                "lines_deleted": 23,
                "commits": 4,
                "reviewers_needed": 2,
                "estimated_review_time": "45 minutes"
            },
            {
                "pr": "PR #236", 
                "author": "Ravali Botta", 
                "title": "Eligibility rule engine refactor for performance", 
                "status": "Changes Requested",
                "complexity": "Medium", 
                "files_changed": 12,
                "urgency": "Medium",
                "description": "Refactoring eligibility processing for 40% performance improvement",
                "lines_added": 234,
                "lines_deleted": 189,
                "commits": 6,
                "feedback": "Add more comprehensive unit tests, consider edge cases for dual eligibility"
            }
        ]
    },
    "engineering_manager": {
        "direct_reports": [
            {
                "name": "Rishab Bhat", 
                "team": "Taj Mahal", 
                "role": "Associate SWE", 
                "current_sprint_load": "85%",
                "performance": "Meeting Expectations",
                "years_experience": 2.5,
                "key_skills": ["Java", "Spring Boot", "Source System Integration", "Data Processing"],
                "current_focus": "Source System Ranking Algorithm implementation",
                "career_goals": ["Senior SWE promotion", "Architecture knowledge", "Team leadership"],
                "last_review": "2024-12-15",
                "next_review": "2025-03-15",
                "development_areas": ["System design", "Performance optimization"],
                "recent_wins": ["Delivered complex ranking algorithm on time", "Mentored new contractor"]
            },
            {
                "name": "Britney Duratinsky", 
                "team": "Taj Mahal", 
                "role": "Associate SWE", 
                "current_sprint_load": "95%",
                "performance": "Exceeds Expectations",
                "years_experience": 3.0,
                "key_skills": ["Java", "Kafka", "Event-Driven Architecture", "Legacy System Migration"],
                "current_focus": "Top of Funnel Kafka migration leadership",
                "career_goals": ["Tech Lead role", "Architecture specialization", "Cross-team collaboration"],
                "last_review": "2024-12-15", 
                "next_review": "2025-03-15",
                "development_areas": ["Team leadership", "Stakeholder communication"],
                "recent_wins": ["Leading critical Kafka migration", "Reduced processing time by 60%"]
            },
            {
                "name": "Scott Forsmann", 
                "team": "Taj Mahal", 
                "role": "Associate SWE", 
                "current_sprint_load": "80%",
                "performance": "Meeting Expectations",
                "years_experience": 2.0,
                "key_skills": ["Database Optimization", "Data Migration", "Performance Tuning", "MySQL"],
                "current_focus": "Large-scale data migration optimization",
                "career_goals": ["Database expertise", "Performance engineering", "Senior SWE promotion"],
                "last_review": "2024-12-15",
                "next_review": "2025-03-15", 
                "development_areas": ["Distributed systems", "Monitoring and observability"],
                "recent_wins": ["50% improvement in migration performance", "Implemented robust rollback procedures"]
            }
        ],
        "team_performance": {
            "taj_mahal": {
                "velocity": 42, 
                "target": 45, 
                "efficiency": "93%", 
                "satisfaction": 4.1,
                "issues": 1,
                "strengths": ["Strong collaboration", "Technical expertise", "Problem-solving"],
                "areas_for_improvement": ["Story estimation accuracy", "Cross-functional communication"],
                "recent_improvements": ["Reduced technical debt by 15%", "Improved code review turnaround"]
            },
            "machu_picchu": {
                "velocity": 38, 
                "target": 40, 
                "efficiency": "95%", 
                "satisfaction": 4.3,
                "issues": 2,
                "strengths": ["Innovation", "Quality focus", "Mentorship"],
                "areas_for_improvement": ["Capacity planning", "Documentation"],
                "recent_improvements": ["Automated testing coverage 90%+", "Reduced cycle time by 1 day"]
            }
        }
    },
    "product_manager": {
        "active_epics": [
            {
                "epic": "EPIC-101", 
                "title": "Kafka Migration Initiative", 
                "progress": 70, 
                "target_date": "2025-03-15", 
                "status": "On Track",
                "business_value": "$500K annual savings",
                "risk_level": "Medium",
                "dependencies": ["Platform team", "Database migration"],
                "key_features": ["Event-driven eligibility", "Real-time processing", "Legacy script retirement"],
                "success_metrics": ["Processing time <5min", "Zero data loss", "50% cost reduction"]
            },
            {
                "epic": "EPIC-102", 
                "title": "Mobile App Integration", 
                "progress": 30, 
                "target_date": "2025-04-30", 
                "status": "At Risk",
                "business_value": "15% member engagement increase",
                "risk_level": "High",
                "blockers": ["iOS review process", "API rate limiting"],
                "key_features": ["Push notifications", "Activity tracking", "Reward redemption"],
                "success_metrics": ["DAU increase 20%", "App store rating >4.5", "API response <2s"]
            }
        ]
    },
    "scrum_master": {
        "team_health": {
            "taj_mahal": {
                "velocity_trend": "stable", 
                "blockers": 1, 
                "satisfaction": 4.1, 
                "capacity": "85%",
                "team_size": 4,
                "sprint_goal_achievement": "80%",
                "retrospective_actions": 3,
                "key_strengths": ["Technical expertise", "Collaboration"],
                "improvement_areas": ["Story estimation", "Cross-team communication"],
                "last_retrospective": "2025-01-15",
                "upcoming_risks": ["Kafka migration complexity", "Resource constraints"]
            },
            "machu_picchu": {
                "velocity_trend": "improving", 
                "blockers": 2, 
                "satisfaction": 4.3, 
                "capacity": "95%",
                "team_size": 6,
                "sprint_goal_achievement": "90%",
                "retrospective_actions": 2,
                "key_strengths": ["Innovation", "Quality focus", "Knowledge sharing"],
                "improvement_areas": ["Capacity planning", "Documentation"],
                "last_retrospective": "2025-01-16",
                "upcoming_risks": ["High utilization", "Technical debt"]
            }
        }
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

def get_relevant_context(question: str, user_info: dict) -> str:
    """Get context based on question keywords - enhanced with user-specific data"""
    question_lower = question.lower()
    
    # Get user-specific team context
    user_team = user_info.get('team', 'Unknown')
    user_role = user_info.get('role', 'Unknown')
    
    # Extract potential names from the question to check against our database
    potential_names = []
    words = question_lower.split()
    for i, word in enumerate(words):
        if word in ['who', 'whos', "who's"] and i + 1 < len(words):
            potential_names.append(words[i + 1])
        elif word in ['about', 'find', 'tell'] and i + 1 < len(words):
            potential_names.append(words[i + 1])
    
    # Check if asking about someone not in our team database
    known_people = ['rishab', 'britney', 'scott', 'michael', 'sofia', 'ravali', 'allesha', 'christopher', 'connie', 'swapna', 'shasikumar', 'ganesh', 'nagarjuna', 'ajit']
    for name in potential_names:
        clean_name = name.lower().strip('.,?!')
        if clean_name not in known_people and len(clean_name) > 2:
            return f"I don't have information about '{name}' in our current team database. The people I know about include the Taj Mahal team (Rishab Bhat, Britney Duratinsky, Scott Forsmann), Machu Picchu team (Sofia Khan, Ravali Botta, Michael Joyce, and contractors), and leadership team (Allesha Fogle, Christopher Jimenez). Could you be thinking of one of these team members?"
    
    # MANAGEMENT REPORTING - Check these first since they're role-specific
    if any(phrase in question_lower for phrase in ["burndown", "sprint progress", "team velocity", "how are we doing", "tell me the burndown"]) and user_role in ["Engineering Manager", "Engineering Director", "Senior Software Engineer"]:
        return """Current Sprint Burndown (Sprint 23, Jan 15-29):
        
        **Taj Mahal Team:**
        - Planned: 42 story points
        - Completed: 28 story points (67%)
        - Remaining: 14 story points
        - Velocity: On Track
        - Days remaining: 5
        - Projected completion: 95% (2 points may slip)
        
        **Machu Picchu Team:**
        - Planned: 38 story points
        - Completed: 31 story points (82%)
        - Remaining: 7 story points
        - Velocity: Ahead of schedule
        - Projected completion: 100%
        
        **Key Risks:**
        - Kafka migration complexity may require extra QA time
        - Database optimization dependent on DBA approval
        - Device sync fix needs production validation
        
        **Sprint Goal Achievement:**
        - Kafka Migration Phase 1: 70% complete ✅
        - Source System Ranking: 65% complete ⚠️
        - Database Performance: 80% complete ✅
        - Device Sync Reliability: 90% complete ✅
        
        **Action Items:**
        - Consider moving LY-1847 subtasks to next sprint
        - Schedule production deployment for Friday
        - Review capacity planning for next sprint"""
    
    # MANAGEMENT REPORTING - Team Health
    elif any(phrase in question_lower for phrase in ["team health", "team satisfaction", "team morale", "how is the team"]) and user_role in ["Engineering Manager", "Engineering Director"]:
        return """Team Health Dashboard:
        
        **Overall Satisfaction: 4.2/5.0** (↗️ +0.3 from last quarter)
        
        **Taj Mahal Team (4.1/5.0):**
        - Strengths: Technical expertise, collaboration, problem-solving
        - Concerns: Story estimation accuracy, workload balance
        - Recent feedback: "Great team dynamic, need better planning"
        - Utilization: 85% (healthy range)
        
        **Machu Picchu Team (4.3/5.0):**
        - Strengths: Innovation, quality focus, mentorship
        - Concerns: High utilization (95%), documentation gaps
        - Recent feedback: "Love the technical challenges, need more time for docs"
        
        **Key Metrics:**
        - Retention: 100% (no departures in 6 months)
        - Internal promotions: 2 pending (Britney, Ravali)
        - Training completion: 87%
        - Work-life balance rating: 4.0/5.0
        
        **Action Items:**
        - Schedule 1:1s with high-performers for retention
        - Address documentation time in sprint planning
        - Continue investing in career development
        - Monitor Machu Picchu team utilization"""
    
    # MANAGEMENT REPORTING - Budget Status
    elif any(phrase in question_lower for phrase in ["budget", "spending", "cost", "financial", "expenses", "budget status"]) and user_role in ["Engineering Manager", "Engineering Director"]:
        return """Q1 2025 Budget Status:
        
        **Personnel (80% utilized):**
        - Used: $1.2M of $1.5M allocated
        - Remaining: $300K
        - Forecast: Under budget by $100K
        
        **Infrastructure (75% utilized):**
        - Used: $300K of $400K allocated
        - AWS costs trending down due to optimization
        - Kafka migration will reduce licensing costs
        
        **Training & Development:**
        - Used: $15K of $25K allocated
        - Upcoming: AWS certifications (3 people)
        - Conference budget: $8K remaining
        
        **Contractor Spend:**
        - Used: $800K of $1M allocated
        - 2 contractors converting to FTE (saves $200K annually)
        - Remaining budget for specialized skills
        
        **Q2 Forecast:**
        - Personnel: $1.8M (2 new hires)
        - Infrastructure: $500K (increased capacity)
        - Training: $20K (leadership development)
        
        **Cost Savings Initiatives:**
        - Kafka migration: $500K annual savings
        - Database optimization: $200K annual savings
        - Cloud rightsizing: $150K annual savings"""
    
    # TECHNICAL UNBLOCKING - Database Connection (Most specific first)
    elif any(phrase in question_lower for phrase in ["connect to the database", "connect to database", "database connection", "connect to db", "connect to the db", "db connection", "how do i connect"]):
        return """Database Connection Instructions:
        
        **Production DB:**
        - Host: loyalty-prod-mysql.optum.com:3306
        - Database: loyalty_platform
        - Connection: Use VPN + bastion host (bastion.optum.com)
        - Credentials: Stored in Vault at vault.optum.com/loyalty/db-prod
        
        **Dev/Stage DB:**
        - Host: loyalty-dev-mysql.optum.com:3306
        - Database: loyalty_platform_dev
        - Direct connection (no bastion needed)
        - Credentials: LOYALTY_DB_USER and LOYALTY_DB_PASS environment variables
        
        **Connection String Example:**
        ```
        jdbc:mysql://loyalty-dev-mysql.optum.com:3306/loyalty_platform_dev?useSSL=true&requireSSL=false
        ```
        
        **Troubleshooting:**
        - If connection fails, check VPN connection
        - Verify credentials haven't expired (rotate every 90 days)
        - Contact DBA team (dba-team@optum.com) for access issues
        
        **Quick Test:**
        ```bash
        # Test connection
        mysql -h loyalty-dev-mysql.optum.com -P 3306 -u $LOYALTY_DB_USER -p$LOYALTY_DB_PASS loyalty_platform_dev
        ```"""
    
    # TECHNICAL UNBLOCKING - Deployment Process
    elif any(phrase in question_lower for phrase in ["how to deploy", "deployment process", "release process", "how to push code", "deploy my code", "how do i deploy"]):
        return """Deployment Process:
        
        **Standard Deployment:**
        1. Create PR against main branch
        2. Get 2 approvals (1 must be senior engineer)
        3. Merge triggers Jenkins build
        4. Auto-deploy to dev environment
        5. Run automated tests (takes ~15 mins)
        6. Manual promotion to stage via Jenkins
        7. Manual promotion to prod (requires manager approval)
        
        **Hotfix Process:**
        1. Create hotfix branch from main
        2. Get 1 senior engineer approval
        3. Direct deploy to prod (skip dev/stage)
        4. Post-deployment verification required
        
        **Commands:**
        - Deploy to dev: Automatic on merge
        - Deploy to stage: `/deploy stage` in #loyalty-deploys Slack
        - Deploy to prod: `/deploy prod` (requires approval)
        
        **Rollback:**
        - Emergency rollback: `/rollback prod` in #loyalty-deploys
        - Standard rollback: Revert commit and redeploy
        
        **Monitoring:**
        - Deployment dashboard: https://jenkins.optum.com/loyalty
        - Logs: https://splunk.optum.com/loyalty-deploys"""
    
    # TECHNICAL UNBLOCKING - Troubleshooting (Specific error patterns first)
    elif any(phrase in question_lower for phrase in ["app won't start", "application won't start", "application isn't starting", "my app won't start", "won't start"]):
        return """Application Won't Start - Troubleshooting:
        
        **Common Causes & Solutions:**
        1. **Port Already in Use:**
           - Check: `lsof -i :8080`
           - Kill process: `kill -9 <PID>`
           - Or change port in application.yml
        
        2. **Java Version Issues:**
           - Check version: `java -version`
           - Need Java 17+
           - Set JAVA_HOME if needed
        
        3. **Missing Environment Variables:**
           - Check: `env | grep LOYALTY`
           - Source setup: `source ./scripts/setup-env.sh`
        
        4. **Database Connection Failed:**
           - Verify VPN connection
           - Test DB: `telnet loyalty-dev-mysql.optum.com 3306`
           - Check credentials in environment
        
        5. **Maven Dependencies:**
           - Clean build: `mvn clean install`
           - Clear cache: `rm -rf ~/.m2/repository`
        
        **Debug Steps:**
        1. Check logs: `tail -f logs/application.log`
        2. Enable debug: Add `--debug` to startup
        3. Verify Docker services: `docker-compose ps`
        
        **Quick Fix Command:**
        ```bash
        ./scripts/restart-local.sh
        ```"""
    
    # TECHNICAL UNBLOCKING - Local Development
    elif any(phrase in question_lower for phrase in ["local setup", "run locally", "local development", "dev environment", "set up locally", "setup local"]):
        return """Local Development Setup:
        
        **Prerequisites:**
        - Java 17+ installed
        - Maven 3.8+
        - Docker Desktop
        - VPN access to Optum network
        
        **Setup Steps:**
        1. Clone repo: `git clone https://github.com/optum/loyalty-platform.git`
        2. Start local services: `docker-compose up -d`
        3. Set environment variables: `source ./scripts/setup-env.sh`
        4. Run application: `mvn spring-boot:run`
        5. Access at: http://localhost:8080
        
        **Local Database:**
        - MySQL container starts automatically
        - Access: localhost:3307 (user: loyalty, pass: dev123)
        - Test data loaded automatically
        
        **Kafka Local:**
        - Confluent container included in docker-compose
        - Control Center: http://localhost:9021
        - Bootstrap servers: localhost:9092
        
        **Useful Commands:**
        - Reset DB: `./scripts/reset-local-db.sh`
        - Run tests: `mvn test`
        - Build: `mvn clean package`"""
    
    # TECHNICAL UNBLOCKING - API Endpoints
    elif any(phrase in question_lower for phrase in ["api endpoints", "api docs", "swagger", "rest api", "how to call api", "api documentation"]):
        return """Loyalty Platform API Information:
        
        **Base URLs:**
        - Dev: https://loyalty-api-dev.optum.com/v1
        - Prod: https://loyalty-api.optum.com/v1
        
        **Key Endpoints:**
        - GET /members/{memberId} - Get member details
        - POST /eligibility/check - Check member eligibility
        - PUT /members/{memberId}/points - Update member points
        - GET /devices/{memberId} - Get connected devices
        
        **Authentication:**
        - Use Bearer token from OAuth2 service
        - Token endpoint: https://auth.optum.com/oauth/token
        - Client credentials stored in Vault
        
        **Documentation:**
        - Swagger UI: https://loyalty-api-dev.optum.com/swagger-ui
        - Postman Collection: shared in #loyalty-dev Slack channel
        
        **Rate Limits:**
        - 1000 requests/minute per client
        - 10,000 requests/hour per client"""
    
    # TECHNICAL UNBLOCKING - General Troubleshooting
    elif any(phrase in question_lower for phrase in ["troubleshoot", "debug", "not working", "how do i fix", "problem", "issue"]):
        return """General Troubleshooting Guide:
        
        **Database Connection Issues:**
        - Verify VPN connection
        - Test connectivity: `telnet loyalty-dev-mysql.optum.com 3306`
        - Check credentials in Vault
        - Review connection pool settings
        
        **Kafka Issues:**
        - Check consumer lag: `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group loyalty-group`
        - Verify topic exists: `kafka-topics.sh --bootstrap-server localhost:9092 --list`
        - Reset consumer: `kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group loyalty-group --reset-offsets --to-earliest --all-topics --execute`
        
        **Common Errors:**
        - 'UhcApiTimeoutException': Increase timeout in application.yml
        - 'EligibilityConflictException': Check dual eligibility logic
        - 'DeviceSyncFailedException': Verify device API credentials
        
        **Who to Contact:**
        - Database issues: DBA team (dba-team@optum.com)
        - Infrastructure: Platform team (#platform-support)
        - Business logic: Product team (Connie Cavallo)"""
    
    # TEAM INFORMATION - Specific teams first
    elif any(phrase in question_lower for phrase in ["taj mahal", "my team", "our team"]) and user_team == "Taj Mahal":
        return """The Taj Mahal team consists of:
        - Rishab Bhat (Associate SWE) - working on Source System Ranking Algorithm
        - Britney Duratinsky (Associate SWE) - leading the Kafka migration from Top of Funnel script
        - Scott Forsmann (Associate SWE) - focusing on database performance optimization
        - Team Lead: Allesha Fogle (Engineering Manager)
        The team focuses on platform engineering, source system integration, and performance optimization."""
    
    elif any(phrase in question_lower for phrase in ["machu picchu", "machu picchu team"]):
        return """The Machu Picchu team includes:
        - Sofia Khan (Associate SWE) - Device sync reliability improvements
        - Ravali Botta (Software Engineer) - Eligibility rule migration framework  
        - Michael Joyce (Senior SWE) - Team technical lead
        - Shasikumar Bommineni (Contractor) - User-friendly error messages
        - Ganesh Nettem (Contractor) - Kafka consumer lag monitoring
        - Nagarjuna Reddy (Software Engineer) - Load testing automation
        - Ajit Krishnan (Software Engineer) - Database connection pool optimization
        Michael Joyce serves as the Senior Engineer leading the team."""
    
    # WORK AND SCHEDULE INFORMATION
    elif any(phrase in question_lower for phrase in ["my work", "my stories", "my tasks"]):
        username = user_info.get('name', '').lower().split()[0]
        if username == 'rishab':
            return "Your current work: LY-1847 (Source System Ranking Algorithm - In Progress, 8 pts), LY-1863 (Source System Health Monitoring Dashboard - Code Review, 5 pts). Focus areas: data source ranking, API integration, performance optimization."
        elif username == 'britney':
            return "Your current work: Leading LY-1834 (Kafka Migration - In Progress, 13 pts). You're converting the Top of Funnel Perl script to event-driven Kafka processing. Critical project for platform modernization."
        elif username == 'scott':
            return "Your current work: LY-1849 (Database Migration Performance Optimization - In Progress, 8 pts). Focus: improving migration performance by 50%, optimizing for 10M+ member records."
        else:
            return f"Your work assignments are visible in your individual dashboard. Current sprint focus varies by team role."
    
    elif any(phrase in question_lower for phrase in ["on call", "oncall", "who's on call"]):
        return "Scott Forsmann is currently on call this week (Jan 20-26). You can reach him at 612-555-0134 with backup Ravali Botta. Next week Ravali Botta will be on call (612-555-0178), followed by Michael Joyce (612-555-0189)."
    
    elif any(phrase in question_lower for phrase in ["sprint", "goals", "current sprint"]):
        return """Current Sprint 23 goals (Jan 15-29, 2025):
        1) Kafka Migration Phase 1 - eliminate Top of Funnel script dependencies (Britney leading)
        2) Source System Ranking Algorithm implementation (Rishab)
        3) Database performance improvements for member lookup queries (Scott)
        4) Device sync reliability improvements (Sofia - Machu Picchu team)
        5) Fix dual eligibility conflict resolution"""
    
    # TECHNICAL INFORMATION
    elif any(phrase in question_lower for phrase in ["tech stack", "technology", "tools"]):
        return "Our tech stack: Java Spring Boot (backend services), MySQL (on-premises database), Kubernetes (container orchestration), Apache Kafka (messaging), Splunk (monitoring/logging), React (some frontend components), Capillary Technologies (main frontend platform)."
    
    elif any(phrase in question_lower for phrase in ["kafka", "migration", "top of funnel"]):
        return "The Kafka migration (led by Britney Duratinsky) involves replacing the legacy Top of Funnel Perl script with event-driven processing. This eliminates daily batch processing delays and enables real-time member eligibility updates. Currently 70% complete."
    
    # GENERAL DATABASE ISSUES (less specific, comes after connection instructions)
    elif any(phrase in question_lower for phrase in ["database", "db issues", "database problems"]):
        return "For database issues: Contact DBA team at dba-team@optum.com. For urgent problems, escalate to Maria Garcia or platform team. Common issues: connection pool exhaustion, query performance problems. Scott Forsmann is our database optimization specialist."
    
    else:
        return f"This is the LoyaltyAI demo system with realistic Optum team data. The complete team roster includes: Taj Mahal team (Rishab Bhat, Britney Duratinsky, Scott Forsmann), Machu Picchu team (Sofia Khan, Ravali Botta, Michael Joyce, Shasikumar Bommineni, Ganesh Nettem, Nagarjuna Reddy, Ajit Krishnan), and leadership (Allesha Fogle, Christopher Jimenez, Connie Cavallo, Swapna Kolimi). All information is part of the demonstration dataset."

def generate_answer_with_ai(question: str, context: str, client, user_info) -> str:
    """Generate answer using AI API or demo responses"""
    if not client:
        # Enhanced demo mode responses when no API key
        demo_responses = {
            "who's on call": "Scott Forsmann is on call this week (Jan 20-26). You can reach him at 612-555-0134.",
            "taj mahal team": "The Taj Mahal team includes Rishab Bhat, Britney Duratinsky, and Scott Forsmann, all Associate Software Engineers managed by Allesha Fogle.",
            "machu picchu team": "The Machu Picchu team includes Sofia Khan, Ravali Botta, Michael Joyce (Senior Engineer/Lead), Shasikumar Bommineni, Ganesh Nettem, Nagarjuna Reddy, and Ajit Krishnan.",
            "my team": f"You're on the {user_info.get('team', 'Unknown')} team. Check your dashboard for current team composition and projects.",
            "sprint goals": "Sprint 23 focuses on Kafka migration (Britney), Source System Ranking (Rishab), database optimization (Scott), and device sync improvements.",
            "tech stack": "Our tech stack: Java Spring Boot, MySQL, Kubernetes, Apache Kafka, Splunk, React, and Capillary Technologies frontend.",
            "database issues": "For database issues, contact dba-team@optum.com or escalate to Maria Garcia for urgent problems.",
            "my work": f"Hi {user_info.get('name', 'there')}! Your current work assignments are shown in your dashboard. This demo includes realistic project data for the Loyalty platform.",
            "kafka migration": "Britney Duratinsky is leading the Kafka migration to replace the legacy Top of Funnel Perl script. Currently 70% complete."
        }
        
        question_lower = question.lower()
        for key, response in demo_responses.items():
            if any(word in question_lower for word in key.split()):
                return response
        
        # Check if context indicates unknown person
        if "don't have information about" in context:
            return context
        
        return f"Hi {user_info.get('name', 'there')}! This is the LoyaltyAI demo with realistic Optum team data. All names and projects are part of the demonstration dataset. The AI would provide detailed answers about your team's work, including specific names and project details, since this is a controlled demo environment."
    
    # Real AI response with API key
    role_context = f"You are LoyaltyAI, an internal team assistant for the Optum Loyalty platform. You're responding to {user_info.get('name', 'a team member')}, a {user_info.get('role', 'team member')} on the {user_info.get('team', 'Unknown')} team."
    
    prompt = f"""{role_context}

IMPORTANT: This is a demonstration application with fictional team data. You must ONLY use information provided in the context below. DO NOT make up or invent any names, people, projects, or details that are not explicitly mentioned in the context.

If someone asks about a person or information not in the context, clearly state that you don't have that information in your database and suggest they might be thinking of someone else from the known team members.

Context about the team: {context}

User question: {question}

Provide a direct, helpful answer using ONLY the information in the context. Do not invent or hallucinate any details not provided."""

    try:
        response = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=800,
            temperature=0.1,  # Lower temperature to reduce hallucination
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
            card_class = "dashboard-card-danger" if 'Current' in schedule['week'] else "dashboard-card"
            st.markdown(f'<div class="{card_class}"><strong>{schedule["week"]}</strong><br>{schedule["engineer"]}<br>📞 {schedule["phone"]}</div>', unsafe_allow_html=True)
        
        st.markdown("#### 🚨 Recent Incidents")
        for incident in DASHBOARD_DATA["individual"]["my_incidents"]:
            priority_class = "dashboard-card-danger" if incident['priority'] == 'P1' else "dashboard-card-alt" if incident['priority'] == 'P2' else "dashboard-card"
            st.markdown(f'<div class="{priority_class}"><strong>{incident["id"]}</strong><br>{incident["title"]}<br><span class="status-badge">{incident["priority"]} - {incident["status"]}</span></div>', unsafe_allow_html=True)

def render_senior_engineer_dashboard(user_info):
    """Render dashboard for senior engineers"""
    st.markdown(f"### 👨‍💼 {user_info['name']} - {user_info['team']} Team Lead")
    
    metrics = DASHBOARD_DATA["senior_engineer"]["team_metrics"]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div class="dashboard-card-success"><div class="metric-number">{metrics["sprint_velocity"]}</div><strong>Sprint Velocity</strong><br><small>{metrics["velocity_trend"]}</small></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="dashboard-card-alt"><div class="metric-number">{metrics["code_coverage"]}%</div><strong>Code Coverage</strong><br><small>{metrics["coverage_trend"]}</small></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="dashboard-card"><div class="metric-number">{metrics["bug_escape_rate"]}</div><strong>Bug Escape Rate</strong></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="dashboard-card"><div class="metric-number">{metrics["avg_cycle_time"]}</div><strong>Avg Cycle Time</strong></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 👥 Team Members")
        for member in DASHBOARD_DATA["senior_engineer"]["team_members"]:
            card_class = "dashboard-card-success" if member['status'] == 'On Track' else "dashboard-card-alt" if member['status'] == 'Ahead' else "dashboard-card"
            st.markdown(f'<div class="{card_class}"><strong>{member["name"]}</strong> - {member["role"]}<br>{member["current_task"]}<br><span class="status-badge">{member["status"]}</span> | Load: {member["current_sprint_load"]}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🔍 Priority Code Reviews")
        for pr in DASHBOARD_DATA["senior_engineer"]["priority_code_reviews"]:
            card_class = "dashboard-card-danger" if pr['urgency'] == 'Critical' else "dashboard-card-alt" if pr['urgency'] == 'Medium' else "dashboard-card"
            st.markdown(f'<div class="{card_class}"><strong>{pr["pr"]}</strong> - {pr["title"]}<br>By: {pr["author"]} | {pr["complexity"]} complexity<br><span class="status-badge">{pr["status"]}</span></div>', unsafe_allow_html=True)

def render_director_dashboard(user_info):
    """Render dashboard for director"""
    st.markdown(f"### 🎯 {user_info['name']} - Leadership Dashboard")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Team Performance")
        for team, data in DASHBOARD_DATA["director"]["team_burndown"].items():
            card_class = "dashboard-card-success" if data['velocity'] == 'Ahead' else "dashboard-card-danger" if data['velocity'] == 'At Risk' else "dashboard-card-alt"
            completion_pct = round((data['completed'] / data['planned']) * 100)
            st.markdown(f'<div class="{card_class}"><strong>{team.replace("_", " ").title()}</strong><br>Progress: {data["completed"]}/{data["planned"]} ({completion_pct}%)<br><span class="status-badge">{data["velocity"]}</span> | Satisfaction: {data["satisfaction"]}/5.0<br>Blockers: {data["blockers"]}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🎯 Strategic Initiatives")
        for initiative in DASHBOARD_DATA["director"]["strategic_initiatives"]:
            card_class = "dashboard-card-success" if initiative['status'] == 'On Track' else "dashboard-card" if initiative['status'] == 'Planning' else "dashboard-card-alt"
            st.markdown(f'<div class="{card_class}"><strong>{initiative["name"]}</strong><br>Progress: {initiative["completion"]}%<br><span class="status-badge">{initiative["status"]}</span><br><small>{initiative["budget"]} | {initiative["timeline"]}</small></div>', unsafe_allow_html=True)
    
    # Risk Register and Hiring Pipeline
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ⚠️ Risk Register")
        for risk in DASHBOARD_DATA["director"]["risk_register"]:
            risk_class = "dashboard-card-danger" if risk['impact'] == 'High' and risk['probability'] == 'Medium' else "dashboard-card-alt"
            st.markdown(f'<div class="{risk_class}"><strong>{risk["risk"]}</strong><br>Impact: {risk["impact"]} | Probability: {risk["probability"]}<br><span class="status-badge">{risk["status"]}</span></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 👔 Hiring Pipeline")
        for hire in DASHBOARD_DATA["director"]["hiring_pipeline"]:
            hire_class = "dashboard-card-success" if hire['stage'] == 'Offer Extended' else "dashboard-card-alt"
            st.markdown(f'<div class="{hire_class}"><strong>{hire["position"]}</strong><br>{hire["team"]} Team | {hire["candidates"]} candidates<br><span class="status-badge">{hire["stage"]}</span><br><small>Target: {hire["hire_date"]}</small></div>', unsafe_allow_html=True)

def render_engineering_manager_dashboard(user_info):
    """Render dashboard for engineering manager"""
    st.markdown(f"### 👩‍💼 {user_info['name']} - Engineering Manager")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 👥 Direct Reports")
        for report in DASHBOARD_DATA["engineering_manager"]["direct_reports"]:
            card_class = "dashboard-card-success" if report['performance'] == 'Exceeds Expectations' else "dashboard-card-alt"
            st.markdown(f'<div class="{card_class}"><strong>{report["name"]}</strong><br>{report["role"]} - {report["team"]}<br><span class="status-badge">{report["performance"]}</span><br>Load: {report["current_sprint_load"]} | Experience: {report["years_experience"]}y</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 📈 Team Performance")
        for team, perf in DASHBOARD_DATA["engineering_manager"]["team_performance"].items():
            efficiency_pct = perf['efficiency'].replace('%', '')
            card_class = "dashboard-card-success" if int(efficiency_pct) >= 90 else "dashboard-card-alt"
            st.markdown(f'<div class="{card_class}"><strong>{team.replace("_", " ").title()}</strong><br>Velocity: {perf["velocity"]}/{perf["target"]} | Efficiency: {perf["efficiency"]}<br>Satisfaction: {perf["satisfaction"]}/5.0<br>Issues: {perf["issues"]}</div>', unsafe_allow_html=True)

def render_product_manager_dashboard(user_info):
    """Render dashboard for product manager"""
    st.markdown(f"### 📊 {user_info['name']} - Product Dashboard")
    
    st.markdown("#### 🎯 Active Epics")
    for epic in DASHBOARD_DATA["product_manager"]["active_epics"]:
        card_class = "dashboard-card-success" if epic['status'] == 'On Track' else "dashboard-card-danger" if epic['status'] == 'At Risk' else "dashboard-card"
        st.markdown(f'<div class="{card_class}"><strong>{epic["epic"]}</strong> - {epic["title"]}<br>Progress: {epic["progress"]}% | Target: {epic["target_date"]}<br><span class="status-badge">{epic["status"]}</span><br><small>{epic["business_value"]} | Risk: {epic["risk_level"]}</small></div>', unsafe_allow_html=True)

def render_scrum_master_dashboard(user_info):
    """Render dashboard for scrum master"""
    st.markdown(f"### 🏃‍♀️ {user_info['name']} - Agile Dashboard")
    
    st.markdown("#### 📈 Team Health Overview")
    for team, health in DASHBOARD_DATA["scrum_master"]["team_health"].items():
        card_class = "dashboard-card-success" if health['satisfaction'] >= 4.0 and health['blockers'] <= 1 else "dashboard-card-alt"
        st.markdown(f'<div class="{card_class}"><strong>{team.replace("_", " ").title()}</strong><br>Satisfaction: {health["satisfaction"]}/5.0 | Capacity: {health["capacity"]}<br>Blockers: {health["blockers"]} | Goal Achievement: {health["sprint_goal_achievement"]}<br>Team Size: {health["team_size"]} | Trend: {health["velocity_trend"]}</div>', unsafe_allow_html=True)

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
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.markdown("---")
        
        client = initialize_ai_client()
        if client:
            st.success("✅ LoyaltyAI Connected")
        else:
            st.info("🎭 Demo Mode - Add API key for full AI responses")
        
        st.markdown("---")
        st.markdown("### 🎮 Test Accounts")
        st.markdown("**All passwords:** optum123")
        st.markdown("- rishab.bhat (Individual)")
        st.markdown("- michael.joyce (Senior Engineer)")
        st.markdown("- christopher.jimenez (Director)")
        st.markdown("- allesha.fogle (Eng Manager)")
        st.markdown("- connie.cavallo (Product)")
        st.markdown("- swapna.kolimi (Scrum Master)")
    
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
                context = get_relevant_context(prompt, user_info)
                client = initialize_ai_client()
                answer = generate_answer_with_ai(prompt, context, client, user_info)
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()