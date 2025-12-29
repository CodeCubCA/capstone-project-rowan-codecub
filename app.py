import streamlit as st
from huggingface_hub import InferenceClient
from PIL import Image
import os
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

# Configuration
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
TEXT_MODEL = "meta-llama/Llama-3.2-3B-Instruct"
IMAGE_MODEL = "black-forest-labs/FLUX.1-schnell"

# Page configuration
st.set_page_config(
    page_title="AI MultiModal Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for space theme interface
st.markdown("""
    <style>
    /* Import space font */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;900&display=swap');

    /* Force dark background on entire page */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background: linear-gradient(to bottom, #0a0e27 0%, #1a1a2e 50%, #16213e 100%) !important;
    }

    .stApp {
        background: linear-gradient(to bottom, #0a0e27 0%, #1a1a2e 50%, #16213e 100%) !important;
    }

    /* Override any white backgrounds */
    section[data-testid="stSidebar"],
    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Animated starfield background */
    .main {
        padding: 1rem 2rem;
        background: linear-gradient(to bottom, #0a0e27 0%, #1a1a2e 50%, #16213e 100%) !important;
        position: relative;
        min-height: 100vh;
    }

    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image:
            radial-gradient(2px 2px at 20% 30%, white, transparent),
            radial-gradient(2px 2px at 60% 70%, white, transparent),
            radial-gradient(1px 1px at 50% 50%, white, transparent),
            radial-gradient(1px 1px at 80% 10%, white, transparent),
            radial-gradient(2px 2px at 90% 60%, white, transparent),
            radial-gradient(1px 1px at 33% 80%, white, transparent),
            radial-gradient(2px 2px at 10% 90%, white, transparent),
            radial-gradient(1px 1px at 70% 20%, white, transparent);
        background-size: 200% 200%;
        animation: twinkle 8s ease-in-out infinite;
        opacity: 0.6;
        z-index: 0;
        pointer-events: none;
    }

    @keyframes twinkle {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 0.8; }
    }

    /* Header styling with cosmic theme */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.5), 0 0 30px rgba(240, 147, 251, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
    }

    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }

    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    .header-title {
        color: white;
        font-size: 3rem;
        font-weight: 900;
        margin: 0;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 10px rgba(255,255,255,0.5), 0 0 20px rgba(102, 126, 234, 0.8);
        position: relative;
        z-index: 1;
        letter-spacing: 3px;
    }

    .header-subtitle {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.2rem;
        margin-top: 0.5rem;
        font-family: 'Orbitron', sans-serif;
        position: relative;
        z-index: 1;
        text-shadow: 0 0 5px rgba(255,255,255,0.3);
    }

    /* Tab styling with neon effect */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background: rgba(26, 26, 46, 0.8);
        border-radius: 15px;
        padding: 0.8rem;
        border: 2px solid rgba(102, 126, 234, 0.3);
        backdrop-filter: blur(10px);
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 0.8rem 1.5rem;
        font-weight: 700;
        font-size: 1rem;
        font-family: 'Orbitron', sans-serif;
        background: rgba(22, 33, 62, 0.6);
        color: rgba(255, 255, 255, 0.7);
        border: 2px solid rgba(102, 126, 234, 0.2);
        transition: all 0.3s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        border-color: rgba(102, 126, 234, 0.6);
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.4);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.8), 0 5px 15px rgba(102, 126, 234, 0.4);
    }

    /* Chat message styling with glow */
    .chat-message {
        padding: 1.2rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(102, 126, 234, 0.2);
        backdrop-filter: blur(5px);
    }

    .user-message {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        color: white;
        margin-left: 20%;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5), 0 5px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .assistant-message {
        background: rgba(22, 33, 62, 0.9);
        color: #e0e0e0;
        margin-right: 20%;
        box-shadow: 0 0 15px rgba(118, 75, 162, 0.3), 0 5px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(102, 126, 234, 0.3);
    }

    /* Button styling with neon glow */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        font-family: 'Orbitron', sans-serif;
        border-radius: 10px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        padding: 0.7rem 1.5rem;
        font-size: 1rem;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 0 30px rgba(102, 126, 234, 0.8), 0 5px 20px rgba(102, 126, 234, 0.6);
        transform: translateY(-2px);
    }

    /* Input fields with glow */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background: rgba(22, 33, 62, 0.8) !important;
        color: white !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 10px !important;
        font-family: 'Orbitron', sans-serif !important;
    }

    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: rgba(102, 126, 234, 0.8) !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.4) !important;
    }

    /* Chat input styling */
    .stChatInput>div>div>textarea,
    .stChatInputContainer>div>div>textarea {
        background: rgba(22, 33, 62, 0.9) !important;
        color: white !important;
        border: 2px solid rgba(102, 126, 234, 0.4) !important;
        border-radius: 12px !important;
        font-family: 'Orbitron', sans-serif !important;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.3);
    }

    .stChatInput>div>div>textarea:focus,
    .stChatInputContainer>div>div>textarea:focus {
        border-color: rgba(102, 126, 234, 0.9) !important;
        box-shadow: 0 0 25px rgba(102, 126, 234, 0.5) !important;
    }

    /* Chat input send button */
    .stChatInput button,
    .stChatInputContainer button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        transition: all 0.3s ease;
    }

    .stChatInput button:hover,
    .stChatInputContainer button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.6) !important;
    }

    /* Selectbox styling */
    .stSelectbox>div>div {
        background: rgba(22, 33, 62, 0.8) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 10px !important;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Info box with cosmic glow */
    .info-box {
        background: rgba(102, 126, 234, 0.15);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
        color: #e0e0e0;
        box-shadow: 0 0 15px rgba(102, 126, 234, 0.2);
        backdrop-filter: blur(10px);
    }

    .warning-box {
        background: rgba(22, 33, 62, 0.95) !important;
        padding: 1.5rem;
        border-radius: 12px;
        border: 3px solid #ffc107;
        margin-bottom: 1rem;
        color: #ffd54f !important;
        box-shadow: 0 0 20px rgba(255, 193, 7, 0.4);
        backdrop-filter: blur(10px);
    }

    .warning-box h3 {
        color: #ffc107 !important;
        margin-top: 0;
    }

    .warning-box a {
        color: #667eea !important;
        text-decoration: underline;
    }

    /* Headings with glow */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif !important;
        color: #e0e0e0 !important;
        text-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(22, 33, 62, 0.8) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
        font-family: 'Orbitron', sans-serif !important;
    }

    /* Success/Error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        background: rgba(22, 33, 62, 0.9) !important;
        border-radius: 10px !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }


    /* Style for st.info messages */
    .stAlert {
        background: rgba(22, 33, 62, 0.9) !important;
        border: 2px solid rgba(102, 126, 234, 0.3) !important;
        color: #e0e0e0 !important;
    }

    /* Audio recorder frame box */
    .audio-recorder-frame {
        background: rgba(22, 33, 62, 0.95) !important;
        border: 3px solid rgba(102, 126, 234, 0.6) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
        box-shadow: 0 0 25px rgba(102, 126, 234, 0.4), 0 5px 15px rgba(0,0,0,0.3) !important;
        margin: 1.5rem auto !important;
        max-width: 600px !important;
        text-align: center;
    }

    /* Voice instruction text */
    .voice-instruction {
        color: #e0e0e0;
        font-family: 'Orbitron', sans-serif;
        font-size: 1rem;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 0 0 5px rgba(102, 126, 234, 0.3);
    }

    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🚀 AI MULTIMODAL ASSISTANT 🌌</h1>
        <p class="header-subtitle">💬 Chat • 🎤 Speak • 🎨 Create Images | ✨ Powered by AI</p>
    </div>
""", unsafe_allow_html=True)

# Check API token
if not HUGGINGFACE_TOKEN:
    st.markdown("""
        <div class="warning-box">
            <h3>⚠️ Setup Required</h3>
            <p>Please configure your HuggingFace API token:</p>
            <ol>
                <li>Go to <a href="https://huggingface.co/settings/tokens" target="_blank">HuggingFace Settings</a></li>
                <li>Create a new token with <b>Write</b> permissions</li>
                <li>Add it to your <code>.env</code> file as: <code>HUGGINGFACE_TOKEN=your_token_here</code></li>
                <li>Restart the application</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# Initialize session states
if 'text_messages' not in st.session_state:
    st.session_state.text_messages = []
if 'voice_messages' not in st.session_state:
    st.session_state.voice_messages = []
if 'generated_image' not in st.session_state:
    st.session_state.generated_image = None
if 'image_prompt' not in st.session_state:
    st.session_state.image_prompt = ""

# Create tabs for different modes
tab1, tab2, tab3 = st.tabs(["💬 Text Chat", "🎤 Voice Mode", "🎨 Image Generator"])

# ==================== TEXT CHAT TAB ====================
with tab1:
    st.markdown("### 💬 Text Chat Mode")
    st.markdown('<div class="info-box">Have a conversation with AI. Ask questions, get help, or just chat!</div>', unsafe_allow_html=True)

    # Display chat history
    for message in st.session_state.text_messages:
        if message["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">👤 You: {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message">🤖 Assistant: {message["content"]}</div>', unsafe_allow_html=True)

    # Chat input using st.chat_input (auto-sends on Enter)
    user_input = st.chat_input("Ask me anything...", key="text_chat_input")

    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.text_messages = []
        st.rerun()

    # Handle message sending (triggers on Enter)
    if user_input and user_input.strip():
        # Add user message
        st.session_state.text_messages.append({"role": "user", "content": user_input})

        try:
            # Initialize HuggingFace client
            client = InferenceClient(token=HUGGINGFACE_TOKEN)

            # Prepare conversation history
            messages = []
            for msg in st.session_state.text_messages:
                messages.append({"role": msg["role"], "content": msg["content"]})

            # Get AI response
            with st.spinner("🤔 Thinking..."):
                response = client.chat_completion(
                    messages=messages,
                    model=TEXT_MODEL,
                    max_tokens=500,
                    stream=False
                )

                if hasattr(response, 'choices') and len(response.choices) > 0:
                    ai_response = response.choices[0].message.content
                else:
                    ai_response = "Sorry, I couldn't generate a response."

            # Add assistant message
            st.session_state.text_messages.append({"role": "assistant", "content": ai_response})
            st.rerun()

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.info("Please check your API token and try again.")

# ==================== VOICE MODE TAB ====================
with tab2:
    st.markdown("### 🎤 Voice Mode")
    st.markdown('<div class="info-box">Speak your questions and hear AI responses!</div>', unsafe_allow_html=True)

    # Voice input section
    st.markdown("#### 🎙️ Voice Input")
    st.markdown('<p class="voice-instruction">✨ Click the microphone button below to start recording your voice ✨</p>', unsafe_allow_html=True)

    try:
        from audio_recorder_streamlit import audio_recorder
        import speech_recognition as sr
        from gtts import gTTS
        import tempfile

        # Audio recorder in styled frame
        st.markdown('<div class="audio-recorder-frame">', unsafe_allow_html=True)
        audio_bytes = audio_recorder(
            text="",
            recording_color="#667eea",
            neutral_color="#764ba2",
            icon_size="3x"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        if audio_bytes:
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio_bytes)
                audio_file_path = f.name

            try:
                # Speech recognition
                recognizer = sr.Recognizer()
                with sr.AudioFile(audio_file_path) as source:
                    audio_data = recognizer.record(source)
                    voice_text = recognizer.recognize_google(audio_data)

                st.success(f"You said: {voice_text}")

                # Add to conversation
                st.session_state.voice_messages.append({"role": "user", "content": voice_text})

                # Get AI response
                client = InferenceClient(token=HUGGINGFACE_TOKEN)
                messages = []
                for msg in st.session_state.voice_messages:
                    messages.append({"role": msg["role"], "content": msg["content"]})

                with st.spinner("🤔 Thinking..."):
                    response = client.chat_completion(
                        messages=messages,
                        model=TEXT_MODEL,
                        max_tokens=300,
                        stream=False
                    )

                    if hasattr(response, 'choices') and len(response.choices) > 0:
                        ai_response = response.choices[0].message.content
                    else:
                        ai_response = "Sorry, I couldn't generate a response."

                st.session_state.voice_messages.append({"role": "assistant", "content": ai_response})

                # Text-to-speech
                tts = gTTS(text=ai_response, lang='en', slow=False)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                    tts.save(fp.name)
                    audio_response_path = fp.name

                st.audio(audio_response_path)
                st.markdown(f"**🤖 AI Response:** {ai_response}")

                # Clean up temp files
                os.unlink(audio_file_path)

            except sr.UnknownValueError:
                st.error("Could not understand audio. Please try again.")
            except sr.RequestError as e:
                st.error(f"Could not request results; {e}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    except ImportError:
        st.warning("Voice features require audio-recorder-streamlit package. Install it to enable voice mode.")

    # Display voice conversation history
    st.markdown("---")
    st.markdown("#### 📝 Voice Conversation History")

    if st.session_state.voice_messages:
        for message in st.session_state.voice_messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">👤 You: {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message">🤖 Assistant: {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.info("No voice conversation yet. Click the microphone button above to start!")

    if st.button("🗑️ Clear Voice History"):
        st.session_state.voice_messages = []
        st.rerun()

# ==================== IMAGE GENERATOR TAB ====================
with tab3:
    st.markdown("### 🎨 Image Generator")
    st.markdown('<div class="info-box">Create stunning AI-generated images from text descriptions!</div>', unsafe_allow_html=True)

    # Image generation controls
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("#### 💭 Describe Your Image")

        # Example prompts
        with st.expander("✨ Need inspiration? Click for examples"):
            st.markdown("""
            - A serene mountain landscape at sunset
            - A magical forest with glowing mushrooms
            - A futuristic city with flying cars
            - A steampunk airship in the clouds
            - A cute robot playing with a kitten
            - A cyberpunk street with neon signs
            - An underwater palace with mermaids
            """)

        # Prompt input
        image_prompt = st.text_area(
            "Enter your image description:",
            height=100,
            placeholder="E.g., A beautiful sunset over a calm ocean with dolphins jumping...",
            value=st.session_state.image_prompt
        )

    with col2:
        st.markdown("#### 🎨 Style Preset")

        # Style options
        style_options = {
            "None": "",
            "Realistic": "photorealistic, highly detailed, 8k, professional photography",
            "Anime": "anime style, manga, vibrant colors, detailed",
            "Digital Art": "digital art, concept art, artstation trending",
            "Watercolor": "watercolor painting, soft colors, artistic",
            "Oil Painting": "oil painting, classical art style, textured brush strokes",
            "Cyberpunk": "cyberpunk style, neon lights, futuristic, dystopian",
            "Fantasy": "fantasy art, magical, epic, detailed illustration",
            "Minimalist": "minimalist art, simple, clean lines, modern",
            "3D Render": "3D render, octane render, high quality, detailed",
            "Sketch": "pencil sketch, hand drawn, artistic, detailed linework"
        }

        selected_style = st.selectbox(
            "Choose a style:",
            options=list(style_options.keys()),
            label_visibility="collapsed"
        )

    # Generate button
    if st.button("🎨 Generate Image", use_container_width=True):
        if not image_prompt.strip():
            st.warning("⚠️ Please enter an image description!")
        else:
            try:
                # Show loading state
                with st.spinner("🎨 Creating your masterpiece... This may take 10-30 seconds..."):
                    # Initialize HuggingFace client
                    client = InferenceClient(token=HUGGINGFACE_TOKEN)

                    # Combine prompt with style
                    style_suffix = style_options[selected_style]
                    full_prompt = f"{image_prompt}, {style_suffix}" if style_suffix else image_prompt

                    # Generate image
                    image = client.text_to_image(
                        prompt=full_prompt,
                        model=IMAGE_MODEL
                    )

                    # Store in session state
                    st.session_state.generated_image = image
                    st.session_state.image_prompt = image_prompt
                    st.session_state.image_style = selected_style

                st.success("✅ Image generated successfully!")

            except Exception as e:
                error_message = str(e)

                # Handle specific errors
                if "401" in error_message or "unauthorized" in error_message.lower():
                    st.error("🔑 Authentication Error: Invalid or missing API token.")
                    st.info("Please check that your HUGGINGFACE_TOKEN in .env file is correct and has Write permissions.")
                elif "rate limit" in error_message.lower() or "429" in error_message:
                    st.error("⏳ Rate Limit Exceeded: You've made too many requests.")
                    st.info("Free tier has limited requests. Please wait a few minutes and try again.")
                elif "model" in error_message.lower() or "not found" in error_message.lower():
                    st.error("🤖 Model Error: The AI model is unavailable.")
                    st.info("The model might be loading or temporarily unavailable. Try again in a moment.")
                else:
                    st.error(f"❌ Error generating image: {error_message}")
                    st.info("Please try again or try a different prompt.")

    # Display generated image
    if st.session_state.generated_image:
        st.markdown("---")
        st.markdown("### 🖼️ Generated Image")

        # Show prompt and style
        style_badge = f" • **Style:** {st.session_state.image_style}" if st.session_state.get('image_style', 'None') != "None" else ""
        st.markdown(f"*{st.session_state.image_prompt}*{style_badge}")

        # Display the image
        st.image(
            st.session_state.generated_image,
            use_column_width=True
        )

        # Download button
        img_bytes = io.BytesIO()
        st.session_state.generated_image.save(img_bytes, format='PNG')
        img_bytes.seek(0)

        st.download_button(
            label="⬇️ Download Image",
            data=img_bytes,
            file_name=f"ai_generated_{st.session_state.image_prompt[:30].replace(' ', '_')}.png",
            mime="image/png",
            use_container_width=True
        )

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #a0a0a0; font-size: 0.9rem; margin-top: 2rem; font-family: 'Orbitron', sans-serif;">
        <p style="text-shadow: 0 0 10px rgba(102, 126, 234, 0.5);">🌟 AI MultiModal Assistant | Capstone Project by Rowan 🌟</p>
        <p style="color: #667eea; text-shadow: 0 0 5px rgba(102, 126, 234, 0.3);">Powered by HuggingFace 🤗 | Built with Streamlit ⚡</p>
        <p style="color: #888; font-size: 0.75rem;">🪐 Exploring the cosmos of AI possibilities 🌠</p>
    </div>
""", unsafe_allow_html=True)
