import streamlit as st
import pandas as pd
import plotly.express as px
import networkx as nx
from streamlit_agraph import agraph, Node, Edge, Config

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Prof. Alex Mercer | Research Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MOCK DATA GENERATION ---
# In a real app, this would come from a Google Scholar API or a CSV file
@st.cache_data
def load_data():
    data = [
        {"id": 1, "title": "Deep Learning for Climate Modeling", "year": 2023, "citations": 45, "field": "AI & Climate", "type": "Journal", "summary": "Using neural networks to predict extreme weather events with 90% accuracy.", "co_authors": ["Sarah Chen", "J. Doe"]},
        {"id": 2, "title": "Ethical Implications of Generative AI", "year": 2024, "citations": 12, "field": "AI Ethics", "type": "Conference", "summary": "A framework for assessing bias in Large Language Models.", "co_authors": ["A. Smith", "Sarah Chen"]},
        {"id": 3, "title": "Quantum Computing in Drug Discovery", "year": 2021, "citations": 150, "field": "Quantum", "type": "Journal", "summary": "Speeding up molecular simulation using 50-qubit processors.", "co_authors": ["M. Johnson"]},
        {"id": 4, "title": "Robotics in Surgery: A Review", "year": 2020, "citations": 300, "field": "Robotics", "type": "Review", "summary": "Comprehensive analysis of automated surgical systems.", "co_authors": ["J. Doe", "M. Johnson"]},
        {"id": 5, "title": "Zero-Shot Learning in Wild", "year": 2025, "citations": 5, "field": "Computer Vision", "type": "Preprint", "summary": "Recognizing animals in the wild without prior training examples.", "co_authors": ["A. Smith"]}
    ]
    return pd.DataFrame(data)

df = load_data()

# --- SIDEBAR INFO ---
with st.sidebar:
    st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=Alex", width=150)
    st.title("Prof. Alex Mercer")
    st.markdown("**Director, Future AI Lab**")
    st.markdown("📍 MIT Media Lab")
    st.write("---")
    st.metric(label="Total Citations", value=df['citations'].sum(), delta="+12 this week")
    st.metric(label="h-index", value=14)
    st.write("---")
    st.markdown("### 📬 Contact")
    st.text("alex@university.edu")
    st.markdown("[Google Scholar](#) | [Twitter](#)")

# --- MAIN TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Impact Dashboard", "📚 Publication Library", "🕸️ Knowledge Graph", "🤖 Chat with Research"])

# --- TAB 1: IMPACT DASHBOARD ---
with tab1:
    st.header("Research Impact & Timeline")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Interactive Timeline
        fig_timeline = px.scatter(
            df, x="year", y="citations", 
            size="citations", color="field",
            hover_name="title", text="year",
            title="Citation Impact over Time",
            size_max=60
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col2:
        # Topic Distribution
        # CORRECT WAY to make a donut chart
        fig_pie = px.pie(
        df, 
        names="field", 
        title="Research Focus Areas", 
        hole=0.4  # <--- This creates the donut shape
    )
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown("### 🌍 Real World Application")
    st.info("💡 **Did you know?** The research on *Climate Modeling* (2023) was cited in the latest **UN IPCC Report**.")

# --- TAB 2: PUBLICATION LIBRARY ---
with tab2:
    st.header("The Library")
    
    # Filters
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        selected_field = st.multiselect("Filter by Topic", options=df['field'].unique(), default=df['field'].unique())
    with col_filter2:
        sort_by = st.selectbox("Sort By", ["Year (Newest)", "Citations (Highest)"])
    
    # Filter Logic
    filtered_df = df[df['field'].isin(selected_field)]
    if "Year" in sort_by:
        filtered_df = filtered_df.sort_values(by="year", ascending=False)
    else:
        filtered_df = filtered_df.sort_values(by="citations", ascending=False)

    # Render Cards
    for index, row in filtered_df.iterrows():
        with st.container():
            c1, c2 = st.columns([0.8, 0.2])
            with c1:
                st.subheader(f"{row['title']}")
                st.caption(f"{row['year']} | {row['type']} | {row['field']}")
                
                # The "Plain English" Toggle Feature
                with st.expander("📝 Read 'Plain English' Summary"):
                    st.markdown(f"**Why this matters:** {row['summary']}")
                    st.markdown("*Click to download PDF* 📄")
            with c2:
                st.metric("Citations", row['citations'])
            st.divider()

# --- TAB 3: KNOWLEDGE GRAPH ---
with tab3:
    st.header("Interactive Network")
    st.markdown("Explore how my papers, co-authors, and research topics connect.")
    
    # Build Graph
    nodes = []
    edges = []
    
    # Add Central Node (The Professor)
    nodes.append(Node(id="Prof. Mercer", label="Prof. Mercer", size=25, color="#FF4B4B"))
    
    # Add Paper Nodes and Links
    for index, row in df.iterrows():
        # Node for the paper
        nodes.append(Node(id=row['title'], label=str(row['year']), size=15, color="#1f77b4"))
        edges.append(Edge(source="Prof. Mercer", target=row['title'], label="authored"))
        
        # Nodes for Co-Authors (linking them to the paper)
        for author in row['co_authors']:
            nodes.append(Node(id=author, label=author, size=10, color="#2ca02c")) # Green for authors
            edges.append(Edge(source=row['title'], target=author, label="co-authored"))

    # Configuration for the Physics Engine
    config = Config(width="100%", height=500, directed=False, 
                    nodeHighlightBehavior=True, highlightColor="#F7A7A6",
                    collapsible=True)

    # Render Graph
    # Note: We convert nodes to a set and back to list to remove duplicates in a real app, 
    # but agraph handles IDs well.
    return_value = agraph(nodes=nodes, edges=edges, config=config)

# --- TAB 4: CHATBOT (MOCK) ---
with tab4:
    st.header("🤖 Chat with my Research")
    st.markdown("""
    I have trained an AI on all my PDF publications. 
    **Ask a question like:** *"What is your stance on bias in AI?"* or *"Summarize your findings on climate neural nets."*
    """)
    
    # Chat UI
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask a question about the research..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response (Mock logic)
        with st.chat_message("assistant"):
            response = "This is a simulated response. In a real app, this would query a Vector Database (like Pinecone) containing chunks of the professor's PDFs."
            if "climate" in prompt.lower():
                response = "In my 2023 paper, I demonstrated that neural networks can improve extreme weather prediction accuracy by 90% compared to traditional physics models."
            
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})