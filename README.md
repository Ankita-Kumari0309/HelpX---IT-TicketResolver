# HelpX AI Assistant – Intelligent IT Support Platform

**HelpX AI Assistant** is a multi-agent system designed to enhance IT support efficiency by automatically classifying tickets, providing instant AI-driven solutions, and escalating unresolved issues via email. The platform leverages **Azure OpenAI**, **vector search**, and **agent-based automation** to reduce response time and improve productivity for IT teams.

---
Output :- 

<img width="1915" height="982" alt="Screenshot 2025-08-17 204758" src="https://github.com/user-attachments/assets/a9d6c165-ed23-4930-af18-ae1cacc51392" />

<img width="1911" height="985" alt="Screenshot 2025-08-17 204809" src="https://github.com/user-attachments/assets/f85e0818-5678-41d2-adb5-01dc6ad392fb" />

<img width="1915" height="971" alt="image" src="https://github.com/user-attachments/assets/2c7be2cc-ff5b-438a-8a9b-817232648cec" />

<img width="1919" height="964" alt="image" src="https://github.com/user-attachments/assets/3a647dac-729d-4b29-9ceb-72ec4ea428a1" />



## Key Features
- **Natural Language Interface**: Users can submit IT issues in plain English.  
- **Automated Ticket Categorization**: AI agents classify tickets (e.g., Password Reset, Network Issue) for faster resolution.  
- **Knowledge Base Retrieval**: Uses vector similarity search to fetch the most relevant solutions from a curated knowledge base.  
- **Email Escalation**: Tickets unresolved by AI are automatically escalated to IT support.  
- **Interactive Streamlit UI**: Simple web interface for submitting tickets, viewing solutions, and providing feedback.  

---

## Project Structure

<img width="636" height="433" alt="image" src="https://github.com/user-attachments/assets/50f310b2-529a-457a-b111-061a415a5d7e" />


## How It Works

1. User submits an IT issue via the web interface.

2. Multi-agent system processes the ticket:

3. Classifier Agent identifies the issue category.

4. Knowledge Base Agent retrieves solutions using vector search.

5. Notification Agent escalates unresolved tickets via email.

6. Users can provide feedback to improve future responses.

## Customization

1. Knowledge Base: Update data/knowledge_base.json with new IT solutions.

2. Agent Prompts: Modify utility/prompt.py to change AI response behavior.

3. Email Settings: Configure SMTP in tools/send_email.py.


## Technologies Used

* Programming Languages: Python

* Frameworks & Libraries: Streamlit, LangChain, pandas, NumPy

* Concepts: Multi-Agent Systems, Vector Search, LLM Integration, Agent-Based Automation

* Cloud: Azure OpenAI, Azure Cognitive Search


