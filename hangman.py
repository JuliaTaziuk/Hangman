# Problem Set 2, hangman.py
# Name: Yuliia Taziuk
# Collaborators: None
# Time spent: ~ 12-14 hours

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    secret_word_letters = set(secret_word)
    letters_guessed_set = set(letters_guessed)

    if letters_guessed_set == secret_word_letters:
      return True
    else:
      return False
    


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    secret_word_lst = list(secret_word)
    
    for e in range(len(secret_word)):
      if secret_word_lst[e] not in letters_guessed:
        secret_word_lst[e] = "_ "
        
    return "".join(secret_word_lst)

            

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet = set(string.ascii_lowercase)
    letters_guessed_set = set(letters_guessed)
    not_guessed = alphabet - letters_guessed_set

    return ''.join(not_guessed)



def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    '''
    #consts
    guesses = 6
    warnings = 3
    letters_guessed = []
    vowels = {"a", "e", "o", "i", "u"}
    #----------------------------------
    while guesses>0 and not is_word_guessed(secret_word, letters_guessed):

      print (f'You have {guesses} guesses left.')
      print (f'Avaible letters: {get_available_letters(letters_guessed)}')
      
      letter = input('Please guess a letter: ' ).strip(' ').lower()

      if letter in letters_guessed:
        if warnings > 0:
          warnings -= 1
          print (f'Oops! You have already guessed that letter. You have {warnings} warnings left:\n{get_guessed_word(secret_word, letters_guessed)}')
          print ("-" * 30)
        elif warnings == 0:
          guesses -= 1
          print (f'Oops! You have already guessed that letter. Unfortunately, you lose a guess:\n{get_guessed_word(secret_word, letters_guessed)}')
          print ("-" * 30)

      elif not letter.isalpha() or len(letter) != 1:
        if warnings > 0:
          warnings -= 1
          print (f'Oops! That is not a valid letter. You have {warnings} warnings left:\n{get_guessed_word(secret_word, letters_guessed)}')
        elif warnings == 0:
          guesses -= 1
          print (f'Oops! That is not a valid letter. You have zero warnings left. Unfortunately, you lose a guess:\n{get_guessed_word(secret_word, letters_guessed)}')

      else:
        letters_guessed.append(letter)
        if letter not in secret_word:
          print (f'Oops! That letter is not in my word:\n{get_guessed_word(secret_word, letters_guessed)}')
          print ("-" * 30)
          if letter in vowels:
            guesses -= 1
          guesses -= 1
        else:
          print (f'Good guess:\n{get_guessed_word(secret_word, letters_guessed)}')
          print ("-" * 30)
          

    if guesses == 0:
      print (f'Sorry, you ran out of guesses. The word was {secret_word}')

    if is_word_guessed(secret_word, letters_guessed):
      print (f'Congratulations, you won! Your total score for this game is: {guesses * len(set(secret_word))}')
  


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    if len(my_word) == len(other_word):
        my_word_set = set(my_word)

        for i in range(len(my_word)):
            if my_word[i] == '_':
                if other_word[i] in my_word_set:
                    return False
            elif my_word[i] != other_word[i]:
                return False
        return True
    return False




def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    words = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            words.append(word)
    if len(words) == 0:
        print("No matches found!")
    else:
        words_str = str(words)
        res = words_str.replace("'", "")
        print(f'Possible word matches are: {res}')



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    '''
    guesses = 6
    warnings = 3
    letters_guessed = []
    vowels = {"a", "e", "o", "i", "u"}
    #-----------------------------------
    while guesses>0 and not is_word_guessed(secret_word, letters_guessed):

      print (f'You have {guesses} guesses left.')
      print (f'Avaible letters: {get_available_letters(letters_guessed)}')
      
      letter = input('Please guess a letter: ' ).strip(' ').lower()

      if letter == '*':
        show_possible_matches(get_guessed_word(secret_word, letters_guessed).replace(" ", ""))

      elif letter in letters_guessed:
        if warnings > 0:
          warnings -= 1
          print (f'Oops! You have already guessed that letter. You have {warnings} warnings left:\n{get_guessed_word(secret_word, letters_guessed)}')
          print ("-" * 30)
        elif warnings == 0:
          guesses -= 1
          print (f'Oops! You have already guessed that letter. Unfortunately, you lose a guess:\n{get_guessed_word(secret_word, letters_guessed)}')
          print ("-" * 30)

      elif not letter.isalpha() or len(letter) != 1:
        if warnings > 0:
          warnings -= 1
          print (f'Oops! That is not a valid letter. You have {warnings} warnings left:\n{get_guessed_word(secret_word, letters_guessed)}')
        elif warnings == 0:
          guesses -= 1
          print (f'Oops! That is not a valid letter. You have zero warnings left. Unfortunately, you lose a guess:\n{get_guessed_word(secret_word, letters_guessed)}')

      else:
        letters_guessed.append(letter)
        if letter not in secret_word:
          print (f'Oops! That letter is not in my word:\n{get_guessed_word(secret_word, letters_guessed)}')
          print ("-" * 30)
          if letter in vowels:
            guesses -= 1
          guesses -= 1
        else:
          print (f'Good guess:\n{get_guessed_word(secret_word, letters_guessed)}')
          print ("-" * 30)
          

    if guesses == 0:
      print (f'Sorry, you ran out of guesses. The word was {secret_word}')

    if is_word_guessed(secret_word, letters_guessed):
      print (f'Congratulations, you won! Your total score for this game is: {guesses * len(set(secret_word))}')




if __name__ == "__main__":
    
    secret_word = choose_word(wordlist)
    print (f'Welcome to the game Hangman!\nI am thinking of a word that is {len(secret_word)} letters long.')
    print (f'{"_ " * len(secret_word)}')
    
    ext = input('Do you want to enable hints? If yes, enter any number; otherwise, enter any other symbol:\t')
    if ext.isnumeric():
      hangman_with_hints(secret_word)
    else:
      hangman(secret_word)
    
    
