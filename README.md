# gandy-grush

## Run
just run 'python main.py'



## TODO

### Screens
Main screen: Just a play - options - quit menu.
Options: It should allow the user to select a different resolution (new menu), change the key mappings (another menu) and nothing else.
Quit: quit.


### Gameplay
grid 8x8 (validate if a vertical grid more in line with pokemon pokemon puzzle league is allowed) items are generated line by line, every new element is generated in a way that it can't create a 3 line vertically or horizontally (or the weird three thing)
Pokemon snap steal everything.


### Sizing
Every element on the screen should be an updatable sprite so resolution can be easily managed, we can also set logic up so things ocuppy relative spaces that are calculated with the game open. (Ex: third of screen centered, third of container, etc.)
For now we should store all graphic elements into a dummy class to be extended later


### Design
Make stupid little fantasy sprite for different runes should be round ideally with clean edges to show the selection borders. Will have faint colors to identify them quickly and we can change the colors intensity to show posible plays.


### Gameplay
We are remaking pokemon puzzle league but with 8 width grid. So elements appear from the bottom at a set schedule (or can be accelerated by pressing a button) and have pseudo physics (they fall when there is nothing below them). They can also fall if they are moved with an empty space. You lose whenever a block goes over the top of the screen for more than 2 seconds. Once you lose the screen freezes and a modal is displayed with (start again, quit to menu)

- 2 player would be so cool, so cool.

