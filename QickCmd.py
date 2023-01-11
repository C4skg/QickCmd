import os,colorama,time,atexit;
from inspect import isfunction;
from getpass import getuser;


class QickTerminal:
    '''
    Basic usage:

    >>> import QickTerminal
    >>> nCmd = QickTerminal('QickTerminal','./')
    >>> @cmd.startCmd()
    >>> def receiveCommand(*args):
    >>>      print(args);

    use nCmd.addCommands to add commands by yourself;
    >>> def printHello():
    >>>     print("hello?");
    >>> nCmd.addCommands('hello',printHello);

    then,you can use key `hello` in terminal:
    >>> $> hello
    >>> $> hello?

    @copyright: (c) 2023 by C4ksg.
    '''

    def __init__(self,TName:str = 'C4skg',awd:str = './') -> None:
        '''
            退出注册
        '''
        atexit.register(self.exitEvent);

        '''
            CONFIG
        '''
        self.CONFIG = {
            'history': 1 #命令历史开关
        }


        self.flag = TName if TName != '' else getuser();
        self.awd = os.path.abspath(awd);
        
        '''
            Color config
        '''
        colorama.init(autoreset=True);
        self.Fore = colorama.Fore.CYAN;             # 左边字体颜色
        self.MAGENTA = colorama.Fore.LIGHTBLUE_EX;  # 用户输入颜色
        self.Warning = colorama.Fore.RED;           # 警告颜色
        self.Info = colorama.Fore.GREEN;            # 提示信息颜色
        self.Reset = colorama.Fore.RESET;           #恢复颜色

        '''
            内部命令增添;
        ''' 
        self.iCmd = {
            '.exit': -1,
            'cd': lambda *args:self.changeAwd(*args)
        };

        '''
            历史命令保存列表
        '''
        self.hisList = ["[ %s ]"%self.getTime()];

        '''
            必须判断路径是否存在;
            不存在直接跳转到当前工作目录;
        '''
        if not os.path.exists(self.awd):
            self.awd = os.path.abspath('./');

    def addCommands(self,cmdName:str,func)-> int:
        '''
            0：添加失败
            1：添加成功oko
            2：命令已存在
        '''
        if self.iCmd.get(cmdName) == None:
            try:
                self.iCmd[cmdName] = lambda *callback:func(*callback);
                return 1;
            except TypeError as e:
                return 0;
            
        else:
            return 2;

    def selfWorkerSpace(self):
        return os.path.split(os.path.realpath(__file__))[0];

    def changeAwd(self,*argvs)->bool:
        if len(argvs) == 1:
            print(self.Warning + 'cd must be given 2 parameters');
            return False;
        target = argvs[1].replace('\\','/');
        awd = os.path.abspath(os.path.join(self.awd.replace('\\','/'),target));
        if os.path.exists(awd):
            try:
                os.chdir(awd);
                self.awd = awd;
            except:
                print(self.Warning + "目录切换失败");
                return False;
            return True;
        print(self.Info + "目录 {} {}".format(self.Warning+awd,self.Info+"不存在"));
        return False;

    def isSystemCmd(self,cmd:str)-> bool:
        '''
            判断系统命令是否存在
        '''
        endle = ['','.bat','.exe','.sh']; #结尾添加检测
        for path in os.environ["PATH"].split(os.pathsep):
            path += "/";
            for end in endle:
                cmdExist = os.access(os.path.join(path,cmd+end),os.X_OK);
                if cmdExist:
                    return True;
        return False;
    
    def w2History(self,cmd=None,cmdlines=None)-> None:
        file = self.selfWorkerSpace()+"\\.Qick_history";
        with open(file,'a+') as history:
            if cmd != None and type(cmd) == str:
                history.write(cmd);
            elif cmdlines!= None and type(cmdlines) == list:
                history.write('\n'.join(cmdlines));
            else:
                return;
            history.write('\n');


    def getTime(self)-> str:
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime());


    def startCmd(self):
        '''
            start your own cmd
            QickTerminal命令 > 系统命令 > 返还用户命令

            返还的参数将以传参形式进入到所调用函数中

            >>> @cmd.startCmd
            >>> def getReturnCommands(*args):
            >>>     print("所获取的命令: " +str(args))
        '''
        def In(*args):
            while True:
                signal = self.Fore + "(%s)%s $> " % (self.awd,self.flag);
                print(signal,end='');
                userIn = str(input(self.MAGENTA)).replace('\t','').split(' ');
                '''
                    恢复色彩
                '''
                print(self.Reset,end='');

                if len(userIn) == 0:
                    continue;
                # 标志
                KEY = userIn[0];

                if KEY in self.iCmd:
                    ready = self.iCmd[KEY];
                    if isfunction(ready):
                        # 函数执行
                        try:
                            result = ready(*userIn);
                        except TypeError as e:
                            raise e;
                    else:
                        result = ready;
                    if result == -1 and type(result) == int:
                        print(self.Info + 'GoodBye~');
                        break;
                elif self.isSystemCmd(KEY):
                    os.system(' '.join(userIn));
                else:
                    '''
                        用户函数返还
                    '''
                    func = args[0];
                    try:
                        func(*userIn);
                    except TypeError as e:
                        raise e;

                    continue;
                self.hisList.append(' '.join(userIn));
        return In;

    def exitEvent(self):
        if len(self.hisList) <= 1 or not (self.CONFIG['history']):
            pass;
        else:
            self.w2History(cmdlines=self.hisList);