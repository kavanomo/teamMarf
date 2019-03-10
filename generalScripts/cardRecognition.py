import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2

def recognizeObject(model, image):
    """
    Given a tensorflow model and an image, classify that image based on the TF model
    :param model:
    :param image:
    :return:
    """
    img = (np.expand_dims(image, 0))
    if img.shape[1:] != model.input_shape[1:]:
        # Input image is not the same size as the desired input
        error = 'Got input shape: ' +str(img.shape[1:]) + ', expected shape: ' + str(model.input_shape[1:])
        return error

    predictions = model.predict(img)
    return predictions

# Check for Foil
# foilModel = keras.models.load_model('foilMode.h5')
# testImg = cv2.imread('yourCardNameHere.jpg')
# testImg = cv2.cvtColor(testImg, cv2.COLOR_RGB2HSV)[:,:,0] # IMPORTANT: Take only the H channel from HSV
# inputShape = foilModel.input_shape[1:] # Get the model's desired input shape
# resized = cv2.resize(testImg, inputShape[::-1]) # Resize the image to the desired input shape (note that x,y are flipped
#
# print(recognizeObject(foilModel, resized)) # Recognize the image

# Check for set icon
classNames = ['15th_Anniversary_Cards', '2016_Heroes_of_the_Realm', 'Aether_Revolt', 'Alara_Reborn', 'Alliances', 'Amonkhet', 'Amonkhet_Invocations', 'Anthologies', 'Antiquities', 'Apocalypse', 'Arabian_Nights', 'Archenemy', 'Archenemy__Nicol_Bolas', 'Arena_League_1996', 'Arena_League_1999', 'Arena_League_2001', 'Arena_New_Player_Experience', 'Avacyn_Restored', 'Battlebond', 'Battle_for_Zendikar', 'Battle_Royale_Box_Set', 'Battle_the_Horde', 'Beatdown_Box_Set', 'Betrayers_of_Kamigawa', 'Champions_of_Kamigawa', 'Chronicles', 'Classic_Sixth_Edition', 'Coldsnap', 'Collectors_Edition', "Commander's_Arsenal", 'Commander_2011', 'Commander_2013', 'Commander_2014', 'Commander_2015', 'Commander_2016', 'Commander_2017', 'Commander_2018', 'Commander_2018_Tokens', 'Commander_Anthology', 'Commander_Anthology_Volume_II', 'Conflux', 'Conspiracy', 'Conspiracy__Take_the_Crown', 'Core_Set_2019', 'Darksteel', 'Dark_Ascension', 'Deckmasters', 'Defeat_a_God', 'Dissension', 'Dominaria', "Dragon's_Maze", 'Dragons_of_Tarkir', 'Dragon_Con', 'Duels_of_the_Planeswalkers', 'Duels_of_the_Planeswalkers_Promos_2009', 'Duels_of_the_Planeswalkers_Promos_2012', 'Duels_of_the_Planeswalkers_Promos_2013', 'Duels_of_the_Planeswalkers_Promos_2014', 'Duel_Decks_Anthology__Divine_vs._Demonic', 'Duel_Decks_Anthology__Elves_vs._Goblins', 'Duel_Decks_Anthology__Garruk_vs._Liliana', 'Duel_Decks_Anthology__Jace_vs._Chandra', 'Duel_Decks__Ajani_vs._Nicol_Bolas', 'Duel_Decks__Blessed_vs._Cursed', 'Duel_Decks__Elspeth_vs._Kiora', 'Duel_Decks__Elspeth_vs._Tezzeret', 'Duel_Decks__Elves_vs._Inventors', 'Duel_Decks__Heroes_vs._Monsters', 'Duel_Decks__Izzet_vs._Golgari', 'Duel_Decks__Jace_vs._Vraska', 'Duel_Decks__Knights_vs._Dragons', 'Duel_Decks__Merfolk_vs._Goblins', 'Duel_Decks__Mind_vs._Might', 'Duel_Decks__Mirrodin_Pure_vs._New_Phyrexia', 'Duel_Decks__Nissa_vs._Ob_Nixilis', 'Duel_Decks__Phyrexia_vs._the_Coalition', 'Duel_Decks__Sorin_vs._Tibalt', 'Duel_Decks__Speed_vs._Cunning', 'Duel_Decks__Venser_vs._Koth', 'Duel_Decks__Zendikar_vs._Eldrazi', 'Eighth_Edition', 'Eldritch_Moon', 'Eternal_Masters', 'Eventide', 'Exodus', 'Explorers_of_Ixalan', 'Face_the_Hydra', 'Fallen_Empires', 'Fate_Reforged', 'Fifth_Dawn', 'Fifth_Edition', 'Foreign_Black_Border', 'Fourth_Edition', 'From_the_Vault__Angels', 'From_the_Vault__Annihilation', 'From_the_Vault__Dragons', 'From_the_Vault__Exiled', 'From_the_Vault__Legends', 'From_the_Vault__Lore', 'From_the_Vault__Realms', 'From_the_Vault__Relics', 'From_the_Vault__Transform', 'From_the_Vault__Twenty', 'Future_Sight', 'Game_Night', 'Gatecrash', 'Global_Series_Jiang_Yanggu_&_Mu_Yanling', 'GRN_Guild_Kit', 'Guildpact', 'Guru', 'Hachette_UK', 'HarperPrism_Book_Promos', 'HasCon_2017', 'Homelands', 'Hour_of_Devastation', 'Ice_Age', 'Iconic_Masters', 'IDW_Comics_2012', 'Innistrad', 'Invasion', 'Ixalan', 'Judgment', 'Kaladesh', 'Kaladesh_Inventions', 'Khans_of_Tarkir', 'Legendary_Cube', 'Legends', 'Legions', 'Limited_Edition_Alpha', 'Limited_Edition_Beta', 'Lorwyn', 'Magic_2010', 'Magic_2011', 'Magic_2012', 'Magic_Online_Avatars', 'Magic_Online_Theme_Decks', 'Magic_Origins', 'Magic_Premiere_Shop_2005', 'Magic_Premiere_Shop_2007', 'Masters_25', 'Masters_Edition', 'Masters_Edition_II', 'Masters_Edition_III', 'Masters_Edition_IV', 'Mercadian_Masques', 'Mirage', 'Mirrodin', 'Mirrodin_Besieged', 'Modern_Event_Deck_2014', 'Modern_Masters', 'Modern_Masters_2015', 'Modern_Masters_2017', 'Morningtide', 'Mythic_Edition', 'Mythic_Edition_Tokens', 'Nemesis', 'New_Phyrexia', 'Ninth_Edition', 'Oath_of_the_Gatewatch', 'Odyssey', 'Onslaught', 'Planar_Chaos', 'Planechase', 'Planechase_2012', 'Planechase_Anthology', 'Planeshift', 'Portal', 'Portal_Second_Age', 'Portal_Three_Kingdoms', 'Premium_Deck_Series__Fire_and_Lightning', 'Premium_Deck_Series__Graveborn', 'Premium_Deck_Series__Slivers', 'Prophecy', 'Ravnica_Allegiance', 'Ravnica_Allegiance_Promos', 'Ravnica_Allegiance_Tokens', 'Renaissance', 'Return_to_Ravnica', 'Rinascimento', 'Rise_of_the_Eldrazi', 'Rivals_of_Ixalan', 'RNA_Ravnica_Weekend', 'Salvat_2011', 'Saviors_of_Kamigawa', 'Scars_of_Mirrodin', 'Scourge', 'Seventh_Edition', 'Shadowmoor', 'Shadows_over_Innistrad', 'Shards_of_Alara', 'Signature_Spellbook__Jace', 'Starter_1999', 'Starter_2000', 'Stronghold', 'Summer_of_Magic', 'Tempest', 'Tempest_Remastered', 'Tenth_Edition', 'The_Dark', 'Time_Spiral', 'Torment', 'Ultimate_Box_Topper', 'Unglued', 'Unhinged', 'Unlimited_Edition', 'Unstable', "Urza's_Destiny", "Urza's_Legacy", 'Vintage_Masters', 'Visions', 'Weatherlight', 'Welcome_Deck_2016', 'Welcome_Deck_2017', 'Worldwake', 'You_Make_the_Cube', 'Zendikar', 'Zendikar_Expeditions']
setIconModel = keras.models.load_model('setIconModel.h5')
testSetImg = cv2.imread('images27.jpg')
testSetImg = (testSetImg[:,:,0])/255
inputSetShape = setIconModel.input_shape[1:]
resizedSet = cv2.resize(testSetImg, inputSetShape[::-1])

print(recognizeObject(setIconModel, resizedSet))
# Same procedure as above, just crop the card image to a black/white box around the set icon and pass in setIconModel