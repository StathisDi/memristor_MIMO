
param(
  [string]$QSPath = "C:\questasim64_2022.4",
  [string]$PyPath = "C:\Program Files\Python311",
  [string]$Compiler = "cl",
  [string]$SrcFile = "fli_interface.cpp",
  [string]$DevShell = "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\Launch-VsDevShell.ps1",
  [string]$Arch = "amd64",
  [string]$HostArch = "amd64",
  [string]$Out = "null",
  [string]$Func = "null",
  [switch]$Help,
  [switch]$Py,
  [switch]$Cpp,
  [switch]$clean
)

function Show_Help {
  "This script can be used to compile c/c++ code in windows. It can link the code with Questasim FLI and python libraries."
  "Usage: .\CompileFLI.ps1 [-QSPath <path>] [-PyPath <path>] [-Compiler <cmdlet>] [-SrcFile <filename>] [-DevShell <path>] [-HostArch <arch name>] [-Arch <arch name>] [-Out <filename>] [-Func <function name>] [-Py] [-Cpp] [-Clean] [-Help]"
  " "
  "[string] -QSPath   : Specifies the path to the ModelSim installation directory. Default is 'C:\questasim64_2022.4'."
  "[string] -PyPath   : Specifies the path to the Python installation directory. Default is 'C:\Program Files\Python311'. This is ignored when the -Py option is not used."
  "[string] -Compiler : Specifies the compiler executable (e.g., 'cl'). Default is 'cl'."
  "[string] -SrcFile  : Specifies the name of the source file to compile. Default is 'fli_interface.cpp'."
  "[string] -DevShell : Specifies the path to the developement shell script for windows, default is C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\Launch-VsDevShell.ps1"
  "[string] -Arch     : Specifies the traget architecture, default is amd64."
  "[string] -HostArch : Specifies the host architecture, default is amd64."
  "[string] -Out      : Specifies the name of the output file name. Default is the same as the input source file name .dll."
  "[string] -Func     : Specifies the name of the foreign function. Default is the same as the input source file name."
  "[switch] -Help     : Displays this help message."
  "[switch] -Clean    : Deletes all generated files instead of compiling."
  "[switch] -Py       : Compiles and links with Python libraries, when specified it requires a valid python path."
  "[switch] -Cpp      : Compiles without linking to the questasim libraries. It compiles simple c++ and can be combined with -Py, it generates an exe."
  " "
  "Example: .\CompileFLI.ps1 -QSPath 'C:\custom\path\to\modelsim' -PyPath 'C:\custom\path\to\python' -Compiler 'C:\path\to\compiler\cl.exe' -SrcFile 'my_custom_file.cpp'"
  exit
}

function Clean_Up {
  $extensions = @("*.dll", "*.exp", "*.lib", "*.obj", ".exe")  
  foreach ($ext in $extensions) {
    Get-ChildItem -Path . -Filter $ext -Recurse | ForEach-Object {
      Write-Host "Deleting $($_.FullName)"
      Remove-Item $_.FullName -ErrorAction Ignore
    }
  }
}

function Compile {
  param (
    [string]$QSPath,
    [string]$PyPath,
    [string]$Compiler,
    [string]$SrcFile,
    [string]$DevShell,
    [string]$Arch,
    [string]$HostArch,
    [string]$Out,
    [string]$Func,
    [boolean]$Py,
    [boolean]$Cpp
  )

  $name = (Get-Item $SrcFile).BaseName

  if ($Out -eq "null") {
    $Out = $name + ".dll"
  }

  if ($Func -eq "null") {
    $Func = $name
  }

  $env:QSPath = $QSPath
  $env:PyPath = $PyPath

  $includeModelSim = "$QSPath\include"
  $includePython = "$PyPath\include"
  $linkModelSimLib = "$QSPath\win64\mtipli.lib"
  $linkPythonLib = "$PyPath\libs\python311.lib"
  $cppStandard = "/std:c++17"

  & $DevShell -Arch $Arch -HostArch $HostArch

  if ($Py) {
    if ($Cpp) {
      Write-Output "Compiling C++ with Python"
      cl /EHsc $cppStandard /I$includePython $SrcFile /link $linkPythonLib
    }
    else {
      Write-Output "Compiling QS with Python"
      & $Compiler -c /EHsc $cppStandard /I$includeModelSim /I$includePython /LD $SrcFile 
      & link -DLL -export:$Func $name".obj" $linkModelSimLib $linkPythonLib /out:$Out
      #& link -DLL -export:py_init $name".obj" $linkModelSimLib $linkPythonLib /out:py_init.dll
      #& link -DLL -export:py_fin $name".obj" $linkModelSimLib $linkPythonLib /out:py_fin.dll
      #& link -DLL $name".obj" $linkModelSimLib $linkPythonLib /out:$Out
      #-export:print_param
    }
  }
  else {
    if ($Cpp) {
      Write-Output "Compiling simple c++"
      cl /EHsc $cppStandard $SrcFile
    }
    else {
      Write-Output "Compiling QS"
      & $Compiler -c /EHsc /I$includeModelSim /LD $SrcFile 
      & link -DLL -export:$Func $name".obj" $linkModelSimLib /out:$Out
    }
  }
}

if ($Help) {
  Show_Help
}

if (-not $QSPath -or -not $PyPath -or -not $Compiler -or -not $SrcFile) {
  "Missing required parameters. Use -Help for more information."
  exit
}

if ($clean) {
  Clean_Up
}
else {
  Compile -QSPath $QSPath -PyPath $PyPath -Compiler $Compiler -SrcFile $SrcFile -DevShell $DevShell -Arch $Arch -HostArch $HostArch -Out $Out -Func $Func -Py $Py -Cpp $Cpp
}


