import json

"""
0: Normal
1: +2
2: +4
3: Block
4: Color change
5: Reverse
"""

# Init dict variable
data = []

def newCard(data, color, number, usage):
    data.append({
        "color": color,
        "number": number,
        "usage": usage
    })

def numberCardLoop(data, color, usage):
    for i in range (0,10):
        if(i == 0):
            newCard(data, color, i, usage)
        else:
            for k in range(2):
                newCard(data, color, i, usage)

def actionCardLoop(data, color, number, usage, amount):
    for i in range(amount):
        newCard(data, color, number, usage)

for color in range(1,5):
    # Standart colored cards
    numberCardLoop(data, color, 0)

# Four colors
for color in range(1,5):

    # Two in each color
    for amount in range(2):

        # +2 colored cards
        newCard(data, color, '+2', 1)

        # Block colored cards
        newCard(data, color, 'x', 3)

        # Reverse colored cards
        newCard(data, color, '↳↰', 5)

# +4 wild cards
actionCardLoop(data, 0, '+4', 2, 4)

# Color change wild cards
actionCardLoop(data, 0, '?!', 4, 4)

# Writing json file
with open('./assets/deck.json','w') as file:
    json.dump(data, file, indent=4)

