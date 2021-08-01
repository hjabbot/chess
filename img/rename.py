 
import os

for old_fn in os.listdir('.'):

	fn = old_fn

	if 'black' in fn:
		fn = fn.replace('black', 'b')

	if 'white' in fn:
		fn = fn.replace('white', 'w')



	if 'pawn' in fn:
		fn = fn.replace('pawn', 'P')
	if 'rook' in fn:
		fn = fn.replace('rook', 'R')
	if 'knight' in fn:
		fn = fn.replace('knight', 'N')
	if 'bishop' in fn:
		fn = fn.replace('bishop', 'B')
	if 'queen' in fn:
		fn = fn.replace('queen', 'Q')
	if 'king' in fn:
		fn = fn.replace('king', 'K')

	fn = fn.replace('_','')

	os.replace(old_fn, fn)

# cmd = 'convert "{}.png" -type truecolor -alpha on "{}.bmp"'
# for fn in os.listdir('.'):
# 	fn = fn.strip('.png')
# 	os.system(cmd.format(fn, fn))