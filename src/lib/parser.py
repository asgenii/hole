def listit(data):
    try:
        command, args = data[0].replace(' ', '').lower(), data[1:]

    except IndexError:
        command, args = '', []

    return command, args