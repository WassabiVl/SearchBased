from Task1.Numpy import NumpyOne, NumpyTwo, NumpyThree, NumpyFour
from Task1.RockPaperScissors import RockPaperScissors


def main():
    print('Choose your options: ')
    print('1 - Rock Paper Scissors ')
    print('2 - numpy ')
    num_choice = input('Which Number? ')
    if num_choice == '1':
        rock_paper_scissors = RockPaperScissors()
        rock_paper_scissors.main()
        return main()
    elif num_choice == '2':
        no = NumpyOne()
        no.main()
        nt = NumpyTwo()
        nt.main()
        nth = NumpyThree()
        nth.main()
        nf = NumpyFour()
        nf.main()
        return main()
    else:
        print('you did not choose a number, try again')
        return main()


main()
