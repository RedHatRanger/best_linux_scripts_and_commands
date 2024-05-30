* To recursively download every file from a website:
```
wget -m -np -c -R "*.iso","*index.html","*.tar.gz","*.zip" http://<site>
```
* Example ISO download:
```
wget https://archive.org/download/tiny-iso-test/TinyIsoTest.iso
```
