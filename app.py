import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, request, render_template
import markdown
import re
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Setup system instruction prompt
SYSTEM_PROMPT = """I have a transcript from a YouTube video,
                and I need a detailed summary. Your task is to extract and present all the essential information, including:
                The main arguments or key points discussed in the video.
                Any evidence, examples, or data used to support those arguments.
                Other notable highlights or insights mentioned.
                Please present the information clearly, using bullet points where necessary for better organization.
                Ensure nothing important is left out, but avoid excessive repetition or irrelevant details.
                If the transcript is in Vietnamese, no need to translate it to English.
                If the transcript is in English, no need to translate, just summarize the content.
                In other cases, please provide a translation into English before summarizing."""
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)

# Initialize Flask app
app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Summary route
@app.route("/summary", methods=["POST"])
def summary():
    # Get video link, extract video ID, get the transcript, summary by Gemini API and return in markdown format
    video_link = request.form.get("link")
    video_id = get_video_id(video_link)
    prompt = get_transcript(video_id)
    response = model.generate_content(prompt)
    summary = markdown.markdown(response.text)
    return render_template("summary.html", summary=summary)


# Get YouTube video ID from link
def get_video_id(video_link):
    try:
        # Handle direct video ID input
        if len(video_link) == 11:
            return video_link
            
        # Extract video ID using regex patterns
        patterns = [
            r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',  # For youtube.com/watch?v=
            r'(?:youtu\.be\/)([0-9A-Za-z_-]{11}).*'  # For youtu.be/
        ]
        
        for pattern in patterns:
            match = re.search(pattern, video_link)
            if match:
                return match.group(1)
                
        return "Error: Invalid YouTube URL format"
    except Exception as e:
        return f"Error: {str(e)}"


# Get YouTube transcript from pytube
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "ja", "vi"])
        if not transcript:
            return "No captions available for this video"
        # Extract and combine all text entries in the transcript dictionary
        full_text = " ".join([entry.get("text") for entry in transcript])
        return full_text
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)