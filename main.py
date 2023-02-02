
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
    print()
    print('----------= ESPER WORDLE =----------')
    print()
    print('> Press ENTER to begin')
    response = input()
    print()
    if response.isnumeric():
      self.maxSlot = int(response)
      print(f'< - GAME STARTED : maxSlot={response} - >')
    else:
      print('< - GAME STARTED - >')
    self.playGame()
    
  def playGame(self): # START THE GAME ITSELF
    self.guessData = []
    for guessNumber in range(0,self.maxSlot):
      attemptData = self.guess(guessNumber)
      self.guessData.append(attemptData)
      self.attemptedGuesses = guessNumber + 1
      if attemptData.checkCorrect(self.correctWord):
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
          if len(self.guessedWord) != 5:
            raise Exception()
          elif self.guessedWord not in allWords:
            raise Exception()
          validGuess = True
        except:
          self.invalidInputs += 1
          print('- Invalid input -')
          print()

    def checkCorrect(self,correctWord): # CHECKING GUESS ANSWER
      correctionCode = ['.','.','.','.','.']
      listGuessedWord = list(self.guessedWord)
      listCorrectWord = list(correctWord)
      for i in range(len(listGuessedWord)):
        if listGuessedWord[i] == correctWord[i]:
          correctionCode[i] = '+'
          listGuessedWord[i] = '*'
          listCorrectWord[i] = '.'
        else:
          correctionCode[i] = ' '
      for i in range(len(listGuessedWord)):
        if listGuessedWord[i] in listCorrectWord:
          correctLetter = listGuessedWord[i]
          correctionCode[i] = '-'
          listCorrectWord[listCorrectWord.index(correctLetter)] = '.'

      correctionCode = ''.join(correctionCode)
      print((' '*6)+correctionCode)
        
      if self.guessedWord == correctWord:
        return True
      else:
        return False



def playLoop():
  # Loop playing the game until x is inputted post-game
  # games is a list with a history of previous games in this running of the program
  games = []
  playing = True
  while playing==True:
    currentGame = game()
    games.append(currentGame)
    pause = input()
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