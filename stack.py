class StackException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

class Stack(object):
    def __init__(self, size):
        self.__TOS = 0
        self.__size = size
        self.__array = []
    
    def isEmpty(self):
        return self.__TOS == 0
    
    def isFull(self):
        return self.__TOS == self.__size
    
    def peek(self):
        if self.isEmpty():
            raise StackException("Stack is empty")
        else:
            return self.__array[self.__TOS - 1]
    
    def push(self, item):
        if self.isFull():
            # messagebox.askyesno(message="You seem to just be going in between screens! Taking you back to the homepage...")
            raise StackException("Stack is full")
        else:
            self.__array.append(item)
            self.__TOS += 1
    
    def pop(self):
        if self.isEmpty():
            raise StackException("Stack is empty")
        else:
            self.__TOS -= 1
            return self.__array.pop()
    
    def display(self):
        print("Screen History Stack:")
        for screen_class in reversed(self.__array[:self.__TOS]):
            print(screen_class.__name__)
    
    def clear(self):
        self.__array = []
        self.__TOS = 0
