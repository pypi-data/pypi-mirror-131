# pyautomouse

```python
import pyautomouse

#class Mouse
m = pyautomouse.Mouse()
# click
m.mouseClick(count=,Time=,x=,y=,button=,isdoubleclick=,istripleClick=) => return None
# getMouseXY
x,y=m.getMouseXY() => return x,y
# MoveTo
m.MoveTo(x=,y=,duration=) => return None
# dragTo
m.dragTo(x=,y=,button=,duration=) => return None
#class keyboard
k = pyautomouse.keyboard()
#hotkey
k.hotkey(args=, count=, Time=)
#press
k.press(key=, count=, Time=)
#keyUp
k.keyUp(key=, count=, Time=)
#keyUp
k.keyDown(key=, count=, Time=)
#keyUp
k.typewrite(key=, count=, Time=)
```[EOF]
