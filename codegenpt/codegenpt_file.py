from os import path


class CodeGenPTFile:

    @property
    def filename(self):
        return '.'.join(self.__filename.split('.')[:-1])
    
    @property
    def extension(self):
        return self.filename.split('.')[-1]
    
    @property
    def prompt(self):
        with (self.__file) as file:
            return ''.join(file.readlines())
        
    @property
    def path(self):
        return self.filename.split('/')[:-1]
    
    @property
    def basename(self):
        return path.basename(self.filename)
        
    @property
    def context(self):
        return {
            'basename': self.basename,
            'extension': self.extension,
            'path': self.path,
        }

    def __init__(self, filename):
        self.__filename = filename
        self.__file = None
        self.file = None

    def __enter__(self):
        self.__file = open(self.__filename, 'r')
        self.file = open(self.filename, 'w+')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__file.close()

    def write(self, content):
        with self.file as file:
            file.write(content)