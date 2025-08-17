import streamlit as st
import random
import string

# Import your multi-agent objects (must be available in project)
# group_chat.py should define `user`, `manager`, and `notification_agent`
from group_chat import user, manager, notification_agent

# ---------- Helpers ----------

def generate_ticket_id(prefix="TKT", length=6):
    """Generate a random alphanumeric ticket ID (uppercase)."""
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}-{suffix}"

def extract_solutions_from_text(text: str) -> str:
    """
    Extract lines that contain the token 'Solution:' and return them nicely.
    If no Solution: token is found, returns the original text trimmed.
    """
    if not text:
        return ""
    solutions = []
    for line in text.splitlines():
        if "Solution:" in line:
            # everything after last "Solution:"
            sol = line.split("Solution:")[-1].strip()
            if sol:
                solutions.append(sol)
    if solutions:
        # return enumerated or bulleted solutions
        return "\n\n".join(f"{i+1}. {s}" for i, s in enumerate(solutions))
    # fallback: return the entire non-empty text
    return text.strip()

# ---------- UI / Layout ----------

st.set_page_config(page_title="HelpX AI Assistant", page_icon="🤖", layout="centered")

# Load custom CSS file (ensure style.css exists in same folder)
try:
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    # graceful fallback if css is missing
    st.warning("style.css not found — continuing with default styling.")

st.markdown(
    """
    <div class="title-container">
        <h1> 🤖 HelpX AI Assistant</h1>
    </div>
    <div class="subtitle">Your smart and reliable IT support partner. </div>
    <div class="description"><em>Describe your issue below and HelpX will try to help.</em></div>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
st.session_state.setdefault("final_response", None)
st.session_state.setdefault("user_input", "")
st.session_state.setdefault("awaiting_feedback", False)
st.session_state.setdefault("feedback_given", False)

# Input section
st.markdown('<div class="input-label">Describe your IT issue:</div>', unsafe_allow_html=True)
# Provide an accessible label but collapse it visually (Streamlit 1.24+)
user_input = st.text_area(
    "Describe your IT issue",
    value=st.session_state.user_input,
    height=160,
    label_visibility="collapsed",
)

# ---------- Chat / Agent invocation ----------

if st.button("Resolve Now") and user_input.strip():
    st.session_state.user_input = user_input.strip()
    st.session_state.final_response = None
    st.session_state.awaiting_feedback = False
    st.session_state.feedback_given = False

    with st.spinner("HelpX is resolving your issue..."):
        # We'll capture messages received by `user.receive`
        responses = []
        original_receive = user.receive  # save original reference

        def receive_and_capture(*args, **kwargs):
            """
            Capture the incoming message safely. Accept both dict messages and strings.
            Append only non-empty text content to `responses`, then call original_receive.
            """
            try:
                message = None
                if args:
                    message = args[0]
                elif "message" in kwargs:
                    message = kwargs["message"]

                content = None
                # Common case: message is dict with a "content" key
                if isinstance(message, dict):
                    # sometimes content is nested; this extracts 'content' if present
                    content = message.get("content") or message.get("output") or None
                    # if content is still a dict, try to stringify if contains 'text' or 'message'
                    if isinstance(content, dict):
                        # attempt to flatten a couple common possibilities
                        content = content.get("text") or content.get("message") or str(content)
                else:
                    # fallback: if message is a plain string or other, stringify
                    content = str(message) if message is not None else None

                if content:
                    content_str = content.strip()
                    if content_str:
                        responses.append(content_str)
            except Exception as e:
                # don't break the flow on unexpected shapes; log for debugging
                print("receive_and_capture error:", e)

            # Call original receive so agent system continues to function
            return original_receive(*args, **kwargs)

        # Monkeypatch user.receive to capture outgoing messages to the user
        user.receive = receive_and_capture

        # Initiate the group chat using your manager / multi-agent flow
        # Note: `manager` is expected to be the GroupChatManager or recipient you used earlier
        user.initiate_chat(recipient=manager, message=user_input)

        # Restore original receive method
        user.receive = original_receive

        # If we captured messages, show cleaned output
        if responses:
            # Join responses with separators so parser can find tool output easily
            combined = "\n\n---\n\n".join(responses)
            # Extract only 'Solution:' parts
            only_solutions = extract_solutions_from_text(combined)

            # If the top-level agent returned just a JSON-like classification as the first message,
            # it might appear earlier in `responses`. We prioritize `only_solutions` if it's non-empty.
            if only_solutions:
                display_text = only_solutions
            else:
                # fallback to full combined content
                display_text = combined

            st.session_state.final_response = display_text
            st.session_state.awaiting_feedback = True
            st.session_state.feedback_given = False

            st.success("AI Response:")
            # Use markdown for nicer formatting (bullet/numbering preserved)
            st.markdown(display_text.replace("\n", "  \n"))  # preserve newlines in markdown
        else:
            st.warning("No response received from the agents. Please check logs or agent config.")

# ---------- Feedback / Escalation ----------

if st.session_state.awaiting_feedback and st.session_state.final_response and not st.session_state.feedback_given:
    st.markdown("### 🙋 Was this solution helpful?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("✅Yes — resolved"):
            st.session_state.feedback_given = True
            st.session_state.awaiting_feedback = False
            st.success("🎉 Great! Happy to help — thank you for your feedback.")

    with col2:
        if st.button("❌No — not helpful"):
            st.session_state.feedback_given = True
            st.session_state.awaiting_feedback = False
            ticket_id = generate_ticket_id()
            st.warning(f"⚠️ We've escalated the issue to IT support. Ticket ID: `{ticket_id}`")

            notification_message = (
                f"Escalation: 🚨Unresolved IT issue\n\n"
                f"User reported: '{st.session_state.user_input}'\n"
                f"📄 Ticket ID: {ticket_id}"
            )

            # Call your notification agent to send email/alert (assumes generate_reply returns dict with content)
            # If notification_agent API differs, adapt accordingly
            reply = notification_agent.generate_reply(
                messages=[{"role": "user", "content": notification_message}],
                sender=user,
            )
            final_reply = reply.get("content") if isinstance(reply, dict) else str(reply)
            st.info(f"Notification agent response:\n\n{final_reply}")
