class Often_char:
    def __init__(self, input_line: str):
        self.input_line = input_line
        
        

    def find_max_count(self):
        maxi = ''
        counter = 0
        for char in self.input_line:
            if self.input_line.count(char) >= counter:
                counter = self.input_line.count(char)
                maxi = char


        return maxi



result = Often_char(input()).find_max_count()
print(result)

