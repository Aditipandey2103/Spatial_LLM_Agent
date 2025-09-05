import os
import streamlit as st
import geopandas as gpd
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_experimental.utilities.python import PythonREPL
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# -----------------------------
# Streamlit UI Setup
# -----------------------------
st.set_page_config(page_title="Spatial LLM Agent", page_icon="🧠")
st.title("Chain-of-Thought Spatial Analysis with LLM")

st.markdown("""
This tool allows you to use natural language to perform **complex spatial operations**  
(like buffering, intersecting, summarizing layers) using an **LLM-powered agent**.
""")

# -----------------------------
# File Uploaders
# -----------------------------
school_file = st.file_uploader("Upload School Zones GeoJSON", type=["geojson"])
flood_file = st.file_uploader("Upload Flood Zones GeoJSON", type=["geojson"])

# -----------------------------
# Utility Functions
# -----------------------------
def load_layer(file):
    return gpd.read_file(file)

def buffer_layer(layer, distance, output_name="buffered_layer"):
    """Buffer a GeoDataFrame layer and save result globally."""
    result = layer.copy().buffer(distance)
    globals()[output_name] = gpd.GeoDataFrame(geometry=result)
    return f"Layer '{output_name}' created successfully."

def intersect_layer(layer1, layer2, output_name="school_zones_in_flood_zones"):
    """Find intersection and save result globally."""
    result = gpd.overlay(layer1, layer2, how="intersection")
    globals()[output_name] = result
    return f"Layer '{output_name}' created successfully."

def summarize_features(layer):
    """Return statistical summary of a GeoDataFrame."""
    return layer.describe(include='all')

def get_layer(name: str):
    """Retrieve a GeoDataFrame layer by name from globals."""
    print("DEBUG get_layer input:", name, type(name))
    if name in globals():
        return globals()[name]
    else:
        raise ValueError(f"Layer '{name}' not found. Available: {list(globals().keys())}")

# -----------------------------
# Define Tools for LLM Agent
# -----------------------------
tools = [
    Tool(
        name="BufferLayer",
        func=lambda x: buffer_layer(
            get_layer(str(x).split(',')[0].strip()),
            float(str(x).split(',')[1]),
            output_name="buffer_result"
        ),
        description="Buffers a given GeoDataFrame layer by a distance in meters. Input: 'layer,distance'"
    ),
    Tool(
        name="IntersectLayers",
        func=lambda x: intersect_layer(
            get_layer(str(x).split(',')[0].strip()),
            get_layer(str(x).split(',')[1].strip()),
            output_name="school_zones_in_flood_zones"
        ),
        description="Finds the intersection between two GeoDataFrame layers. Input: 'layer1,layer2'"
    ),
    Tool(
        name="SummarizeFeatures",
        func=lambda x: str(summarize_features(get_layer(str(x).strip()))),
        description="Returns a statistical summary of the GeoDataFrame. Input: 'layer'"
    ),
    Tool(
        name="Python REPL",
        func=PythonREPL().run,
        description="A Python shell. Use this to execute raw Python code."
    )
]

# -----------------------------
# LLM Setup
# -----------------------------
llm = ChatOpenAI(
    temperature=0,
    model_name="llama-3.3-70b-versatile",
    openai_api_base="https://api.groq.com/openai/v1",
    openai_api_key=groq_api_key
)

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

# -----------------------------
# Main App Logic
# -----------------------------
if school_file and flood_file:
    school_zones = load_layer(school_file)
    flood_zones = load_layer(flood_file)

    # Store initial layers globally
    globals()["school_zones"] = school_zones
    globals()["flood_zones"] = flood_zones

    # Input query from user
    query = st.text_area(
        "Enter your spatial query:",
        "Given school_zones and flood_zones layers, find which schools lie in flood zones and summarize them."
    )

    if st.button("Run Query"):
        with st.spinner("Thinking..."):
            try:
                response = agent.run(query)
                st.success("Query complete!")
                st.markdown("**LLM Output:**")
                st.code(response)

                if "school_zones_in_flood_zones" in globals():
                    st.subheader("Intersection Results")
                    st.dataframe(globals()["school_zones_in_flood_zones"])

                # ✅ Automatically display buffer results if generated
                if "buffer_result" in globals():
                    st.subheader("Buffered Layer Results")
                    st.dataframe(globals()["buffer_result"])



            except Exception as r:
                st.error(f"Error: {str(r)}")
else:
    st.warning("Please upload both GeoJSON layers to proceed.")


