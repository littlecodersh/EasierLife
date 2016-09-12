# joystick 160912

joystick 提供了一个方便、易懂的操作手柄的方式

## Install

可以通过两种方式使用该代码段：

**一种是通过安装remote-joystick**

通过该命令安装remote-joystick

```bash
pip install remote-joystick
```

之后在项目中这样导入joystick代码段：

```python
from remote-joystick.models.controller.joystick import joystick
```

**另一种是直接将该代码直接放在项目目录下**

当然，你还是需要安装pygame

```bash
pip install pygame
```

之后在项目中这样导入joystick代码段：

```python
from joystick import joystick
```

## Usage

手柄有三种类型的输入：Button, Axis, Hat（按键，摇杆，方向板）

相对应的，这里给出三种注册装饰符：button_register, axis_register, hat_register

例如，我需要获取手柄上的A按键的状态，就可以这么写：

```python
#coding=utf8
from remotejoystick.models.controller.joystick import joystick

js = joystick()

# A为0号按键
@js.button_register(0)
def button_fn(motion):
    if motion == 'down':
        print('A is pressed')
    elif motion == 'up':
        print('A is released')

if js.init():
    js.start()
    try:
        print('Joystick is connected, press Ctrl-C to exit.')
        while 1: raw_input()
    except:
        print('Bye~')
    js.stop()
else:
    print('Restart this program when joystick is plugged in')
```

同样的，剩下的两种输入也是类似的注册。

具体如何操作可以参考我给出的[示例程序][demo-program]

## Attention

该程序在Windows 8.1 -64 Python 2.7.10 通过测试

[demo-program]: https://github.com/littlecodersh/EasierLife/tree/master/Plugins/JoyStick/README.md
