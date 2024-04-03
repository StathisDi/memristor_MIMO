
param(
  [string]$QSPath = "C:\questasim64_2022.4",
  [string]$PyPath = "C:\Program Files\Python311",
  [string]$Compiler = "cl",
  [string]$SrcFile = "fli_interface.cpp",
  [string]$Out = "null",
  [switch]$Help,
  [switch]$Py,
  [switch]$clean
)

function Show-Help {
  "Usage: .\CompileFLI.ps1 [-QSPath <path>] [-PyPath <path>] [-Compiler <path>] [-SrcFile <filename>] [-Help]"
  " "
  "-QSPath   : Specifies the path to the ModelSim installation directory. Default is 'C:\questasim64_2022.4'."
  "-PyPath   : Specifies the path to the Python installation directory. Default is 'C:\Program Files\Python311'."
  "-Compiler : Specifies the path to the compiler executable (e.g., 'cl'). Default is 'cl'."
  "-SrcFile  : Specifies the name of the source file to compile. Default is 'fli_interface.cpp'."
  "-Help     : Displays this help message."
  " "
  "Example: .\CompileFLI.ps1 -MSPath 'C:\custom\path\to\modelsim' -PyPath 'C:\custom\path\to\python' -Compiler 'C:\path\to\compiler\cl.exe' -SrcFile 'my_custom_file.cpp'"
  exit
}

function Clean-Up {
  $extensions = @("*.dll", "*.exp", "*.lib", "*.obj")  
  foreach ($ext in $extensions) {
    Get-ChildItem -Path . -Filter $ext -Recurse | ForEach-Object {
      Write-Host "Deleting $($_.FullName)"
      Remove-Item $_.FullName -ErrorAction Ignore
    }
  }
}

function compile {
  param (
    [string]$QSPath,
    [string]$PyPath,
    [string]$Compiler,
    [string]$SrcFile,
    [switch]$Py
  )

  $name = (Get-Item $SrcFile).BaseName

  if ($Out -eq "null") {
    $Out = $name + ".dll"
  }
  
  echo $Out
  $env:QSPath = $QSPath
  $env:PyPath = $PyPath

  $includeModelSim = "C:\questasim64_2022.4\include"
  $includePython = "$PyPath\include"
  $linkModelSimLib = "$QSPath\win64\mtipli.lib"
  $linkPythonLib = "$PyPath\libs\python311.lib"

  if ($Py) {
    & 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\Launch-VsDevShell.ps1' -Arch amd64 -HostArch amd64 # allias to lunch VS tools C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\Launch-VsDevShell.ps1

    #cl -c -EHsc -IC:\questasim64_2022.4\include .\hello_world.cpp /link /DLL -export:print_param hello_world.obj C:\questasim64_2022.4\win64\mtipli.lib

    #cl -c /I"C:\questasim64_2022.4\include" /I"C:\Program Files\Python311\include" /LD hello_world.cpp /link -export:print_param print_param.obj C:\questasim64_2022.4\win64\mtipli.lib C:\Program Files\Python311\libs\python311.lib /Fe:print_param.dll

    & $Compiler -c /EHsc /I$includeModelSim /LD $SrcFile 
    & link -DLL -export:print_param $name".obj" C:\questasim64_2022.4\win64\mtipli.lib /out:$name".dll"
  }
  else {
    & 'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\Launch-VsDevShell.ps1' -Arch amd64 -HostArch amd64 # allias to lunch VS tools C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\Launch-VsDevShell.ps1
    
    #cl -c -EHsc -IC:\questasim64_2022.4\include .\hello_world.cpp /link /DLL -export:print_param hello_world.obj C:\questasim64_2022.4\win64\mtipli.lib
    
    #cl -c /I"C:\questasim64_2022.4\include" /I"C:\Program Files\Python311\include" /LD hello_world.cpp /link -export:print_param print_param.obj C:\questasim64_2022.4\win64\mtipli.lib C:\Program Files\Python311\libs\python311.lib /Fe:print_param.dll
    
    & $Compiler -c /EHsc /I$includeModelSim /LD $SrcFile 
    & link -DLL -export:print_param $name".obj" C:\questasim64_2022.4\win64\mtipli.lib /out:$name".dll"
  }
}

if ($Help) {
  Show-Help
}

if (-not $QSPath -or -not $PyPath -or -not $Compiler -or -not $SrcFile) {
  "Missing required parameters. Use -Help for more information."
  exit
}

if ($clean) {
  Clean-Up
}
else {
  Compile -QSPath $QSPath -PyPath $PyPath -Compiler $Compiler -SrcFile $SrcFile -Py $Py
}


