import os
import streamlit as st
import requests
import time
import uuid
import logfire
from dotenv import load_dotenv


# ---------------------------------------------------------
# LOAD LOCAL ENVIRONMENT
# ---------------------------------------------------------
env_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", ".env")
)
load_dotenv(dotenv_path=env_path)


# ---------------------------------------------------------
# LOGFIRE
# ---------------------------------------------------------
try:
    token = st.secrets.get("LOGFIRE_TOKEN", os.getenv("LOGFIRE_TOKEN"))

    if token:
        logfire.configure(token=token)
        LOGFIRE_STATUS = "Connected & Tracing"
    else:
        LOGFIRE_STATUS = "Standby (No Token)"

except Exception as e:
    LOGFIRE_STATUS = f"Standby (Error: {e})"


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Enterprise Agentic RAG",
    page_icon="🤖",
    layout="wide",
)


# ---------------------------------------------------------
# AVATARS
# ---------------------------------------------------------
AI_AVATAR = "🤖"
USER_AVATAR = "👤"


# ---------------------------------------------------------
# BACKEND URL
# ---------------------------------------------------------
try:
    BACKEND_URL = st.secrets.get(
        "BACKEND_URL",
        os.getenv("BACKEND_URL", "http://localhost:8000")
    )
except Exception:
    BACKEND_URL = os.getenv(
        "BACKEND_URL",
        "http://localhost:8000"
    )

BACKEND_URL = BACKEND_URL.rstrip("/")


# ---------------------------------------------------------
# SESSION MANAGEMENT
# ---------------------------------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

    try:
        logfire.info(
            f"✨ New User Session Created: "
            f"{st.session_state.session_id}"
        )
    except Exception:
        pass


if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:

    st.title("🧠 Agent OS")
    st.markdown("---")

    st.success(f"Logfire: {LOGFIRE_STATUS}")

    st.info(
        f"Memory ID: "
        f"{st.session_state.session_id[:8]}"
    )

    if st.button(
        "🗑️ Clear History & Memory",
        width="stretch",
        type="primary"
    ):
        try:
            logfire.warning(
                "🗑️ Memory Wipe Triggered for session: "
                f"{st.session_state.session_id}"
            )
        except Exception:
            pass

        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())

        st.rerun()


# ---------------------------------------------------------
# MAIN CHAT
# ---------------------------------------------------------
st.title("🤖 Enterprise Agentic Assistant")


# ---------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------
for message in st.session_state.messages:

    avatar = (
        AI_AVATAR
        if message["role"] == "assistant"
        else USER_AVATAR
    )

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):
        st.markdown(message["content"])


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------
if prompt := st.chat_input(
    "Ask about your documentation..."
):

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message(
        "user",
        avatar=USER_AVATAR
    ):
        st.markdown(prompt)


    # -----------------------------------------------------
    # ASSISTANT RESPONSE
    # -----------------------------------------------------
    with st.chat_message(
        "assistant",
        avatar=AI_AVATAR
    ):

        data = {}

        with st.status(
            "🔍 Agent is thinking...",
            expanded=True
        ) as status:

            try:

                # -----------------------------------------
                # BACKEND REQUEST
                # -----------------------------------------
                with logfire.span(
                    "📡 Calling RAG Backend"
                ):

                    url = f"{BACKEND_URL}/query"

                    payload = {
                        "q": prompt,
                        "thread_id":
                            st.session_state.session_id
                    }

                    response = requests.post(
                        url,
                        json=payload,
                        timeout=120
                    )


                # -----------------------------------------
                # HTTP ERROR
                # -----------------------------------------
                if response.status_code != 200:

                    st.error(
                        f"Backend Error: "
                        f"{response.status_code}"
                    )

                    st.code(response.text)

                    status.update(
                        label="❌ Backend Error",
                        state="error"
                    )

                    st.stop()


                # -----------------------------------------
                # JSON RESPONSE
                # -----------------------------------------
                data = response.json()


                # -----------------------------------------
                # THOUGHT PROCESS
                # -----------------------------------------
                steps = data.get(
                    "thought_process",
                    []
                )

                for step in steps:
                    st.write(f"⚙️ {step}")


                status.update(
                    label="✅ Answer Synthesized",
                    state="complete",
                    expanded=False
                )


            except requests.exceptions.ConnectionError:

                status.update(
                    label="❌ Backend Unreachable",
                    state="error"
                )

                st.error(
                    "❌ Cannot connect to the FastAPI backend."
                )

                st.info(
                    f"Backend URL currently configured as:\n\n"
                    f"`{BACKEND_URL}`"
                )

                st.stop()


            except requests.exceptions.Timeout:

                status.update(
                    label="❌ Backend Timeout",
                    state="error"
                )

                st.error(
                    "❌ The backend took too long to respond."
                )

                st.stop()


            except Exception as e:

                try:
                    logfire.error(
                        f"❌ UI-Backend Connection Failed: {e}"
                    )
                except Exception:
                    pass

                status.update(
                    label="❌ Connection Failed",
                    state="error"
                )

                st.error(
                    f"Unexpected error: {e}"
                )

                st.stop()


        # -------------------------------------------------
        # ANSWER
        # -------------------------------------------------
        answer_placeholder = st.empty()

        full_answer = data.get(
            "answer",
            "No response."
        )

        curr_text = ""

        for char in full_answer:

            curr_text += char

            answer_placeholder.markdown(
                curr_text + "▌"
            )

            time.sleep(0.005)

        answer_placeholder.markdown(
            full_answer
        )


        # -------------------------------------------------
        # SOURCES
        # -------------------------------------------------
        sources = data.get(
            "sources",
            []
        )

        if sources:

            with st.expander(
                f"📄 Retrieved Context "
                f"({len(sources)} chunks)"
            ):

                for i, source in enumerate(sources):

                    st.caption(
                        f"Chunk {i + 1}"
                    )

                    st.info(source)

        else:

            st.caption(
                "ℹ️ No context retrieved — "
                "conversational response."
            )


        # -------------------------------------------------
        # SAVE ASSISTANT MESSAGE
        # -------------------------------------------------
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_answer
            }
        )

        try:
            logfire.info(
                "✅ Chat cycle completed successfully."
            )
        except Exception:
            pass