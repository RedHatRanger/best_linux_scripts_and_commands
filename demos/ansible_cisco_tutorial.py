import streamlit as st

# ============================
# PowerPoint-Style Config
# ============================
st.set_page_config(
    page_title="Ansible 101 - The Automation Revolution",
    page_icon="Cisco",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Clean, professional styling
st.markdown("""
<style>
    .main { background: #0e1117; color: white; }
    .slide-title { font-size: 3.0rem !important; font-weight: bold; text-align: center; margin: 2rem 0; 
                   background: linear-gradient(90deg, #EE2E24, #1E88E5); -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent; }
    .slide-subtitle { font-size: 2.2rem; text-align: center; color: #aaa; margin-bottom: 3rem; }
    .big-text { font-size: 2.5rem; text-align: center; line-height: 1.6; }
    .code-block { background: #1e1e1e; padding: 20px; border-radius: 15px; font-size: 1.6rem; margin: 30px 0; }
    .footer { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); color: #666; font-size: 1.2rem; }
    .nav-btn { font-size: 2rem; height: 80px; width: 200px; }
    hr { border: 1px solid #333; margin: 60px 0; }
</style>
""", unsafe_allow_html=True)

# ============================
# Slides (One message per slide — pure PowerPoint style)
# ============================
slides = [
    {"title": "Ansible: The Basics", "subtitle": "The simplest way to automate everything", "content": "Cisco"},
    
    {"title": "No Agents", "content": """
    <div class="big-text">
    Just SSH + Python<br><br>
    Nothing to install on managed servers<br>
    No daemons, no services, no hassle
    </div>
    """},
    
    {"title": "Pure YAML", "content": """
    <div class="big-text">
    Playbooks = Human-readable automation<br><br>
    Declarative Style<br>
    No custom scripting language<br>
    Just clean, simple YAML
    </div>
    """},
    
    {"title": "Idempotent", "content": """
    <div class="big-text">
    Run your playbook 1× or 100×<br>
    → Same perfect result<br><br>
    Safe. Predictable. Professional.
    </div>
    """},
    
    {"title": "Your First Command", "content": """
    <div class="code-block">
    ansible all -m ping
    </div>
    <div class="big-text">→ You get green <code>pong!</code> from every server</div>
    """},
    
    {"title": "Your First Playbook", "content": """
    <div class="code-block">
    ---
    - name: Web server setup
      hosts: webservers
      become: yes
      tasks:
        - name: Install Nginx
          apt:
            name: nginx
            state: present

        - name: Start service
          service:
            name: nginx
            state: started
            enabled: yes
        </div>
    """},
    
    {"title": "Run It", "content": """
    <div class="code-block">
    ansible-playbook site.yml
    </div>
    <div class="big-text">→ First run: <span style="color:#ff9900">changed</span><br>
    → Second run: <span style="color:#00ff00">already perfect</span></div>
    """},
    
    {"title": "From 1 to 10,000 servers", "content": """
    <div class="big-text">
    Same exact playbook works on<br>
    • Your laptop<br>
    • 5 dev servers<br>
    • 10,000 production nodes<br><br>
    No changes needed
    </div>
    """},
    
    {"title": "Real World Structure", "content": """
    <div class="big-text">
    Roles → Reusable, shareable, testable<br><br>
    <code>ansible-galaxy role init webserver</code><br>
    Used by Netflix, NASA, Red Hat, and you!
    </div>
    """},
    
    {"title": "Congrats! You Are Now Dangerous", "content": """
    <div class="big-text">
    Go forth and automate!<br><br>
    <code>pip install ansible</code><br>
    → Then change the world
    </div>
    """},
    
    {"title": "Thank You!", "subtitle": "Questions?", "content": "Raised Hands"},
]

# ============================
# Session State
# ============================
if "slide" not in st.session_state:
    st.session_state.slide = 0

max_slide = len(slides) - 1

# ============================
# Navigation
# ============================
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("Previous Slide", disabled=st.session_state.slide == 0, use_container_width=True, key="prev"):
        st.session_state.slide -= 1
        st.rerun()

with col2:
    current = slides[st.session_state.slide]
    st.markdown(f"<h1 class='slide-title'>{current['title']}</h1>", unsafe_allow_html=True)
    if "subtitle" in current:
        st.markdown(f"<h3 class='slide-subtitle'>{current['subtitle']}</h3>", unsafe_allow_html=True)

with col3:
    if st.button("Next Slide", disabled=st.session_state.slide == max_slide, use_container_width=True, key="next"):
        st.session_state.slide += 1
        st.rerun()

# Progress
st.progress((st.session_state.slide + 1) / len(slides))

# Main content
current = slides[st.session_state.slide]
if "content" in current and current["content"] not in ["Cisco", "Raised Hands"]:
    st.markdown(current["content"], unsafe_allow_html=True)
else:
    st.markdown(f"<div class='big-text'>{current['content']}</div>", unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class="footer">
Slide {st.session_state.slide + 1} / {len(slides)}  •  Press F for fullscreen  •  Made with Streamlit
</div>
""", unsafe_allow_html=True)

# Final celebration
if st.session_state.slide == max_slide:
    if st.button("That's all folks!"):
        st.balloons()
