alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

direction = input("Type 'encode' to encrypt, type 'decode' to decrypt:\n").lower()
text = input("Type your message:\n").lower()
shift = int(input("Type the shift number:\n"))

def caesar(original_text, shift_amount, cipher_direction):
    result_text = ""
    for letter in original_text:
        if cipher_direction == "encode":
            shifted_position = alphabet.index(letter) + shift_amount
            shifted_position %= len(alphabet)
            result_text += alphabet[shifted_position]
        else:
            shifted_position = alphabet.index(letter) - shift_amount
            result_text += alphabet[shifted_position]
    print(f"Here is the {cipher_direction}d result: {result_text}")

caesar(text, shift, direction)