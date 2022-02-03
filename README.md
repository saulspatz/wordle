This is a reimplementation of the wordle game at https://www.powerlanguage.co.uk/wordle/.  I've made three important changes.



1. Allow repeated game play instead of one game a day.
2. Allow word lengths greater than 5.
2. Introduce "extreme" mode of play.

As a consequence of the second point, I'm also allowing the user to configure the number of guesses.  While I think the original designer made a great choice in allowing 6 guesses for a 5-letter word, it will take experimentation to determine good choices for longer words.  Also, one might want to use this game to teach spelling to a child, and more guesses would be needed.

In hard mode, letters that are discovered to be in the word must be used in subsequent guesses, and letters that are found in particular places must be used in these places.  Extreme mode extend this.  Letters that are discovered to not be in the word may not be used in subsequent guesses, and letter that are discovered to not be in particular places may not be used in those places.  Also, when the exact number of a particular letter becomes known, that number must be used in every subsequent guess.  (For example, if there guess is "sever" and the first 'e' is colored yellow and the second red, we know there is exactly one 'e' in the word, and that it's not in the second or fourth position.)  In short, no guess may be made if it contradicts the evidence accumulated so far.



During play, it is permitted to downgrade from extreme mode to hard mode or normal mode, or from hard mode to normal mode, but not to upgrade.



This is very much a work in progress.  In particular, I haven't generated the word lists for lengths greater than 5.  I've downloaded the Big English Word Lists from https://www.keithv.com/software/wlist/index.php, and I'm working on it.  





