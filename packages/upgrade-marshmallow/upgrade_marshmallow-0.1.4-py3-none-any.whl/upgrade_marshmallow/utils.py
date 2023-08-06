def output_file(data, file):
    with open(file, 'w') as fp:
        fp.writelines(data)
