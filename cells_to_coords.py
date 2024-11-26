if __name__ == "__main__":
    filename = input("Skriv in filnamn på fil med .cells format\n")
    offset_x = int(input("Offset x\n"))
    offset_y = int(input("Offset y\n"))
    file = open("all/" + filename + ".cells", "r")

    alive_cells = set()
    y = 0
    for line in file.readlines():
        if line.startswith("!"):
            continue

        for x, letter in enumerate(line):
            if letter == "O":
                alive_cells.add((x + offset_x, y + offset_y))

        y += 1

    file.close()

    print(alive_cells)
    file = open("gen/" + filename + ".txt", "w")
    for x, y in alive_cells:
        file.write(str(x) + " " + str(y) + "\n")

    file.close()
