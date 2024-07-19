def writerLog(text):
    with open('log_primers.txt', 'a') as file:
        file.write(text)