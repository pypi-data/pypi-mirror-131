def command(func):
    print('Bok')
    def execution(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return execution