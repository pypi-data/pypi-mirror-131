import math
import wave
import struct

SAMPLERATE = 44100
DRANGE = 2**15-1

def note(string, oct):
    string = string.upper()
    num = 0;
    if string == "A1":
        num = 1
    elif string == "B":
        num = 2
    elif string == "C":
        num = -9
    elif string == "C1":
        num = -8
    elif string == "D":
        num = -7
    elif string == "D1":
        num = -6
    elif string == "E":
        num = -5
    elif string == "F":
        num = -4
    elif string == "F1":
        num = -3
    elif string == "G":
        num = -2
    elif string == "G1":
        num = -1

    offset_A = BASE_A * math.pow(2, oct)

    return int(offset_A * math.pow(2, num/12))

def filesize(name):
    with open(name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def render(frequency,duration,amplitude,filename):
    arr = []
    for i in range(len(frequency)):
        try:
            arr.append([frequency[i],duration[i]*0.4,amplitude[i]])
        except IndexError:
            print("Please ensure that all the notes are complete with all 3 inputs (frequency, duration, and Amplitude)")
    build(arr,str(filename))
    make(str(filename))

def build(arr,name):
    percent = -1
    ticks = 0
    file = open(name+".sbld","w")
    phase = 0;
    lastf = arr[0][0];
    lasta = 0;
    for i in range(len(arr)):
        s = arr[i][1]
        a = arr[i][2]/100*DRANGE
        freq = arr[i][0]
        if percent < math.floor(ticks/len(arr)*100):
            percent = math.floor(ticks/len(arr)*100)
            print("\rBuilding: " + str(percent) + "%", end="")
        for j in range(int(SAMPLERATE*s)+10000):
            if(int(math.sin(freq*(j+phase)*2*math.pi/SAMPLERATE)*a)==int(math.sin(lastf*(j+phase)*2*math.pi/SAMPLERATE)*lasta)):
                phase += j-SAMPLERATE*s
                break;
        for j in range(int(SAMPLERATE*s)):
            lasta += (a-lasta)*0.1
            file.write(str(int(math.sin(freq*(j+phase)*2*math.pi/SAMPLERATE)*lasta))+"\n")
        ticks += 1;
        lastf = freq;
    return

def add(track1,track2,newname):
    file = open(str(newname+".sbld"),"w")
    file1 = open(str(track1+".sbld"),"r")
    file2 = open(str(track2+".sbld"),"r")
    ticks = max([filesize(track1+".sbld"),filesize(track2+".sbld")])
    percent = 0
    for i in range(ticks):
        if percent < math.floor(i/ticks*100):
            percent = math.floor(i/ticks*100)
            print("\rAdding: " + str(percent) + "%", end="")
        string1 = file1.readline()[:-2]
        if string1 == "":
            string1 = "0"
        elif string1 == "-":
            string1 = "0"
        elif string1 == " ":
            string1 = "0"
        string2 = file2.readline()[:-2]
        if string2 == "":
            string2 = "0"
        elif string2 == "-":
            string2 = "0"
        elif string2 == " ":
            string2 = "0"
        num = (int(string1)+int(string2))
        file.write(str(num)+"\n")

def amplify(track, factor):
    output = ""
    file = open(str(track + ".sbld"), "r")
    ticks = filesize(track + ".sbld")
    percent = 0
    for i in range(ticks):
        string = file.readline()[:-2]
        if string == "":
            string = "0"
        elif string == "-":
            string = "0"
        elif string == " ":
            string = "0"
        num = int(int(string) * factor)
        output += str(num) + "\n"
    file.close()
    file = open(str(track + ".txt"), "w")
    file.write(output)
    file.close()

def clip(track):
    output = ""
    file = open(str(track + ".sbld"), "r")
    ticks = filesize(track + ".sbld")
    percent = 0
    for i in range(ticks):
        string = file.readline()[:-2]
        if string == "":
            string = "0"
        elif string == "-":
            string = "0"
        elif string == " ":
            string = "0"
        num = int(string)
        if num > DRANGE:
            num = DRANGE
        elif num < -1*DRANGE:
            num = -1*DRANGE
        output += str(num)+"\n"
    file.close()
    file = open(str(track + ".sbld"), "w")
    file.write(output)
    file.close()


def make(file_name):
    # Open up a wav file
    wav_file=wave.open(file_name+".wav","w")
    build = open(str(file_name+".sbld"),"r")

    # wav params
    nchannels = 1
    sample_rate = SAMPLERATE
    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The standard for low quality
    # is 8000 or 8kHz.
    nframes = filesize(file_name+".sbld")
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theoretically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    ticks = 0
    percent = -1
    string = ""
    for i in range(nframes):
        string = build.readline()[:-1]
        if string == "":
            string = "0"
        elif string == "-":
            string = "0"
        elif string == " ":
            string = "0"
        wav_file.writeframes(struct.pack('h', int(string)))
        ticks+=1
        if percent < math.floor(ticks/nframes*100):
           percent = math.floor(ticks/nframes*100)
           print("\rCompiling: " + str(percent) + "%", end="")


    wav_file.close()
    build.close()

    return

BASE_A = 440
C  = note("c", 0)  # -9
C1 = note("c1", 0) # -8
D  = note("d", 0)  # -7
D1 = note("d1", 0) # -6
E  = note("e", 0)  # -5
F  = note("f", 0)  # -4
F1 = note("f1", 0) # -3
G  =  note("g", 0) # -2
G1 = note("g", 0)  # -1
A  = note("a", 0)  #  0
A1 = note("a1", 0) #  1
B  = note("b", 0)  #  2
