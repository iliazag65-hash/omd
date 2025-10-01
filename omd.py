# Guido van Rossum <guido@python.org>


def step1():
    print("Утка-маляр 🦆 решила выпить зайти в бар. " "Взять ей зонтик? ☂️")
    option = ""
    options = {"да": True, "нет": False}
    while option not in options:
        print("Выберите: {}/{}".format(*options))
        option = input()

    if options[option]:
        return step2_umbrella()
    return step2_no_umbrella()


def step2_umbrella():
    print("Утка взяла зонтик и пошла в бар")
    return game_over()


def step2_no_umbrella():
    print("Утка не взяла зонт, промокла и заболела")
    print("Продлжить приключение?")
    option = ""
    options = {"да": True, "нет": False}
    while option not in options:
        print("Выберите: {}/{}".format(*options))
        option = input()

    if options[option]:
        print("Возрождение:")
        print("1")
        print("2")
        print("3")
        print("==================================")
        return step1()
    return game_over()


def game_over():
    print("Приключение закночено. Приходите ещё.")


if __name__ == "__main__":
    step1()
