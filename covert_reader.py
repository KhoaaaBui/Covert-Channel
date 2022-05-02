from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import make_chunks
import math

def msg_from_song(chunks):
    msg = []
    # normalize volume for all audio chunks to the max chunk's volume.
    ref_vol = chunks[0].dBFS
    print("reference volume", ref_vol)
    for chunk in chunks[1:]:
        change_in_dBFS = ref_vol - chunk.dBFS
        print("Change in dBFS", round(change_in_dBFS))
        msg.append(round(change_in_dBFS))
    return msg

def main():
    # Import audio file
    sound = AudioSegment.from_file(file = "song.mp3", format="mp3")
    print("Found sound")
    # Split audio file into chunks of 5 seconds.
    chunk_length = 50000 # in ms
    chunks = make_chunks(sound, chunk_length)
    msg = msg_from_song(chunks)
    print(msg)

if __name__ == "__main__":
    main()

