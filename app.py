import os
import json
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Plaid GTM Handoff Structurer", layout="wide")

st.markdown(
    """
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subtext {
        font-size: 1.05rem;
        color: #B0B7C3;
        margin-bottom: 1.2rem;
    }
    .info-card {
        background-color: #111827;
        border: 1px solid #2A3342;
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 1.2rem;
    }
    .section-card {
        background-color: #0F172A;
        border: 1px solid #1F2937;
        border-radius: 16px;
        padding: 16px 18px;
        margin-top: 0.8rem;
        margin-bottom: 1rem;
    }
    .small-label {
        font-size: 0.9rem;
        color: #9CA3AF;
        margin-bottom: 0.35rem;
    }
        .status-badge {
        display: inline-block;
        padding: 8px 14px;
        border-radius: 999px;
        font-size: 0.95rem;
        font-weight: 700;
        margin-top: 0.4rem;
        margin-bottom: 0.8rem;
    }
    .status-ready {
        background-color: rgba(34, 197, 94, 0.18);
        color: #86EFAC;
        border: 1px solid rgba(34, 197, 94, 0.35);
    }
    .status-clarify {
        background-color: rgba(245, 158, 11, 0.18);
        color: #FCD34D;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .status-blocked {
        background-color: rgba(239, 68, 68, 0.18);
        color: #FCA5A5;
        border: 1px solid rgba(239, 68, 68, 0.35);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">Plaid GTM Handoff Structurer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtext">Turn messy sales and implementation notes into a structured, implementation-ready GTM brief.</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-card">
        <div class="small-label">What this prototype does</div>
        It extracts customer context, identifies blockers, scores handoff readiness, and recommends owner-based next steps so downstream teams can start faster with less manual triage.
    </div>
    """,
    unsafe_allow_html=True
)

if not api_key:
    st.error("Missing GEMINI_API_KEY in your .env file")
    st.stop()

client = genai.Client(api_key=api_key)

handoff_notes = st.text_area(
    "Paste handoff notes here",
    height=300,
    placeholder="Paste AE notes, CRM notes, discovery notes, or internal handoff text here..."
)

