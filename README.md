# Daily Words

Daily Words is a chrome extension designed to make learning vocabulary as fun and convenient as possible. Source your own learning material and have translations 
sent to your phone or email every single day.

### Configuring your settings

1) Click on the extension icon in the top right of your browser, then click the three dots next to Daily Words, and then select "options".
2) When a menu pops up, select where you would like to receive your translations daily. You may choose email, phone, or both. If you would like words to
be sent to your phone, please include your phone number in the input box that will appear upon selecting "phone". You may also indicate how many translations you would like to be sent per day.
![alt text](https://github.com/bcvance/DailyWords/blob/development/media/options.gif)


3) Google may ask for authentication as shown below. This is necessary for the extension to have access to your email address and identify the account being used.  
![alt text](https://github.com/bcvance/DailyWords/blob/development/media/daily_words_authentication.png)

#### In the Works
Currently words are sent based on a FIFO (first in first out) queue pattern. That is, the least recently seen words will be sent to your phone or email before
more recent ones. Upon receiving a translation, it gets cycled back to the end of the queue. Currently, a spaced repetition option is in development as well. 
This option would enable users to provide feedback regarding ease of recall for each translation, which would alter the wait time before next review of that word accordingly.

### Using the extension:
1) Install the extension from the Chrome Web Store (extension not yet published)
2) Navigate to article in foreign language of your choosing.
3) Activate the extension by clicking the extension icon in the top right of your browser, clicking on "Daily Words" and then "activate".  
![alt text](https://github.com/bcvance/DailyWords/blob/development/media/activate.gif)

4) Click on a word or highlight an entire phrase to get a translation. Translations are done using the DeepL API.  
5) To save your translation, click "Save This Word" to save it to the database.  
![alt text](https://github.com/bcvance/DailyWords/blob/development/media/translate_demonstration.gif)
6) When you are done reading, repeat step 3 to deactivate the extension.


## Receiving words
Words will be sent directly to the number provided in your extension options at the indicated time/s.  
![alt text](https://github.com/bcvance/DailyWords/blob/development/media/texts_resized.gif)
