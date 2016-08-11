colorscheme desert  "Changes the color scheme. Change this to your liking. Lookin /usr/share/vim/vim61/colors/ for options.
syntax on  "Enables syntax highlighting for programming languages
set tabstop=4       " number of visual spaces per TAB
set softtabstop=4   " number of spaces in tab when editing
set number          " show line numbers
set showcmd         " show command in bottom bar
set cursorline          " highlight current line
"filetype indent on      " load filetype-specific indent files
set showmatch           " highlight matching [{()}]
set incsearch           " search as characters are entered
set hlsearch            " highlight matches

" Make double-<Esc> clear search highlights
nnoremap <silent> <Esc><Esc> <Esc>:nohlsearch<CR><Esc>

" move to beginning/end of line
nnoremap B ^
nnoremap W $

" highlight last inserted text
nnoremap gV `[v`]

" jk is escape
inoremap jk <esc>

" J and K to jump up and down in doc
nnoremap J 15j
nnoremap K 15k

" toggle gundo
nnoremap <leader>u :GundoToggle<CR>
