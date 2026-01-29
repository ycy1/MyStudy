import asyncio
import edge_tts
import time
import markdown
from bs4 import BeautifulSoup

# edge-tts --list-voices
async def generate_speech(file_path="summary.md", output_file="output.mp3"):
    with open(file_path, "r", encoding="utf-8") as file:
        data = file.read()  

    data = markdown.markdown(data)
    soup = BeautifulSoup(data, 'html.parser')
    data = soup.get_text()  
    print("Text:", data)
    print("Generating speech...")
    start_time = time.time()
    tts = edge_tts.Communicate(text=data, voice="zh-CN-YunjianNeural")
    await tts.save(output_file)
    print("Speech generated successfully!")
    end_time = time.time()
    print(f"Time: {end_time - start_time:.2f} seconds") 


# from transformers import AutoProcessor, AutoModel
# import scipy

# processor = AutoProcessor.from_pretrained("suno/bark")
# model = AutoModel.from_pretrained("suno/bark")

# inputs = processor(data, voice_preset="v2/zh_speaker_6")
# audio_array = model.generate(**inputs)
# audio_array = audio_array.cpu().numpy().squeeze()

# scipy.io.wavfile.write("bark_output.wav", rate=24000, data=audio_array)

if __name__ == "__main__":
    asyncio.run(generate_speech())