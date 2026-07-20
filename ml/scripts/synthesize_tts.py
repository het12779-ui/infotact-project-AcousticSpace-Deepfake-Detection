import pyttsx3
import os

def synthesize_tts_samples(output_dir="../data/tts_samples"):
    os.makedirs(output_dir, exist_ok=True)
    engine = pyttsx3.init()
    phrases = [
        "The weather today is sunny with a slight breeze.",
        "Please confirm your account details before proceeding.",
        "This is a test of the emergency broadcast system.",
        "Thank you for calling customer support.",
        "The meeting has been rescheduled to next Tuesday.",
    ]
    
    for i, phrase in enumerate(phrases):
        path = f"{output_dir}/tts_{i:02d}.wav"
        engine.save_to_file(phrase, path)
    engine.runAndWait()
    print(f"Synthesized {len(phrases)} TTS clips into {output_dir}/")

if __name__ == "__main__":
    synthesize_tts_samples()
