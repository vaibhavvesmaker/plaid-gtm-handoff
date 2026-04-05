# ⚡ Plaid GTM Handoff Structurer
### *Automating the "Bandaids": Bridging the gap between Sales Discovery and Technical Implementation.*
![Streamlit](https://img.shields.io/badge/Live_Prototype-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) 
👉 [Click here to view the Live App](https://plaid-gtm-handoff-5teplzqnevly6drj6mgay7.streamlit.app/)


## 🎯 The Mission
In high-growth Fintech GTM, the "Sales-to-Implementation" handoff is often a friction point. Messy discovery notes lead to manual triage, delayed integration, and slower "Time to First Transaction" (TTFT).

This prototype is a **GTM Intelligence Agent** designed to ingest raw, unstructured sales notes and output a structured, implementation-ready technical brief. It moves Plaid's GTM from **Manual Triage** to **Automated Intelligence.**

## 🚀 Core Features
* **Entity Extraction:** Automatically identifies Account Names, Deal Stages, and Stakeholders.
* **Product Mapping:** Uses a specialized schema to identify **Explicit** vs. **Inferred** Plaid products (Auth, Signal, Transfer, etc.).
* **Readiness Scoring:** A proprietary 0-100 score that determines if a deal is "Ready," "Needs Clarification," or "Blocked."
* **Owner-Based Actions:** Generates specific, high-velocity next steps for AEs, Solutions Engineers, and Implementation Managers.
* **Risk Detection:** Flags "Critical Blockers" like missing technical owners or unresolved compliance dependencies.

## 🛠️ The Tech Stack
* **Engine:** Gemini 2.0 Flash (via Google GenAI SDK)
* **Framework:** Python & Streamlit
* **Logic:** Structured JSON Schema Prompting (Agentic Reasoning)
* **Environment:** Secure Secret Management (Streamlit Secrets / .env)

## 📊 How it Works
1.  **Input:** Paste raw notes from a CRM, Slack, or a discovery call.
2.  **Process:** The Agent parses the text against Plaid’s product suite and GTM operational requirements.
3.  **Output:** A clean, actionable dashboard showing exactly what needs to happen to get the customer live.

## 📈 Scalability (The GTM Ops Vision)
This prototype is a proof-of-concept for a wider **GTM Engineering** vision:
* **CRM Integration:** Trigger via Salesforce Webhooks when a stage changes to 'Verbal Commit'.
* **RAG Implementation:** Connect to Plaid's internal Documentation (via Pinecone/Vector DB) for real-time technical gap analysis.
* **Slack Ops:** Automated "Handoff Alerts" sent directly to the assigned Implementation Engineer.

---
*Created with a focus on GTM Strategy & Operations @ Plaid.*
