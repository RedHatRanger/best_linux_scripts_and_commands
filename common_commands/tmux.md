# tmux Cheatsheet
- For 4 split screens:
```bash
tmux new-session -t htop \; split-window -h "ssh server2" \; split-window -v "ssh server4" \; select-pane -t 0 \; split-window -v "ssh server3" \; select-pane -t 0
```
# To toggle pane synchronization:
Enable sync: Press Ctrl+b, then type : and enter setw synchronize-panes
Disable sync: Press Ctrl+b, then type : and enter setw synchronize-panes off


# tmux Session
New Sessions
```
tmux

# OR

tmux new -s <session_name>
```
Remove Sessions
tmux kill-ses

tmux kill-session -t <session_name>


Attaching Sessions
```
tmux a

# OR

tmux a -t <session_name>
```

tmux Windows
Windows are like tabs in a browser. Windows exist in sessions and occupy the same screen of a session.

Key Bindings
Ctrl + B 0-9: Select window by number

Ctrl + B B: Select window by name

Ctrl + B <: Change window number

Ctrl + B ,: Rename window

Ctrl + B C: Create window

Ctrl + B N: Move to next window

Ctrl + B P: Move to previous window

Ctrl + B L: Move to last used window

Ctrl + B F: Search windows

Ctrl + B &: Kill window

Ctrl + B W: List windows

tmux Panes
Panes are sections of windows that have been split into different screens, just like the panes on this cheatsheet.

Key Bindings
Ctrl + B %: Vertical split

Ctrl + B ": Horizontal split

Ctrl + B ↑: Move up to pane

Ctrl + B ↓: Move down to pane

Ctrl + B →: Move to pane to the right

Ctrl + B ←: Move to pane to the left

Ctrl + B 0: Go to next pane

Ctrl + B ;: Go to last active pane

Ctrl + B }: Move pane right

Ctrl + B {: Move pane left

Ctrl + B !: Convert pane to window

Ctrl + B X: Kill pane



tmux Copy Mode

Key Bindings

Ctrl + B [: Enter copy mode

Ctrl + B ]: Paste from buffer

Copy Mode Commands
Ctrl + Space: Start selection

Ctrl + W: Copy selection

Ctrl + G: Clear selection

PageUp: Scroll up page

PageDown: Scroll down page

Alt + <: Go to top

Alt + >: Go to bottom

← ↓ →: Move cursor

Ctrl + S: Search

N: Next search

Q: Quit

EMACS MODE - DEFAULT
