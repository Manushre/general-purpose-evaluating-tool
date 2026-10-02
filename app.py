import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# -----------------------------
# Configuration
# -----------------------------
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("GEMINI_API_KEY not found in .env")
    st.stop()

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.5-flash-lite"

# -----------------------------
# Page
# -----------------------------
st.set_page_config(
    page_title="General Purpose Evaluating Tool",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 General Purpose Evaluating Tool")
st.caption("AI-powered software discovery, evaluation and comparison")

st.divider()

# -----------------------------
# Requirement
# -----------------------------
st.subheader("What tool do you need?")

user_request = st.text_area(
    "Describe your requirement",
    placeholder=(
        "Example: I need a platform to learn Agentic AI "
        "with practical projects and Python support."
    ),
    height=120
)

evaluate = st.button("Evaluate Tools", type="primary")


# -----------------------------
# Agent Instructions
# -----------------------------
def build_prompt(requirement):

    return f"""
You are a General Purpose Tool Evaluation Agent.

USER REQUIREMENT:
{requirement}

Your job is to evaluate software/tools for ANY requirement.

You must dynamically perform these steps:

1. Understand the user's actual goal.
2. Identify the required tool category.
3. Generate evaluation criteria based on THIS requirement.
4. Identify 3 to 5 suitable tools.
5. Evaluate each tool against the criteria.
6. Compare the tools.
7. Identify strengths and limitations.
8. Select the tool that best matches the stated requirements.
9. Explain the decision and trade-offs.

Do NOT assume a fixed category.

The user may ask for:
- AI tools
- marketing tools
- meeting tools
- learning platforms
- CRM tools
- ABM tools
- coding tools
- design tools
- automation tools
- project management tools
- or any other software.

Return the result using this structure:

# REQUIREMENT ANALYSIS

**Goal:**
**Tool Category:**
**Important Requirements:**

# DYNAMIC EVALUATION CRITERIA

1.
2.
3.
4.
5.

# TOOL DISCOVERY

| Tool | Purpose | Key Capability |
|---|---|---|

# COMPARISON

| Criteria | Tool 1 | Tool 2 | Tool 3 | Tool 4 |
|---|---|---|---|---|

# EVALUATION

For every tool provide:

**Strengths**
- 

**Limitations**
- 

**Requirement Fit**
- 

# RECOMMENDATION

**Recommended Tool:**

**Why it matches:**

**Important Trade-offs:**

# AGENT DECISION SUMMARY

**Requirement understood:**

**Criteria generated:**

**Tools evaluated:**

**Decision reasoning:**

Keep the answer professional and concise.

Do not invent exact pricing, features, or certifications when uncertain.
"""


# -----------------------------
# Run Agent
# -----------------------------
if evaluate:

    if not user_request.strip():
        st.warning("Please enter your requirement.")
        st.stop()

    st.info("Agent is analysing your requirement...")

    try:

        prompt = build_prompt(user_request)

        # New Gemini Interactions API
        interaction = client.interactions.create(
            model=MODEL,
            input=prompt
        )

        result = interaction.output_text

        if result:

            st.success("Evaluation completed.")

            st.divider()

            st.markdown(result)

        else:

            st.error("The AI returned an empty response.")

    except Exception as e:

        error = str(e)

        st.error("Evaluation could not be completed.")

        with st.expander("Technical details"):
            st.code(error)

        if "429" in error:
            st.warning(
                "Gemini quota has been reached for this API project. "
                "The application code is working, but the API project "
                "needs available quota."
            )

        elif "404" in error:
            st.warning(
                "The selected Gemini model is not available for this API key."
            )

        elif "503" in error:
            st.warning(
                "Gemini is temporarily unavailable. Please try again."
            )