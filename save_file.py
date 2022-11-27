#!/usr/bin/python
import cgi, os
import cgitb; cgitb.enable()
form = cgi.FieldStorage()
# Get filename here.
fileitem = form['filename']
# Test if the file was uploaded
if fileitem.filename:
   # strip leading path from file name to avoid
   # directory traversal attacks
   fn = os.path.basename(fileitem.filename)
   open('/tmp/' + fn, 'wb').write(fileitem.file.read())
   message1 = 'The file "' + fn + '" was uploaded successfully'
else:
   message1 = 'No file was uploaded'
print("""\
Content-Type: text/html

<html>
<body>
   <p>{}</p>
</body>
</html>
""".format(message1))