from os import path
from pydub import AudioSegment

# files                                                                         
# src = "C:\Users\Szymon\Downloads\download.wab"
dst = "test.wav"

# convert wav to mp3                                                            
sound = AudioSegment.from_wav(src)
sound.export(dst, format="wav")