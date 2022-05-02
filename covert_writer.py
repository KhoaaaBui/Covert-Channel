from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import make_chunks


def normalize_volume(chunks):
    # normalize volume for all audio chunks to the max chunk's volume.
    max_vol = max(chunk.dBFS for chunk in chunks)
    new_chunks = []
    print("Max vol chunk", max_vol)
    for chunk in chunks:
        change_in_dBFS = max_vol - chunk.dBFS
        chunk = chunk.apply_gain(change_in_dBFS)
        print("Change in dBFS", chunk.dBFS)
        new_chunks.append(chunk)
    return new_chunks

def set_volume(chunks, msg):
    # Keep the first chunk as a reference point.
    audio_msg = chunks[0]

    # reduce the volume by the number in the message (dB).
    for i in range(len(msg)):
        change_in_dBFS = -float(msg[i])
        print("Reduced by", change_in_dBFS)
        print("Before:", chunks[i+1].dBFS)
        chunks[i+1] = chunks[i+1].apply_gain(change_in_dBFS) 
        print("After:", chunks[i+1].dBFS)
        # Also combine the reduced volume audio chunk.
        audio_msg += chunks[i+1]
    for chunk in chunks:
        print("Final dBFS:", chunk.dBFS)
    return audio_msg

def get_message(chunkNum):
    chunkNum -= 1
    msg = []
    print("Enter", chunkNum, " numbers: ")
    for i in range(0,chunkNum):
        num = int(input())
        msg.append(num)
    print(msg)
    return msg

def main():
    # Import audio file
    sound = AudioSegment.from_file(file = "sample.mp3", format="mp3")
    # Split audio file into chunks of 5 seconds.
    chunk_length = 50000 # in ms
    chunks = make_chunks(sound, chunk_length)

    # Normalize the audio to a certain volume through out the track.
    volumeDiff = -20
    chunks = normalize_volume(chunks)

    # Enter a list of numbers with the length of the chunk list.
    msg = get_message(len(chunks))

    # Change the volume each chunks.
    song = set_volume(chunks, msg)

    # Save the output.
    song.export("song.mp3", format = "mp3")

if __name__ == "__main__":
    main()


