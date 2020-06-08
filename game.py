from random import randint

score = None

prompt = "> "

all_options = tuple(["sponge", "paper", "air", "water", "dragon", "devil",
                     "lightning", "gun", "rock", "fire", "scissors", "snake",
                     "human", "tree", "wolf"])

area = len(all_options) // 2

win_dict = {}
lose_dict = {}


def main():

    print("Enter your name:")

    name = input(prompt)

    rating = open("rating.txt", encoding='utf-8')

    global score

    score = find_score(rating, name)

    rewind(rating)

    score_list = rating.readlines()

    rating.close()

    print(f"Hello, {name}")

    while True:

        print("Enter the options:")
        options = input(prompt)

        if options:

            options = tuple(x.strip() for x in options.split(","))

        else:

            options = tuple(["rock", "paper", "scissors"])

            break

        if win_dict_assign(options):

            break

    print("Okay, let's start")

    lose_dict_assign(options)

    while True:

        move = input(prompt).strip()
        computer = options[randint(0, len(options) - 1)]

        if move == "!rating":

            print(f"Your rating: {score}")

        elif move == "!exit":

            print("Bye!")
            break

        elif move in win_dict[computer]:

            print(f"Sorry, but computer chose {computer}")

        elif move in lose_dict[computer]:

            score += 100
            print(f"Well done. Computer chose {computer} and failed")

        elif move == computer:

            score += 50
            print(f"There is a draw ({computer})")

        else:

            print("Invalid input")

    rating = open("rating.txt", mode="w", encoding="utf-8")

    write_score(rating, score_list, score, name)

    rating.close()


def rewind(file):

    file.seek(0)


def write_score(rating, score_list, score, name):

    flag = False

    for line in score_list:

        if name in line:

            index = score_list.index(line)

            score_list[index] = name + " " + str(score) + "\n"

            flag = True

            break

    if not flag:

        score_list.append(name + " " + str(score) + "\n")

    rating.write("".join(score_list))


def win_dict_assign(options):

    global win_dict
    global all_options
    global area

    for option in options:

        try:

            index = all_options.index(option)

        except ValueError:

            print("Wrong option! Take a look at options.jpg.")

            return False

        if index + area < len(all_options):

            win_dict[option] = set(all_options[index+1:index+area+1])

        else:

            last = area - (len(all_options) - index - 1)

            win_dict[option] = set(all_options[index+1:] + all_options[:last])
            # list concatenation

    return True


def lose_dict_assign(options):

    global lose_dict
    global all_options
    global area

    for option in options:

        index = all_options.index(option)

        if index - area >= 0:

            lose_dict[option] = set(all_options[index-1:index-area-1:-1])

        else:

            last = area - index

            lose_dict[option] = set(all_options[:index]
                                    + all_options[len(all_options)-last:])


def find_score(file, name):

    for line in file:

        if name in line:

            return int(line.strip().strip(name).strip())

    return 0


main()
