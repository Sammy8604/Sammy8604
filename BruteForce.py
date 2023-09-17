import time, itertools, string

chars = string.ascii_letters + string.digits + string.punctuation
guess = ""
passw = ("Enter a password:")
for i in range(0, len(passw)):
    time.sleep(0.04)
    print(passw[i], end="", flush=True)
password = input("\n")
num = 0
count = 1
found = False
for i in range(0, len(password)):
    if password[i] == "" or password[i] == " ":
        run = False
        break
    else:
        run = True

if run == False:
    print("Not valid password")
    exit()
else:
    ques = ("Do you want to print the working out?\n1=Yes\n2=No\nNote its slower to print:")
    for i in range(0, len(ques)):
        time.sleep(0.04)
        print(ques[i], end="", flush=True)

    question = int(input("\n"))
    start = time.time()
    if question == 1:
        while found == False:
            num = num + 1
            for char in itertools.product(chars, repeat=num):
                guess = "".join(char)
                print(guess)
                if guess == password:
                    found = True
                    break
                count += 1

    elif question == 2:
        while found == False:
            num = num + 1
            for char in itertools.product(chars, repeat=num):
                guess = "".join(char)
                if guess == password:
                    found = True
                    break
                count += 1

    else:
        print("invalid input")

end = time.time()
print("The password was found in", count, "guesses")
print("Time was", end - start, "seconds")