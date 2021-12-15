
class membership():
    
    def __init__ (self,init_members):
        self.members = []
        for mem in init_members:
            self.members.append(mem)
    def add(self,input):
        self.members.append(input)
    def delete(self,input):
        self.members.remove(input)
    def get(self):
        return list(self.members)