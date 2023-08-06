<a href="https://pypi.org/project/P4WorkspaceCreator">![ci](https://img.shields.io/github/v/release/sachinrising/p4-workspace-creator)</a> <a href="https://github.com/sachinrising/p4-workspace-creator/releases">![ci](https://img.shields.io/github/release-date/sachinrising/p4workspacecreator)</a> <a href="">![ci](https://img.shields.io/pypi/pyversions/P4WorkspaceCreator)</a>  <a href="https://en.wikipedia.org/wiki/MIT_License">![ci](https://img.shields.io/github/license/sachinrising/P4WorkspaceCreator)</a>


<a href="https://github.com/sachinrising/p4-workspace-creator/tree/main#readme"><img alt="GitHub code size in bytes" src="https://img.shields.io/github/languages/code-size/sachinrising/p4workspacecreator"></a>
# P4WorkspaceCreator

## Description
To automate the creation of perforce workspace using spec file stored in the depot path

Spec file could be like
`//spec/... //[placeholder]/spec/...`

It creates perforce workspace using spec file which is stored in the depot path

## How to install 

```
python -m pip install P4WorkspaceCreator
```

## Usage

Usage example
```
python -m P4WorkspaceCreator -u User -p Password -port perforce:1666 -c User_MachineName_P4WorkspaceCreator -r C:\users\sachin\perforce-workspace -s //spec/example/p4workspacecreator.txt -l "<ClientName>"
```

```
  -u USER, --user USER  Perforce user name
  -p PASSWORD, --password PASSWORD
                        Perforce password
  -port PORT, --port PORT
                        Perforce port address
  -c CLIENT, --client CLIENT
                        Client name which will be used to create workspace
  -r ROOT, --root ROOT  Workspace root path
  -s SPEC, --spec SPEC  Spec file path in depot
  -l PLACEHOLDER, --placeholder PLACEHOLDER
                        Place holder used in the spec file e.g '<ClientName>'
```