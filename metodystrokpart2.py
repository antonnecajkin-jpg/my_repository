class First_and_last_occurrence:
    def __init__(self, input_line: str):
        self.input_line = input_line
        self.find_char = 'f'
        
        

    def find_index_char(self):
        first_char_in = 0
        last_char_in = 0
        if self.find_char not in self.input_line:
            return 'NO'
        else:
             first_char_in = self.input_line.find(self.find_char)
             for_rfind = self.input_line.replace(self.input_line[0:first_char_in], '_'*first_char_in) 
             last_char_in = for_rfind.rfind(self.find_char)
             if last_char_in != 1:
                 last_char_in = last_char_in
             return first_char_in, last_char_in
             
                 
                 
                 
        



result = First_and_last_occurrence(input()).find_index_char()
print(result)

