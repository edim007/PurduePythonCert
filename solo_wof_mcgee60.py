"""
Author: Edi McGee, mcgee60@purdue.edu
Assignment: 12.1 - Solo Wof
Date: 11/18/2021

Description:
    The program generates a solo Wheel of Fortune game for the user. It consists
    of four rounds where phrases from the phrases.txt document are pulled for
    guessing.

Contributors:
    Name, login@purdue.edu [repeat for each]

My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""
'''LIBRARIES'''
import random as r

'''GLOBAL VARIABLES'''
global total # keeps track of round total
global letter # keeps track of letter guess
global correct # determines the end of the game
global allTotal # keeps track of game total
global choice # determines if user quits game
allTotal = 0
correct = 0
choice = 0

'''FUNCTIONS'''
# determines the value of the user's spin of the wheel
def spin_the_wheel():
    wheel = [500, 500, 500, 500, 550, 550, 600, 600, 600, 600, 650, 650, 650,
        700, 700, 800, 800, 900, 2500, 'BANKRUPT', 'BANKRUPT']
    spin = r.choice(wheel)
    return spin

# loads the phrases for all four rounds
def load_phrases():
    f = open('phrases.txt','r')
    words = f.readlines()
    noNew = [] # new line characters removed
    for i in range(len(words)):
        noNew.append(words[i].strip('\n'))
    f.close()
    return r.sample(noNew, len(noNew))

'''CLASSES'''
class Round(): # main class where game is played
    def __init__(self, phrase, round):
        # initialize global variables
        global total
        global correct
        global allTotal
        global choice
        total = 0
        correct = 0
        # initialize class instances
        self.blank = self.blank_phrase(phrase) # disguises phrase with blanks
        self.round = round
        self.vowels = 'AEIOU'
        self.consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
        self.num = 0
        # determine round and print statements to user
        while self.num != 4 and self.blank != phrase and correct != 1:
            print(f':: Solo WoF :::::::::::::::::::::::::::::: Round {self.round} of 4 ::')
            # WIDTH IS 56
            print(f'::{self.blank.center(54)}::')
            print(f'::::::::::::::::::::::::::::::::::::::::::::::::::::::::::')
            x = '{:,d}'.format(total)
            print(f'::{self.vowels.center(11)}::{self.consonants.center(27)}::'
                f"{'$'+x:>11} ::")
            print(f'::::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n')
            print('Menu:\n  1 - Spin the wheel.\n  2 - Buy a vowel.\n'
                '  3 - Solve the puzzle.\n  4 - Quit the game.\n')
            self.num = self.get_num()
            # case stricture to evaluate user guess
            if self.num == 1: # goes to class Option1()
                Option1(phrase, self.vowels, self.consonants)
                self.consonants, self.blank, self.vowels = self.contribute_letter(self.vowels,
                    self.consonants, phrase, self.blank, letter)
            elif self.num == 2: # goes to class Option2()
                Option2(phrase, self.vowels, self.consonants)
                self.consonants, self.blank, self.vowels = self.contribute_letter\
                (self.vowels, self.consonants, phrase, self.blank, letter)
            elif self.num == 3: # goes to class Option3()
                Option3(phrase, self.vowels, self.consonants, self.blank)
            elif self.num == 4: # quits game
                total = 0
                choice = 'quit'
        print(f'\nYou earned ${total:,d} this round.\n')
        allTotal += total
    # determines if user's choice is valid
    def get_num(self):
        num = str(input('Enter the number of your choice: '))
        while num not in ['1', '2', '3', '4']:
            print(f'"{num}" is an invalid choice.\n')
            print('Menu:\n  1 - Spin the Wheel.\n  2 - Buy a vowel.\n'
                '  3 - Solve the puzzle.\n  4 - Quit the game.\n')
            num = str(input('Enter the number of your choice: '))
        return int(num)

    # disguises the phrase into a blank version
    def blank_phrase(self, phrase):
        spaced = []
        for i in range(len(phrase)):
            if phrase[i].isalpha():
                spaced.append('_')
            else:
                spaced.append(phrase[i])
        return ('').join(spaced)

    def contribute_letter(self, vows, cons, phrase, blank, letter):
        newCons = []
        for i in range(len(cons)):
            if cons[i].lower() == letter:
                newCons.append(' ')
            else:
                newCons.append(cons[i])
        newPhrase = []
        for i in range(len(phrase)):
            if phrase[i].lower() == letter:
                newPhrase.append(letter.upper())
            else:
                newPhrase.append(blank[i])
        newVows = []
        for i in range(len(vows)):
            if vows[i].lower() == letter:
                newVows.append(' ')
            else:
                newVows.append(vows[i])

        return ''.join(newCons), ''.join(newPhrase), ''.join(newVows)

class Option1(): # user guesses for consonants
    def __init__(self, phrase, vows, cons):
        global total
        global letter
        if cons == '                     ': # if empty string, user doesn't guess
            print('There are no more consonants to choose.\n')
        else: # determine user's spin on wheel
            self.wheel = str(spin_the_wheel())
            if self.wheel.isalpha():
                print(f'The wheel landed on {self.wheel}.')
            else:
                #y = '{:,d}'.format(total)
                print(f'The wheel landed on ${int(self.wheel):,d}.')

            # retrieve a letter guess from the user
            if self.wheel == 'BANKRUPT':
                print(f'You lost ${total:,d}!\n')
                total = 0
                letter = '0'
            else: # determine if user guess is valid
                self.guess = str(input('Pick a consonant: '))
                while not self.guess.isalpha() or len(self.guess)>1 or\
                self.guess.upper() in vows or self.guess.upper() not in cons:
                    if len(self.guess)>1 or self.guess == '':
                        print('Please enter exactly one character.')
                    elif not self.guess.isalpha():
                        print(f'The character {self.guess} is not a letter.')
                    elif self.guess.upper() in 'AEIOU':
                        print('Vowels must be purchased.')
                    elif self.guess.upper() not in cons:
                        print(f'The letter {self.guess.upper()} has already been used.')
                    self.guess = str(input('Pick a consonant: '))

                # check if guess is in phrase
                if self.guess.lower() in phrase.lower():
                    # determine amount user earn's with correct guess
                    if phrase.lower().count(self.guess.lower()) > 1:
                        self.earnings = phrase.lower().count(self.guess.lower()) * int(self.wheel)
                        print(f"There are {phrase.lower().count(self.guess.lower())}"
                            f" {self.guess.upper()}'s, which earns you "
                            f"${self.earnings:,d}.\n")
                    else: # handle incorrect guess
                        self.earnings = int(phrase.lower().count(self.guess.lower())) * self.wheel
                        print(f"There is {phrase.lower().count(self.guess.lower())}"
                            f" {self.guess.upper()}, which earns you "
                            f"${int(self.wheel):,d}.\n")
                    letter = self.guess.lower()
                    total += int(self.earnings)
                elif self.guess.lower() not in phrase.lower():
                    print(f"I'm sorry, there are no {self.guess.upper()}'s.\n")
                    total += 0
                    letter = self.guess.lower()

class Option2(): # user guesses for vowels
    def __init__(self, phrase, vows, cons):
        global letter
        global total
        # check input
        if total < 275: # needs at least $275 to guess vowels
            print('You need at least $275 to buy a vowel.\n')
            letter = '0'
        elif vows == '     ':
            print('There are no more vowels to buy.\n')
        else: # user guesses vowels
            self.vowguess = str(input('Pick a vowel: '))
            # determine if user guess is valid
            while not self.vowguess.isalpha() or len(self.vowguess)>1 or\
            self.vowguess.upper() in cons or self.vowguess.upper() not in vows:
                if len(self.vowguess)>1 or self.vowguess == '':
                    print('Please enter exactly one character.')
                elif not self.vowguess.isalpha():
                    print(f'The character {self.vowguess} is not a letter.')
                elif self.vowguess.upper() in 'BCDFGHJKLMNPQRSTVWXYZ':
                    print('Consonants cannot be purchased.')
                elif self.vowguess.upper() not in vows:
                    print(f'The letter {self.vowguess.upper()} has already been purchased.')
                self.vowguess = str(input('Pick a vowel: '))
            # determine if user guess is in phrase
            if self.vowguess.lower() in phrase.lower():
                if phrase.lower().count(self.vowguess.lower()) > 1:
                    print(f"There are {phrase.lower().count(self.vowguess.lower())}"
                        f" {self.vowguess.upper()}'s.\n")
                else:
                    print(f"There is {phrase.lower().count(self.vowguess.lower())}"
                        f" {self.vowguess.upper()}.\n")
                letter = self.vowguess.lower()
                total -= 275
            elif self.vowguess.lower() not in phrase.lower():
                print(f"I'm sorry, there are no {self.vowguess.upper()}'s.\n")
                total -= 275
                letter = self.vowguess.lower()

class Option3(): # determines if the user has the correct solution
    def __init__(self, phrase, vows, cons, blank):
        global total
        global correct
        print('Enter your solution.')
        print(f'  Clues: {blank}')
        self.user = str(input('  Guess: '))

        if self.user.lower() == phrase.lower(): # correct solution
            print('Ladies and gentlemen, we have a winner!')
            correct = 1
            if total < 1000: # user's total becomes $1000 if they have less
                total = 1000
        else:
            print(f"I'm sorry. The correct solution was:\n{phrase.upper()}")
            total = 0 # user's total is 0 if they guess incorrectly
            correct = 1


'''MAIN'''
def main():
    global total # keeps track of round total
    global letter # keeps track of letter guess
    global correct # determines the end of the game
    global allTotal # keeps track of game total
    global choice # determines if user quits game
    allTotal = 0
    correct = 0
    choice = 0
    
    # introduce the user to the game
    print('Welcome to Solo Wheel of Fortune!\n')
    phrases = load_phrases() # call the random phrases used in the game

    # send the game to the classes to play
    for i in [1,2,3,4]:
        Round(phrases[i-1], i)
        if choice == 'quit':
            break
    print(f'Thanks for playing!')
    print(f'You earned a total of ${allTotal:,d}.')

if __name__ == '__main__':
    main()
