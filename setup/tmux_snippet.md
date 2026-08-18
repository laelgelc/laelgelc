Use `tmux`:
```shell script
tmux new -s jubilee_speech
```
Inside the session:
```shell script
conda activate whisperx_pyannote
cd ~/cl_st1_carol/cl_st1_ph0_carol

python transcribe_jubilee_debates_whisperx.py --no-test-mode
python align_jubilee_debates_whisperx.py --no-test-mode
python diarise_jubilee_debates_pyannote.py --no-test-mode
python assign_speakers_jubilee_debates.py --no-test-mode
python qc_jubilee_debates_speaker_diarisation.py --no-test-mode
```
Detach from `tmux`:
```plain text
Ctrl+B
D
```
List the active sessions:
```shell script
tmux ls
```
```shell script
jubilee_speech: 1 windows (created Tue Aug 18 16:56:54 2026)
```
Reattach:
```shell script
tmux attach -t jubilee_speech
```