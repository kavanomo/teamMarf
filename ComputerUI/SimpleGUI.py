import PySimpleGUI as sg


def getNumCategories(sortName):
    categoryLayout = [[sg.Text('Number of ' + sortName + 'Categories', justification='center', size=(30, 1))],
                      [sg.Spin([i for i in range(1, 6)], initial_value=1,size=(5, 1)),
                       sg.Text(' categories', size=(25, 1))],
                      [sg.Submit(tooltip='Click to confirm this selection')]]
    catWindow = sg.Window('Cardobot').Layout(categoryLayout)

    button, values = catWindow.Read()

    return int(values[0])


def getColourSortOptions(numCategories):
    colSelectLayout = [[sg.Text('Select your sorting categories.', size=(30,1))]]
    for i in range(numCategories):
        colSelectLayout.append([sg.Text('Category ' + str(i+1)),sg.Checkbox('Black'), sg.Checkbox('Blue'), sg.Checkbox('Green'), sg.Checkbox('Red'),
                                sg.Checkbox('White')])

    colSelectLayout.append([sg.Submit(tooltip='Click to confirm this selection')])

    colourWindow = sg.Window('Cardobot').Layout(colSelectLayout)
    button, values = colourWindow.Read()
    print(button)
    print(values)



if __name__ == '__main__':
    # Start with choice between colour, catalogue, or
    sortOptions = ['Colour Sort', 'Value Sort', 'Catalogue Sort']
    introLayout = [[sg.Text('Welcome to Cardobot!', justification='center', size=(30, 1))],
                   [sg.Button(button_text=sortOptions[0], size=(30, 3))],
                   [sg.Button(button_text=sortOptions[1], size=(30, 3))],
                   [sg.Button(button_text=sortOptions[2], size=(30, 3))],
                   [sg.Quit(button_text='Yeet on out of here', size=(30, 3))]
                   ]
    startWindow = sg.Window('Cardobot').Layout(introLayout)

    button, values = startWindow.Read()

    if button == sortOptions[0]:
        print('Looks like you are trying to do colour sort. Want some help with that?')
        numCategories = getNumCategories('Colour')
        getColourSortOptions(numCategories)


