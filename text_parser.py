def parse(content):
    titles = []
    with open(content, mode='r', encoding='utf-8') as reader:
        paragraphs = []
        lines = reader.readlines()
        new_lines = []
        for i in lines:
            if i != '\n':
                new_lines.append(i.replace('=', ''))
        for line in lines:
            if '==' in line:
                titles.append(line.replace('=', ''))
        first_title = new_lines.index(titles[0])
        for title in titles[1:]:
            ind = new_lines.index(title)

            paragraphs.append(new_lines[first_title + 1:ind])

            first_title = ind
    paragraphs.append(new_lines[first_title:])

    return titles, paragraphs
