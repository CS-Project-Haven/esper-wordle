
from random import randint

def getWordList(fileName):
  file = open(fileName,'r')
  rawDictionary = file.readlines()
  dictionary = [word[:-1] for word in rawDictionary]
  file.close()
  return dictionary
allWords = getWordList('dictionary.csv')

def selectRandomWord():
  wordIndex = randint(0,len(allWords)-1)
  selectedWord = allWords[wordIndex]
  return selectedWord

def clearScreen():
  print('\n'*50)

class game():
  def __init__(self): # START THE PROCEDURE
    self.success = False
    self.maxSlot = 6
    self.correctWord = selectRandomWord()
    self.botActive = False
    print()
    print('----------= ESPER WORDLE =----------')
    print()
    print('(Enter a number to adjust [maxSlot])')
    print('(Enter \'bot\' to set [botActive=True])')
    print()
    print('> Press ENTER to begin')
    response = input()
    print()
    if response.isnumeric():
      self.maxSlot = int(response)
      print(f'< - GAME STARTED : maxSlot={response} - >')
      self.playGame
    elif response == 'bot':
      print('< - GAME STARTED : botActive=True - >')
      self.botActive = True
    else:
      print('< - GAME STARTED - >')
    self.playGame()
    
  def playGame(self): # START THE GAME ITSELF
    self.guessData = []
    self.potentialWords = allWords
    for guessNumber in range(0,self.maxSlot):
      if self.botActive:
        attemptData = self.botGuess(guessNumber,self.potentialWords)
      else:
        attemptData = self.guess(guessNumber)
      self.guessData.append(attemptData)
      self.attemptedGuesses = guessNumber + 1
      if attemptData.guessedWord == 'x':
        break
      if self.checkCorrect(attemptData.guessedWord,self.correctWord):
        self.success = True
        break
    if self.success == False:
      print()
      print(f'Ans | {self.correctWord.upper()}')
    print()
    self.endGame()
  
  def endGame(self): # END THE GAME
    print('< - GAME COMPLETE - >')
    if self.success:
      print(' Success  :{0:>9}'.format('True'))
    else:
      print(' Success  :{0:>9}'.format('False'))
    print(f' Attempts :{self.attemptedGuesses:>9}')
    print()

  def checkCorrect(self,guessedWord,correctWord): # CHECKING GUESS ANSWER
    correctionCode = ['.','.','.','.','.']
    listGuessedWord = list(guessedWord)
    listCorrectWord = list(correctWord)
    for i in range(len(listGuessedWord)): # CHECK CORRECT LETTER + PLACEMENT
      if listGuessedWord[i] == correctWord[i]:
        self.assessWords(guessedWord,i,2)
        correctionCode[i] = '+'
        listGuessedWord[i] = '*'
        listCorrectWord[i] = '.'
      else:
        correctionCode[i] = ' '
    for i in range(len(listGuessedWord)): # CHECK CORRECT LETTER
      if listGuessedWord[i] in listCorrectWord:
        self.assessWords(guessedWord,i,1)
        correctLetter = listGuessedWord[i]
        listGuessedWord[i] = '*'
        correctionCode[i] = '-'
        listCorrectWord[listCorrectWord.index(correctLetter)] = '.'
    for i in range(len(guessedWord)): # (BOT) INVALIDATE INCORRECT LETTERS
      if guessedWord[i] not in correctWord:
        self.assessWords(guessedWord,i,0)
    correctionCode = ''.join(correctionCode)
    print((' '*6)+correctionCode)
    if guessedWord == correctWord:
      return True
    else:
      return False

  def assessWords(self,guessedWord,slot,placedCorrect): # FOR BOT TO CHECK ADJUST WORDS
    newPotentialWords = []
    letter = guessedWord[slot]
    if placedCorrect == 2: # ADJUST WORDS BASED ON CORRECT LETTER + PLACEMENT
      for word in self.potentialWords:
        if word[slot] == letter and word != guessedWord:
          newPotentialWords.append(word)
    elif placedCorrect == 1: # ADJUST WORDS BASED ON CORRECT LETTER
      for word in self.potentialWords:
        if letter in word and word != guessedWord:
          newPotentialWords.append(word)
    elif placedCorrect == 0: # ADJUST WORDS BASED ON WRONG LETTER
      for word in self.potentialWords:
        if letter not in word:
          newPotentialWords.append(word)
    self.potentialWords = newPotentialWords

  def getData(self,desiredData): # RETRIEVE DATA ON A GAME (unnecessary but cool)
    try:
      return eval(f'self.{desiredData}')
    except:
      try:
        data = []
        for guess in self.guessData:
          data.append(eval(f'guess.{desiredData}'))
        return data
      except:
        return None
  

  class guess(): # GUESS OBJECT
    
    def __init__(self,guessNumber): # GUESSING PROCEDURE
      validGuess = False
      self.invalidInputs = 0
      print()
      while validGuess == False:
        try:
          self.guessedWord = input(f'{guessNumber+1:>3} | ').lower()
          if self.guessedWord.isalpha() == False:
            raise Exception()
          if len(self.guessedWord) != 5 and self.guessedWord != 'x':
            raise Exception()
          elif self.guessedWord not in allWords and self.guessedWord != 'x':
            raise Exception()
          validGuess = True
        except:
          self.invalidInputs += 1
          print('- Invalid input -')
          print()

  class botGuess(): # GUESS OBJECT (BOT)
    
    def __init__(self,guessNumber,potentialWords): # GUESSING PROCEDURE (BOT)
      print()
      maxWordValue = len(potentialWords)-1
      self.guessedWord = potentialWords[randint(0,maxWordValue)]
      print(f'{guessNumber+1:>3} | {self.guessedWord}')


def playLoop():
  # Loop playing the game until x is inputted post-game
  # games is a list with a history of previous games in this running of the program
  global games
  games = []
  playing = True
  while playing==True:
    currentGame = game()
    games.append(currentGame)
    pause = input('>')
    if pause == 'x':
      break
playLoop()
# Loop can be started again by callng playLoop()

def filterWords():
  allWords = getWordList('aqawords.txt')
  filteredWords = []
  for word in allWords:
    if len(word) == 5:
      filteredWords.append(word.lower()+'\n')
  newfile = open('dictionary.csv','w')
  newfile.writelines(filteredWords)
  newfile.close()