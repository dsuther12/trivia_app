import requests
import random
import html

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

def displayCorrectAnswer(correctAnswer):
    print("The correct answer is: " + correctAnswer)
    

def playTrivia():
    response = requests.get("https://opentdb.com/api.php?amount=10")
    questionList = response.json()['results']

    print("-------------------------------------------------------------")
    print("See how many of these 10 trivia questions you can get right!")
    print("-------------------------------------------------------------")

    correctCount = 0
    incorrectCount = 0
    
    for question in questionList:
        answersList = question['incorrect_answers']
        correctAnswer = question['correct_answer']
        answersList.append(question['correct_answer'])
        random.shuffle(answersList)            
        print("\033[1mCategory: \033[0m" + html.unescape(question['category']))
        print("\033[1mQuestion: \033[0m" + html.unescape(question['question']) + "\n")
        answers = answerLayout(answersList, question['type'])

        for k, v in answers.items():
            print(k + ". " + v)
            if v == question['correct_answer']:
                userCorrectAnswer = k

        print("\n")
        print("Which of these answers are correct? Choose wisely...")

        while True:
            userAnswer = input()

            if userAnswer == userCorrectAnswer:
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
                print("Please type the letter corresponding to the answer you want to choose")

    print("Here are your results!")
    print("Correct: " + str(correctCount))
    print("Incorrect: " + str(incorrectCount))



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