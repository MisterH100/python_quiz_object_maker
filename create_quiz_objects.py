import json
import random
import uuid
#import pymongo
#client = pymongo.MongoClient("")
#database = client[""]
#collection = database[""]

class QuestionsObject:
    def __init__(self, question, correctAns,incorrectAnsList):
        self.question = question
        self.correctAns = correctAns
        self.incorrectAnsList = incorrectAnsList

class AnswersObject:
    def __init__(self,id:int,name:str):
        self.id = id
        self.name = name

class QuizObject:
    def __init__(self,id,question:str,answers:list[AnswersObject],correctAnswer:str,points:int,answered:bool,answer:str):
        self.id = id
        self.question = question
        self.answers = answers
        self.correctAnswer = correctAnswer
        self.points = points
        self.answered = answered
        self.answer = answer

inputTextFile = str
outputJSONFile = str
quizzes = []
pointsList = [50,80,100]
questionsList =[]
correctAnsList=[]
questionsObjectList =[]
wrongAnsList =[]
def createQuestionObject(questionText:str,correctText:str,incorrectList:list[str]):
    global question
    global correctAnswerName
    global correctAnswerObject
    global points
    answers = []
    randomIndex = random.randint(0,2)
    question = questionText
    points = pointsList[randomIndex]
    correctAnswerObject = AnswersObject(str(uuid.uuid4()),correctText)
    correctAnswerName = correctAnswerObject.name
    for i in range(2):
        wrongAnswerObject= AnswersObject(str(uuid.uuid4()),incorrectList[i])      
        answers.append(wrongAnswerObject.__dict__)
    answers.insert(randomIndex,correctAnswerObject.__dict__)
    quizObject = QuizObject(str(uuid.uuid4()),question,answers,correctAnswerName,points,False,"")
    quizzes.append(quizObject.__dict__)


def readTextFile(filepath:str):
    try:
        with open(filepath,"r") as text_file:
            for line in text_file:
                cleanQuestion = str(line).split("?",len(line))[0].strip()
                questionsList.append(cleanQuestion)
                cleanAnswer = str(line).split("?")[1].split("[")[0].strip()
                correctAnsList.append(cleanAnswer)
                cleanIncorrectAns = str(line).split("[")[1].split("]")[0].strip()
                incorrectOne =  cleanIncorrectAns.split(",")[0].strip()
                incorrectTwo =  cleanIncorrectAns.split(",")[1].strip()
                incorrectList = [incorrectOne,incorrectTwo]
                wrongAnsList.append(incorrectList)

            for i in range(len(questionsList)):
                questionsObjectList.append(QuestionsObject(questionsList[i],correctAnsList[i],wrongAnsList[i]).__dict__)
    except FileNotFoundError:
        print(filepath + " File not found")
        fileInputs()

def writeJSONFile(filepath:str):
    with open(filepath, "w") as outfile:
        quizzesJSON = json.dumps(quizzes)
        outfile.write(quizzesJSON)
        
def fileInputs():
    global inputTextFile
    global outputJSONFile
    inputText = str(input("Enter input file path .txt*"))
    inputTextFile =inputText.strip()
    if ".txt" not in inputTextFile:
        print("file extension required")
        fileInputs()
    
    inputText = str(input("Enter output file path .json*"))
    outputJSONFile =inputText.strip()
    if ".json" not in outputJSONFile:
        print("file extension required")
        fileInputs()
    
if __name__ == '__main__':
    fileInputs()
    readTextFile(inputTextFile)
    for i in range(len(questionsObjectList)):  
        createQuestionObject(questionsObjectList[i]["question"],questionsObjectList[i]["correctAns"],questionsObjectList[i]["incorrectAnsList"])
    writeJSONFile(outputJSONFile)

