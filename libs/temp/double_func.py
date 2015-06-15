class Module(object):
    def create(self, arg):
        print(arg)

    def read(self, arg):
        return(arg)


module = Module()

module.create('Module created')
