class Shell:
    def read(self):
        return input('Ɛ>').split()
    
    def send(self, data):
        if data:
            print(data)