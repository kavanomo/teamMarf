### teamMarf

Repo for the Card sorter extraordinaire! 

#### Testing

---
To test the card sorter you first need the `secrets.json` file. Without that, nothing works. 

1. Clone the [Flask app](https://github.com/rowlowles/flaskServer), install requirements.txt and run it. 
2. Setup the Pi so that it is making requests to `127.0.0.1:5000` (or whatever address the Flask app is running on)
3. You are good to go!

If you want to modify the database (either to create more test sorts or update card info):
1. Run `python3  /generalScripts/databaseUpdater.py [process] [numSorts] [sortChoice]`
* `[process]`: Optional. Choices: `populate-cards`, `populate-sets`, `update`, `create-sorts`. 
`Update` grabs the most recent pricing data for cards. `create-sorts` creates several random sorts for testing the sorting algo.
Defaults to `create-sorts` if left blank.
* `[numSorts]`: Optional integer. Number of random sorts to be created. Defaults to 5. 
* `[sortChoice]`: Optional. Choices: `cat`, `col`, `val`. Defaults to random choice. 


---
TODO:  
* Decide on how to deal with shiny/foil cards  
* Actually build the dang thing
