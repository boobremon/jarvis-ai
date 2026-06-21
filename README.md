# J.A.R.V.I.S - AI Desktop Assistant

**Created and Designed by Sohail Karim**

A sophisticated Windows 11 desktop AI assistant inspired by the JARVIS system from Iron Man. Features real-time voice interaction, system monitoring, automation, and a cinematic futuristic HUD interface.

---

## Features

### Voice System
- **Wake Word Detection**: Say "Jarvis" or "Hey Jarvis" to activate
- **Speech Recognition**: Google Speech Recognition with real-time processing
- **Text-to-Speech**: Natural voice synthesis with JARVIS personality
- **Continuous Listening**: Optional always-listening mode for hands-free operation

### AI Capabilities
- **Conversational Memory**: Context-aware conversations with session persistence
- **Command Understanding**: Natural language command parsing
- **Multi-turn Conversations**: Maintains context across messages

### System Monitoring
- **CPU**: Real-time usage percentage and frequency
- **RAM**: Memory usage with available/used metrics
- **GPU** (NVIDIA): GPU utilization, memory, and temperature
- **Network**: Upload/download speeds
- **Disk**: Storage usage and activity
- **Battery**: Level and charging status

### Automation
- **Application Launcher**: Open Chrome, Edge, VS Code, Steam, Discord, Spotify, and more
- **System Commands**: Shutdown, restart, sleep, lock
- **Web Navigation**: Search Google, YouTube, open websites
- **Volume Control**: Set, mute, unmute system volume

### User Interface
- **Cinematic HUD**: Iron Man-inspired futuristic design
- **AI Core Animation**: Circular reactor with state indicators
- **Live Transcript**: Color-coded conversation history
- **System Stats Panel**: Real-time metrics display
- **Quick Actions**: One-click command shortcuts
- **Dark Theme**: Cyan/Blue/White color scheme

---

## Installation

### Prerequisites
- Python 3.10 or higher
- Windows 11 (primary target)
- NVIDIA GPU (optional, for GPU monitoring)
- Microphone (for voice input)

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/boobremon/jarvis-ai.git
   cd jarvis-ai
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run JARVIS**:
   ```bash
   python run_jarvis.py
   ```

---

## Configuration

JARVIS stores configuration in:
```
~/.jarvis/config.json
```

### Voice Settings
- `wake_word`: Wake word to activate (default: "jarvis")
- `voice_rate`: Speech speed (default: 180)
- `voice_volume`: Volume level 0.0-1.0 (default: 1.0)
- `voice_id`: 0 for male, 1 for female voice

### UI Settings
- `primary_color`: Main accent color (default: "#00D4FF")
- `animation_enabled`: Enable/disable animations
- `show_system_stats`: Show/hide stats panel

### AI Settings
- `model`: AI model for conversations
- `context_window`: Number of messages to remember
- `memory_enabled`: Persist conversation history

---

## Usage

### Voice Commands

**Wake Word Detection**:
- "Jarvis, open Chrome"
- "Hey Jarvis, what time is it?"
- "Jarvis, search Google for Python tutorials"

**Information Commands**:
- "What time is it?"
- "What's the date today?"
- "What's the weather?"
- "Tell me the system status"

**Application Control**:
- "Open Chrome"
- "Open YouTube"
- "Open Spotify"
- "Open VS Code"
- "Run Steam"

**Web Search**:
- "Search Google for Python tutorials"
- "Search YouTube for coding videos"
- "Open ChatGPT"

**System Commands**:
- "Shutdown the computer"
- "Restart PC"
- "Lock screen"
- "Set volume to 50 percent"
- "Mute"

**Assistance**:
- "Tell me a joke"
- "Remember that I need to call mom"
- "What do you remember?"

### Keyboard Shortcuts
- **Enter** in command input: Submit text command
- **Quick Action Buttons**: One-click commands

---

## Project Structure

```
jarvis-ai/
├── jarvis_app/
│   ├── __init__.py
│   ├── assistant.py           # Main controller
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   └── logger.py          # Logging system
│   ├── voice/
│   │   ├── recognition.py     # Speech recognition
│   │   └── synthesis.py       # Text-to-speech
│   ├── memory/
│   │   └── conversation.py    # Conversation memory
│   ├── ai/
│   │   └── engine.py          # AI command processing
│   ├── automation/
│   │   └── apps.py            # Application automation
│   ├── system_monitor/
│   │   └── monitor.py         # System statistics
│   └── ui/
│       ├── main_window.py     # Main HUD window
│       ├── startup_screen.py  # Boot animation
│       ├── styles.py          # Theme and stylesheets
│       └── widgets/
│           ├── ai_core.py
│           ├── transcript_panel.py
│           ├── stats_panel.py
│           ├── action_bar.py
│           ├── status_bar.py
│           └── settings_panel.py
├── run_jarvis.py              # Entry point
├── requirements.txt
└── README.md
```

---

## Customization

### Adding New Commands

1. **Add command type** in `ai/engine.py`:
```python
class CommandType(Enum):
    YOUR_COMMAND = "your_command"
```

2. **Add pattern** in `CommandParser`:
```python
CommandType.YOUR_COMMAND: [
    r"^your pattern here (.+)$",
]
```

3. **Register handler** in `assistant.py`:
```python
def handle_your_command(parsed):
    # Your logic here
    return "Response message", True, {}
self.ai_engine.register_handler(CommandType.YOUR_COMMAND, handle_your_command)
```

### Adding New Applications

Edit `automation/apps.py` and add to `_app_registry`:
```python
"your_app": [
    "C:\\Path\\To\\YourApp.exe",
]
```

### Customizing Theme

Edit values in `ui/styles.py`:
```python
class JarvisTheme:
    PRIMARY = "#00D4FF"  # Change primary color
    # ...
```

---

## Troubleshooting

### Voice Recognition Not Working
1. Ensure microphone is connected and selected as default
2. Check internet connection (Google Speech Recognition requires it)
3. Try recalibrating: The system calibrates automatically

### NVIDIA GPU Not Detected
1. Ensure NVIDIA drivers are installed
2. Verify `nvidia-smi` command works in terminal
3. GPU monitoring requires NVIDIA GPU with latest drivers

### Application Not Opening
1. Check if the application is installed
2. Verify path in `config.json` or let auto-detect
3. Check logs in `~/.jarvis/logs/`

---

## Requirements Details

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt6 | >=6.4.0 | GUI Framework |
| SpeechRecognition | >=3.10.0 | Voice Recognition |
| pyttsx3 | >=2.90 | Text-to-Speech |
| psutil | >=5.9.0 | System Monitoring |
| requests | >=2.28.0 | HTTP Requests |
| pyjokes | >=0.6.0 | Joke Generation |

---

## License

This project is open source. See LICENSE file for details.

---

## Credits

**Created and Designed by: Sohail Karim**

Inspired by J.A.R.V.I.S from Iron Man films.

---

## Changelog

### v2.0.0
- Complete rewrite with modular architecture
- PyQt6-based futuristic HUD interface
- Real-time system monitoring
- Wake word detection
- Conversation memory
- Application automation
- Cinematic boot sequence

---

**J.A.R.V.I.S - Just A Rather Very Intelligent System**
