; Stock Management Application - Inno Setup Script
; Creates a complete Windows installer with MongoDB bundled

#define MyAppName "Stock Management"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Your Company Name"
#define MyAppURL "https://yourwebsite.com"
#define MyAppExeName "StockManagement.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
AppId={{A1B2C3D4-E5F6-4A5B-9C8D-7E6F5A4B3C2D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE.txt
OutputDir=installer_output
OutputBaseFilename=StockManagement_Setup_v{#MyAppVersion}
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Application files
Source: "dist\StockManagement\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; MongoDB files
Source: "mongodb\*"; DestDir: "{app}\mongodb"; Flags: ignoreversion recursesubdirs createallsubdirs

; Documentation
Source: "LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion isreadme

; Scripts
Source: "scripts_installer\*"; DestDir: "{app}\scripts"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\scripts\launch_app.bat"; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\scripts\launch_app.bat"; WorkingDir: "{app}"; IconFilename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Install MongoDB as Windows Service
Filename: "{app}\scripts\install_mongodb_service.bat"; Parameters: """{app}"""; StatusMsg: "Installing MongoDB service..."; Flags: runhidden waituntilterminated

; Start MongoDB service
Filename: "net"; Parameters: "start StockManagementMongoDB"; StatusMsg: "Starting MongoDB service..."; Flags: runhidden waituntilterminated

; Run the application after installation
Filename: "{app}\scripts\launch_app.bat"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; Stop MongoDB service
Filename: "net"; Parameters: "stop StockManagementMongoDB"; Flags: runhidden waituntilterminated

; Remove MongoDB service
Filename: "{app}\mongodb\bin\mongod.exe"; Parameters: "--remove --serviceName=""StockManagementMongoDB"""; Flags: runhidden waituntilterminated

[Code]
var
  DataDirPage: TInputDirWizardPage;

procedure InitializeWizard;
begin
  { Create custom page for data directory }
  DataDirPage := CreateInputDirPage(wpSelectDir,
    'Select Data Location', 'Where should database files be stored?',
    'Select the folder where the application data will be stored, then click Next.',
    False, '');
  DataDirPage.Add('Database location:');
  DataDirPage.Values[0] := ExpandConstant('{commonappdata}\{#MyAppName}');
end;

function GetDataDir(Param: String): String;
begin
  Result := DataDirPage.Values[0];
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
  DataPath: String;
begin
  if CurStep = ssPostInstall then
  begin
    { Create data directories }
    DataPath := DataDirPage.Values[0];
    CreateDir(DataPath);
    CreateDir(DataPath + '\db');
    CreateDir(DataPath + '\logs');
    
    { Save data path to config file }
    SaveStringToFile(ExpandConstant('{app}\data_path.txt'), DataPath, False);
  end;
end;
