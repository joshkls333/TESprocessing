import os
import re
import matplotlib.pyplot as plt


def pathtraverse(root_dir, keyword):

    outputdictionary = {}

    bgdictionary = {}

    for root, dirs, files in os.walk(root_dir):
        rootcount = 0
        for filesearch in files:
            if re.match(keyword, filesearch):
                rootcount += 1
                print(os.path.join(root, filesearch))
            print(rootcount)

            outputdictionary[root] = rootcount

            if rootcount > 0:
                bgdictionary[root] = rootcount

    print(outputdictionary)

    plt.bar(range(len(bgdictionary)), bgdictionary.values(), align='center')
    plt.xticks(range(len(bgdictionary)), bgdictionary.keys())

    ax = plt.subplot()
    ax.set_xlabel(bgdictionary.keys())

    plt.show()

if __name__ == '__main__':
    # print('Test 1:')
    # pywalker('C:\Users\jklaus\Documents', '^[a-zA-Z]+_TESTResult.*')

    print('--------------------------------------------------------')
    print('Test 2:')
    pathtraverse('C:\Users\jklaus\Documents\Python_Testing\\fire_retardant\\python_scripts\\' , '^[a-zA-Z]+_[a-zA-Z]+.*')