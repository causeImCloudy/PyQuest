if __name__ == '__main__':
    letters = []

    while len(letters) <= 12:
        c = input("Enter a letter")
        letters.append(c)

        print(''.join(letters))

    print(f'Letters: "{letters}"')
