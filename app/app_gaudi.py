#from typing import Generator
import streamlit as st
import requests

st.set_page_config(page_icon="💬", layout="wide",
                   page_title="Groq på svenska")

st.title("Mixtral-gaudi på svenska lokalt")

st.subheader("Mixtral-gaudi på svenska lokalt", divider="rainbow", anchor=False)

# Initialize chat history and selected model
if "messages" not in st.session_state:
    st.session_state.messages = []

# Define model details
models = {
    "gaudi-mixtral": {"name": "Gaudi-Mixtral", "tokens": 64000, "developer": "Mistral"},
    "mixtral-8x7b-32768": {"name": "Mixtral-8x7b-Instruct-v0.1", "tokens": 32768, "developer": "Mistral"},
}
# --- API Configuration ---
api_url = "192.55.42.72:8090/generate"


headers = {"Content-Type": "application/json"}
max_new_tokens = 512

# Layout for model selection and max_tokens slider
col1, col2 = st.columns(2)

with col1:
    model_option = st.selectbox(
        "Choose a model:",
        options=list(models.keys()),
        format_func=lambda x: models[x]["name"],
        index=0  # Default
    )

# Detect model change and clear chat history if model has changed
#if st.session_state.selected_model != model_option:
#    st.session_state.messages = []
#    st.session_state.selected_model = model_option

max_tokens_range = models[model_option]["tokens"]

with col2:
    # Adjust max_tokens slider dynamically based on the selected model
    max_tokens = st.slider(
        "Max Tokens:",
        min_value=512,  # Minimum value to allow some flexibility
        max_value=max_tokens_range,
        # Default value or max allowed if less
        value=min(32768, max_tokens_range),
        step=512,
        help=f"Adjust the maximum number of tokens (words) for the model's response. Max for selected model: {max_tokens_range}"
    )

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    avatar = '🤖' if message["role"] == "assistant" else '👨‍💻'
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Skriv din prompt här..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user", avatar='👨‍💻'):
        st.markdown(prompt)

    # Fetch response 
    try:
        # Prepare the entire chat history for the request
        data = {
            "inputs": prompt,
            "messages": st.session_state.messages,  # Send the full chat history
            "parameters": {"max_new_tokens": max_new_tokens},
        }

        response = requests.post(api_url, headers=headers, json=data, timeout=30)

        # Process the response
        if response.status_code == 200:
            response_data = response.json()
            if isinstance(response_data, dict) and "generated_text" in response_data:
                assistant_response = response_data["generated_text"]
                with st.chat_message("assistant"):
                    st.markdown(assistant_response)
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            else:
                st.error("Error: Unexpected response format from the LLM server")
        else:
            st.error(f"Error: Request to LLM server failed with status code {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with the LLM server: {e}")

    except Exception as e:
        st.error(e, icon="🚨")
