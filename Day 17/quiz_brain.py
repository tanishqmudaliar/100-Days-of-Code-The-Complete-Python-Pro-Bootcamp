class QuizBrain:
    def __init__(self, question_bank):
        self.question_number = 0
        self.question_list = question_bank
        self.score = 0

    def next_question(self):
        question = self.question_list[self.question_number]
        self.question_number += 1
        answer = input(f"Q{self.question_number}: {question.question} (True/False)")
        self.check_answer(answer, question.answer)

    def still_has_questions(self):
        return len(self.question_list) > self.question_number

    def check_answer(self, received_answer, correct_answer):
        if received_answer.lower() == correct_answer.lower():
            print("Yayyyy!")
            self.score += 1
        else:
            print("Incorrect!")
            print("Correct answer: ", correct_answer)
        print(f"Your Current Score is: {self.score}/{self.question_number}\n")