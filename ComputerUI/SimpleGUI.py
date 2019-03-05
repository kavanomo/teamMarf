import PySimpleGUI as sg

colours = ['Black', 'Blue', 'Green', 'Red', 'White']


def getNumCategories(sortName):
    categoryLayout = [[sg.Text('Number of ' + sortName + 'Categories', justification='center', size=(30, 1))],
                      [sg.Spin([i for i in range(1, 6)], initial_value=1,size=(5, 1)),
                       sg.Text(' categories', size=(25, 1))],
                      [sg.Submit(tooltip='Click to confirm this selection')]]
    catWindow = sg.Window('Cardobot').Layout(categoryLayout)
    button, values = catWindow.Read()
    catWindow.Close()
    return int(values[0])


def getColourSortOptions(numCategories):
    colSelectLayout = [[sg.Text('Select your sorting categories.', size=(30,1))]]
    for i in range(numCategories):
        colSelectLayout.append([sg.Text('Category ' + str(i+1)),sg.Checkbox(colours[0]), sg.Checkbox(colours[1]),
                                sg.Checkbox(colours[2]), sg.Checkbox(colours[3]), sg.Checkbox(colours[4])])

    colSelectLayout.append([sg.Submit(tooltip='Click to confirm this selection')])

    colourWindow = sg.Window('Cardobot').Layout(colSelectLayout)
    button, values = colourWindow.Read()
    return [values[i:i+5] for i in range(0, len(values), 5)]


def getValueSorts(numCategories):
    print('foo')
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
            if sortBounds[j]>sortBounds[j+1]:
                sortBounds[j+1] = sortBounds[j]
        for k in range(numCategories):
            valueWindow.FindElement('cat'+str(k)).Update(sortBounds[k])

        if event == 'Submit':
            break

    return values



if __name__ == '__main__':
    # Start with choice between colour, catalogue, or
    sortOptions = ['Colour Sort', 'Value Sort', 'Catalogue Sort']
    introLayout = [[sg.Text('Welcome to Cardobot!', justification='center', size=(30, 1))],
                   [sg.Button(button_text=sortOptions[0], size=(30, 3))],
                   [sg.Button(button_text=sortOptions[1], size=(30, 3))],
                   [sg.Button(button_text=sortOptions[2], size=(30, 3))],
                   [sg.Quit(button_text='Yeet on out of here', size=(30, 3))]]

    startWindow = sg.Window('Cardobot').Layout(introLayout)

    button, values = startWindow.Read()

    if button == sortOptions[0]:
        print('Looks like you are trying to do colour sort. Want some help with that?')
        numCategories = getNumCategories('Colour')
        colourSelections = getColourSortOptions(numCategories)

    if button == sortOptions[1]:
        numCategories = getNumCategories('Value')
        sortBounds = getValueSorts(numCategories)
        print(sortBounds)


