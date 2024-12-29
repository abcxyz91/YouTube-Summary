# YouTube Video Summarizer

A Flask web application that generates concise summaries of YouTube videos using Google's Gemini AI. The app extracts video transcripts and creates intelligent summaries, making it easier to quickly understand video content without watching the entire video.

## Features

- Extract transcripts from YouTube videos using video URL or ID
- Support for multiple languages (English, Japanese, Vietnamese)
- AI-powered summarization using Google's Gemini-1.5-flash model
- Clean, responsive web interface
- Error handling and user feedback
- Markdown formatting for structured summaries

## Prerequisites

- Python 3.8+
- Google Cloud Platform account with Gemini API access
- YouTube Data API access

## Installation

1. Clone the repository:
```bash
git clone https://github.com/abcxyz91/07.-YouTube-Summary
cd 07.-YouTube-Summary
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your API keys:
```
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development  # Change to 'production' for production deployment
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Enter a YouTube video URL or video ID in the input field

4. Click "Summarize" to generate the video summary

## Project Structure

```
youtube-summarizer/
├── app.py              # Main Flask application
├── templates/
│   ├── index.html     # Home page template
│   └── summary.html   # Summary display template
├── .env               # Environment variables
├── requirements.txt   # Project dependencies
└── README.md         # Project documentation
```

## API Reference

The application uses the following external APIs:

- Google Gemini API for text generation
- YouTube Transcript API for caption extraction

## Error Handling

The application handles various error cases:
- Invalid YouTube URLs
- Missing video transcripts
- API failures
- Network issues

Each error is presented to the user with a clear message and appropriate feedback.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini API for providing the AI summarization capabilities
- YouTube Transcript API for caption extraction functionality
- Flask framework for the web application structure
- TailwindCSS for the user interface styling

## Support

For support, please open an issue in the repository.