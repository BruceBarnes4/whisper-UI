# whisper-UI
## What is the whisper
Whisper is openAI's opensource speech to text deeplearning model. It is free. with whisper, you could easely convert your lecture record into the text, which is very helpful for the non-native speaker or oversea student like me. 
## What is this? What is whisper-UI
Whisper-UI is a small tool that you can convert your record to text without command or program. (Don't judge my code style. I know my code is like shit.) What is more that after you convert it to record, in my tool, you can simply click the text, and this tool will play the record from what the text you click in. So, this tool is not only can help you understand what your lecturer said, but also help you practise your English listening.
## Prepare
This tool is just a UI program. In order to use it, you have to install python, ffmpeg, whisper. Please follow this instructions. https://github.com/openai/whisper

And, because I use moviepy to convert the .m3a .opus file into .mp3 file, the installation of moviepy is necessary. Don't worry, it is very simple. In your terminal, just input this command. (Before this you had install the python and pip)
```
pip install moviepy
```

And PyQt5 also have to be installed.

```
pip install PyQt5
```

After all the above is finished, you can simply use this tool. In terminal, cd into the whisper-UI folder. And use `python main.py` to launch this tool.
## How to use it
As you launch this tool, you will see a small window. And click the "Select File" to select the record which you want to convert.

If that record is not converted before, it will be converted and it will take a long time. Patience please. After converting is finished. A new window will open. And you can simply click the text to play the record. Very useful English listening practice tool right? 
## something weird
I use the `setPosition(milliseconds)` to set what time your record play begins. But, I just found that it should be 2 times milliseconds. That is weird.