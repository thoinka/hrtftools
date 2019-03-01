# HRTF Tools

The Python scripts contained in this repo aim to help with the calculation of HRTFs (Head-related transfer function) and the processing of audio files without professional equipment (seriously!)

## How to

### Requirements

* Some microphone with somewhat isotropic directivity (I use the microphone that comes with my Apple EarPods)
* A computer that can record audio incl. some software to do the job (say, Audacity)
* Some playback device that is not your computer (I use my iPhone)
* Python 3 with
	* `numpy`
	* `scipy`
	* `click`

### Methodology

1. Use `sweep.py` to generate a sweep file.
```
python sweep.py -o sweep.wav
```
With default settings, the audio file contains two sweeps separated by 5 seconds of silence.

2. Make sure you can playback the sweep on some device. In the simplest case that may be just your phone.

3. Plug in your microphone, start recording and put the microphone on your left ear

4. Play the sweep sound

5. In the 5 second break, put the microphone on your right ear

6. Once the sweep has finished, save the recording.

7. Now use `process.py` to calculate the HRTF
```
python process.py -i your_recording.wav -o your_hrtf.wav
```

8. Done. You can now use `convolver.py` to process some music
```
python convolver.py -i your_music.wav -r hrtf_right_speaker.wav -l hrtf_left_speaker.wav -o your_music_binaural.wav
```

## Additional details

All of the scripts have a fair amount of parameters, it may be instructive to tweak them in case th result is not satisfying or something goes wrong.