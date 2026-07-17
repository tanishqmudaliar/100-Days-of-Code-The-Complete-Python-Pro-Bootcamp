#TODO: Create a letter using starting_letter.txt 
#for each name in invited_names.txt
#Replace the [name] placeholder with the actual name.
#Save the letters in the folder "ReadyToSend".
    
#Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
    #Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
        #Hint3: This method will help you: https://www.w3schools.com/python/ref_string_strip.asp

with open("Input/Letters/starting_letter.txt", "r") as file:
    letter = file.read()

with open("Input/Names/invited_names.txt", "r") as file:
    list_of_names = file.read()

names = list_of_names.split("\n")

for name in names:
    output = letter.replace("[name]", name)
    with open(f"Output/ReadyToSend/letter_for_{name}.txt", "w") as mail:
        mail.write(output)