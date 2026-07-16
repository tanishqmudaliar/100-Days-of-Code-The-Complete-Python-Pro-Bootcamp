alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))

def encrypt(original_text, shift_amount):
    original_text = original_text.lower()
    output_text = []
    for letter in original_text:
        if letter in alphabet:
            total_length = len(alphabet)
            pos = alphabet.index(letter) + shift_amount
            if pos > (total_length - 1):
                pos = pos - total_length
            output_text.append(alphabet[pos])
        else:
            print("Only alphabets are allowed!")
    output_text = ''.join(output_text)
    print(f"Here is the encoded result: {output_text}")

encrypt(text, shift)