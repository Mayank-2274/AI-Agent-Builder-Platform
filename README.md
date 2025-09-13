# AI Chat Assistant Chrome Extension

A Chrome extension that provides an AI-powered chatbot interface to help you analyze and discuss webpage content using the Airia API.

## 🚀 Features

- **Current Tab Integration**: Automatically detects the current webpage and provides context to the AI
- **Real-time Chat**: Interactive chatbot interface with conversation history
- **Dark/Light Theme**: Automatic theme detection with manual toggle
- **Clean UI**: Modern, responsive design that adapts to your preferences
- **Error Handling**: Robust error handling with user-friendly messages
- **Conversation Management**: Clear chat functionality and persistent conversations

## 📁 Project Structure

```
├── extension/
│   ├── manifest.json       # Extension configuration
│   ├── popup.html         # Extension popup interface
│   ├── popup.css          # Styles for the popup
│   ├── popup.js           # Popup functionality and API communication
│   └── content.js         # Optional content script for page analysis
├── server.py              # Flask server for API communication
├── chat.py                # Standalone CLI chat interface
└── README.md              # This file
```

## 🛠️ Setup Instructions

### 1. Install Dependencies

First, install the required Python packages:

```bash
pip install flask flask-cors requests
```

### 2. Start the Local Server

Run the Flask server that handles communication with the Airia API:

```bash
python server.py
```

The server will start on `http://localhost:5000`

### 3. Load the Chrome Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" in the top right
3. Click "Load unpacked" and select the `extension` folder
4. The extension should now appear in your extensions list

### 4. Add Extension Icons (Optional)

Create or add these icon files to the `extension` folder:
- `icon16.png` (16x16 pixels)
- `icon48.png` (48x48 pixels)  
- `icon128.png` (128x128 pixels)

## 🎯 Usage

### Chrome Extension

1. **Navigate to any webpage** you want to analyze
2. **Click the extension icon** in your Chrome toolbar
3. **Start chatting!** The AI will have context about the current page
4. **Ask questions** like:
   - "What is this page about?"
   - "Summarize the main points"
   - "What are the key features mentioned?"
   - "Explain this topic in simple terms"

### Command Line Interface

You can also use the standalone CLI:

```bash
# Interactive mode
python chat.py

# Single question
python chat.py "What is artificial intelligence?"

# Question about a specific webpage
python chat.py https://example.com "What is this website about?"
```

### CLI Commands

- `help` - Show available commands
- `url <webpage_url>` - Set context for a specific webpage
- `clear` - Clear conversation history
- `exit` or `quit` - End the chat session

## 🔧 Configuration

### API Configuration

The Airia API configuration is set in both `server.py` and `chat.py`:

```python
AIRIA_URL = 'https://prodaus.api.airia.ai/v2/PipelineExecution/eacc757c-c433-414f-90b2-e40d7710e530'
AIRIA_HEADERS = {
    'Content-Type': 'application/json',
    'X-API-KEY': 'your-api-key-here'
}
```

### Extension Permissions

The extension requires these permissions:
- `activeTab` - Access current tab information
- `scripting` - Execute scripts for content analysis
- `storage` - Store user preferences (theme)

## 🎨 Customization

### Themes

The extension supports both light and dark themes:
- Automatically detects system preference
- Manual toggle via the theme button
- Persistent theme preference storage

### Styling

Modify `popup.css` to customize the appearance:
- Colors are defined using CSS custom properties
- Responsive design that works in the popup context
- Smooth animations and transitions

## 🛡️ Error Handling

The extension includes comprehensive error handling:

- **Network errors**: Connection issues with the server
- **API errors**: Problems with the Airia API
- **Permission errors**: Tab access issues
- **Timeout errors**: Long-running requests

## 🔍 Troubleshooting

### Common Issues

1. **"Extension permissions may be needed"**
   - Ensure the extension has access to the current tab
   - Try refreshing the page and reopening the extension

2. **"Make sure the server is running on localhost:5000"**
   - Start the Flask server: `python server.py`
   - Check that port 5000 is not blocked

3. **Empty or error responses from AI**
   - Verify your Airia API key is correct
   - Check server logs for detailed error messages
   - Ensure the API endpoint is accessible

### Debug Mode

To enable debug logging in the server:

```bash
# The server runs in debug mode by default
python server.py
```

Check the browser console (F12) for client-side debugging information.

## 📈 API Endpoints

### Server Endpoints

- `POST /api/chat` - Send chat message with page context
- `GET /api/health` - Health check endpoint

### Request Format

```json
{
  "userInput": "User's message",
  "conversationHistory": [
    {"role": "user", "content": "Previous message"},
    {"role": "assistant", "content": "Previous response"}
  ],
  "tabInfo": {
    "url": "https://example.com",
    "title": "Page Title",
    "id": 123
  }
}
```

## 🚀 Advanced Features

### Content Script (Optional)

The `content.js` script can extract detailed page content:
- Page headings and structure
- Meta descriptions
- Main text content
- Clean content extraction

To enable, add to `manifest.json`:

```json
"content_scripts": [{
  "matches": ["<all_urls>"],
  "js": ["content.js"]
}]
```

### Page Context Enhancement

The extension automatically provides page context to the AI:
- Current URL and page title
- Enhanced first message with page information
- Conversation history with page context

## 📄 License

This project is open source. Feel free to modify and distribute according to your needs.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Author**: github.com/RiturajSingh2004

For questions or issues, please create an issue in the repository.