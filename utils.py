def process_file(filepath):
    return_msg = False
    resource_ids = []
    try:
        with filepath.open('r') as f:
            for line in f:
                append(line)

        try:
            tmp = []
            for _id in resource_ids:
                tmp.append(int(_id))
            return_msg = tmp
        except:
            pass
    except:
        pass

    return return_msg

def get_alts(file_ids):
    pass
