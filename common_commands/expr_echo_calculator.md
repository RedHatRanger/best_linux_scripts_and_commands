* To use the command line calculator
```
[ansible@ctrl ~]$ expr 1000 / 60
16
```

```
[ansible@ctrl ~]$ expr 1000 / 50
20
```

* To use the echo command and load the math library:
```
[ansible@ctrl ~]$ echo "1000/60" | bc -l
16.66666666666666666666
```
