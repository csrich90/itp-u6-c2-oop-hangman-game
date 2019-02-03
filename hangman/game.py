from .exceptions import *
import random


class GuessAttempt(object):        
    def __init__(self, letter, hit = None, miss = None):
        if hit == miss:
            raise InvalidGuessAttempt
        if hit is not None:
            self._hit = hit
            self._miss = not hit
        else:
            self._hit = not miss
            self._miss = miss
        
    def is_hit(self):
        return self._hit
        
    def is_miss(self):
         return self._miss

class GuessWord(object):
    
    def __init__(self, word):
        self.answer = word
        self.masked = self._mask_word(word)
        
    def perform_attempt(self, letter):
        new_word = ''
        new_word = self._uncover_word(self.answer, self.masked, letter)
        if self.masked != new_word:
            self.masked = new_word
            return GuessAttempt(letter,True,False)
        else:
            return GuessAttempt(letter,False,True)
      
    def _mask_word(self,word):
        if word:
            return '*' * len(word)
        else:
            raise InvalidWordException
            
    def _uncover_word(self,answer_word, masked_word, character):
        if not answer_word or len(answer_word) != len(masked_word):
            raise InvalidWordException
        if len(character) > 1:
            raise InvalidGuessedLetterException
        res = ''
        for index,letter in enumerate(answer_word.lower()):
            if letter.lower() == character.lower():
                res+= character.lower()
            else:
                res += masked_word[index]
        return res


class HangmanGame(object):
    
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self,word_list = WORD_LIST, number_of_guesses = 5):
        self.remaining_misses = number_of_guesses
        self.word_list = word_list
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(word_list))
        
    def guess(self,letter):
        if self.is_finished():
            raise GameFinishedException
        
        lower_letter = letter.lower()
        res = self.word.perform_attempt(lower_letter)
        self.previous_guesses.append(lower_letter)
        if res.is_miss():
            self.remaining_misses -= 1
        if self.is_won():
            raise GameWonException
        if self.is_lost():
            raise GameLostException
        
        return res
    
    def is_won(self):
        return self.word.answer == self.word.masked
    
    def is_lost(self):
        return self.remaining_misses < 1
    
    def is_finished(self):
        return self.is_lost() or self.is_won()
    
    @classmethod    
    def select_random_word(cls,list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException
        return list_of_words[random.randint(0,len(list_of_words) -1)]