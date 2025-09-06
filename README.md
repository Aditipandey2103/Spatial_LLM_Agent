🧠 Chain-of-Thought Spatial Analysis LLM Agent

An AI-powered geospatial analysis app built with LangChain, Groq LLaMA-3, GeoPandas, and Streamlit.
It enables users to perform complex spatial operations (buffering, intersections, summarization, etc.) using natural language queries.

This app is not just another mapping tool — it’s a next-generation intelligent geospatial assistant.
Using Groq LLaMA-3, LangChain, and GeoPandas, the app can think, plan, and execute complex spatial analysis tasks based on natural language instructions.

It bridges the gap between AI reasoning and geospatial computation, enabling automated chain-of-thought orchestration for solving advanced problems like:

Predicting areas at risk during floods

Detecting overlapping hazard zones

Summarizing critical infrastructure impacts

Extracting insights from massive spatial datasets

Handling buffering, intersections, overlays, summarizations, and more

🚀 Features

✅ Chain-of-Thought Reasoning — Uses LLM to intelligently plan & execute geospatial tasks
✅ Spatial Analysis — Supports buffering, intersections, summarization & more
✅ GeoJSON Uploads — Upload your school zone & flood zone data
✅ Groq LLaMA-3 Integration — Super-fast LLM inference via Groq API
✅ Streamlit UI — Clean & interactive web interface
✅ Secrets Management — Secure handling of your API key

The app will:

Load both layers

Perform intersection analysis

Summarize the affected schools

Return the structured results

🛠 Tech Stack
Component	Technology Used
Frontend	Streamlit
Backend	Python
LLM Engine	Groq LLaMA-3 (via LangChain)
Spatial Ops	GeoPandas, Shapely, Fiona, Pyproj
Deployment	Streamlit Cloud

💡 Example Queries

Upload your GeoJSON layers and ask things like:

“Find which schools are located within flood-prone areas and summarize the total number of affected students.”

“Compare hospital coverage areas with population density zones and highlight regions lacking healthcare access.”

“Detect road networks that intersect active landslide-prone regions and suggest alternative routes.”

The agent automatically:

Breaks your request into smaller reasoning steps

Generates a Chain-of-Thought plan

Executes the geospatial operations

Returns clear, concise results — no manual scripting required.

📧 Contact

👩‍💻 Author: Aditi Pandey
📌 GitHub: Aditipandey2103

📌 Project Repo: Spatial_LLM_Agent
