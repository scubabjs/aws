user_input = "This\nstring has\tsome whitespaces...\r\n"

character_map = {
    ord('\n'): ' ',
    ord('\t'): ' ',
    ord('\r'): None
}
user_input.translate(character_map)  # This string has some whitespaces... "
