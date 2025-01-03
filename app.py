import google.generativeai as genai
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, request, render_template, flash
import markdown
import re
import os

# Load environment variables and validate API key
load_dotenv()
if not os.getenv("GEMINI_API_KEY"):
    raise EnvironmentError("API key is missing or invalid")
else:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Setup system instruction prompt
SYSTEM_PROMPT = """I have a transcript from a YouTube video,
                and I need a detailed summary. Your task is to extract and present all the essential information, including:
                The main arguments or key points discussed in the video.
                Any evidence, examples, or data used to support those arguments.
                If the transcript mentions any specific data, statistics, or numbers, please include them in the summary.
                Other notable highlights or insights mentioned.
                Please present the information clearly, using bullet points where necessary for better organization.
                Ensure nothing important is left out, but avoid excessive repetition or irrelevant details.
                If the transcript is in Vietnamese, no need to translate it into English, just summerize it in Vietnamese.
                If in other languages, please provide a translation into English before summarizing.
                However, if the transcript mentions any kind of promotional content, please ignore it and focus on the main content of the video."""
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM_PROMPT)

# Initialize Flask app & secret key for flash messages
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Summary route
@app.route("/summary", methods=["POST"])
def summary():
    # Get video link, extract video ID, get the transcript, summary by Gemini API and return in markdown format
    try:
        video_link = request.form.get("link")
        if not video_link:
            flash("Please provide a valid YouTube video link", "error")
            return render_template("index.html")
        video_id = get_video_id(video_link)
        prompt = get_transcript(video_id)
        response = model.generate_content(prompt)
        if not response.text:
            flash("No summary generated for the video", "error")
            return render_template("index.html")
        summary = markdown.markdown(response.text)
        return render_template("summary.html", summary=summary, video_id=video_id)
    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return render_template("index.html")


# Get YouTube video ID from link
def get_video_id(video_link):
    if not video_link:
        raise ValueError("No video link provided")
    else:
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
                    
            raise ValueError("Invalid YouTube video link")
        except Exception as e:
            raise ValueError(f"Error: {str(e)}")


# Get YouTube transcript from video ID
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en", "ja", "vi"])
        if not transcript:
            raise ValueError("No transcript found for the video")
        # Extract and combine all text entries in the transcript dictionary
        full_text = " ".join([entry.get("text") for entry in transcript])
        return full_text
    except Exception as e:
        raise ValueError(f"Error: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)
