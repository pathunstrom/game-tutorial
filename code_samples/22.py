def file_spawner(file_name):
    with open(path.join(path.dirname(__file__), file_name), "r") as spawn_file:
        spawn_reader = csv.reader(csvfile)
        for row in spawn_reader:
            yield float(row[0]), int(row[1])