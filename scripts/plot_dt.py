KEY_WORD = "dt = "

def read_dt(file_name):
    dt_list = []
    with open(file_name) as fh:
        for line in fh:
            if KEY_WORD in line:
                dt = line.split(KEY_WORD)[1].strip()
                dt_list.append(float(dt))
    return dt_list

print(read_dt("nohup.out"))
