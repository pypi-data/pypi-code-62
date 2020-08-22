import sys
import pyuts

def getArgv(index,defValue=None):
    if len(sys.argv) > index:
        return sys.argv[index]
    return defValue

def getParms(key,defValue=None):
    if 1 >= len(sys.argv):
        return defValue
    for i in range(1, len(sys.argv), 2):
        pkey = getArgv(i)
        if key == pkey:
            return getArgv(i+1,defValue)
    return defValue
  
def printHelp():
    print('python crawl.py command testCrawl -p 【projectName】 -a paramstr')  
    print('python crawl.py spider Test -p 【projectName】 -a paramstr')


if __name__ == "__main__":
    option = getArgv(1,'')
    if option in ['help','h','--help','-help','-h']:
        printHelp()
    elif option in ['command','c','-c','-command','--command']:
        commandName = getParms(option,'')
        projectName = getParms('-p','') 
        if len(commandName) == 0 or len(projectName) == 0:
            printHelp()
            exit()
        params = getParms('-a','')
        _a = f' -a {params}' if len(params) > 0 else ''
        cmd = f"scrapy {commandName}{_a}"
        pyuts.cmdU().run(cmd, cwd=f'./{projectName}')
    elif option in ['spider','s','-s','-spider','--spider']:
        spiderName = getParms(option,'')
        projectName = getParms('-p','') 
        if len(spiderName) == 0 or len(projectName) == 0:
            printHelp()
            exit()
        params = getParms('-a','')
        _a = f' -a {params}' if len(params) > 0 else ''
        cmd = f"scrapy crawl {spiderName}{_a}"
        pyuts.cmdU().run(cmd, cwd=f'./{projectName}')
        