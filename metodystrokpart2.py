def the_hardest_word(words):
    list_ = []
    cnt = 0
    for word in words:
        for i in word:
            cnt += ord(i)
        list_.append(cnt)
        cnt = 0
    return words[list_.index(max(list_))]
            

        

    

words = [input() for _ in range(4)]
print(the_hardest_word(words))