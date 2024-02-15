from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
#from pprint import pprint


app = Flask(__name__)

@app.route('/api/transcript', methods=['POST'])
def get_transcript():
    data = request.json
    video_url = data.get('video_url')
    #video_url = 'https://www.youtube.com/watch?v=86Gy035z_KA'
    language = data.get('language', 'en')  # Default to English if not specified

    # Extract video ID from the URL
    video_id = video_url.split("v=")[1].split("&")[0]

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript([language]).fetch()
        return jsonify({'status': 'success', 'transcript': transcript})
    except (TranscriptsDisabled, NoTranscriptFound):
        return jsonify({'status': 'error', 'message': 'Transcript not available for this video.'}), 404
    
    #try:
    #    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    #    transcript = transcript_list.find_transcript([language]).fetch()
    #    pprint(transcript)  # Use pprint here to print the transcript data
    #    return jsonify({'status': 'success', 'transcript': transcript})
    #except (TranscriptsDisabled, NoTranscriptFound):
    #    return jsonify({'status': 'error', 'message': 'Transcript not available for this video.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
