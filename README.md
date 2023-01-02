# QickCmd

### 一、简介



### 二、使用方法

1. 基本使用

   ```python
   from QickCmd import QickTerminal
   
   cmd = QickTerminal('C4skg','./')
   
   @cmd.startCmd()
   def start(*args):
   	print("命令返还 -> ", args);
   ```

2. 添加命令并执行

   当 `QickCmd` 捕获到添加的指令后，会自动调用该方法，并传入命令后的所有参数

   ```python
   def hello(*args):
       print('hello ?')
   
   cmd.addCommands('hello!',hello);
   ```

3. 命令相关

   + 命令优先级

     ` 自定义命令 > 系统命令 > 返还命令 `


   + 命令历史

     通过配置可以更改是否生成命令的历史记录

     ```python
     '''
     	开 = 1 //默认值
     	关 = 0
     '''
     cmd.CONFIG['histroy'] = 1
     ```



### 三、写在最后

+ 通过简单的一些方法混合使用得到的可以自定义的命令窗口，功能会慢慢加上

+ 若有更好的建议，代码问题，侵权相关请开 `issue`
  
+ 代码功底不好，不要喷