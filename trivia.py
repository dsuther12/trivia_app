import requests
import random
import html

# Formats how answers will be displayed based on if it is a MC or boolean question
def answerLayout(answerList, questionType):
    if questionType == "multiple":
        answerDict = {
            "a": html.unescape(answerList[0]),
            "b": html.unescape(answerList[1]),
            "c": html.unescape(answerList[2]),
            "d": html.unescape(answerList[3]),
        }
    elif questionType == "boolean":
        answerDict = {
            "a": answerList[0],
            "b": answerList[1]
        } 
    return answerDict

# Displays correct answer to question
def displayCorrectAnswer(correctAnswer):
    print("The correct answer is: " + correctAnswer)

# Display answers that users get to choose from based on the question
def displayAnswers(question, answers, correctCount, incorrectCount):
    userCorrectAnswer = None
    for k, v in answers.items():
            print(f"{k}. {v}")
            if html.unescape(v) == html.unescape(question['correct_answer']):
                userCorrectAnswer = k

    if userCorrectAnswer is None:
         print("\033[31mError: No correct answer found!\033[0m") 
         return correctCount, incorrectCount

    print("\n")
    print("Which of these answers are correct? Choose wisely...")
    return collectUserInput(userCorrectAnswer, answers, question, correctCount, incorrectCount)


# Logic for when the user inputs their answer to a question
def collectUserInput(correctAnswer, answers, question, correctCount, incorrectCount):
    while True:
        userAnswer = input()

        if userAnswer == correctAnswer:
            print("\033[32mNicely done!\033[0m")
            print("-----------------------------------------------------------------------")
            correctCount += 1
            break
        elif userAnswer in answers:
            print("\033[31mSorry wrong answer!\033[0m")
            displayCorrectAnswer(question['correct_answer'])
            print("-----------------------------------------------------------------------")
            incorrectCount += 1
            break
        else:
            print("\033[31mPlease type the letter corresponding to the answer you want to choose\033[0m")

    return correctCount, incorrectCount


# Calls trivia API and begins game
def playTrivia():

    correctCount, incorrectCount = 0, 0

    response = requests.get("https://opentdb.com/api.php?amount=10")
    questionList = response.json()['results']

    print("-------------------------------------------------------------")
    print("See how many of these 10 trivia questions you can get right!")
    print("-------------------------------------------------------------")
    
    for question in questionList:
        answersList = question['incorrect_answers']
        answersList.append(question['correct_answer'])
        random.shuffle(answersList)            
        print("\033[1mCategory: \033[0m" + html.unescape(question['category']))
        print("\033[1mQuestion: \033[0m" + html.unescape(question['question']) + "\n")
        answers = answerLayout(answersList, question['type'])

        correctCount, incorrectCount = displayAnswers(question, answers, correctCount, incorrectCount)

    print("\033[1mHere are your results!\033[0m")
    print("\033[32mCorrect: \033[0m" + str(correctCount))
    print("\033[31mIncorrect: \033[0m" + str(incorrectCount))

        



print("Would you like to play trivia? Yes or No?")

while True:
    answer = input().lower()
    if answer == "yes" or answer == "y":
        playTrivia()
        break
    elif answer == "no" or answer == "n":
        print("Awwww u lame af")
        break
    else:
        print("Please enter yes or no")