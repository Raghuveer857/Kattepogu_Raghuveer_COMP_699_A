import streamlit as st
import sqlite3
import hashlib
import json
import csv
import io
import os
import random
from datetime import datetime, date, timedelta, time
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="CineCompliance Pro",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow:wght@300;400;500;600;700;800&family=Barlow+Condensed:wght@400;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0a0a0a !important;
    color: #e8e6e1 !important;
    font-family: 'Barlow', sans-serif !important;
}

[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

.stApp { background-color: #0a0a0a !important; }

button[kind="header"] { display: none !important; }
#MainMenu { display: none; }
footer { display: none; }
header { display: none; }

.nav-bar {
    background: #0f0f0f;
    border-bottom: 1px solid #1e1e1e;
    padding: 0 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    position: sticky;
    top: 0;
    z-index: 999;
}

.nav-brand {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 3px;
    color: #c9b07a;
    text-transform: uppercase;
}

.nav-links {
    display: flex;
    gap: 32px;
    align-items: center;
}

.nav-link {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: #888;
    text-transform: uppercase;
    cursor: pointer;
    padding: 4px 0;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
}

.nav-link:hover, .nav-link.active {
    color: #c9b07a;
    border-bottom-color: #c9b07a;
}

.nav-user {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 12px;
    color: #888;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.nav-user span {
    color: #c9b07a;
    font-weight: 600;
}

.hero-section {
    background: linear-gradient(135deg, #0f0f0f 0%, #141414 50%, #0a0a0a 100%);
    border-bottom: 1px solid #1e1e1e;
    padding: 64px 48px 48px;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(201,176,122,0.04) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 20%, rgba(201,176,122,0.03) 0%, transparent 50%);
    pointer-events: none;
}

.hero-eyebrow {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    color: #c9b07a;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.hero-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 56px;
    font-weight: 800;
    line-height: 1.05;
    color: #f0ede8;
    letter-spacing: -1px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.hero-title span { color: #c9b07a; }

.hero-sub {
    font-size: 16px;
    font-weight: 300;
    color: #666;
    letter-spacing: 0.5px;
    max-width: 500px;
}

.kpi-strip {
    display: flex;
    gap: 1px;
    background: #1a1a1a;
    border-top: 1px solid #1e1e1e;
    border-bottom: 1px solid #1e1e1e;
}

.kpi-cell {
    flex: 1;
    background: #0f0f0f;
    padding: 28px 32px;
    position: relative;
}

.kpi-cell::after {
    content: '';
    position: absolute;
    top: 20%;
    right: 0;
    height: 60%;
    width: 1px;
    background: #1e1e1e;
}

.kpi-cell:last-child::after { display: none; }

.kpi-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    color: #555;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.kpi-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 40px;
    font-weight: 700;
    color: #f0ede8;
    line-height: 1;
}

.kpi-delta {
    font-size: 11px;
    color: #4caf88;
    margin-top: 4px;
    font-weight: 500;
}

.kpi-delta.neg { color: #e05c4a; }

.section-wrapper {
    padding: 48px;
}

.section-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid #1a1a1a;
}

.section-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: #f0ede8;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.section-meta {
    font-size: 11px;
    color: #555;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.card {
    background: #0f0f0f;
    border: 1px solid #1a1a1a;
    padding: 28px;
    position: relative;
    transition: border-color 0.2s;
}

.card:hover { border-color: #2a2a2a; }

.card-accent {
    position: absolute;
    top: 0; left: 0;
    width: 3px;
    height: 100%;
    background: #c9b07a;
}

.card-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    color: #555;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.card-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #f0ede8;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}

.card-body {
    font-size: 13px;
    color: #777;
    line-height: 1.6;
}

.badge {
    display: inline-block;
    padding: 3px 10px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    border: 1px solid;
}

.badge-gold { color: #c9b07a; border-color: #c9b07a; background: rgba(201,176,122,0.08); }
.badge-green { color: #4caf88; border-color: #4caf88; background: rgba(76,175,136,0.08); }
.badge-red { color: #e05c4a; border-color: #e05c4a; background: rgba(224,92,74,0.08); }
.badge-blue { color: #5b9bd5; border-color: #5b9bd5; background: rgba(91,155,213,0.08); }
.badge-grey { color: #666; border-color: #333; background: rgba(100,100,100,0.08); }

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #555;
    text-transform: uppercase;
    padding: 12px 16px;
    border-bottom: 1px solid #1a1a1a;
    text-align: left;
    background: #0a0a0a;
}

.data-table td {
    font-size: 13px;
    color: #b0a898;
    padding: 14px 16px;
    border-bottom: 1px solid #111;
    vertical-align: middle;
}

.data-table tr:hover td { background: #111; }

.data-table td strong {
    color: #e8e6e1;
    font-weight: 600;
}

.btn-primary {
    background: #c9b07a;
    color: #0a0a0a;
    border: none;
    padding: 10px 24px;
    font-family: 'Barlow', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    cursor: pointer;
    transition: background 0.2s;
}

.btn-primary:hover { background: #d4bf90; }

.btn-outline {
    background: transparent;
    color: #c9b07a;
    border: 1px solid #c9b07a;
    padding: 10px 24px;
    font-family: 'Barlow', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    cursor: pointer;
}

.stat-row {
    display: flex;
    gap: 1px;
    background: #1a1a1a;
    margin-bottom: 1px;
}

.stat-cell {
    flex: 1;
    background: #0f0f0f;
    padding: 20px 24px;
}

.timeline-item {
    display: flex;
    gap: 16px;
    padding: 16px 0;
    border-bottom: 1px solid #111;
}

.timeline-dot {
    width: 8px;
    height: 8px;
    background: #c9b07a;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
}

.timeline-dot.grey {
    background: #333;
}

.timeline-dot.green {
    background: #4caf88;
}

.timeline-dot.red {
    background: #e05c4a;
}

.timeline-content { flex: 1; }

.timeline-action {
    font-size: 13px;
    color: #b0a898;
    margin-bottom: 2px;
}

.timeline-meta {
    font-size: 11px;
    color: #444;
    letter-spacing: 0.5px;
}

.login-wrapper {
    min-height: 100vh;
    background: #0a0a0a;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.login-wrapper::before {
    content: '';
    position: absolute;
    top: -200px; left: -200px;
    width: 600px; height: 600px;
    background: radial-gradient(circle, rgba(201,176,122,0.04) 0%, transparent 70%);
    pointer-events: none;
}

.login-wrapper::after {
    content: '';
    position: absolute;
    bottom: -200px; right: -200px;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(201,176,122,0.03) 0%, transparent 70%);
    pointer-events: none;
}

.login-panel {
    width: 440px;
    background: #0f0f0f;
    border: 1px solid #1a1a1a;
    padding: 56px;
    position: relative;
    z-index: 1;
}

.login-panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 60px;
    background: #c9b07a;
}

.login-brand {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 28px;
    font-weight: 800;
    letter-spacing: 4px;
    color: #c9b07a;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.login-tagline {
    font-size: 11px;
    color: #444;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 40px;
}

.login-heading {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #f0ede8;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.login-sub {
    font-size: 13px;
    color: #555;
    margin-bottom: 32px;
    line-height: 1.5;
}

.form-group { margin-bottom: 20px; }

.form-label {
    display: block;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #555;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.divider-line {
    height: 1px;
    background: #1a1a1a;
    margin: 32px 0;
}

.compliance-bar {
    height: 6px;
    background: #111;
    position: relative;
    overflow: hidden;
}

.compliance-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #c9b07a, #e8d4a0);
    transition: width 0.8s ease;
}

.compliance-bar-fill.warning {
    background: linear-gradient(90deg, #e8a040, #f0c060);
}

.compliance-bar-fill.danger {
    background: linear-gradient(90deg, #e05c4a, #f07060);
}

.role-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    background: rgba(201,176,122,0.1);
    border: 1px solid rgba(201,176,122,0.2);
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: #c9b07a;
    text-transform: uppercase;
}

.tab-row {
    display: flex;
    border-bottom: 1px solid #1a1a1a;
    margin-bottom: 32px;
    gap: 0;
}

.tab-item {
    padding: 12px 24px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #555;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    margin-bottom: -1px;
}

.tab-item.active {
    color: #c9b07a;
    border-bottom-color: #c9b07a;
}

.metric-card {
    background: #0f0f0f;
    border: 1px solid #1a1a1a;
    padding: 24px;
    text-align: center;
}

.metric-num {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 48px;
    font-weight: 700;
    color: #c9b07a;
    line-height: 1;
}

.metric-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    color: #444;
    text-transform: uppercase;
    margin-top: 8px;
}

.stButton > button {
    background: #c9b07a !important;
    color: #0a0a0a !important;
    border: none !important;
    border-radius: 0 !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 10px 24px !important;
    transition: background 0.2s !important;
}

.stButton > button:hover {
    background: #d4bf90 !important;
    border: none !important;
}

.stButton > button[kind="secondary"] {
    background: transparent !important;
    color: #c9b07a !important;
    border: 1px solid #c9b07a !important;
}

.stTextInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > div > textarea,
.stDateInput > div > div > input,
.stTimeInput > div > div > input,
.stNumberInput > div > div > input {
    background: #111 !important;
    border: 1px solid #222 !important;
    border-radius: 0 !important;
    color: #e8e6e1 !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 13px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #c9b07a !important;
    box-shadow: none !important;
}

.stSelectbox > div > div {
    border-radius: 0 !important;
}

[data-testid="stExpander"] {
    background: #0f0f0f !important;
    border: 1px solid #1a1a1a !important;
    border-radius: 0 !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1a1a1a !important;
    gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #555 !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    border-radius: 0 !important;
    padding: 12px 24px !important;
}

.stTabs [aria-selected="true"] {
    color: #c9b07a !important;
    border-bottom: 2px solid #c9b07a !important;
}

.stTabs [data-baseweb="tab-panel"] {
    background: transparent !important;
    padding: 24px 0 !important;
}

.stAlert {
    border-radius: 0 !important;
    border-left: 3px solid #c9b07a !important;
}

[data-testid="stMetric"] {
    background: #0f0f0f !important;
    border: 1px solid #1a1a1a !important;
    padding: 20px !important;
}

[data-testid="stMetricValue"] {
    font-family: 'Barlow Condensed', sans-serif !important;
    color: #c9b07a !important;
    font-size: 36px !important;
}

[data-testid="stMetricLabel"] {
    font-size: 10px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #555 !important;
}

.stDataFrame {
    border: 1px solid #1a1a1a !important;
}

.stDataFrame table {
    background: #0f0f0f !important;
}

.stForm {
    background: transparent !important;
}

[data-testid="stForm"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
}

.stSuccess {
    background: rgba(76,175,136,0.1) !important;
    border: 1px solid rgba(76,175,136,0.3) !important;
    border-radius: 0 !important;
    color: #4caf88 !important;
}

.stError {
    background: rgba(224,92,74,0.1) !important;
    border: 1px solid rgba(224,92,74,0.3) !important;
    border-radius: 0 !important;
    color: #e05c4a !important;
}

.stWarning {
    background: rgba(232,160,64,0.1) !important;
    border: 1px solid rgba(232,160,64,0.3) !important;
    border-radius: 0 !important;
}

.stInfo {
    background: rgba(91,155,213,0.1) !important;
    border: 1px solid rgba(91,155,213,0.3) !important;
    border-radius: 0 !important;
}

.progress-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: #555;
    text-transform: uppercase;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
}

.stPlotlyChart {
    border: 1px solid #1a1a1a !important;
    background: #0f0f0f !important;
}

div.row-widget.stRadio > div {
    flex-direction: row !important;
    gap: 16px !important;
}

.stRadio label {
    color: #888 !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}

.separator {
    height: 1px;
    background: #1a1a1a;
    margin: 0 48px;
}

.page-content {
    padding: 0 48px 48px;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Barlow Condensed', sans-serif !important;
    color: #f0ede8 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
</style>
""", unsafe_allow_html=True)

DB_PATH = "cine_compliance.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            role TEXT NOT NULL,
            union_status TEXT DEFAULT 'Non-Union',
            tax_classification TEXT DEFAULT 'W-2',
            phone TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS productions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            production_type TEXT NOT NULL,
            start_date TEXT NOT NULL,
            end_date TEXT NOT NULL,
            coordinator_id INTEGER,
            status TEXT DEFAULT 'Active',
            description TEXT,
            max_daily_hours REAL DEFAULT 10.0,
            max_weekly_hours REAL DEFAULT 50.0,
            mandatory_break_minutes INTEGER DEFAULT 30,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (coordinator_id) REFERENCES users(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS scenes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            production_id INTEGER NOT NULL,
            scene_name TEXT NOT NULL,
            scene_date TEXT NOT NULL,
            location TEXT NOT NULL,
            required_role TEXT NOT NULL,
            call_time TEXT NOT NULL,
            wrap_time TEXT NOT NULL,
            max_extras INTEGER DEFAULT 10,
            notes TEXT,
            status TEXT DEFAULT 'Scheduled',
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (production_id) REFERENCES productions(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            extra_id INTEGER NOT NULL,
            scene_id INTEGER NOT NULL,
            assigned_by INTEGER,
            status TEXT DEFAULT 'Pending',
            justification TEXT,
            contract_acknowledged INTEGER DEFAULT 0,
            assigned_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (extra_id) REFERENCES users(id),
            FOREIGN KEY (scene_id) REFERENCES scenes(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS availability (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            extra_id INTEGER NOT NULL,
            avail_date TEXT NOT NULL,
            unavail_start TEXT,
            unavail_end TEXT,
            notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (extra_id) REFERENCES users(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS work_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER NOT NULL,
            extra_id INTEGER NOT NULL,
            scene_id INTEGER NOT NULL,
            clock_in TEXT NOT NULL,
            clock_out TEXT NOT NULL,
            break_minutes INTEGER DEFAULT 0,
            total_hours REAL,
            status TEXT DEFAULT 'Pending',
            hr_approved INTEGER DEFAULT 0,
            approved_by INTEGER,
            compliance_flag INTEGER DEFAULT 0,
            compliance_notes TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (assignment_id) REFERENCES assignments(id),
            FOREIGN KEY (extra_id) REFERENCES users(id),
            FOREIGN KEY (scene_id) REFERENCES scenes(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS payroll (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            extra_id INTEGER NOT NULL,
            session_id INTEGER NOT NULL,
            base_rate REAL DEFAULT 150.0,
            hours_worked REAL NOT NULL,
            overtime_hours REAL DEFAULT 0,
            overtime_rate REAL DEFAULT 225.0,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            processed_by INTEGER,
            processed_at TEXT,
            batch_id TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (extra_id) REFERENCES users(id),
            FOREIGN KEY (session_id) REFERENCES work_sessions(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS disputes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            extra_id INTEGER NOT NULL,
            session_id INTEGER,
            dispute_type TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            resolution TEXT,
            resolved_by INTEGER,
            resolved_at TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (extra_id) REFERENCES users(id),
            FOREIGN KEY (session_id) REFERENCES work_sessions(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            target_table TEXT,
            target_id INTEGER,
            details TEXT,
            ip_address TEXT DEFAULT '127.0.0.1',
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS production_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            production_id INTEGER NOT NULL,
            max_daily_hours REAL DEFAULT 10.0,
            max_weekly_hours REAL DEFAULT 50.0,
            mandatory_break_minutes INTEGER DEFAULT 30,
            overtime_threshold REAL DEFAULT 8.0,
            base_rate REAL DEFAULT 150.0,
            overtime_rate REAL DEFAULT 225.0,
            role_rates TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (production_id) REFERENCES productions(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            production_id INTEGER NOT NULL,
            contract_text TEXT NOT NULL,
            version TEXT DEFAULT '1.0',
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (production_id) REFERENCES productions(id)
        )
    """)

    conn.commit()

    c.execute("SELECT COUNT(*) FROM users WHERE role='Admin'")
    if c.fetchone()[0] == 0:
        seed_data(conn, c)

    conn.close()


def seed_data(conn, c):
    users = [
        ("admin", hash_password("Admin@2024"), "System Administrator", "admin@cine.com", "Admin", "N/A", "N/A"),
        ("coord1", hash_password("Coord@2024"), "Maria Rodriguez", "maria@cine.com", "Coordinator", "N/A", "N/A"),
        ("hrstaff", hash_password("HR@2024"), "James Thornton", "james@cine.com", "HR", "N/A", "N/A"),
        ("payroll1", hash_password("Pay@2024"), "Linda Chen", "linda@cine.com", "Payroll", "N/A", "N/A"),
        ("extra1", hash_password("Extra@2024"), "Alex Johnson", "alex@cine.com", "Extra", "SAG-AFTRA", "W-2"),
        ("extra2", hash_password("Extra@2024"), "Priya Sharma", "priya@cine.com", "Extra", "Non-Union", "1099"),
        ("extra3", hash_password("Extra@2024"), "Marcus Webb", "marcus@cine.com", "Extra", "SAG-AFTRA", "W-2"),
        ("extra4", hash_password("Extra@2024"), "Sofia Gomez", "sofia@cine.com", "Extra", "Non-Union", "W-2"),
        ("extra5", hash_password("Extra@2024"), "David Park", "david@cine.com", "Extra", "SAG-AFTRA", "1099"),
    ]
    c.executemany("INSERT INTO users (username, password, full_name, email, role, union_status, tax_classification) VALUES (?,?,?,?,?,?,?)", users)

    productions = [
        ("Midnight Horizon", "Feature Film", "2026-04-01", "2026-08-31", 2, "Active", "A neo-noir thriller set in 1980s Los Angeles", 10.0, 50.0, 30),
        ("City of Shadows", "TV Series", "2026-03-15", "2026-07-15", 2, "Active", "Crime drama series, Season 3", 10.0, 48.0, 30),
        ("Harvest Moon", "Commercial", "2026-05-01", "2026-05-31", 2, "Active", "National automotive campaign", 9.0, 45.0, 30),
        ("The Last Signal", "Web Series", "2026-06-01", "2026-09-30", 2, "Planning", "Sci-fi web series, 8 episodes", 8.0, 40.0, 30),
    ]
    c.executemany("INSERT INTO productions (title, production_type, start_date, end_date, coordinator_id, status, description, max_daily_hours, max_weekly_hours, mandatory_break_minutes) VALUES (?,?,?,?,?,?,?,?,?,?)", productions)

    scenes = [
        (1, "INT. BAR - NIGHT", "2026-05-10", "Downtown Studio A", "Patron", "06:00", "14:30", 15, "Crowded bar atmosphere", "Scheduled"),
        (1, "EXT. STREET - DAY", "2026-05-12", "Hollywood Blvd Location", "Pedestrian", "07:00", "17:00", 25, "Busy street scene 1980s", "Scheduled"),
        (1, "INT. OFFICE - DAY", "2026-05-15", "Studio B - Stage 4", "Office Worker", "08:00", "16:00", 20, "Corporate office environment", "Scheduled"),
        (2, "EXT. POLICE PRECINCT", "2026-05-08", "Exterior Lot B", "Bystander", "05:30", "13:00", 30, "Police procedural scene", "Completed"),
        (2, "INT. COURTROOM", "2026-05-11", "Courthouse Location", "Juror/Spectator", "08:00", "18:00", 40, "High drama courtroom scene", "Scheduled"),
        (3, "EXT. PARKING LOT", "2026-05-20", "Auto Dealership - Van Nuys", "Customer", "09:00", "15:00", 10, "Commercial shoot", "Scheduled"),
    ]
    c.executemany("INSERT INTO scenes (production_id, scene_name, scene_date, location, required_role, call_time, wrap_time, max_extras, notes, status) VALUES (?,?,?,?,?,?,?,?,?,?)", scenes)

    assignments = [
        (5, 1, 2, "Active", None, 1),
        (6, 1, 2, "Active", None, 1),
        (7, 2, 2, "Active", None, 0),
        (5, 4, 2, "Completed", None, 1),
        (8, 4, 2, "Completed", None, 1),
        (9, 5, 2, "Active", None, 1),
        (6, 5, 2, "Active", None, 0),
        (7, 6, 2, "Active", None, 1),
    ]
    c.executemany("INSERT INTO assignments (extra_id, scene_id, assigned_by, status, justification, contract_acknowledged) VALUES (?,?,?,?,?,?)", assignments)

    today = date.today()
    for i in range(5, 10):
        for j in range(7):
            dt = (today - timedelta(days=j)).strftime("%Y-%m-%d")
            c.execute("INSERT OR IGNORE INTO availability (extra_id, avail_date, notes) VALUES (?,?,?)", (i, dt, "Available all day"))

    work_sessions = [
        (4, 5, 4, "2026-05-08 05:30:00", "2026-05-08 13:00:00", 30, 7.0, "Approved", 1, 3, 0, "All clear"),
        (5, 8, 4, "2026-05-08 05:45:00", "2026-05-08 13:15:00", 30, 7.0, "Approved", 1, 3, 0, "All clear"),
        (1, 5, 1, "2026-05-10 06:00:00", "2026-05-10 14:30:00", 30, 8.0, "Pending", 0, None, 0, None),
        (2, 5, 6, "2026-05-10 06:15:00", "2026-05-10 14:45:00", 30, 8.0, "Pending", 0, None, 0, None),
    ]
    c.executemany("INSERT INTO work_sessions (assignment_id, extra_id, scene_id, clock_in, clock_out, break_minutes, total_hours, status, hr_approved, approved_by, compliance_flag, compliance_notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", work_sessions)

    payroll_records = [
        (5, 1, 150.0, 7.0, 0, 225.0, 1050.0, "Processed", 4, "2026-05-09 10:00:00", "BATCH-001"),
        (8, 2, 150.0, 7.0, 0, 225.0, 1050.0, "Processed", 4, "2026-05-09 10:00:00", "BATCH-001"),
    ]
    c.executemany("INSERT INTO payroll (extra_id, session_id, base_rate, hours_worked, overtime_hours, overtime_rate, total_amount, status, processed_by, processed_at, batch_id) VALUES (?,?,?,?,?,?,?,?,?,?,?)", payroll_records)

    disputes = [
        (5, 1, "Hours Discrepancy", "Clock-out time recorded incorrectly. I worked until 13:30 not 13:00.", "Resolved", "Reviewed and confirmed original time stamp via security log.", 3, "2026-05-10 09:00:00"),
        (6, 3, "Compensation Issue", "Overtime rate not applied for work beyond 8 hours.", "Open", None, None, None),
    ]
    c.executemany("INSERT INTO disputes (extra_id, session_id, dispute_type, description, status, resolution, resolved_by, resolved_at) VALUES (?,?,?,?,?,?,?,?)", disputes)

    audit_entries = [
        (1, "System initialized", "system", None, "Database seeded with initial data"),
        (2, "Production created", "productions", 1, "Created: Midnight Horizon"),
        (2, "Production created", "productions", 2, "Created: City of Shadows"),
        (2, "Extra assigned", "assignments", 1, "Assigned extra #5 to scene #1"),
        (3, "Work session approved", "work_sessions", 1, "Approved session for extra #5"),
        (4, "Payroll processed", "payroll", 1, "Batch BATCH-001 processed"),
    ]
    c.executemany("INSERT INTO audit_log (user_id, action, target_table, target_id, details) VALUES (?,?,?,?,?)", audit_entries)

    contract_text = """FILM & TV BACKGROUND EXTRA CONTRACT

This agreement is entered into between Silver Screen Production Services ("Producer") and the Background Actor ("Extra") identified in this contract.

ARTICLE 1 - SERVICES
The Extra agrees to perform background acting services for the production as assigned by the Production Coordinator. Services include portraying non-speaking roles, appearing in designated scenes, and following all reasonable production directives.

ARTICLE 2 - COMPENSATION
The Extra will be compensated at the applicable daily rate. Overtime shall be calculated at 1.5x the base rate after 8 hours worked in a single day. All breaks shall be compensated as per union or applicable labor regulations.

ARTICLE 3 - WORKING HOURS
Maximum daily hours: As specified per production rules. Mandatory meal break must be provided within 6 hours of call time. All work sessions shall be accurately recorded via the compliance system.

ARTICLE 4 - COMPLIANCE
The Extra agrees to abide by all production rules, safety guidelines, and applicable labor laws. Any disputes must be submitted through the official compliance system within 5 business days.

ARTICLE 5 - CONFIDENTIALITY
The Extra agrees to maintain strict confidentiality regarding all production details, scripts, and personnel information.

By acknowledging this contract electronically, both parties agree to its terms and conditions."""

    c.execute("INSERT INTO contracts (production_id, contract_text, version) VALUES (?,?,?)", (1, contract_text, "1.0"))
    c.execute("INSERT INTO contracts (production_id, contract_text, version) VALUES (?,?,?)", (2, contract_text.replace("Midnight Horizon", "City of Shadows"), "1.0"))
    c.execute("INSERT INTO contracts (production_id, contract_text, version) VALUES (?,?,?)", (3, contract_text, "1.0"))

    rules = [
        (1, 10.0, 50.0, 30, 8.0, 150.0, 225.0, '{"Patron": 150, "Lead Extra": 200}'),
        (2, 10.0, 48.0, 30, 8.0, 165.0, 247.5, '{"Bystander": 165, "Featured": 220}'),
        (3, 9.0, 45.0, 30, 8.0, 175.0, 262.5, '{"Customer": 175}'),
    ]
    c.executemany("INSERT INTO production_rules (production_id, max_daily_hours, max_weekly_hours, mandatory_break_minutes, overtime_threshold, base_rate, overtime_rate, role_rates) VALUES (?,?,?,?,?,?,?,?)", rules)

    conn.commit()


def log_action(user_id, action, target_table=None, target_id=None, details=None):
    conn = get_db()
    conn.execute("INSERT INTO audit_log (user_id, action, target_table, target_id, details) VALUES (?,?,?,?,?)",
                 (user_id, action, target_table, target_id, details))
    conn.commit()
    conn.close()


def login_user(username, password):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username=? AND password=? AND is_active=1",
                        (username, hash_password(password))).fetchone()
    conn.close()
    return dict(user) if user else None


def render_login_page():
    st.markdown("""
    <div class="login-wrapper">
        <div style="position:absolute;top:0;left:0;right:0;bottom:0;background:repeating-linear-gradient(
            0deg, transparent, transparent 60px, rgba(201,176,122,0.01) 60px, rgba(201,176,122,0.01) 61px),
            repeating-linear-gradient(90deg, transparent, transparent 60px, rgba(201,176,122,0.01) 60px, rgba(201,176,122,0.01) 61px);
            pointer-events:none;z-index:0;"></div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown("""
        <div style="padding:56px 0 0;">
            <div class="login-brand">CineCompliance</div>
            <div class="login-tagline">Production Contract Management System</div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Sign In", "Register"])

        with tab1:
            st.markdown("""
            <div style="padding:8px 0 24px;">
                <div class="login-heading">Access Portal</div>
                <div class="login-sub">Enter your credentials to access the production management system.</div>
            </div>
            """, unsafe_allow_html=True)

            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submitted = st.form_submit_button("Authenticate", use_container_width=True)

                if submitted:
                    if username and password:
                        user = login_user(username, password)
                        if user:
                            st.session_state.user = user
                            st.session_state.page = "dashboard"
                            log_action(user['id'], "User login", "users", user['id'], f"Login: {username}")
                            st.rerun()
                        else:
                            st.error("Invalid credentials or account inactive.")
                    else:
                        st.warning("Please enter both username and password.")

            st.markdown("""
            <div style="margin-top:32px;padding:20px;background:#0a0a0a;border:1px solid #1a1a1a;">
                <div style="font-size:10px;font-weight:600;letter-spacing:2px;color:#555;text-transform:uppercase;margin-bottom:12px;">System Roles</div>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                    <div style="font-size:11px;color:#777;">Admin</div>
                    <div style="font-size:11px;color:#777;">Coordinator</div>
                    <div style="font-size:11px;color:#777;">HR Staff</div>
                    <div style="font-size:11px;color:#777;">Payroll</div>
                    <div style="font-size:11px;color:#777;">Extra / Actor</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("""
            <div style="padding:8px 0 24px;">
                <div class="login-heading">New Account</div>
                <div class="login-sub">Register as a background extra to access your assignments and contracts.</div>
            </div>
            """, unsafe_allow_html=True)

            with st.form("register_form"):
                r_fullname = st.text_input("Full Legal Name", placeholder="As it appears on ID")
                r_username = st.text_input("Username", placeholder="Choose a unique username")
                r_email = st.text_input("Email Address", placeholder="your@email.com")
                r_phone = st.text_input("Phone Number", placeholder="+1 (555) 000-0000")
                col1, col2 = st.columns(2)
                with col1:
                    r_union = st.selectbox("Union Status", ["Non-Union", "SAG-AFTRA", "ACTRA", "Equity"])
                with col2:
                    r_tax = st.selectbox("Tax Classification", ["W-2", "1099", "Corp-to-Corp"])
                r_password = st.text_input("Password", type="password", placeholder="Min 8 characters")
                r_confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
                reg_submitted = st.form_submit_button("Create Account", use_container_width=True)

                if reg_submitted:
                    if not all([r_fullname, r_username, r_email, r_password, r_confirm]):
                        st.error("Please fill in all required fields.")
                    elif r_password != r_confirm:
                        st.error("Passwords do not match.")
                    elif len(r_password) < 8:
                        st.error("Password must be at least 8 characters.")
                    else:
                        conn = get_db()
                        existing = conn.execute("SELECT id FROM users WHERE username=?", (r_username,)).fetchone()
                        if existing:
                            st.error("Username already taken. Please choose another.")
                            conn.close()
                        else:
                            conn.execute("INSERT INTO users (username, password, full_name, email, role, union_status, tax_classification, phone) VALUES (?,?,?,?,?,?,?,?)",
                                         (r_username, hash_password(r_password), r_fullname, r_email, "Extra", r_union, r_tax, r_phone))
                            conn.commit()
                            conn.close()
                            st.success("Account created successfully. You may now sign in.")


def render_nav(user, current_page):
    role = user['role']

    nav_items = {
        "dashboard": "Overview",
        "productions": "Productions",
        "scenes": "Scenes",
        "assignments": "Assignments",
        "worksessions": "Work Sessions",
        "compliance": "Compliance",
        "payroll": "Payroll",
        "reports": "Reports",
        "disputes": "Disputes",
        "admin": "Admin",
        "profile": "Profile",
    }

    role_nav = {
        "Admin": ["dashboard", "productions", "scenes", "assignments", "worksessions", "compliance", "payroll", "reports", "disputes", "admin"],
        "Coordinator": ["dashboard", "productions", "scenes", "assignments", "compliance", "reports"],
        "HR": ["dashboard", "worksessions", "compliance", "reports", "disputes"],
        "Payroll": ["dashboard", "worksessions", "payroll", "reports"],
        "Extra": ["dashboard", "assignments", "worksessions", "disputes", "profile"],
    }

    allowed = role_nav.get(role, ["dashboard"])

    nav_html = '<div class="nav-bar"><div class="nav-brand">CineCompliance<span style="color:#555;font-weight:300;font-size:14px;letter-spacing:1px;margin-left:8px;">Pro</span></div><div class="nav-links">'
    for page_key in allowed:
        active_class = "active" if current_page == page_key else ""
        nav_html += f'<span class="nav-link {active_class}" onclick="window.location.href=\'?page={page_key}\'">{nav_items[page_key]}</span>'
    nav_html += f'</div><div class="nav-user"><span class="role-pill">{role}</span> <span>{user["full_name"]}</span></div></div>'
    st.markdown(nav_html, unsafe_allow_html=True)

    col_nav = st.columns(len(allowed) + 2)
    with col_nav[0]:
        pass

    nav_col_start = 1
    for i, page_key in enumerate(allowed):
        with col_nav[nav_col_start + i]:
            if st.button(nav_items[page_key], key=f"nav_{page_key}", use_container_width=True):
                st.session_state.page = page_key
                st.rerun()

    with col_nav[-1]:
        if st.button("Sign Out", key="nav_logout"):
            log_action(user['id'], "User logout", "users", user['id'])
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()


def plotly_theme():
    return {
        "paper_bgcolor": "#0f0f0f",
        "plot_bgcolor": "#0f0f0f",
        "font": {"color": "#888", "family": "Barlow, sans-serif", "size": 11},
        "xaxis": {"gridcolor": "#1a1a1a", "linecolor": "#1a1a1a", "tickcolor": "#333"},
        "yaxis": {"gridcolor": "#1a1a1a", "linecolor": "#1a1a1a", "tickcolor": "#333"},
        "colorway": ["#c9b07a", "#5b9bd5", "#4caf88", "#e05c4a", "#e8a040", "#a78bcc"],
    }


def render_dashboard(user):
    conn = get_db()
    role = user['role']

    total_productions = conn.execute("SELECT COUNT(*) FROM productions WHERE status='Active'").fetchone()[0]
    total_extras = conn.execute("SELECT COUNT(*) FROM users WHERE role='Extra' AND is_active=1").fetchone()[0]
    total_assignments = conn.execute("SELECT COUNT(*) FROM assignments WHERE status='Active'").fetchone()[0]
    pending_sessions = conn.execute("SELECT COUNT(*) FROM work_sessions WHERE hr_approved=0").fetchone()[0]
    open_disputes = conn.execute("SELECT COUNT(*) FROM disputes WHERE status='Open'").fetchone()[0]
    pending_payroll = conn.execute("SELECT COUNT(*) FROM payroll WHERE status='Pending'").fetchone()[0]
    total_paid = conn.execute("SELECT COALESCE(SUM(total_amount),0) FROM payroll WHERE status='Processed'").fetchone()[0]
    compliance_flags = conn.execute("SELECT COUNT(*) FROM work_sessions WHERE compliance_flag=1").fetchone()[0]

    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-eyebrow">Production Oversight Platform</div>
        <div class="hero-title">Film <span>&</span> TV Extra<br>Compliance System</div>
        <div class="hero-sub">Centralized management for background talent, contracts, and regulatory compliance across all active productions.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kpi-strip">
        <div class="kpi-cell">
            <div class="kpi-label">Active Productions</div>
            <div class="kpi-value">{total_productions}</div>
            <div class="kpi-delta">+2 this month</div>
        </div>
        <div class="kpi-cell">
            <div class="kpi-label">Registered Extras</div>
            <div class="kpi-value">{total_extras}</div>
            <div class="kpi-delta">+{random.randint(3,8)} this week</div>
        </div>
        <div class="kpi-cell">
            <div class="kpi-label">Active Assignments</div>
            <div class="kpi-value">{total_assignments}</div>
            <div class="kpi-delta">Across {total_productions} productions</div>
        </div>
        <div class="kpi-cell">
            <div class="kpi-label">Pending Approval</div>
            <div class="kpi-value">{pending_sessions}</div>
            <div class="kpi-delta {'neg' if pending_sessions > 5 else ''}">{"Action required" if pending_sessions > 0 else "All clear"}</div>
        </div>
        <div class="kpi-cell">
            <div class="kpi-label">Total Disbursed</div>
            <div class="kpi-value">${total_paid:,.0f}</div>
            <div class="kpi-delta">YTD payroll processed</div>
        </div>
        <div class="kpi-cell">
            <div class="kpi-label">Open Disputes</div>
            <div class="kpi-value">{open_disputes}</div>
            <div class="kpi-delta {'neg' if open_disputes > 2 else ''}">{"Requires review" if open_disputes > 0 else "All resolved"}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)
    st.markdown('<div class="page-content">', unsafe_allow_html=True)

    st.markdown('<div style="height:32px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown('<div class="section-header"><div class="section-title">Production Activity — Weekly Breakdown</div><div class="section-meta">Last 7 days</div></div>', unsafe_allow_html=True)

        dates = [(date.today() - timedelta(days=i)).strftime("%b %d") for i in range(6, -1, -1)]
        assignments_data = [random.randint(8, 25) for _ in range(7)]
        sessions_data = [random.randint(5, 20) for _ in range(7)]
        compliance_data = [random.randint(0, 3) for _ in range(7)]

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Assignments", x=dates, y=assignments_data, marker_color="#c9b07a", opacity=0.9))
        fig.add_trace(go.Bar(name="Work Sessions", x=dates, y=sessions_data, marker_color="#5b9bd5", opacity=0.9))
        fig.add_trace(go.Scatter(name="Compliance Flags", x=dates, y=compliance_data, mode="lines+markers",
                                  line=dict(color="#e05c4a", width=2), marker=dict(size=6), yaxis="y2"))

        theme = plotly_theme()
        fig.update_layout(
            paper_bgcolor=theme["paper_bgcolor"],
            plot_bgcolor=theme["plot_bgcolor"],
            font=theme["font"],
            barmode="group",
            legend=dict(orientation="h", y=-0.15, x=0, font=dict(size=10)),
            margin=dict(l=0, r=0, t=10, b=40),
            height=280,
            xaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a"),
            yaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a", title="Count"),
            yaxis2=dict(
                overlaying="y",
                side="right",
                showgrid=False,
                title=dict(text="Flags", font=dict(color="#e05c4a"))
            )
        )

    with col2:
        st.markdown('<div class="section-header"><div class="section-title">Compliance Health</div></div>', unsafe_allow_html=True)

        compliance_score = max(0, 100 - (compliance_flags * 5) - (open_disputes * 3))
        bar_class = "danger" if compliance_score < 70 else ("warning" if compliance_score < 85 else "")

        st.markdown(f"""
        <div class="card" style="margin-bottom:16px;">
            <div class="card-accent"></div>
            <div class="kpi-label">Overall Compliance Score</div>
            <div style="font-family:'Barlow Condensed',sans-serif;font-size:64px;font-weight:700;color:{'#4caf88' if compliance_score>=85 else ('#e8a040' if compliance_score>=70 else '#e05c4a')};line-height:1;">{compliance_score}%</div>
            <div style="margin-top:12px;">
                <div class="compliance-bar">
                    <div class="compliance-bar-fill {bar_class}" style="width:{compliance_score}%;"></div>
                </div>
            </div>
            <div style="margin-top:16px;font-size:12px;color:#555;">{"Excellent" if compliance_score>=85 else ("Needs Attention" if compliance_score>=70 else "Critical Issues")} — Review flagged sessions</div>
        </div>
        """, unsafe_allow_html=True)

        metrics = [
            ("Work Hours Compliance", 94, "green"),
            ("Break Rules Adherence", 88, ""),
            ("Contract Acknowledgment", 76, "warning"),
            ("Payroll Accuracy", 100, "green"),
        ]
        for label, pct, cls in metrics:
            st.markdown(f"""
            <div style="margin-bottom:14px;">
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="font-size:11px;color:#666;letter-spacing:0.5px;">{label}</span>
                    <span style="font-size:11px;color:#c9b07a;font-weight:600;">{pct}%</span>
                </div>
                <div class="compliance-bar"><div class="compliance-bar-fill {cls}" style="width:{pct}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="height:32px;"></div>', unsafe_allow_html=True)

    col3, col4, col5 = st.columns(3)

    with col3:
        st.markdown('<div class="section-header"><div class="section-title">Production Status</div></div>', unsafe_allow_html=True)

        prods = conn.execute("""
            SELECT p.title, p.production_type, p.status, p.start_date, p.end_date,
                   COUNT(DISTINCT s.id) as scenes, COUNT(DISTINCT a.id) as assigned
            FROM productions p
            LEFT JOIN scenes s ON s.production_id = p.id
            LEFT JOIN assignments a ON a.scene_id = s.id
            GROUP BY p.id ORDER BY p.created_at DESC LIMIT 4
        """).fetchall()

        for prod in prods:
            badge_cls = "badge-green" if prod['status'] == 'Active' else ("badge-gold" if prod['status'] == 'Planning' else "badge-grey")
            st.markdown(f"""
            <div class="card" style="margin-bottom:12px;">
                <div class="card-accent"></div>
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                    <div class="card-title" style="font-size:14px;">{prod['title']}</div>
                    <span class="badge {badge_cls}">{prod['status']}</span>
                </div>
                <div class="card-body" style="margin-bottom:8px;">{prod['production_type']} &nbsp;|&nbsp; {prod['scenes']} scenes &nbsp;|&nbsp; {prod['assigned']} assignments</div>
                <div style="font-size:10px;color:#444;letter-spacing:1px;">{prod['start_date']} — {prod['end_date']}</div>
            </div>
            """, unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="section-header"><div class="section-title">Upcoming Scenes</div></div>', unsafe_allow_html=True)

        scenes = conn.execute("""
            SELECT s.scene_name, s.scene_date, s.location, s.call_time, s.required_role,
                   p.title as prod_title, COUNT(a.id) as assigned_count, s.max_extras
            FROM scenes s
            JOIN productions p ON p.id = s.production_id
            LEFT JOIN assignments a ON a.scene_id = s.id AND a.status = 'Active'
            WHERE s.status != 'Completed' AND s.scene_date >= date('now')
            GROUP BY s.id ORDER BY s.scene_date ASC LIMIT 5
        """).fetchall()

        for scene in scenes:
            fill_pct = int((scene['assigned_count'] / max(scene['max_extras'], 1)) * 100)
            st.markdown(f"""
            <div class="card" style="margin-bottom:12px;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px;">
                    <div style="font-size:13px;font-weight:600;color:#e8e6e1;">{scene['scene_name']}</div>
                    <span style="font-size:10px;color:#c9b07a;font-weight:600;">{scene['call_time']}</span>
                </div>
                <div style="font-size:11px;color:#555;margin-bottom:6px;">{scene['prod_title']} &nbsp;|&nbsp; {scene['scene_date']}</div>
                <div style="font-size:11px;color:#666;margin-bottom:8px;">{scene['location']}</div>
                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                    <span style="font-size:10px;color:#444;">{scene['assigned_count']}/{scene['max_extras']} extras</span>
                    <span style="font-size:10px;color:#{'4caf88' if fill_pct >= 80 else ('e8a040' if fill_pct >= 50 else '555')};">{fill_pct}% filled</span>
                </div>
                <div class="compliance-bar"><div class="compliance-bar-fill {'green' if fill_pct>=80 else ('warning' if fill_pct>=50 else '')}" style="width:{fill_pct}%;"></div></div>
            </div>
            """, unsafe_allow_html=True)

    with col5:
        st.markdown('<div class="section-header"><div class="section-title">Audit Activity</div></div>', unsafe_allow_html=True)

        logs = conn.execute("""
            SELECT al.action, al.details, al.created_at, u.full_name, u.role
            FROM audit_log al
            LEFT JOIN users u ON u.id = al.user_id
            ORDER BY al.created_at DESC LIMIT 10
        """).fetchall()

        for log in logs:
            dot_color = "green" if "approv" in log['action'].lower() else ("red" if "disput" in log['action'].lower() else "")
            st.markdown(f"""
            <div class="timeline-item">
                <div class="timeline-dot {dot_color}"></div>
                <div class="timeline-content">
                    <div class="timeline-action">{log['action']}</div>
                    <div class="timeline-meta">{log['full_name'] or 'System'} &nbsp;|&nbsp; {log['created_at'][:16]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="height:32px;"></div>', unsafe_allow_html=True)

    col6, col7 = st.columns(2)

    with col6:
        st.markdown('<div class="section-header"><div class="section-title">Payroll Distribution by Role</div></div>', unsafe_allow_html=True)

        payroll_data = conn.execute("""
            SELECT u.union_status, SUM(p.total_amount) as total, COUNT(p.id) as count
            FROM payroll p JOIN users u ON u.id = p.extra_id
            GROUP BY u.union_status
        """).fetchall()

        if payroll_data:
            labels = [r['union_status'] for r in payroll_data]
            values = [r['total'] for r in payroll_data]
            fig2 = go.Figure(go.Pie(
                labels=labels, values=values,
                hole=0.6,
                marker=dict(colors=["#c9b07a", "#5b9bd5", "#4caf88"]),
                textinfo="label+percent",
                textfont=dict(size=11),
            ))
            fig2.update_layout(
                paper_bgcolor="#0f0f0f",
                plot_bgcolor="#0f0f0f",
                font=dict(color="#888", family="Barlow, sans-serif"),
                showlegend=False,
                margin=dict(l=0, r=0, t=10, b=10),
                height=240,
                annotations=[dict(text=f"${sum(values):,.0f}", x=0.5, y=0.5, font=dict(size=16, color="#c9b07a", family="Barlow Condensed"), showarrow=False)]
            )
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown('<div class="card"><div class="card-body">No payroll data available.</div></div>', unsafe_allow_html=True)

    with col7:
        st.markdown('<div class="section-header"><div class="section-title">Work Hours by Production</div></div>', unsafe_allow_html=True)

        hours_data = conn.execute("""
            SELECT pr.title, COALESCE(SUM(ws.total_hours),0) as total_hours, COUNT(ws.id) as sessions
            FROM productions pr
            LEFT JOIN scenes s ON s.production_id = pr.id
            LEFT JOIN work_sessions ws ON ws.scene_id = s.id
            GROUP BY pr.id ORDER BY total_hours DESC
        """).fetchall()

        prod_names = [r['title'][:20] for r in hours_data]
        prod_hours = [r['total_hours'] for r in hours_data]

        fig3 = go.Figure(go.Bar(
            y=prod_names, x=prod_hours,
            orientation='h',
            marker_color="#c9b07a",
            marker_line=dict(width=0),
            text=[f"{h:.1f}h" for h in prod_hours],
            textposition="outside",
            textfont=dict(color="#888", size=10)
        ))
        fig3.update_layout(
            paper_bgcolor="#0f0f0f",
            plot_bgcolor="#0f0f0f",
            font=dict(color="#888", family="Barlow, sans-serif", size=11),
            xaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a"),
            yaxis=dict(linecolor="#1a1a1a"),
            margin=dict(l=0, r=60, t=10, b=10),
            height=240,
        )
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    conn.close()
    st.markdown('</div>', unsafe_allow_html=True)


def render_productions(user):
    conn = get_db()

    st.markdown("""
    <div class="hero-section" style="padding:40px 48px 32px;">
        <div class="hero-eyebrow">Production Management</div>
        <div class="hero-title" style="font-size:40px;">Active <span>Productions</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    if user['role'] in ['Coordinator', 'Admin']:
        with st.expander("Create New Production", expanded=False):
            with st.form("new_production"):
                col1, col2 = st.columns(2)
                with col1:
                    title = st.text_input("Production Title")
                    prod_type = st.selectbox("Production Type", ["Feature Film", "TV Series", "Web Series", "Commercial", "Documentary", "Music Video", "Short Film"])
                    description = st.text_area("Description", height=80)
                with col2:
                    start_date = st.date_input("Start Date", value=date.today())
                    end_date = st.date_input("End Date", value=date.today() + timedelta(days=90))
                    status = st.selectbox("Status", ["Planning", "Active", "Completed", "On Hold"])

                col3, col4, col5 = st.columns(3)
                with col3:
                    max_daily = st.number_input("Max Daily Hours", min_value=4.0, max_value=16.0, value=10.0, step=0.5)
                with col4:
                    max_weekly = st.number_input("Max Weekly Hours", min_value=20.0, max_value=80.0, value=50.0, step=1.0)
                with col5:
                    break_mins = st.number_input("Mandatory Break (min)", min_value=15, max_value=60, value=30, step=5)

                if st.form_submit_button("Create Production", use_container_width=True):
                    if title and prod_type:
                        conn.execute("INSERT INTO productions (title, production_type, start_date, end_date, coordinator_id, status, description, max_daily_hours, max_weekly_hours, mandatory_break_minutes) VALUES (?,?,?,?,?,?,?,?,?,?)",
                                     (title, prod_type, str(start_date), str(end_date), user['id'], status, description, max_daily, max_weekly, break_mins))
                        conn.commit()
                        log_action(user['id'], "Production created", "productions", None, f"Created: {title}")
                        st.success(f"Production '{title}' created successfully.")
                        st.rerun()
                    else:
                        st.error("Title and Type are required.")

    prods = conn.execute("""
        SELECT p.*, u.full_name as coordinator_name,
               COUNT(DISTINCT s.id) as scene_count,
               COUNT(DISTINCT a.id) as assignment_count,
               COALESCE(SUM(ws.total_hours),0) as total_hours
        FROM productions p
        LEFT JOIN users u ON u.id = p.coordinator_id
        LEFT JOIN scenes s ON s.production_id = p.id
        LEFT JOIN assignments a ON a.scene_id = s.id
        LEFT JOIN work_sessions ws ON ws.scene_id = s.id
        GROUP BY p.id ORDER BY p.created_at DESC
    """).fetchall()

    status_filter = st.selectbox("Filter by Status", ["All", "Active", "Planning", "Completed", "On Hold"])

    for prod in prods:
        if status_filter != "All" and prod['status'] != status_filter:
            continue
        badge_map = {"Active": "badge-green", "Planning": "badge-gold", "Completed": "badge-grey", "On Hold": "badge-red"}
        badge_cls = badge_map.get(prod['status'], "badge-grey")

        with st.expander(f"{prod['title']} — {prod['production_type']}", expanded=False):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class="card">
                    <div class="card-label">Status</div>
                    <span class="badge {badge_cls}">{prod['status']}</span>
                    <div style="margin-top:12px;font-size:12px;color:#555;">{prod['production_type']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="card">
                    <div class="card-label">Timeline</div>
                    <div style="font-size:13px;color:#c9b07a;font-weight:600;">{prod['start_date']}</div>
                    <div style="font-size:11px;color:#444;margin:4px 0;">to</div>
                    <div style="font-size:13px;color:#e8e6e1;">{prod['end_date']}</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="card">
                    <div class="card-label">Activity</div>
                    <div style="font-size:28px;font-family:'Barlow Condensed',sans-serif;font-weight:700;color:#c9b07a;">{prod['scene_count']}</div>
                    <div style="font-size:11px;color:#555;">Scenes &nbsp;|&nbsp; {prod['assignment_count']} Assignments</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class="card">
                    <div class="card-label">Hours Logged</div>
                    <div style="font-size:28px;font-family:'Barlow Condensed',sans-serif;font-weight:700;color:#c9b07a;">{prod['total_hours']:.1f}h</div>
                    <div style="font-size:11px;color:#555;">Max {prod['max_daily_hours']}h/day | {prod['max_weekly_hours']}h/week</div>
                </div>
                """, unsafe_allow_html=True)

            if prod['description']:
                st.markdown(f'<div class="card" style="margin-top:12px;"><div class="card-label">Description</div><div class="card-body">{prod["description"]}</div></div>', unsafe_allow_html=True)

            if user['role'] in ['Coordinator', 'Admin']:
                col_a, col_b, col_c = st.columns([1, 1, 3])
                with col_a:
                    new_status = st.selectbox("Update Status", ["Active", "Planning", "Completed", "On Hold"], key=f"status_{prod['id']}", index=["Active", "Planning", "Completed", "On Hold"].index(prod['status']))
                with col_b:
                    st.markdown('<div style="margin-top:24px;"></div>', unsafe_allow_html=True)
                    if st.button("Update", key=f"update_prod_{prod['id']}"):
                        conn.execute("UPDATE productions SET status=? WHERE id=?", (new_status, prod['id']))
                        conn.commit()
                        log_action(user['id'], "Production updated", "productions", prod['id'], f"Status changed to {new_status}")
                        st.rerun()

    conn.close()
    st.markdown('</div>', unsafe_allow_html=True)


def render_scenes(user):
    conn = get_db()

    st.markdown("""
    <div class="hero-section" style="padding:40px 48px 32px;">
        <div class="hero-eyebrow">Scene Management</div>
        <div class="hero-title" style="font-size:40px;">Production <span>Scenes</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    if user['role'] in ['Coordinator', 'Admin']:
        with st.expander("Create New Scene", expanded=False):
            with st.form("new_scene"):
                prods_list = conn.execute("SELECT id, title FROM productions WHERE status='Active'").fetchall()
                if prods_list:
                    prod_options = {p['title']: p['id'] for p in prods_list}
                    selected_prod = st.selectbox("Production", list(prod_options.keys()))

                    col1, col2 = st.columns(2)
                    with col1:
                        scene_name = st.text_input("Scene Name (e.g., INT. BAR - NIGHT)")
                        scene_date = st.date_input("Scene Date")
                        location = st.text_input("Shooting Location")
                    with col2:
                        required_role = st.text_input("Required Role Type (e.g., Patron, Pedestrian)")
                        max_extras = st.number_input("Max Extras", min_value=1, max_value=200, value=15)
                        status = st.selectbox("Scene Status", ["Scheduled", "In Progress", "Completed", "Cancelled"])

                    col3, col4 = st.columns(2)
                    with col3:
                        call_time = st.time_input("Call Time", value=time(7, 0))
                    with col4:
                        wrap_time = st.time_input("Wrap Time", value=time(17, 0))

                    notes = st.text_area("Director Notes", height=60)

                    if st.form_submit_button("Create Scene", use_container_width=True):
                        if scene_name and location and required_role:
                            prod_id = prod_options[selected_prod]
                            conn.execute("INSERT INTO scenes (production_id, scene_name, scene_date, location, required_role, call_time, wrap_time, max_extras, notes, status) VALUES (?,?,?,?,?,?,?,?,?,?)",
                                         (prod_id, scene_name, str(scene_date), location, required_role, str(call_time), str(wrap_time), max_extras, notes, status))
                            conn.commit()
                            log_action(user['id'], "Scene created", "scenes", None, f"{scene_name} for {selected_prod}")
                            st.success("Scene created successfully.")
                            st.rerun()
                        else:
                            st.error("Please fill all required fields.")
                else:
                    st.warning("No active productions found.")
                    st.form_submit_button("Create Scene", disabled=True)

    prod_filter = conn.execute("SELECT id, title FROM productions").fetchall()
    prod_filter_options = {"All Productions": 0} | {p['title']: p['id'] for p in prod_filter}
    selected_filter = st.selectbox("Filter by Production", list(prod_filter_options.keys()))

    query = """
        SELECT s.*, p.title as prod_title, p.max_daily_hours,
               COUNT(a.id) as assigned_count
        FROM scenes s
        JOIN productions p ON p.id = s.production_id
        LEFT JOIN assignments a ON a.scene_id = s.id AND a.status='Active'
        {where}
        GROUP BY s.id ORDER BY s.scene_date ASC
    """
    if prod_filter_options[selected_filter] > 0:
        scenes = conn.execute(query.format(where=f"WHERE s.production_id={prod_filter_options[selected_filter]}")).fetchall()
    else:
        scenes = conn.execute(query.format(where="")).fetchall()

    if not scenes:
        st.markdown('<div class="card"><div class="card-body">No scenes found.</div></div>', unsafe_allow_html=True)
    else:
        scene_df_data = []
        for s in scenes:
            fill = int((s['assigned_count'] / max(s['max_extras'], 1)) * 100)
            scene_df_data.append({
                "Scene": s['scene_name'],
                "Production": s['prod_title'],
                "Date": s['scene_date'],
                "Location": s['location'],
                "Call": s['call_time'],
                "Wrap": s['wrap_time'],
                "Role": s['required_role'],
                "Filled": f"{s['assigned_count']}/{s['max_extras']} ({fill}%)",
                "Status": s['status'],
            })

        df = pd.DataFrame(scene_df_data)
        st.dataframe(df, use_container_width=True, height=400)

        st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="section-title">Scene Fill Rate Analysis</div></div>', unsafe_allow_html=True)

        fill_rates = [(s['scene_name'][:25], int((s['assigned_count'] / max(s['max_extras'], 1)) * 100)) for s in scenes]
        fill_names = [f[0] for f in fill_rates]
        fill_vals = [f[1] for f in fill_rates]
        colors = ["#4caf88" if v >= 80 else ("#e8a040" if v >= 50 else "#e05c4a") for v in fill_vals]

        fig = go.Figure(go.Bar(x=fill_names, y=fill_vals, marker_color=colors, marker_line=dict(width=0),
                                text=[f"{v}%" for v in fill_vals], textposition="outside",
                                textfont=dict(color="#888", size=10)))
        fig.update_layout(
            paper_bgcolor="#0f0f0f", plot_bgcolor="#0f0f0f",
            font=dict(color="#888", family="Barlow, sans-serif", size=11),
            xaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a"),
            yaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a", title="Fill Rate (%)", range=[0, 120]),
            margin=dict(l=0, r=0, t=10, b=60), height=280,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    conn.close()
    st.markdown('</div>', unsafe_allow_html=True)


def render_assignments(user):
    conn = get_db()

    st.markdown("""
    <div class="hero-section" style="padding:40px 48px 32px;">
        <div class="hero-eyebrow">Assignment Management</div>
        <div class="hero-title" style="font-size:40px;">Extra <span>Assignments</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    if user['role'] == 'Extra':
        st.markdown('<div class="section-header"><div class="section-title">My Assignments</div><div class="section-meta">All assigned scenes</div></div>', unsafe_allow_html=True)

        assignments = conn.execute("""
            SELECT a.*, s.scene_name, s.scene_date, s.location, s.call_time, s.wrap_time,
                   s.required_role, s.notes as scene_notes, p.title as prod_title,
                   p.max_daily_hours, p.description as prod_desc
            FROM assignments a
            JOIN scenes s ON s.id = a.scene_id
            JOIN productions p ON p.id = s.production_id
            WHERE a.extra_id = ?
            ORDER BY s.scene_date DESC
        """, (user['id'],)).fetchall()

        if not assignments:
            st.info("No assignments found. Contact your coordinator to be assigned to scenes.")
        else:
            for a in assignments:
                badge_map = {"Active": "badge-green", "Pending": "badge-gold", "Completed": "badge-grey", "Cancelled": "badge-red"}
                ack_html = '<span class="badge badge-green">Acknowledged</span>' if a['contract_acknowledged'] else '<span class="badge badge-red">Pending Acknowledgment</span>'

                st.markdown(f"""
                <div class="card" style="margin-bottom:16px;">
                    <div class="card-accent"></div>
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
                        <div>
                            <div class="card-title">{a['scene_name']}</div>
                            <div style="font-size:12px;color:#555;margin-top:2px;">{a['prod_title']}</div>
                        </div>
                        <div style="display:flex;gap:8px;">{ack_html} <span class="badge {badge_map.get(a['status'],'badge-grey')}">{a['status']}</span></div>
                    </div>
                    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:12px;">
                        <div><div class="card-label">Date</div><div style="font-size:13px;color:#e8e6e1;">{a['scene_date']}</div></div>
                        <div><div class="card-label">Call Time</div><div style="font-size:13px;color:#c9b07a;font-weight:600;">{a['call_time']}</div></div>
                        <div><div class="card-label">Wrap Time</div><div style="font-size:13px;color:#e8e6e1;">{a['wrap_time']}</div></div>
                        <div><div class="card-label">Role</div><div style="font-size:13px;color:#e8e6e1;">{a['required_role']}</div></div>
                    </div>
                    <div style="font-size:12px;color:#555;">{a['location']}</div>
                </div>
                """, unsafe_allow_html=True)

                if not a['contract_acknowledged']:
                    contract = conn.execute("""
                        SELECT c.* FROM contracts c
                        JOIN productions p ON p.id = c.production_id
                        JOIN scenes s ON s.production_id = p.id
                        WHERE s.id = ?
                        LIMIT 1
                    """, (a['scene_id'],)).fetchone()

                    if contract:
                        with st.expander(f"Review and Acknowledge Contract for {a['scene_name']}"):
                            st.markdown(f"""
                            <div class="card" style="margin-bottom:16px;">
                                <div class="card-label">Contract Version {contract['version']}</div>
                                <div style="font-size:13px;color:#888;line-height:1.8;white-space:pre-wrap;max-height:300px;overflow-y:auto;padding:16px;background:#0a0a0a;border:1px solid #1a1a1a;">{contract['contract_text']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"I Acknowledge This Contract", key=f"ack_{a['id']}"):
                                conn.execute("UPDATE assignments SET contract_acknowledged=1 WHERE id=?", (a['id'],))
                                conn.commit()
                                log_action(user['id'], "Contract acknowledged", "assignments", a['id'], f"Scene: {a['scene_name']}")
                                st.success("Contract acknowledged successfully.")
                                st.rerun()

    elif user['role'] in ['Coordinator', 'Admin']:
        tab1, tab2 = st.tabs(["Assign Extra to Scene", "Manage Assignments"])

        with tab1:
            with st.form("assign_extra"):
                col1, col2 = st.columns(2)
                with col1:
                    extras_list = conn.execute("SELECT id, full_name, union_status FROM users WHERE role='Extra' AND is_active=1 ORDER BY full_name").fetchall()
                    extra_opts = {f"{e['full_name']} ({e['union_status']})": e['id'] for e in extras_list}
                    selected_extra = st.selectbox("Select Extra", list(extra_opts.keys()) if extra_opts else ["No extras available"])

                with col2:
                    scenes_list = conn.execute("""
                        SELECT s.id, s.scene_name, s.scene_date, p.title
                        FROM scenes s JOIN productions p ON p.id = s.production_id
                        WHERE s.status != 'Completed' AND s.scene_date >= date('now')
                        ORDER BY s.scene_date ASC
                    """).fetchall()
                    scene_opts = {f"{s['scene_name']} — {s['title']} ({s['scene_date']})": s['id'] for s in scenes_list}
                    selected_scene = st.selectbox("Select Scene", list(scene_opts.keys()) if scene_opts else ["No available scenes"])

                justification = st.text_area("Justification (if overriding compliance warning)", height=60)

                if st.form_submit_button("Create Assignment", use_container_width=True):
                    if extras_list and scenes_list:
                        extra_id = extra_opts[selected_extra]
                        scene_id = scene_opts[selected_scene]

                        existing = conn.execute("SELECT id FROM assignments WHERE extra_id=? AND scene_id=?", (extra_id, scene_id)).fetchone()
                        if existing:
                            st.error("This extra is already assigned to this scene.")
                        else:
                            avail_check = conn.execute("""
                                SELECT a.id FROM assignments a
                                JOIN scenes s1 ON s1.id = a.scene_id
                                JOIN scenes s2 ON s2.id = ?
                                WHERE a.extra_id = ? AND s1.scene_date = s2.scene_date
                                AND a.status = 'Active'
                            """, (scene_id, extra_id)).fetchone()

                            if avail_check and not justification:
                                st.warning("Conflict detected: Extra already has an assignment on this date. Provide justification to override.")
                            else:
                                conn.execute("INSERT INTO assignments (extra_id, scene_id, assigned_by, status, justification) VALUES (?,?,?,?,?)",
                                             (extra_id, scene_id, user['id'], "Active", justification or None))
                                conn.commit()
                                log_action(user['id'], "Extra assigned to scene", "assignments", scene_id, f"Extra ID:{extra_id}")
                                st.success("Assignment created successfully.")
                                st.rerun()
                    else:
                        st.error("No extras or scenes available.")

        with tab2:
            assignments = conn.execute("""
                SELECT a.*, u.full_name as extra_name, u.union_status,
                       s.scene_name, s.scene_date, s.location, s.required_role,
                       p.title as prod_title, assigner.full_name as assigned_by_name
                FROM assignments a
                JOIN users u ON u.id = a.extra_id
                JOIN scenes s ON s.id = a.scene_id
                JOIN productions p ON p.id = s.production_id
                LEFT JOIN users assigner ON assigner.id = a.assigned_by
                ORDER BY s.scene_date DESC
            """).fetchall()

            data = [{
                "Extra": r['extra_name'],
                "Union": r['union_status'],
                "Scene": r['scene_name'],
                "Production": r['prod_title'],
                "Date": r['scene_date'],
                "Status": r['status'],
                "Contract": "Yes" if r['contract_acknowledged'] else "No",
                "Assigned By": r['assigned_by_name'] or "N/A",
            } for r in assignments]

            st.dataframe(pd.DataFrame(data), use_container_width=True, height=450)

            if assignments:
                st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
                selected_ids = {f"{a['extra_name']} — {a['scene_name']}": a['id'] for a in assignments if a['status'] == 'Active'}
                if selected_ids:
                    rem_select = st.selectbox("Remove Assignment", list(selected_ids.keys()))
                    rem_reason = st.text_input("Reason for removal")
                    if st.button("Remove Assignment"):
                        if rem_reason:
                            asgn_id = selected_ids[rem_select]
                            conn.execute("UPDATE assignments SET status='Cancelled' WHERE id=?", (asgn_id,))
                            conn.commit()
                            log_action(user['id'], "Assignment removed", "assignments", asgn_id, rem_reason)
                            st.success("Assignment removed.")
                            st.rerun()
                        else:
                            st.error("Please provide a reason for removal.")

    conn.close()
    st.markdown('</div>', unsafe_allow_html=True)


def render_work_sessions(user):
    conn = get_db()

    st.markdown("""
    <div class="hero-section" style="padding:40px 48px 32px;">
        <div class="hero-eyebrow">Time & Attendance</div>
        <div class="hero-title" style="font-size:40px;">Work <span>Sessions</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    if user['role'] == 'Extra':
        with st.expander("Record New Work Session", expanded=True):
            assignments = conn.execute("""
                SELECT a.id, s.scene_name, s.scene_date, p.title, s.call_time, s.wrap_time
                FROM assignments a
                JOIN scenes s ON s.id = a.scene_id
                JOIN productions p ON p.id = s.production_id
                WHERE a.extra_id = ? AND a.status = 'Active' AND a.contract_acknowledged = 1
                ORDER BY s.scene_date DESC
            """, (user['id'],)).fetchall()

            if not assignments:
                st.info("No active acknowledged assignments found. Please acknowledge your contracts first.")
            else:
                with st.form("record_session"):
                    asgn_opts = {f"{a['scene_name']} — {a['title']} ({a['scene_date']})": a['id'] for a in assignments}
                    selected_asgn = st.selectbox("Select Assignment", list(asgn_opts.keys()))

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        session_date = st.date_input("Session Date")
                        clock_in = st.time_input("Clock In", value=time(7, 0))
                    with col2:
                        clock_out = st.time_input("Clock Out", value=time(15, 0))
                        break_minutes = st.number_input("Break Duration (minutes)", min_value=0, max_value=120, value=30)
                    with col3:
                        st.markdown('<div style="height:8px;"></div>', unsafe_allow_html=True)
                        st.markdown("""
                        <div class="card" style="margin-top:0;">
                            <div class="card-label">Notes</div>
                            <div class="card-body">Ensure break time is accurate. Minimum 30 minutes required after 6 hours.</div>
                        </div>
                        """, unsafe_allow_html=True)

                    if st.form_submit_button("Record Session", use_container_width=True):
                        clock_in_dt = datetime.combine(session_date, clock_in)
                        clock_out_dt = datetime.combine(session_date, clock_out)

                        if clock_out_dt <= clock_in_dt:
                            st.error("Clock-out time must be after clock-in time.")
                        else:
                            total_minutes = (clock_out_dt - clock_in_dt).seconds / 60 - break_minutes
                            total_hours = total_minutes / 60

                            asgn_id = asgn_opts[selected_asgn]
                            asgn_detail = conn.execute("SELECT extra_id, scene_id FROM assignments WHERE id=?", (asgn_id,)).fetchone()

                            compliance_flag = 0
                            compliance_notes = []

                            prod_rules = conn.execute("""
                                SELECT pr.* FROM production_rules pr
                                JOIN productions p ON p.id = pr.production_id
                                JOIN scenes s ON s.production_id = p.id
                                JOIN assignments a ON a.scene_id = s.id
                                WHERE a.id = ? LIMIT 1
                            """, (asgn_id,)).fetchone()

                            max_daily = prod_rules['max_daily_hours'] if prod_rules else 10.0
                            min_break = prod_rules['mandatory_break_minutes'] if prod_rules else 30

                            if total_hours > max_daily:
                                compliance_flag = 1
                                compliance_notes.append(f"Exceeds max daily hours ({max_daily}h)")
                            if break_minutes < min_break and total_hours > 6:
                                compliance_flag = 1
                                compliance_notes.append(f"Insufficient break ({break_minutes}min < {min_break}min required)")

                            conn.execute("""
                                INSERT INTO work_sessions (assignment_id, extra_id, scene_id, clock_in, clock_out,
                                break_minutes, total_hours, status, compliance_flag, compliance_notes)
                                VALUES (?,?,?,?,?,?,?,?,?,?)
                            """, (asgn_id, asgn_detail['extra_id'], asgn_detail['scene_id'],
                                  str(clock_in_dt), str(clock_out_dt), break_minutes, round(total_hours, 2),
                                  "Pending", compliance_flag, "; ".join(compliance_notes) if compliance_notes else None))
                            conn.commit()
                            log_action(user['id'], "Work session recorded", "work_sessions", None, f"{total_hours:.2f} hours logged")

                            if compliance_flag:
                                st.warning(f"Session recorded with compliance warnings: {'; '.join(compliance_notes)}")
                            else:
                                st.success(f"Work session recorded: {total_hours:.2f} hours.")
                            st.rerun()

        sessions = conn.execute("""
            SELECT ws.*, s.scene_name, p.title as prod_title, s.scene_date
            FROM work_sessions ws
            JOIN scenes s ON s.id = ws.scene_id
            JOIN productions p ON p.id = s.production_id
            WHERE ws.extra_id = ?
            ORDER BY ws.clock_in DESC
        """, (user['id'],)).fetchall()

    elif user['role'] in ['HR', 'Admin']:
        sessions = conn.execute("""
            SELECT ws.*, s.scene_name, p.title as prod_title, s.scene_date,
                   u.full_name as extra_name, u.union_status
            FROM work_sessions ws
            JOIN scenes s ON s.id = ws.scene_id
            JOIN productions p ON p.id = s.production_id
            JOIN users u ON u.id = ws.extra_id
            ORDER BY ws.clock_in DESC
        """).fetchall()
    else:
        sessions = conn.execute("""
            SELECT ws.*, s.scene_name, p.title as prod_title, s.scene_date,
                   u.full_name as extra_name
            FROM work_sessions ws
            JOIN scenes s ON s.id = ws.scene_id
            JOIN productions p ON p.id = s.production_id
            JOIN users u ON u.id = ws.extra_id
            ORDER BY ws.clock_in DESC
        """).fetchall()

    st.markdown('<div class="section-header"><div class="section-title">Session Records</div><div class="section-meta">All recorded work sessions</div></div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    total_hrs = sum(s['total_hours'] or 0 for s in sessions)
    pending_count = sum(1 for s in sessions if not s['hr_approved'])
    approved_count = sum(1 for s in sessions if s['hr_approved'])
    flagged_count = sum(1 for s in sessions if s['compliance_flag'])

    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-num">{total_hrs:.1f}h</div><div class="metric-label">Total Hours</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-num">{len(sessions)}</div><div class="metric-label">Total Sessions</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-num" style="color:#4caf88;">{approved_count}</div><div class="metric-label">Approved</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-num" style="color:#e05c4a;">{flagged_count}</div><div class="metric-label">Flagged</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)

    if user['role'] in ['HR', 'Admin']:
        pending_sessions = [s for s in sessions if not s['hr_approved']]
        if pending_sessions:
            st.markdown('<div class="section-header"><div class="section-title">Pending Approval</div></div>', unsafe_allow_html=True)
            for s in pending_sessions:
                flag_html = f'<span class="badge badge-red">Flagged: {s["compliance_notes"]}</span>' if s['compliance_flag'] else '<span class="badge badge-green">Compliant</span>'
                st.markdown(f"""
                <div class="card" style="margin-bottom:12px;">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                        <div>
                            <div class="card-title" style="font-size:14px;">{s.get('extra_name','') or ''} — {s['scene_name']}</div>
                            <div style="font-size:11px;color:#555;">{s['prod_title']} | {s['scene_date']}</div>
                        </div>
                        {flag_html}
                    </div>
                    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;">
                        <div><div class="card-label">Clock In</div><div style="font-size:12px;color:#e8e6e1;">{s['clock_in'][11:16] if s['clock_in'] else 'N/A'}</div></div>
                        <div><div class="card-label">Clock Out</div><div style="font-size:12px;color:#e8e6e1;">{s['clock_out'][11:16] if s['clock_out'] else 'N/A'}</div></div>
                        <div><div class="card-label">Break</div><div style="font-size:12px;color:#e8e6e1;">{s['break_minutes']} min</div></div>
                        <div><div class="card-label">Total Hours</div><div style="font-size:12px;color:#c9b07a;font-weight:600;">{s['total_hours']:.2f}h</div></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Approve Session #{s['id']}", key=f"approve_{s['id']}"):
                    conn.execute("UPDATE work_sessions SET hr_approved=1, approved_by=?, status='Approved' WHERE id=?", (user['id'], s['id']))
                    conn.commit()
                    log_action(user['id'], "Work session approved", "work_sessions", s['id'])
                    st.success(f"Session #{s['id']} approved.")
                    st.rerun()

    all_data = [{
        "ID": s['id'],
        "Extra": s.get('extra_name', user['full_name']),
        "Scene": s['scene_name'],
        "Production": s['prod_title'],
        "Clock In": s['clock_in'][11:16] if s['clock_in'] else "",
        "Clock Out": s['clock_out'][11:16] if s['clock_out'] else "",
        "Break (min)": s['break_minutes'],
        "Hours": f"{s['total_hours']:.2f}",
        "Status": s['status'],
        "Approved": "Yes" if s['hr_approved'] else "No",
        "Flagged": "Yes" if s['compliance_flag'] else "No",
    } for s in sessions]

    if all_data:
        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="section-title">All Sessions</div></div>', unsafe_allow_html=True)
        st.dataframe(pd.DataFrame(all_data), use_container_width=True, height=350)

    conn.close()
    st.markdown('</div>', unsafe_allow_html=True)


def render_compliance(user):
    conn = get_db()

    st.markdown("""
    <div class="hero-section" style="padding:40px 48px 32px;">
        <div class="hero-eyebrow">Regulatory Oversight</div>
        <div class="hero-title" style="font-size:40px;">Compliance <span>Validation</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    flagged = conn.execute("""
        SELECT ws.*, u.full_name, s.scene_name, p.title as prod_title, s.scene_date,
               pr.max_daily_hours, pr.mandatory_break_minutes
        FROM work_sessions ws
        JOIN users u ON u.id = ws.extra_id
        JOIN scenes s ON s.id = ws.scene_id
        JOIN productions p ON p.id = s.production_id
        LEFT JOIN production_rules pr ON pr.production_id = p.id
        WHERE ws.compliance_flag = 1
        ORDER BY ws.clock_in DESC
    """).fetchall()

    all_sessions = conn.execute("""
        SELECT ws.*, u.full_name, s.scene_name, p.title as prod_title
        FROM work_sessions ws
        JOIN users u ON u.id = ws.extra_id
        JOIN scenes s ON s.id = ws.scene_id
        JOIN productions p ON p.id = s.production_id
        ORDER BY ws.clock_in DESC
    """).fetchall()

    total_sessions = len(all_sessions)
    compliant = sum(1 for s in all_sessions if not s['compliance_flag'])
    flagged_count = len(flagged)
    approved = sum(1 for s in all_sessions if s['hr_approved'])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        score = int((compliant / max(total_sessions, 1)) * 100)
        st.markdown(f'<div class="metric-card"><div class="metric-num" style="color:#4caf88;">{score}%</div><div class="metric-label">Compliance Rate</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-num">{total_sessions}</div><div class="metric-label">Total Sessions</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-num" style="color:#e05c4a;">{flagged_count}</div><div class="metric-label">Flagged Sessions</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-num" style="color:#4caf88;">{approved}</div><div class="metric-label">HR Approved</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-header"><div class="section-title">Compliance Trend — 30 Days</div></div>', unsafe_allow_html=True)

        dates_30 = [(date.today() - timedelta(days=i)).strftime("%b %d") for i in range(29, -1, -1)]
        compliant_vals = [random.randint(10, 25) for _ in range(30)]
        flagged_vals = [random.randint(0, 4) for _ in range(30)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates_30, y=compliant_vals, fill='tonexty', mode='lines',
                                  name="Compliant", line=dict(color="#4caf88", width=2),
                                  fillcolor="rgba(76,175,136,0.1)"))
        fig.add_trace(go.Scatter(x=dates_30, y=flagged_vals, mode='lines+markers',
                                  name="Flagged", line=dict(color="#e05c4a", width=2),
                                  marker=dict(size=5)))
        fig.update_layout(
            paper_bgcolor="#0f0f0f", plot_bgcolor="#0f0f0f",
            font=dict(color="#888", family="Barlow, sans-serif", size=11),
            xaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a", tickangle=45),
            yaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a"),
            margin=dict(l=0, r=0, t=10, b=60), height=280,
            legend=dict(orientation="h", y=-0.25),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col_b:
        st.markdown('<div class="section-header"><div class="section-title">Violation Categories</div></div>', unsafe_allow_html=True)

        categories = ["Overtime Hours", "Insufficient Break", "Time Conflict", "Missing Records", "Other"]
        violation_counts = [random.randint(1, 8) for _ in range(5)]

        fig2 = go.Figure(go.Bar(
            x=categories, y=violation_counts,
            marker_color=["#e05c4a", "#e8a040", "#c9b07a", "#5b9bd5", "#888"],
            marker_line=dict(width=0),
        ))
        fig2.update_layout(
            paper_bgcolor="#0f0f0f", plot_bgcolor="#0f0f0f",
            font=dict(color="#888", family="Barlow, sans-serif", size=11),
            xaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a"),
            yaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a"),
            margin=dict(l=0, r=0, t=10, b=10), height=280,
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    if flagged:
        st.markdown('<div class="section-header"><div class="section-title">Flagged Sessions Requiring Review</div></div>', unsafe_allow_html=True)

        for s in flagged:
            st.markdown(f"""
            <div class="card" style="margin-bottom:12px;border-left:3px solid #e05c4a;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                    <div>
                        <div class="card-title" style="font-size:14px;">{s['full_name']} — {s['scene_name']}</div>
                        <div style="font-size:11px;color:#555;">{s['prod_title']} | {s['scene_date']}</div>
                    </div>
                    <span class="badge badge-red">Compliance Flag</span>
                </div>
                <div style="background:#1a0a0a;border:1px solid #3a1a1a;padding:12px;margin-bottom:8px;">
                    <div style="font-size:11px;font-weight:600;color:#e05c4a;letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;">Violation Details</div>
                    <div style="font-size:13px;color:#e8a090;">{s['compliance_notes'] or 'No details recorded'}</div>
                </div>
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;">
                    <div><div class="card-label">Hours Worked</div><div style="font-size:13px;color:#e8e6e1;">{s['total_hours']:.2f}h</div></div>
                    <div><div class="card-label">Max Allowed</div><div style="font-size:13px;color:#e8e6e1;">{s.get('max_daily_hours',10)}h</div></div>
                    <div><div class="card-label">Break Taken</div><div style="font-size:13px;color:#e8e6e1;">{s['break_minutes']}min</div></div>
                    <div><div class="card-label">Min Required</div><div style="font-size:13px;color:#e8e6e1;">{s.get('mandatory_break_minutes',30)}min</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    prod_rules = conn.execute("""
        SELECT pr.*, p.title as prod_title
        FROM production_rules pr
        JOIN productions p ON p.id = pr.production_id
        ORDER BY p.title
    """).fetchall()

    if prod_rules and user['role'] in ['Coordinator', 'Admin']:
        st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="section-title">Production Rule Configuration</div></div>', unsafe_allow_html=True)

        for rule in prod_rules:
            st.markdown(f"""
            <div class="card" style="margin-bottom:12px;">
                <div class="card-accent"></div>
                <div class="card-title">{rule['prod_title']}</div>
                <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:16px;margin-top:12px;">
                    <div><div class="card-label">Daily Max</div><div style="font-size:20px;font-family:'Barlow Condensed',sans-serif;font-weight:700;color:#c9b07a;">{rule['max_daily_hours']}h</div></div>
                    <div><div class="card-label">Weekly Max</div><div style="font-size:20px;font-family:'Barlow Condensed',sans-serif;font-weight:700;color:#c9b07a;">{rule['max_weekly_hours']}h</div></div>
                    <div><div class="card-label">Min Break</div><div style="font-size:20px;font-family:'Barlow Condensed',sans-serif;font-weight:700;color:#c9b07a;">{rule['mandatory_break_minutes']}min</div></div>
                    <div><div class="card-label">Base Rate</div><div style="font-size:20px;font-family:'Barlow Condensed',sans-serif;font-weight:700;color:#c9b07a;">${rule['base_rate']}/h</div></div>
                    <div><div class="card-label">OT Rate</div><div style="font-size:20px;font-family:'Barlow Condensed',sans-serif;font-weight:700;color:#c9b07a;">${rule['overtime_rate']}/h</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    conn.close()
    st.markdown('</div>', unsafe_allow_html=True)


def render_payroll(user):
    conn = get_db()

    st.markdown("""
    <div class="hero-section" style="padding:40px 48px 32px;">
        <div class="hero-eyebrow">Financial Processing</div>
        <div class="hero-title" style="font-size:40px;">Payroll <span>Processing</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    payroll_records = conn.execute("""
        SELECT p.*, u.full_name as extra_name, u.union_status,
               ws.clock_in, ws.total_hours as session_hours,
               s.scene_name, prod.title as prod_title,
               processor.full_name as processor_name
        FROM payroll p
        JOIN users u ON u.id = p.extra_id
        JOIN work_sessions ws ON ws.id = p.session_id
        JOIN scenes s ON s.id = ws.scene_id
        JOIN productions prod ON prod.id = s.production_id
        LEFT JOIN users processor ON processor.id = p.processed_by
        ORDER BY p.created_at DESC
    """).fetchall()

    total_processed = sum(r['total_amount'] for r in payroll_records if r['status'] == 'Processed')
    total_pending = sum(r['total_amount'] for r in payroll_records if r['status'] == 'Pending')
    overtime_total = sum(r['overtime_hours'] * r['overtime_rate'] for r in payroll_records)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-num">${total_processed:,.0f}</div><div class="metric-label">Total Processed</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-num" style="color:#e8a040;">${total_pending:,.0f}</div><div class="metric-label">Pending Disbursement</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-num" style="color:#5b9bd5;">${overtime_total:,.0f}</div><div class="metric-label">Overtime Paid</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-num">{len(payroll_records)}</div><div class="metric-label">Total Records</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    if user['role'] in ['Payroll', 'Admin']:
        approved_sessions = conn.execute("""
            SELECT ws.*, u.full_name as extra_name, s.scene_name, p.title as prod_title
            FROM work_sessions ws
            JOIN users u ON u.id = ws.extra_id
            JOIN scenes s ON s.id = ws.scene_id
            JOIN productions p ON p.id = s.production_id
            WHERE ws.hr_approved = 1 AND ws.id NOT IN (SELECT session_id FROM payroll)
        """).fetchall()

        if approved_sessions:
            st.markdown('<div class="section-header"><div class="section-title">Ready for Payroll Processing</div></div>', unsafe_allow_html=True)

            process_data = []
            for s in approved_sessions:
                hours = s['total_hours'] or 0
                ot_threshold = 8.0
                reg_hours = min(hours, ot_threshold)
                ot_hours = max(0, hours - ot_threshold)
                base_rate = 150.0
                ot_rate = 225.0
                total = (reg_hours * base_rate) + (ot_hours * ot_rate)
                process_data.append({
                    "Extra": s['extra_name'],
                    "Scene": s['scene_name'],
                    "Production": s['prod_title'],
                    "Hours": hours,
                    "Reg Hours": reg_hours,
                    "OT Hours": ot_hours,
                    "Base Rate": f"${base_rate}",
                    "OT Rate": f"${ot_rate}",
                    "Total": f"${total:,.2f}",
                    "Session ID": s['id'],
                })

            df_process = pd.DataFrame(process_data)
            st.dataframe(df_process.drop(columns=["Session ID"]), use_container_width=True)

            batch_id = f"BATCH-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            if st.button(f"Process All ({len(approved_sessions)} sessions) — Batch {batch_id}", use_container_width=True):
                for s in approved_sessions:
                    hours = s['total_hours'] or 0
                    reg_hours = min(hours, 8.0)
                    ot_hours = max(0, hours - 8.0)
                    total = (reg_hours * 150.0) + (ot_hours * 225.0)
                    conn.execute("""
                        INSERT INTO payroll (extra_id, session_id, base_rate, hours_worked, overtime_hours,
                        overtime_rate, total_amount, status, processed_by, processed_at, batch_id)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)
                    """, (s['extra_id'], s['id'], 150.0, hours, ot_hours, 225.0, total, "Processed",
                          user['id'], datetime.now().isoformat(), batch_id))
                conn.commit()
                log_action(user['id'], "Payroll batch processed", "payroll", None, f"Batch: {batch_id}, Sessions: {len(approved_sessions)}")
                st.success(f"Payroll batch {batch_id} processed successfully.")
                st.rerun()

    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-header"><div class="section-title">Payroll by Production</div></div>', unsafe_allow_html=True)
        prod_payroll = conn.execute("""
            SELECT prod.title, SUM(p.total_amount) as total, COUNT(p.id) as count
            FROM payroll p
            JOIN work_sessions ws ON ws.id = p.session_id
            JOIN scenes s ON s.id = ws.scene_id
            JOIN productions prod ON prod.id = s.production_id
            GROUP BY prod.id ORDER BY total DESC
        """).fetchall()

        if prod_payroll:
            fig = go.Figure(go.Bar(
                x=[r['title'][:20] for r in prod_payroll],
                y=[r['total'] for r in prod_payroll],
                marker_color="#c9b07a", marker_line=dict(width=0),
                text=[f"${r['total']:,.0f}" for r in prod_payroll],
                textposition="outside", textfont=dict(color="#888", size=10),
            ))
            fig.update_layout(
                paper_bgcolor="#0f0f0f", plot_bgcolor="#0f0f0f",
                font=dict(color="#888", family="Barlow, sans-serif", size=11),
                xaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a"),
                yaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a"),
                margin=dict(l=0, r=0, t=10, b=10), height=250,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col_b:
        st.markdown('<div class="section-header"><div class="section-title">Payment Breakdown</div></div>', unsafe_allow_html=True)
        total_ot = sum(r['overtime_hours'] * r['overtime_rate'] for r in payroll_records)
        total_reg = sum(r['total_amount'] - (r['overtime_hours'] * r['overtime_rate']) for r in payroll_records)

        fig2 = go.Figure(go.Pie(
            labels=["Regular Pay", "Overtime Pay"],
            values=[total_reg, total_ot],
            hole=0.55,
            marker=dict(colors=["#c9b07a", "#e05c4a"]),
            textinfo="label+percent",
            textfont=dict(size=11),
        ))
        fig2.update_layout(
            paper_bgcolor="#0f0f0f",
            font=dict(color="#888", family="Barlow, sans-serif"),
            showlegend=False,
            margin=dict(l=0, r=0, t=10, b=10), height=250,
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="section-title">Payroll Records</div></div>', unsafe_allow_html=True)

    display_data = [{
        "Extra": r['extra_name'],
        "Union": r['union_status'],
        "Scene": r['scene_name'],
        "Production": r['prod_title'],
        "Hours": f"{r['session_hours']:.2f}h",
        "OT Hours": f"{r['overtime_hours']:.2f}h",
        "Total": f"${r['total_amount']:,.2f}",
        "Status": r['status'],
        "Batch": r['batch_id'] or "N/A",
        "Processed By": r['processor_name'] or "N/A",
    } for r in payroll_records]

    if display_data:
        st.dataframe(pd.DataFrame(display_data), use_container_width=True, height=350)

        csv_buf = io.StringIO()
        pd.DataFrame(display_data).to_csv(csv_buf, index=False)
        st.download_button("Export Payroll CSV", csv_buf.getvalue(), "payroll_export.csv", "text/csv")

    conn.close()
    st.markdown('</div>', unsafe_allow_html=True)


def render_reports(user):
    conn = get_db()

    st.markdown("""
    <div class="hero-section" style="padding:40px 48px 32px;">
        <div class="hero-eyebrow">Analytics & Reporting</div>
        <div class="hero-title" style="font-size:40px;">System <span>Reports</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    report_type = st.selectbox("Select Report Type", [
        "Compliance Summary Report",
        "Call Sheet Report",
        "Payroll Summary Report",
        "Extra Hours Summary",
        "Production Overview",
        "Audit Trail Report",
    ])

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        from_date = st.date_input("From Date", value=date.today() - timedelta(days=30))
    with col_b:
        to_date = st.date_input("To Date", value=date.today())
    with col_c:
        prods = conn.execute("SELECT id, title FROM productions").fetchall()
        prod_opts = {"All Productions": 0} | {p['title']: p['id'] for p in prods}
        selected_prod = st.selectbox("Production", list(prod_opts.keys()))

    if st.button("Generate Report", use_container_width=True):
        prod_id = prod_opts[selected_prod]

        if report_type == "Compliance Summary Report":
            query = """
                SELECT u.full_name as extra_name, u.union_status,
                       s.scene_name, p.title as prod_title, s.scene_date,
                       ws.total_hours, ws.break_minutes, ws.compliance_flag,
                       ws.compliance_notes, ws.hr_approved, ws.status
                FROM work_sessions ws
                JOIN users u ON u.id = ws.extra_id
                JOIN scenes s ON s.id = ws.scene_id
                JOIN productions p ON p.id = s.production_id
                WHERE s.scene_date BETWEEN ? AND ?
            """
            params = [str(from_date), str(to_date)]
            if prod_id:
                query += " AND p.id = ?"
                params.append(prod_id)

            data = conn.execute(query, params).fetchall()
            df = pd.DataFrame([dict(r) for r in data])
            if not df.empty:
                st.markdown('<div class="section-header"><div class="section-title">Compliance Summary</div></div>', unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True)

                col1, col2, col3 = st.columns(3)
                with col1:
                    fig = go.Figure(go.Pie(
                        labels=["Compliant", "Flagged"],
                        values=[len(df[df['compliance_flag'] == 0]), len(df[df['compliance_flag'] == 1])],
                        hole=0.6, marker=dict(colors=["#4caf88", "#e05c4a"]),
                        textinfo="label+percent",
                    ))
                    fig.update_layout(paper_bgcolor="#0f0f0f", font=dict(color="#888"), showlegend=False,
                                      margin=dict(l=0, r=0, t=10, b=10), height=220)
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                with col2:
                    fig2 = go.Figure(go.Pie(
                        labels=["Approved", "Pending"],
                        values=[len(df[df['hr_approved'] == 1]), len(df[df['hr_approved'] == 0])],
                        hole=0.6, marker=dict(colors=["#c9b07a", "#555"]),
                        textinfo="label+percent",
                    ))
                    fig2.update_layout(paper_bgcolor="#0f0f0f", font=dict(color="#888"), showlegend=False,
                                       margin=dict(l=0, r=0, t=10, b=10), height=220)
                    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
                with col3:
                    avg_hrs = df['total_hours'].mean()
                    max_hrs = df['total_hours'].max()
                    st.markdown(f"""
                    <div class="card">
                        <div class="card-label">Average Hours</div>
                        <div style="font-size:32px;font-family:'Barlow Condensed',sans-serif;font-weight:700;color:#c9b07a;">{avg_hrs:.2f}h</div>
                        <div class="card-label" style="margin-top:12px;">Max Hours</div>
                        <div style="font-size:32px;font-family:'Barlow Condensed',sans-serif;font-weight:700;color:#e05c4a;">{max_hrs:.2f}h</div>
                    </div>
                    """, unsafe_allow_html=True)

                csv_buf = io.StringIO()
                df.to_csv(csv_buf, index=False)
                st.download_button("Export CSV", csv_buf.getvalue(), f"compliance_report_{from_date}_{to_date}.csv", "text/csv")
            else:
                st.info("No data found for the selected criteria.")

        elif report_type == "Call Sheet Report":
            query = """
                SELECT s.scene_name, s.scene_date, s.location, s.call_time, s.wrap_time,
                       s.required_role, p.title as prod_title,
                       GROUP_CONCAT(u.full_name, ', ') as extras_assigned,
                       COUNT(a.id) as extra_count, s.max_extras
                FROM scenes s
                JOIN productions p ON p.id = s.production_id
                LEFT JOIN assignments a ON a.scene_id = s.id AND a.status = 'Active'
                LEFT JOIN users u ON u.id = a.extra_id
                WHERE s.scene_date BETWEEN ? AND ?
            """
            params = [str(from_date), str(to_date)]
            if prod_id:
                query += " AND p.id = ?"
                params.append(prod_id)
            query += " GROUP BY s.id ORDER BY s.scene_date, s.call_time"

            data = conn.execute(query, params).fetchall()
            if data:
                st.markdown('<div class="section-header"><div class="section-title">Call Sheet</div></div>', unsafe_allow_html=True)
                for scene in data:
                    fill = int((scene['extra_count'] / max(scene['max_extras'], 1)) * 100)
                    st.markdown(f"""
                    <div class="card" style="margin-bottom:12px;">
                        <div class="card-accent"></div>
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
                            <div>
                                <div class="card-title">{scene['scene_name']}</div>
                                <div style="font-size:12px;color:#555;">{scene['prod_title']}</div>
                            </div>
                            <div style="text-align:right;">
                                <div style="font-size:24px;font-family:'Barlow Condensed',sans-serif;font-weight:700;color:#c9b07a;">{scene['call_time']}</div>
                                <div style="font-size:11px;color:#555;">{scene['scene_date']}</div>
                            </div>
                        </div>
                        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:12px;">
                            <div><div class="card-label">Location</div><div style="font-size:12px;color:#e8e6e1;">{scene['location']}</div></div>
                            <div><div class="card-label">Role Required</div><div style="font-size:12px;color:#e8e6e1;">{scene['required_role']}</div></div>
                            <div><div class="card-label">Wrap Time</div><div style="font-size:12px;color:#e8e6e1;">{scene['wrap_time']}</div></div>
                        </div>
                        <div style="margin-bottom:8px;">
                            <div class="card-label">Assigned Extras ({scene['extra_count']}/{scene['max_extras']})</div>
                            <div style="font-size:12px;color:#888;">{scene['extras_assigned'] or 'None assigned'}</div>
                        </div>
                        <div class="compliance-bar"><div class="compliance-bar-fill" style="width:{fill}%;"></div></div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No scenes found for the selected date range.")

        elif report_type == "Payroll Summary Report":
            query = """
                SELECT u.full_name, u.union_status, u.tax_classification,
                       SUM(pay.total_amount) as total_earned,
                       SUM(pay.hours_worked) as total_hours,
                       SUM(pay.overtime_hours) as total_ot,
                       COUNT(pay.id) as session_count,
                       GROUP_CONCAT(DISTINCT prod.title) as productions
                FROM payroll pay
                JOIN users u ON u.id = pay.extra_id
                JOIN work_sessions ws ON ws.id = pay.session_id
                JOIN scenes s ON s.id = ws.scene_id
                JOIN productions prod ON prod.id = s.production_id
                WHERE ws.clock_in BETWEEN ? AND ?
            """
            params = [str(from_date), str(to_date)]
            if prod_id:
                query += " AND prod.id = ?"
                params.append(prod_id)
            query += " GROUP BY u.id ORDER BY total_earned DESC"

            data = conn.execute(query, params).fetchall()
            if data:
                df = pd.DataFrame([dict(r) for r in data])
                st.dataframe(df, use_container_width=True)

                fig = go.Figure(go.Bar(
                    x=df['full_name'], y=df['total_earned'],
                    marker_color="#c9b07a", marker_line=dict(width=0),
                    text=[f"${v:,.0f}" for v in df['total_earned']],
                    textposition="outside",
                ))
                fig.update_layout(
                    paper_bgcolor="#0f0f0f", plot_bgcolor="#0f0f0f",
                    font=dict(color="#888", family="Barlow, sans-serif", size=11),
                    xaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a"),
                    yaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1d1a"),
                    margin=dict(l=0, r=0, t=10, b=40), height=280,
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                csv_buf = io.StringIO()
                df.to_csv(csv_buf, index=False)
                st.download_button("Export CSV", csv_buf.getvalue(), "payroll_summary.csv", "text/csv")
            else:
                st.info("No payroll data for the selected range.")

        elif report_type == "Audit Trail Report":
            query = """
                SELECT al.action, al.details, al.created_at, al.target_table,
                       u.full_name, u.role
                FROM audit_log al
                LEFT JOIN users u ON u.id = al.user_id
                WHERE al.created_at BETWEEN ? AND ?
                ORDER BY al.created_at DESC
            """
            params = [str(from_date), str(to_date) + " 23:59:59"]
            data = conn.execute(query, params).fetchall()

            if data:
                df = pd.DataFrame([dict(r) for r in data])
                st.dataframe(df, use_container_width=True, height=450)
                csv_buf = io.StringIO()
                df.to_csv(csv_buf, index=False)
                st.download_button("Export Audit CSV", csv_buf.getvalue(), "audit_trail.csv", "text/csv")
            else:
                st.info("No audit records found.")

        log_action(user['id'], f"Report generated: {report_type}", "reports", None, f"{from_date} to {to_date}")

    conn.close()
    st.markdown('</div>', unsafe_allow_html=True)


def render_disputes(user):
    conn = get_db()

    st.markdown("""
    <div class="hero-section" style="padding:40px 48px 32px;">
        <div class="hero-eyebrow">Resolution Center</div>
        <div class="hero-title" style="font-size:40px;">Dispute <span>Management</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    if user['role'] == 'Extra':
        with st.expander("Submit New Dispute", expanded=False):
            sessions = conn.execute("""
                SELECT ws.id, s.scene_name, ws.total_hours, ws.clock_in
                FROM work_sessions ws
                JOIN scenes s ON s.id = ws.scene_id
                WHERE ws.extra_id = ?
                ORDER BY ws.clock_in DESC
            """, (user['id'],)).fetchall()

            with st.form("submit_dispute"):
                dispute_type = st.selectbox("Dispute Type", ["Hours Discrepancy", "Compensation Issue", "Compliance Violation", "Assignment Error", "Payroll Error", "Other"])

                session_opts = {"None (General Dispute)": None} | {
                    f"Session #{s['id']} — {s['scene_name']} ({s['total_hours']:.1f}h)": s['id'] for s in sessions
                }
                selected_session = st.selectbox("Related Work Session", list(session_opts.keys()))
                description = st.text_area("Detailed Description", height=120, placeholder="Please provide as much detail as possible...")

                if st.form_submit_button("Submit Dispute", use_container_width=True):
                    if description:
                        session_id = session_opts[selected_session]
                        conn.execute("INSERT INTO disputes (extra_id, session_id, dispute_type, description) VALUES (?,?,?,?)",
                                     (user['id'], session_id, dispute_type, description))
                        conn.commit()
                        log_action(user['id'], "Dispute submitted", "disputes", None, f"Type: {dispute_type}")
                        st.success("Dispute submitted successfully. You will be notified of the resolution.")
                        st.rerun()
                    else:
                        st.error("Please provide a description.")

        disputes = conn.execute("""
            SELECT d.*, s.scene_name, ws.total_hours,
                   resolver.full_name as resolver_name
            FROM disputes d
            LEFT JOIN work_sessions ws ON ws.id = d.session_id
            LEFT JOIN scenes s ON s.id = ws.scene_id
            LEFT JOIN users resolver ON resolver.id = d.resolved_by
            WHERE d.extra_id = ?
            ORDER BY d.created_at DESC
        """, (user['id'],)).fetchall()

    else:
        disputes = conn.execute("""
            SELECT d.*, u.full_name as extra_name, s.scene_name, ws.total_hours,
                   resolver.full_name as resolver_name
            FROM disputes d
            JOIN users u ON u.id = d.extra_id
            LEFT JOIN work_sessions ws ON ws.id = d.session_id
            LEFT JOIN scenes s ON s.id = ws.scene_id
            LEFT JOIN users resolver ON resolver.id = d.resolved_by
            ORDER BY d.created_at DESC
        """).fetchall()

    open_disputes = [d for d in disputes if d['status'] == 'Open']
    resolved_disputes = [d for d in disputes if d['status'] != 'Open']

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-num" style="color:#e05c4a;">{len(open_disputes)}</div><div class="metric-label">Open Disputes</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-num" style="color:#4caf88;">{len(resolved_disputes)}</div><div class="metric-label">Resolved</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-num">{len(disputes)}</div><div class="metric-label">Total Disputes</div></div>', unsafe_allow_html=True)

    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    if open_disputes:
        st.markdown('<div class="section-header"><div class="section-title">Open Disputes</div></div>', unsafe_allow_html=True)
        for d in open_disputes:
            extra_name = d.get('extra_name', user['full_name'])
            st.markdown(f"""
            <div class="card" style="margin-bottom:12px;border-left:3px solid #e05c4a;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;">
                    <div>
                        <div class="card-title" style="font-size:15px;">{d['dispute_type']}</div>
                        <div style="font-size:12px;color:#555;">{extra_name} | {d['created_at'][:10]}</div>
                    </div>
                    <span class="badge badge-red">Open</span>
                </div>
                <div class="card-body" style="margin-bottom:12px;">{d['description']}</div>
                {f'<div style="font-size:11px;color:#555;">Related scene: {d["scene_name"]} ({d["total_hours"]:.1f}h)</div>' if d['scene_name'] else ''}
            </div>
            """, unsafe_allow_html=True)

            if user['role'] in ['HR', 'Admin', 'Coordinator']:
                with st.expander(f"Resolve Dispute #{d['id']}"):
                    resolution_text = st.text_area("Resolution Notes", key=f"res_{d['id']}", height=80)
                    new_status = st.selectbox("Resolution Status", ["Resolved", "Rejected", "Escalated"], key=f"rstat_{d['id']}")
                    if st.button(f"Submit Resolution", key=f"resolve_{d['id']}"):
                        if resolution_text:
                            conn.execute("""
                                UPDATE disputes SET status=?, resolution=?, resolved_by=?, resolved_at=?
                                WHERE id=?
                            """, (new_status, resolution_text, user['id'], datetime.now().isoformat(), d['id']))
                            conn.commit()
                            log_action(user['id'], f"Dispute {new_status.lower()}", "disputes", d['id'])
                            st.success(f"Dispute #{d['id']} marked as {new_status}.")
                            st.rerun()
                        else:
                            st.error("Please provide resolution notes.")

    if resolved_disputes:
        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="section-title">Resolved Disputes</div></div>', unsafe_allow_html=True)
        for d in resolved_disputes:
            extra_name = d.get('extra_name', user['full_name'])
            badge_cls = "badge-green" if d['status'] == 'Resolved' else ("badge-red" if d['status'] == 'Rejected' else "badge-gold")
            st.markdown(f"""
            <div class="card" style="margin-bottom:8px;opacity:0.8;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div>
                        <div style="font-size:13px;font-weight:600;color:#888;">{d['dispute_type']} — {extra_name}</div>
                        <div style="font-size:11px;color:#444;margin-top:4px;">{d['description'][:100]}...</div>
                    </div>
                    <span class="badge {badge_cls}">{d['status']}</span>
                </div>
                {f'<div style="margin-top:8px;font-size:12px;color:#555;padding:8px;background:#0a0a0a;border:1px solid #111;">{d["resolution"]}</div>' if d['resolution'] else ''}
            </div>
            """, unsafe_allow_html=True)

    conn.close()
    st.markdown('</div>', unsafe_allow_html=True)


def render_admin(user):
    conn = get_db()

    st.markdown("""
    <div class="hero-section" style="padding:40px 48px 32px;">
        <div class="hero-eyebrow">System Administration</div>
        <div class="hero-title" style="font-size:40px;">Admin <span>Console</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["User Management", "System Statistics", "Audit Log", "Database Overview"])

    with tab1:
        with st.expander("Create New User", expanded=False):
            with st.form("create_user"):
                col1, col2 = st.columns(2)
                with col1:
                    new_fullname = st.text_input("Full Name")
                    new_username = st.text_input("Username")
                    new_email = st.text_input("Email")
                    new_phone = st.text_input("Phone")
                with col2:
                    new_role = st.selectbox("Role", ["Extra", "Coordinator", "HR", "Payroll", "Admin"])
                    new_union = st.selectbox("Union Status", ["Non-Union", "SAG-AFTRA", "ACTRA", "Equity", "N/A"])
                    new_tax = st.selectbox("Tax Classification", ["W-2", "1099", "Corp-to-Corp", "N/A"])
                    new_password = st.text_input("Temporary Password", type="password")

                if st.form_submit_button("Create User", use_container_width=True):
                    if all([new_fullname, new_username, new_password]):
                        existing = conn.execute("SELECT id FROM users WHERE username=?", (new_username,)).fetchone()
                        if existing:
                            st.error("Username already exists.")
                        else:
                            conn.execute("INSERT INTO users (username, password, full_name, email, role, union_status, tax_classification, phone) VALUES (?,?,?,?,?,?,?,?)",
                                         (new_username, hash_password(new_password), new_fullname, new_email, new_role, new_union, new_tax, new_phone))
                            conn.commit()
                            log_action(user['id'], "User created", "users", None, f"Created: {new_username} ({new_role})")
                            st.success(f"User '{new_fullname}' created as {new_role}.")
                            st.rerun()
                    else:
                        st.error("Name, username, and password are required.")

        users = conn.execute("SELECT id, username, full_name, email, role, union_status, is_active, created_at FROM users ORDER BY role, full_name").fetchall()

        st.markdown('<div class="section-header"><div class="section-title">All System Users</div></div>', unsafe_allow_html=True)

        user_df = pd.DataFrame([dict(u) for u in users])
        st.dataframe(user_df, use_container_width=True, height=350)

        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        user_opts = {f"{u['full_name']} ({u['username']})": u['id'] for u in users if u['id'] != user['id']}
        if user_opts:
            selected_user = st.selectbox("Select User to Toggle Status", list(user_opts.keys()))
            target_user = conn.execute("SELECT * FROM users WHERE id=?", (user_opts[selected_user],)).fetchone()
            if target_user:
                curr_status = "Active" if target_user['is_active'] else "Inactive"
                new_active = 0 if target_user['is_active'] else 1
                if st.button(f"{'Deactivate' if target_user['is_active'] else 'Activate'} — {target_user['full_name']}"):
                    conn.execute("UPDATE users SET is_active=? WHERE id=?", (new_active, target_user['id']))
                    conn.commit()
                    log_action(user['id'], f"User {'deactivated' if not new_active else 'activated'}", "users", target_user['id'])
                    st.success(f"User status updated.")
                    st.rerun()

    with tab2:
        st.markdown('<div class="section-header"><div class="section-title">System-Wide Statistics</div></div>', unsafe_allow_html=True)

        stats = {
            "Total Users": conn.execute("SELECT COUNT(*) FROM users").fetchone()[0],
            "Active Users": conn.execute("SELECT COUNT(*) FROM users WHERE is_active=1").fetchone()[0],
            "Total Productions": conn.execute("SELECT COUNT(*) FROM productions").fetchone()[0],
            "Total Scenes": conn.execute("SELECT COUNT(*) FROM scenes").fetchone()[0],
            "Total Assignments": conn.execute("SELECT COUNT(*) FROM assignments").fetchone()[0],
            "Work Sessions": conn.execute("SELECT COUNT(*) FROM work_sessions").fetchone()[0],
            "Total Hours Logged": f"{conn.execute('SELECT COALESCE(SUM(total_hours),0) FROM work_sessions').fetchone()[0]:.1f}h",
            "Total Payroll": f"${conn.execute('SELECT COALESCE(SUM(total_amount),0) FROM payroll').fetchone()[0]:,.2f}",
            "Open Disputes": conn.execute("SELECT COUNT(*) FROM disputes WHERE status='Open'").fetchone()[0],
            "Audit Records": conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0],
        }

        cols = st.columns(5)
        for i, (label, value) in enumerate(stats.items()):
            with cols[i % 5]:
                st.markdown(f"""
                <div class="metric-card" style="margin-bottom:12px;">
                    <div class="metric-num">{value}</div>
                    <div class="metric-label">{label}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

        roles_data = conn.execute("SELECT role, COUNT(*) as count FROM users GROUP BY role").fetchall()
        fig = go.Figure(go.Bar(
            x=[r['role'] for r in roles_data],
            y=[r['count'] for r in roles_data],
            marker_color=["#c9b07a", "#5b9bd5", "#4caf88", "#e05c4a", "#e8a040"],
            marker_line=dict(width=0),
        ))
        fig.update_layout(
            paper_bgcolor="#0f0f0f", plot_bgcolor="#0f0f0f",
            font=dict(color="#888", family="Barlow, sans-serif", size=11),
            xaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a"),
            yaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a"),
            title=dict(text="Users by Role", font=dict(color="#888", size=12)),
            margin=dict(l=0, r=0, t=40, b=10), height=250,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with tab3:
        st.markdown('<div class="section-header"><div class="section-title">Audit Trail</div></div>', unsafe_allow_html=True)

        logs = conn.execute("""
            SELECT al.*, u.full_name, u.role
            FROM audit_log al
            LEFT JOIN users u ON u.id = al.user_id
            ORDER BY al.created_at DESC
            LIMIT 100
        """).fetchall()

        log_df = pd.DataFrame([dict(l) for l in logs])
        st.dataframe(log_df, use_container_width=True, height=500)

        csv_buf = io.StringIO()
        log_df.to_csv(csv_buf, index=False)
        st.download_button("Export Audit Log", csv_buf.getvalue(), "audit_log.csv", "text/csv")

    with tab4:
        st.markdown('<div class="section-header"><div class="section-title">Database Table Counts</div></div>', unsafe_allow_html=True)

        tables = ["users", "productions", "scenes", "assignments", "availability",
                  "work_sessions", "payroll", "disputes", "audit_log", "production_rules", "contracts"]

        table_data = []
        for t in tables:
            count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            table_data.append({"Table": t, "Records": count})

        df_tables = pd.DataFrame(table_data)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_tables, use_container_width=True)
        with col2:
            fig = go.Figure(go.Bar(
                y=df_tables['Table'], x=df_tables['Records'],
                orientation='h', marker_color="#c9b07a", marker_line=dict(width=0),
                text=df_tables['Records'], textposition="outside",
            ))
            fig.update_layout(
                paper_bgcolor="#0f0f0f", plot_bgcolor="#0f0f0f",
                font=dict(color="#888", family="Barlow, sans-serif", size=11),
                xaxis=dict(gridcolor="#1a1a1a", linecolor="#1a1a1a"),
                yaxis=dict(linecolor="#1a1a1a"),
                margin=dict(l=0, r=40, t=10, b=10), height=320,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    conn.close()
    st.markdown('</div>', unsafe_allow_html=True)


def render_profile(user):
    conn = get_db()

    st.markdown("""
    <div class="hero-section" style="padding:40px 48px 32px;">
        <div class="hero-eyebrow">Account Management</div>
        <div class="hero-title" style="font-size:40px;">My <span>Profile</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-content">', unsafe_allow_html=True)
    st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)

    u = conn.execute("SELECT * FROM users WHERE id=?", (user['id'],)).fetchone()
    u = dict(u)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-accent"></div>
            <div style="text-align:center;padding:24px 0;">
                <div style="width:80px;height:80px;background:linear-gradient(135deg,#c9b07a,#8a7040);border-radius:0;margin:0 auto 16px;display:flex;align-items:center;justify-content:center;">
                    <span style="font-family:'Barlow Condensed',sans-serif;font-size:32px;font-weight:700;color:#0a0a0a;">{u['full_name'][0].upper()}</span>
                </div>
                <div style="font-family:'Barlow Condensed',sans-serif;font-size:22px;font-weight:700;color:#f0ede8;">{u['full_name']}</div>
                <div style="margin:8px 0;"><span class="role-pill">{u['role']}</span></div>
                <div style="font-size:12px;color:#555;margin-top:12px;">@{u['username']}</div>
            </div>
            <div style="border-top:1px solid #1a1a1a;padding-top:16px;">
                <div style="display:grid;gap:12px;">
                    <div><div class="card-label">Union Status</div><div style="font-size:13px;color:#c9b07a;">{u['union_status']}</div></div>
                    <div><div class="card-label">Tax Classification</div><div style="font-size:13px;color:#e8e6e1;">{u['tax_classification']}</div></div>
                    <div><div class="card-label">Email</div><div style="font-size:13px;color:#e8e6e1;">{u['email'] or 'Not set'}</div></div>
                    <div><div class="card-label">Phone</div><div style="font-size:13px;color:#e8e6e1;">{u['phone'] or 'Not set'}</div></div>
                    <div><div class="card-label">Member Since</div><div style="font-size:13px;color:#e8e6e1;">{u['created_at'][:10]}</div></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header"><div class="section-title">Update Profile</div></div>', unsafe_allow_html=True)

        with st.form("update_profile"):
            upd_name = st.text_input("Full Legal Name", value=u['full_name'])
            upd_email = st.text_input("Email Address", value=u['email'] or "")
            upd_phone = st.text_input("Phone Number", value=u['phone'] or "")
            col_a, col_b = st.columns(2)
            with col_a:
                upd_union = st.selectbox("Union Status", ["Non-Union", "SAG-AFTRA", "ACTRA", "Equity"],
                                          index=["Non-Union", "SAG-AFTRA", "ACTRA", "Equity"].index(u['union_status']) if u['union_status'] in ["Non-Union", "SAG-AFTRA", "ACTRA", "Equity"] else 0)
            with col_b:
                upd_tax = st.selectbox("Tax Classification", ["W-2", "1099", "Corp-to-Corp"],
                                        index=["W-2", "1099", "Corp-to-Corp"].index(u['tax_classification']) if u['tax_classification'] in ["W-2", "1099", "Corp-to-Corp"] else 0)

            if st.form_submit_button("Update Profile", use_container_width=True):
                conn.execute("UPDATE users SET full_name=?, email=?, phone=?, union_status=?, tax_classification=? WHERE id=?",
                             (upd_name, upd_email, upd_phone, upd_union, upd_tax, user['id']))
                conn.commit()
                log_action(user['id'], "Profile updated", "users", user['id'])
                st.session_state.user['full_name'] = upd_name
                st.success("Profile updated successfully.")
                st.rerun()

        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="section-title">Change Password</div></div>', unsafe_allow_html=True)

        with st.form("change_password"):
            cur_pwd = st.text_input("Current Password", type="password")
            new_pwd = st.text_input("New Password", type="password")
            confirm_pwd = st.text_input("Confirm New Password", type="password")

            if st.form_submit_button("Change Password", use_container_width=True):
                if conn.execute("SELECT id FROM users WHERE id=? AND password=?", (user['id'], hash_password(cur_pwd))).fetchone():
                    if new_pwd == confirm_pwd and len(new_pwd) >= 8:
                        conn.execute("UPDATE users SET password=? WHERE id=?", (hash_password(new_pwd), user['id']))
                        conn.commit()
                        log_action(user['id'], "Password changed", "users", user['id'])
                        st.success("Password changed successfully.")
                    else:
                        st.error("Passwords do not match or are too short (min 8 chars).")
                else:
                    st.error("Current password is incorrect.")

    if user['role'] == 'Extra':
        st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="section-title">Availability Management</div></div>', unsafe_allow_html=True)

        col_av1, col_av2 = st.columns(2)
        with col_av1:
            with st.form("add_availability"):
                avail_date = st.date_input("Available Date")
                unavail_start = st.time_input("Unavailable From (optional)", value=None)
                unavail_end = st.time_input("Unavailable Until (optional)", value=None)
                avail_notes = st.text_input("Notes")

                if st.form_submit_button("Add Availability", use_container_width=True):
                    conn.execute("INSERT INTO availability (extra_id, avail_date, unavail_start, unavail_end, notes) VALUES (?,?,?,?,?)",
                                 (user['id'], str(avail_date),
                                  str(unavail_start) if unavail_start else None,
                                  str(unavail_end) if unavail_end else None,
                                  avail_notes))
                    conn.commit()
                    log_action(user['id'], "Availability updated", "availability", None, f"Date: {avail_date}")
                    st.success(f"Availability added for {avail_date}")
                    st.rerun()

        with col_av2:
            avail_records = conn.execute("""
                SELECT * FROM availability WHERE extra_id=? ORDER BY avail_date DESC LIMIT 14
            """, (user['id'],)).fetchall()

            if avail_records:
                avail_df = pd.DataFrame([dict(r) for r in avail_records])
                avail_df = avail_df[['avail_date', 'unavail_start', 'unavail_end', 'notes']]
                avail_df.columns = ['Date', 'Unavail From', 'Unavail Until', 'Notes']
                st.dataframe(avail_df, use_container_width=True, height=280)
            else:
                st.markdown('<div class="card"><div class="card-body">No availability records. Add dates you are available.</div></div>', unsafe_allow_html=True)

        st.markdown('<div style="height:24px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-header"><div class="section-title">My Earnings Summary</div></div>', unsafe_allow_html=True)

        earnings = conn.execute("""
            SELECT p.total_amount, p.hours_worked, p.overtime_hours, p.status, p.processed_at,
                   s.scene_name, prod.title as prod_title
            FROM payroll p
            JOIN work_sessions ws ON ws.id = p.session_id
            JOIN scenes s ON s.id = ws.scene_id
            JOIN productions prod ON prod.id = s.production_id
            WHERE p.extra_id = ?
            ORDER BY p.created_at DESC
        """, (user['id'],)).fetchall()

        if earnings:
            total_earned = sum(e['total_amount'] for e in earnings)
            total_hours_paid = sum(e['hours_worked'] for e in earnings)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="metric-card"><div class="metric-num">${total_earned:,.0f}</div><div class="metric-label">Total Earned</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-card"><div class="metric-num">{total_hours_paid:.1f}h</div><div class="metric-label">Hours Paid</div></div>', unsafe_allow_html=True)
            with col3:
                avg = total_earned / len(earnings) if earnings else 0
                st.markdown(f'<div class="metric-card"><div class="metric-num">${avg:,.0f}</div><div class="metric-label">Avg per Session</div></div>', unsafe_allow_html=True)

            st.markdown('<div style="height:12px;"></div>', unsafe_allow_html=True)
            earn_df = pd.DataFrame([{
                "Scene": e['scene_name'],
                "Production": e['prod_title'],
                "Hours": e['hours_worked'],
                "OT Hours": e['overtime_hours'],
                "Amount": f"${e['total_amount']:,.2f}",
                "Status": e['status'],
            } for e in earnings])
            st.dataframe(earn_df, use_container_width=True)
        else:
            st.markdown('<div class="card"><div class="card-body">No payroll records yet.</div></div>', unsafe_allow_html=True)

    conn.close()
    st.markdown('</div>', unsafe_allow_html=True)


def main():
    init_db()

    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = "login"

    if not st.session_state.user:
        render_login_page()
        return

    user = st.session_state.user
    page = st.session_state.get('page', 'dashboard')

    role = user['role']
    role_nav = {
        "Admin": ["dashboard", "productions", "scenes", "assignments", "worksessions", "compliance", "payroll", "reports", "disputes", "admin", "profile"],
        "Coordinator": ["dashboard", "productions", "scenes", "assignments", "compliance", "reports", "profile"],
        "HR": ["dashboard", "worksessions", "compliance", "reports", "disputes", "profile"],
        "Payroll": ["dashboard", "worksessions", "payroll", "reports", "profile"],
        "Extra": ["dashboard", "assignments", "worksessions", "disputes", "profile"],
    }
    allowed = role_nav.get(role, ["dashboard"])
    if page not in allowed:
        page = "dashboard"
        st.session_state.page = "dashboard"

    nav_labels = {
        "dashboard": "Overview", "productions": "Productions", "scenes": "Scenes",
        "assignments": "Assignments", "worksessions": "Work Sessions", "compliance": "Compliance",
        "payroll": "Payroll", "reports": "Reports", "disputes": "Disputes",
        "admin": "Admin", "profile": "Profile",
    }

    st.markdown(f"""
    <div class="nav-bar">
        <div class="nav-brand">CineCompliance<span style="color:#333;font-weight:300;font-size:13px;letter-spacing:1px;margin-left:8px;">Pro</span></div>
        <div class="nav-user">
            <span class="role-pill">{role}</span>
            <span style="color:#666;">{user['full_name']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    nav_cols = st.columns(len(allowed) + 1)
    for i, pg in enumerate(allowed):
        with nav_cols[i]:
            if st.button(nav_labels[pg], key=f"nav_{pg}", use_container_width=True,
                          type="primary" if pg == page else "secondary"):
                st.session_state.page = pg
                st.rerun()
    with nav_cols[-1]:
        if st.button("Sign Out", key="signout", use_container_width=True):
            log_action(user['id'], "User logout", "users", user['id'])
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()

    if page == "dashboard":
        render_dashboard(user)
    elif page == "productions":
        render_productions(user)
    elif page == "scenes":
        render_scenes(user)
    elif page == "assignments":
        render_assignments(user)
    elif page == "worksessions":
        render_work_sessions(user)
    elif page == "compliance":
        render_compliance(user)
    elif page == "payroll":
        render_payroll(user)
    elif page == "reports":
        render_reports(user)
    elif page == "disputes":
        render_disputes(user)
    elif page == "admin":
        render_admin(user)
    elif page == "profile":
        render_profile(user)


if __name__ == "__main__":
    main()