import PyQuest


if __name__ == '__main__':
    quest1 = PyQuest.PyQuest(config="demo.json")
    quest1.start()

    answer = quest1.get_furthest_answer()

    print(f"You selected {answer.get_viewable_text()}")
