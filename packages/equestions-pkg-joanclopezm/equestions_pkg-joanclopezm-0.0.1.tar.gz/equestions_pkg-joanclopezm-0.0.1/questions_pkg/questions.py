import random

class Questions:

    def Bunch_of_questions(self, question_number):
        questions=['Little interest or pleasure in doing things',
        'Feeling down, depressed, or hopeless','Trouble falling or staying asleep, or sleeping too much',
        'Feeling tired or having little energy','Poor appetite or overeating',
        'Feeling bad about yourself - or that you are a failure or have let yourself or your family down',
        'Trouble concentrating on things, such as reading the newspaper or watching television',
        'Moving or speaking so slowly that other people could have noticed Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual',
        'Thoughts that you would be better off dead, or of hurting yourself',
        'If you checked off any problems, how difficult have these problems made it for you at work, home, or with other people',
        'I feel sad.','I feel agitated or restless (I pace, am unable to stay calm, or need to move constantly).','I feel worn out.',
        'I feel so guilty that I can barely take it.','When I wake up in the morning, I feel like there is nothing to look forward to.',
        'I think about death.','When needed, I can make up my mind quickly.','I get mad at myself if I do not achieve the goals I have set out to reach.'
        'When something is bothering me, I cannot stop thinking about it.']
        print(len(questions))
        return questions[question_number]

#select 10 random questions from our bunch of questions
    def Select_Questions(self):
        selected_questions=[]
        print(type(random))  
        for x in range(10):
            number = random.randint(0, 17)
            selected_questions.append(self.Bunch_of_questions(number))
        
        return selected_questions
        
    
    def Calculate_Depression(self, array_results):
        count_of_yes = [s for s in array_results if "Yes" in s]
        result= 'You are no depressed'
        if(len(count_of_yes) > 5) :
            result = 'You are depressed, ask for help'
        
        if(len(count_of_yes) > 8) :
            result = 'Your response to this questions indicates that you may be at risk of harming yourself or someone else. If you are in need of immediate assistance'
       
        return result
    
if __name__ == '__main__':
    test = Questions()
    results = ['Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','Yes','No']
    questions = test.Select_Questions()
    print(questions)
    print('Number of questions {}'.format(len(questions)))
    
    print('\n Resutlt of test \n {}'.format(test.Calculate_Depression(results)))
 