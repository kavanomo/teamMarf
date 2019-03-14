import PySimpleGUI as sg
import datetime
import json
import mysql.connector

colours = ['Black', 'Blue', 'Green', 'Red', 'White']
sortOptions = ['Colour Sort', 'Value Sort', 'Catalogue Sort']
secrets = json.load(open('../secrets.json', encoding="utf8"))

teamMarfDB = mysql.connector.connect(
    host=secrets['host'],
    port=secrets['port'],
    user=secrets['user'],
    password=secrets['password'],
    db=secrets['db']
)
mycursor = teamMarfDB.cursor()


def pushSort(sortObject):
    query = "INSERT INTO sortCommands (timestamp, sortType, numCat, categories, userName) VALUES (%s, %s, %s, %s, %s)"
    mycursor.execute(query, sortObject)
    teamMarfDB.commit()
    return


def assembleMessage(sortType, sortParams, username='t_senlin'):
    """

    :param sortType:
    :param sortParams: nxm list. n is num of categories, m is dependent on context of sort. Never more than 5
    :return:
    """
    message = {'categories': {}}
    currentTime = datetime.datetime.now()
    numCat = len(sortParams)
    if sortType == sortOptions[0]:
        # Colour sort
        sortType = 'col'
        for j, sort in enumerate(sortParams):
            category = 'cat'+str(j)
            message['categories'][category] = {}
            for i, colourChoice in enumerate(sort):
                message['categories'][category][colours[i].lower()] = int(colourChoice)

    if sortType == sortOptions[1]:
        # Value sort
        sortType = 'val'
        for j, sort in enumerate(sortParams):
            category = 'cat' + str(j)
            val1 = sortParams[j-1] if (j >= 1) else 0
            val2 = sort
            message['categories'][category] = {'val1': val1, 'val2': val2}

    if sortType == sortOptions[2]:
        sortType = 'cat'
        message['categories'] = sortParams

    pushSort((currentTime, sortType, numCat, json.dumps(message), username))

def getNumCategories(sortName):
    categoryLayout = [[sg.Text('Number of ' + sortName + 'Categories', justification='center', size=(30, 1))],
                      [sg.Spin([i for i in range(1, 6)], initial_value=1,size=(5, 1)),
                       sg.Text(' categories', size=(25, 1))],
                      [sg.Submit(tooltip='Click to confirm this selection')]]
    catWindow = sg.Window('Cardobot').Layout(categoryLayout)
    button, values = catWindow.Read()
    catWindow.Close()
    return int(values[0])


def noNullColourChoice(choices):
    """
    Find if user marked at least one colour choice as true in each sort category. If any choice doesn't have True in it,
    then it means we have an empty category.
    :param choices: 2d list in format [[Bool, Bool, Bool, Bool, Bool]*numCategories]
    :return:
    """
    return all(True in sub for sub in choices)


def noIdenticalChoices(choices):
    """
    Make sure that no choice of colours is repeated in any category. If any choice is repeated in the list of choices,
    return a false
    :param choices: 2d ordered list in format [[Bool, Bool, Bool, Bool, Bool]*numCategories]
    :return:
    """
    return not(max([choices.count(choice)-1 for choice in choices]))


def getColourSortOptions(numCategories):
    colSelectLayout = [[sg.Text('Select your sorting categories.', size=(30,1))]]
    for i in range(numCategories):
        colSelectLayout.append([sg.Text('Category ' + str(i+1)),sg.Checkbox(colours[0]), sg.Checkbox(colours[1]),
                                sg.Checkbox(colours[2]), sg.Checkbox(colours[3]), sg.Checkbox(colours[4])])

    colSelectLayout.append([sg.Submit(tooltip='Click to confirm this selection')])

    colourWindow = sg.Window('Cardobot').Layout(colSelectLayout)

    while True:
        button, values = colourWindow.Read()
        values = [values[i:i+5] for i in range(0, len(values), 5)]
        distinctChoices = noIdenticalChoices(values)
        madeChoices = noNullColourChoice(values)
        if madeChoices and distinctChoices:
            break
        elif not(distinctChoices) and not(madeChoices):
            sg.Popup('Must select at least one colour for each category!\nEach category must be different!')
        elif not(distinctChoices):
            sg.Popup('Each category must be different!')
        else:
            sg.Popup('Must select at least one colour for each category!')


    colourWindow.Close()

    return values


def getValueSorts(numCategories):
    valueLayout = [[sg.Text('Choose the cost categories')]]

    for i in range(numCategories):
        valueLayout.append([sg.Text('Category ' + str(i)), sg.Slider(range=(1,100), orientation='h', key='cat'+str(i),
                                                                     change_submits=True)])

    valueLayout.append([sg.Submit(tooltip='Click to confirm this selection')])
    valueWindow = sg.Window('Cardobot').Layout(valueLayout)

    while True:
        event, values = valueWindow.Read()
        sortBounds = list(values.values())
        for j in range(numCategories-1):
            if sortBounds[j] > sortBounds[j+1]:
                sortBounds[j+1] = sortBounds[j]
        for k in range(numCategories):
            valueWindow.FindElement('cat'+str(k)).Update(sortBounds[k])

        if event == 'Submit':
            break

    valueWindow.Close()
    return list(values.values())


if __name__ == '__main__':
    # Start with choice between colour, catalogue, or value
    introLayout = [[sg.Text('Welcome to Cardobot!', justification='center', size=(22, 1), font='Helvetica 15')],
                   [sg.Text('Username:'), sg.InputText(size=(24,3))],
                   [sg.Button(button_text=sortOptions[0], size=(30, 3))],
                   [sg.Button(button_text=sortOptions[1], size=(30, 3))],
                   [sg.Button(button_text=sortOptions[2], size=(30, 3))],
                   [sg.Quit(button_text='Quit', size=(30, 3))]]

    startWindow = sg.Window('Cardobot').Layout(introLayout)

    while True:
        button, values = startWindow.Read()

        if not values[0]:
            sg.Popup('Please enter a username.')

        if button == sortOptions[0] and values[0]:
            numCategories = getNumCategories('Colour')
            colourSelections = getColourSortOptions(numCategories)
            assembleMessage(button, colourSelections, values[0])
            sg.Popup('Sort received!')

        if button == sortOptions[1] and values[0]:
            numCategories = getNumCategories('Value')
            sortBounds = getValueSorts(numCategories)
            # assembleMessage(button, sortBounds, values[0])
            sg.Popup('Sort received!')

        if button == sortOptions[2] and values[0]:
            # assembleMessage(button, 'catalogue', values[0])
            sg.Popup('Sort received!')

