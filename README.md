# Communi3 $SCI tokens parser
 App based on [Selenium](https://github.com/SeleniumHQ/selenium/tree/trunk/py) to parse [Communi3](https://nft.communi3.io/) NFTs from [hyperspace market](https://hyperspace.xyz/collection/communi3madscientists) and get `$SCI` price for all of them.

## Requirements
* Windows OS
* Python (tested on `3.10.2`, but should work with `>=3.7`)
* Chrome installed
* Chromedriver (lookup your chrome version in settings: `chrome://settings/help`) and download chromedriver that suits it from [here](https://chromedriver.chromium.org/downloads))

## How to run
1. [Download](https://github.com/danijcom/Communi3-SCI-tokens-parser/archive/refs/heads/main.zip) the project folder, unpack it
2. Download [chromedriver](https://chromedriver.chromium.org/downloads), replace `chromium/chromedriver.exe` with .exe you downloaded
3. Open the console in the script folder (or use `cd` to reach it)
4. Install requirements. Command: `py -m pip install -r requirements.txt`
5. Optional: edit `main.py` file, replace variable `MAX_PRICE` (_line 140 as for now_) with the amount you need (default is 9999), save changes
6. Run script (most likely `py main.py`)

## Troubleshooting

**Error "Can't find NFTs cards":** if Hyperspace changes some in their site, they can update the class name of the NFT card. For 01.11.2022 its css-g0fuxu, but it can be changed in the future.

To fix it you should go [here](https://hyperspace.xyz/collection/communi3madscientists), press with the right mouse button on the card with some NFT, press Inspect, find an element with the whole card and copy its class name (please, check the video above).

https://user-images.githubusercontent.com/46953160/199119299-1744f409-4ef3-4629-92d5-b1569e3cf4eb.MP4

Then, you should replace the old class name in `main.py` (_css-g0fuxu, line 65, 71 as for now_) with the class name you have copied (its 2 occurrences, use file search).

Then save and run script again. 

## Output example

**Console:**
```
Processing #2720...
Authority: 9otwyjX7msBhQ1tVHuEVQgiMZFFyMsZp3q4zg5dQfSF6
Tokens: 3095
#2720:  3095 $SCI - 18.90 $SOL - https://hyperspace.xyz/token/C9w7nXXMog1oCAcJVR8dRVBC1KXXxbNF2DSqDsgoztqE - 9otwyjX7msBhQ1tVHuEVQgiMZFFyMsZp3q4zg5dQfSF6
```
**Output file:**
```
#2720:  3095 $SCI - 18.90 $SOL - https://hyperspace.xyz/token/C9w7nXXMog1oCAcJVR8dRVBC1KXXxbNF2DSqDsgoztqE - 9otwyjX7msBhQ1tVHuEVQgiMZFFyMsZp3q4zg5dQfSF6
```

## Credits

Thanks to the developer of https://www.madsci-status.app/, and sorry for using your tool in not so proper way.

If someone knows how to calculate $SCI amount using only blockchain data - open PR.