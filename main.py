import bot.bot as main
import os

if __name__ == '__main__':
    main.main(open(os.getcwd()+os.sep+'token', 'r').read().strip())
