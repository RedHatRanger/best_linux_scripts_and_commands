# You must first install Powershell for your version of Linux, then download Evaluate-STIG from here (NOTE: you will need a CAC to download it):
https://spork.navsea.navy.mil/nswc-crane-division/evaluate-stig

* To run Evaluate-STIG with an answerfile:
```
yum install -y libicu lshw
pwsh /path/to/Evaluate-STIG.ps1 -ScanType "Unclassified" -Marking "NotSecret" -Output CKL,CKLB -OutputPath /opt -AFPath /path/to/Evaluate-STIG/AnswerFiles
```
