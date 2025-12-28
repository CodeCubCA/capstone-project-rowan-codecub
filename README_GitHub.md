# AI MultiModal Assistant 🤖

A comprehensive AI-powered assistant that combines text chat, voice interaction, and image generation capabilities in a single, beautiful Streamlit interface.

## ✨ Features

### 💬 Text Chat Mode
- Real-time AI conversations
- Full conversation history
- Context-aware responses
- Powered by Meta Llama 3.2 3B Instruct

### 🎤 Voice Mode
- Speech-to-text input using Google Speech Recognition
- Text-to-speech output using gTTS
- Voice conversation history
- Hands-free interaction

### 🎨 Image Generator
- Text-to-image generation using FLUX.1-schnell
- 10 artistic style presets:
  - Realistic (photorealistic, 8K)
  - Anime (manga style)
  - Digital Art (concept art)
  - Watercolor
  - Oil Painting
  - Cyberpunk
  - Fantasy
  - Minimalist
  - 3D Render
  - Sketch
- Download generated images
- Example prompts for inspiration

## 🛠️ Technologies Used

- **Python 3.8+**
- **Streamlit** - Web framework for the UI
- **HuggingFace Inference API** - AI model inference
- **FLUX.1-schnell** - Image generation model
- **Meta Llama 3.2 3B** - Text generation model
- **gTTS** - Text-to-speech
- **SpeechRecognition** - Speech-to-text
- **audio-recorder-streamlit** - Voice recording
- **Pillow (PIL)** - Image processing
- **python-dotenv** - Environment variable management

## 📦 Installation

1. **Clone the repository:**
```bash
git clone https://github.com/CodeCubCA/capstone-project-rowan-codecub.git
cd capstone-project-rowan-codecub
```

2. **Install required dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up your HuggingFace API token:**
   - Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
   - Create a new token with **Write** permissions
   - Create a `.env` file in the project root:
   ```
   HUGGINGFACE_TOKEN=your_token_here
   ```

## 🚀 How to Run Locally

1. **Start the Streamlit app:**
```bash
streamlit run app.py
```

2. **Open your browser and navigate to:**
```
http://localhost:8501
```

3. **Choose your mode:**
   - **Text Chat** - Type your questions and get instant AI responses
   - **Voice Mode** - Speak your questions and hear AI responses
   - **Image Generator** - Describe an image and watch AI create it

## 📖 Usage

### Text Chat Mode
1. Navigate to the "💬 Text Chat" tab
2. Type your message in the input box
3. Click "Send" or press Enter
4. View AI response in the chat history
5. Continue the conversation!

### Voice Mode
1. Navigate to the "🎤 Voice Mode" tab
2. Click the microphone button to start recording
3. Speak your question clearly
4. Click again to stop recording
5. Listen to the AI's voice response
6. View conversation history below

### Image Generator
1. Navigate to the "🎨 Image Generator" tab
2. Enter a detailed description of your desired image
3. Optionally choose a style preset
4. Click "🎨 Generate Image"
5. Wait 10-30 seconds for generation
6. Download your created image

## 🎯 Example Prompts

### Text Chat
- "Explain quantum physics in simple terms"
- "Write a short story about a robot"
- "Help me with my Python homework"

### Voice
- Speak naturally as you would to a person
- Ask questions, request explanations
- Have a conversation

### Image Generation
- "A serene mountain landscape at sunset"
- "A magical forest with glowing mushrooms"
- "A futuristic city with flying cars"
- "A cyberpunk street with neon signs"
- "A steampunk airship in the clouds"

## 🏗️ Project Structure

```
capstone-project-rowan-codecub/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following:

```env
HUGGINGFACE_TOKEN=your_huggingface_token_here
```

### Models Used

- **Text Generation:** `meta-llama/Llama-3.2-3B-Instruct`
- **Image Generation:** `black-forest-labs/FLUX.1-schnell`

## 🌐 Deployment

### Deploy to HuggingFace Spaces

1. Create a new Space on [HuggingFace Spaces](https://huggingface.co/spaces)
2. Choose "Streamlit" as the SDK
3. Upload your files or connect your GitHub repository
4. Add your `HUGGINGFACE_TOKEN` as a secret in Space settings
5. Your app will be live at: `https://huggingface.co/spaces/your-username/your-space-name`

## 🎓 Capstone Project

This project was created as a capstone assignment for the AI with Python course at CodeCub. It demonstrates:

- Multi-modal AI integration (text, voice, image)
- Clean, professional UI/UX design
- API integration with HuggingFace
- Speech recognition and synthesis
- Image generation with AI
- Session state management
- Error handling and user feedback

## 📝 License

MIT License - feel free to use this project for learning and development!

## 👨‍💻 Author

**Rowan** - Student at CodeCub
AI with Python Course - Capstone Project

## 🙏 Credits

- Powered by [HuggingFace](https://huggingface.co/) 🤗
- Built with [Streamlit](https://streamlit.io/)
- FLUX.1-schnell model by Black Forest Labs
- Meta Llama 3.2 by Meta AI

---

**Made with ❤️ by Rowan | December 2024**
