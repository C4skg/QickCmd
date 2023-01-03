from QickCmd import QickTerminal;

cmd = QickTerminal();
cmd.CONFIG['history'] = 0;
def hello(*args):
    print("hello ?" ,args);

cmd.addCommands('hello',hello);

@cmd.startCmd()
def start(*args):
    print("start" ,args);
