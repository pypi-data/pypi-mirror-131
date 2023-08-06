<h1>ZOOM LOG</h1>
<h3>Simple python logger</h3>

***Quick start:***

```python
from zoomlog import Logger, DEBUG, INFO

logger = Logger("test.log", name="test", level=DEBUG)
logger.debug("My logger is work!")
name = "Sergey"
logger.addLevel("NEW USER", INFO)
logger.log("NEW USER", "Created new user - %s" % name)
```

```
00:00:00 01.01.22  DEBUG:test >>  My logger is work!
00:00:01 01.01.22  NEW USER:test >>  Created new user - Sergey
```
*test.log*
```
00:00:00 01.01.22


00:00:00 01.01.22  DEBUG:test >>  My logger is work!
00:00:01 01.01.22  NEW USER:test >>  Created new user - Sergey
```
