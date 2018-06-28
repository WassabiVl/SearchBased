import random

rock = 'rock'
paper = 'paper'
scissor = 'scissor'
list1 = [rock, paper, scissor]
start = 'lets play Rock,Paper,Scissors'
instructions = 'Select Rock, Paper, or Scissor'
error = 'You did not input rock, paper, scissor. try again'
you_win = 'You win this round'
you_lose = 'You lose this round'


def random_choice():
    return random.choice(list1)


def print_string(the_string):
    print(the_string)
    return


class RockPaperScissors:
    user, computer = 0, 0

    @staticmethod
    def winner(user_choice, computer_choice):
        if computer_choice == user_choice:
            return print_string('draw')
        else:
            if computer_choice == rock:
                if user_choice == paper:
                    RockPaperScissors.user += 1
                    return print_string(you_win)
                elif user_choice == scissor:
                    RockPaperScissors.computer += 1
                    return print_string(you_lose)
            elif computer_choice == paper:
                if user_choice == rock:
                    RockPaperScissors.computer += 1
                    return print_string(you_lose)
                elif user_choice == scissor:
                    RockPaperScissors.user += 1
                    return print_string(you_win)
            elif computer_choice == scissor:
                if user_choice == paper:
                    RockPaperScissors.computer += 1
                    return print_string(you_lose)
                elif user_choice == rock:
                    RockPaperScissors.user += 1
                    return print_string(you_win)

    def main(self):
        print(start)
        print_string(instructions)
        user_choice = input()
        if not any(user_choice.lower() in s for s in list1):
            print(error)
            return RockPaperScissors.main(self)
        else:
            computer_choice = random_choice()
        print_string('computer chooses ' + computer_choice)
        RockPaperScissors.winner(user_choice, computer_choice)
        print_string('current score')
        print_string('you: ' + RockPaperScissors.user.__str__())
        print_string('computer: ' + RockPaperScissors.computer.__str__())
        to_continue = input('Do you want to continue (yes/no): ')
        if to_continue == 'yes':
            return RockPaperScissors.main(self)
