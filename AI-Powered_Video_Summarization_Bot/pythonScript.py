import moviepy.editor as mp
import speech_recognition as sr
import io
from pydub import AudioSegment

def convertVideoToText(video_path="sampleVideo.mp4"):
    # Load the video
    video = mp.VideoFileClip(video_path)
    
    # Extract audio from the video
    audio = video.audio
    audio.write_audiofile("temp_audio.wav")
    
    # Load the audio file
    audio_segment = AudioSegment.from_wav("temp_audio.wav")
    
    # Split the audio into 30-second chunks
    chunk_length_ms = 30000  # 30 seconds
    chunks = [audio_segment[i:i+chunk_length_ms] for i in range(0, len(audio_segment), chunk_length_ms)]
    
    # Initialize recognizer
    r = sr.Recognizer()
    
    full_text = ""
    
    # Process each chunk
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i+1}/{len(chunks)}...")
        
        # Export the chunk to a buffer
        audio_buffer = io.BytesIO()
        chunk.export(audio_buffer, format="wav")
        audio_buffer.seek(0)
        
        # Perform speech recognition on the chunk
        with sr.AudioFile(audio_buffer) as source:
            audio_data = r.record(source)
            try:
                text = r.recognize_google(audio_data)
                full_text += text + " "
            except sr.UnknownValueError:
                full_text += "[Unable to understand audio chunk] "
            except sr.RequestError as e:
                full_text += f"[Error processing chunk: {e}] "
    
    return full_text

# Call the function and store the result
resultant_text = convertVideoToText()

# Print or save the result
print("\nThe resultant text from the video is: \n")
print(resultant_text)

# Optionally, save the result to a file
with open("outputText.txt", "w") as f:
    f.write(resultant_text)