if st.button("Generate Handoff Brief"):
    if not handoff_notes.strip():
        st.warning("Please paste some handoff notes first.")
    else:
        prompt = f"""
You are a GTM Operations analyst at Plaid.

Your job is to convert messy sales or handoff notes into a structured internal brief.

Return ONLY valid JSON with the following keys:
- account_name
- deal_stage
- customer_use_case
- products_explicitly_mentioned
- products_inferred
- stakeholders
- risks
- missing_information
- next_steps
- handoff_readiness_score
- handoff_status
- critical_blockers
- owner_actions
- score_reasoning
- draft_handoff_summary

Rules:
- If something is not explicitly known, write "Unknown" for a single value or [] for a list.
- products_explicitly_mentioned should include only products directly named in the notes.
- products_inferred should be conservative and include only products strongly supported by the notes.
- Do not infer Plaid products unless there is clear evidence from the use case.
- Do not include generic Plaid products just because the customer works in payments.
- If inference is weak or uncertain, return [].
- handoff_readiness_score should be a number from 0 to 100.
- handoff_status must be one of: "Ready", "Needs Clarification", "Blocked".
- critical_blockers should be short bullet-style strings, not long paragraphs.
- owner_actions must be a JSON object with keys like "AE", "Implementation", "Customer", "Risk/Compliance", and "Solutions Engineering" when relevant.
- Each owner_actions value must be a list of short action items.
- Prioritize Plaid/GTM handoff issues over generic project management issues.
- Focus blockers and actions on implementation readiness, technical discovery, operational ownership, and customer onboarding risk.
- Prefer blockers such as unclear payment flow, unknown current processor, undefined webhook requirements, missing fraud/risk workflow, missing fallback verification requirements, lack of technical owner, and unresolved compliance dependencies.
- Owner actions should be specific, operational, and relevant to a fintech GTM handoff.
- Avoid vague actions like "follow up" unless paired with exactly what needs to be clarified.
- Be practical and concise.
- Focus on operational usefulness.
- Do not include markdown.
- Output only raw JSON.
- Do not make compliance-related assumptions beyond what is stated in the notes.
- If compliance is mentioned but not specified, refer to it generically as "compliance review" or "compliance dependency".
- Keep owner action bullets short and direct, ideally under 12 words.
- Only include an owner in owner_actions if there is at least one concrete action.
- Keep actions grounded in the notes and avoid adding unsupported specificity.
- If a role has no action items, omit it from owner_actions.
- Do not rewrite "compliance review" into a more specific compliance process unless explicitly stated.

Handoff Notes:
{handoff_notes}
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            raw_output = response.text.strip()
            clean_output = raw_output.replace("```json", "").replace("```", "").strip()

            try:
                parsed = json.loads(clean_output)
            except json.JSONDecodeError:
                with st.expander("Raw Model Output (Invalid JSON)"):
                    st.code(raw_output)
                st.error("The model did not return valid JSON. Try again with clearer notes.")
                st.stop()

            with st.expander("Raw Model Output"):
                st.code(clean_output, language="json")

            st.subheader("Handoff Overview")

            col1, col2, col3 = st.columns(3)
            col1.metric("Account", parsed.get("account_name", "Unknown"))
            col2.metric("Stage", parsed.get("deal_stage", "Unknown"))
            col3.metric("Readiness Score", parsed.get("handoff_readiness_score", "Unknown"))

            # --- STATUS BADGE LOGIC ---
            status = parsed.get("handoff_status", "Unknown")

            if status == "Ready":
                status_class = "status-ready"
            elif status == "Needs Clarification":
                status_class = "status-clarify"
            elif status == "Blocked":
                status_class = "status-blocked"
            else:
                status_class = "status-clarify"

            st.markdown(
                f'<div class="status-badge {status_class}">{status}</div>',
                unsafe_allow_html=True
            )
            # --- END STATUS BADGE LOGIC ---
            st.markdown(f"**Use Case:** {parsed.get('customer_use_case', 'Unknown')}")

            st.subheader("Products")

            explicit_products = parsed.get("products_explicitly_mentioned", [])
            inferred_products = parsed.get("products_inferred", [])

            st.markdown("**Explicitly Mentioned**")
            if explicit_products:
                for item in explicit_products:
                    st.markdown(f"- {item}")
            else:
                st.markdown("- None")

            st.markdown("**Inferred**")
            if inferred_products:
                for item in inferred_products:
                    st.markdown(f"- {item}")
            else:
                st.markdown("- None")

            st.subheader("Stakeholders")
            stakeholders = parsed.get("stakeholders", [])
            if stakeholders:
                for item in stakeholders:
                    st.markdown(f"- {item}")
            else:
                st.markdown("- None identified")

            st.subheader("Risks")
            risks = parsed.get("risks", [])
            if risks:
                for item in risks:
                    st.markdown(f"- {item}")
            else:
                st.markdown("- None identified")

            st.subheader("Missing Information")
            missing_info = parsed.get("missing_information", [])
            if missing_info:
                for item in missing_info:
                    st.markdown(f"- {item}")
            else:
                st.markdown("- None")

            st.subheader("Critical Blockers")
            blockers = parsed.get("critical_blockers", [])
            cleaned_blockers = [b.strip() for b in blockers if isinstance(b, str) and b.strip()] if isinstance(blockers, list) else []

            if cleaned_blockers:
                for item in cleaned_blockers:
                    st.markdown(f"- {item}")
            else:
                st.markdown("- None")

            st.subheader("Owner Actions")
            owner_actions = parsed.get("owner_actions", {})

            shown_owner = False
            if owner_actions and isinstance(owner_actions, dict):
                for owner, actions in owner_actions.items():
                    if isinstance(actions, list):
                        cleaned_actions = [a.strip() for a in actions if isinstance(a, str) and a.strip()]
                        if cleaned_actions:
                            shown_owner = True
                            st.markdown(f"**{owner}**")
                            for action in cleaned_actions:
                                st.markdown(f"- {action}")
                    elif isinstance(actions, str) and actions.strip():
                        shown_owner = True
                        st.markdown(f"**{owner}**")
                        st.markdown(f"- {actions.strip()}")

            if not shown_owner:
                st.markdown("- No owner actions assigned")

            st.subheader("Next Steps")
            next_steps = parsed.get("next_steps", [])
            cleaned_steps = [s.strip() for s in next_steps if isinstance(s, str) and s.strip()] if isinstance(next_steps, list) else []

            if cleaned_steps:
                for step in cleaned_steps:
                    st.markdown(f"- {step}")
            else:
                st.markdown("- None")

            st.subheader("Score Reasoning")
            score_reasoning = parsed.get("score_reasoning", "No reasoning provided.")
            st.write(score_reasoning.strip() if isinstance(score_reasoning, str) else "No reasoning provided.")

            st.subheader("Draft Summary")
            draft_summary = parsed.get("draft_handoff_summary", "No summary generated.")
            st.write(draft_summary.strip() if isinstance(draft_summary, str) else "No summary generated.")

        except Exception as e:
            st.error(f"Error: {e}")