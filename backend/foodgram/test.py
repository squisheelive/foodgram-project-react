class Svetka():
    def __init__(self, vova):
        self.vova = vova

    def nadya(self):
        return 'привет, я Надя!'

x = locals()['Svetka'](vova='asda')
# x = Svetka(vova='bbb')

print(x.vova)