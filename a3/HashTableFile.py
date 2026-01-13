import base64

# Utility class to store a file in memory
class HashTableFile:
    def __init__(self, path: str | None, class_dict: dict | None):
        if path:
            with open(path, 'rb') as file:
                self.path = path
                self.data = base64.b64encode(file.read()).decode('utf-8')
                self.size = file.tell()
        elif class_dict:
            self.path = class_dict['path']
            self.data = class_dict['data']
            self.size = class_dict['size']
    
    def unpack(self):
        with open(self.path, 'wb') as file:
            file.write(base64.b64decode(self.data))