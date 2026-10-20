import sys
import os
import curses

# Colori e stili Matrix
COLOR_BG = curses.COLOR_BLACK
COLOR_FG = curses.COLOR_GREEN
COLOR_DIM = 2  # Verde scuro simulato
COLOR_ACCENT = curses.COLOR_WHITE

KEYWORDS = {"def", "class", "import", "from", "return", "if", "else", "elif", "while", "for", "in", "try", "except", "with", "as", "True", "False", "None", "and", "or", "not"}

def draw_matrix_banner(stdscr, height, width):
    banner = "=== [ MATRIX TERMINAL EDITOR v1.0 ] ==="
    if width > len(banner):
        stdscr.attron(curses.color_pair(2) | curses.A_BOLD)
        stdscr.addstr(0, (width - len(banner)) // 2, banner)
        stdscr.attroff(curses.color_pair(2) | curses.A_BOLD)

class MatrixEditor:
    def __init__(self, stdscr, filename):
        self.stdscr = stdscr
        self.filename = filename
        self.lines = [""]
        self.cy = 0
        self.cx = 0
        self.row_offset = 0
        self.col_offset = 0
        self.modified = False
        
        # Carica il file se esiste
        if filename and os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read().splitlines()
                if content:
                    self.lines = content

    def run(self):
        curses.curs_set(1)
        while True:
            self.stdscr.clear()
            height, width = self.stdscr.getmaxyx()
            
            # Area di editing effettiva (lasciamo spazio per banner sopra e status sotto)
            editor_height = height - 2
            
            # Gestione dello scrolling verticale
            if self.cy < self.row_offset:
                self.row_offset = self.cy
            elif self.cy >= self.row_offset + editor_height:
                self.row_offset = self.cy - editor_height + 1

            # Disegna il testo
            for i in range(editor_height):
                file_row = self.row_offset + i
                if file_row >= len(self.lines):
                    break
                
                line_str = self.lines[file_row]
                # Stampa il numero di riga in stile matrix (dim)
                line_num_str = f"{file_row + 1:3d} | "
                try:
                    self.stdscr.addstr(i + 1, 0, line_num_str, curses.color_pair(2))
                except curses.error:
                    pass
                
                # Renderizza la riga con sintassi colorata
                self.draw_colored_line(i + 1, len(line_num_str), line_str, width - len(line_num_str))

            # Disegna la barra di stato in basso
            self.draw_status_bar(height, width)

            # Posiziona il cursore
            cursor_screen_y = self.cy - self.row_offset + 1
            cursor_screen_x = self.cx + 6 # offset del numero di riga
            if cursor_screen_y < height - 1 and cursor_screen_x < width:
                try:
                    self.stdscr.move(cursor_screen_y, cursor_screen_x)
                except curses.error:
                    pass

            self.stdscr.refresh()

            # Gestione input tastiera
            key = self.stdscr.getch()
            if self.handle_input(key):
                break

    def draw_colored_line(self, y, start_x, line_str, max_width):
        # Semplice evidenziatore lessicale in stile Matrix
        words = line_str.split(' ')
        current_x = start_x
        
        for word in words:
            if current_x >= start_x + max_width:
                break
            
            # Scegli il colore
            color = curses.color_pair(1) # Verde standard
            if word in KEYWORDS:
                color = curses.color_pair(3) | curses.A_BOLD # Bianco/Chiaro per le keyword
            elif word.startswith('"') or word.startswith("'") or word.endswith('"') or word.endswith("'"):
                color = curses.color_pair(2) # Verde scuro/sfumato per stringhe
            elif word.isdigit():
                color = curses.color_pair(3)

            to_draw = word + " "
            if current_x + len(to_draw) > start_x + max_width:
                to_draw = to_draw[:start_x + max_width - current_x]

            try:
                self.stdscr.addstr(y, current_x, to_draw, color)
            except curses.error:
                pass
            current_x += len(to_draw)

    def draw_status_bar(self, height, width):
        status_y = height - 1
        mod_flag = " [+] " if self.modified else "     "
        fname = self.filename if self.filename else "[No Name]"
        status_text = f" FILE: {fname}{mod_flag} | POS: {self.cy+1},{self.cx+1} | ^S: Salva  ^Q: Esci "
        if len(status_text) > width:
            status_text = status_text[:width]
        
        try:
            self.stdscr.attron(curses.color_pair(4)) # Sfondo invertito o evidenziato
            self.stdscr.addstr(status_y, 0, status_text.ljust(width))
            self.stdscr.attroff(curses.color_pair(4))
        except curses.error:
            pass

    def handle_input(self, key):
        # Ctrl+Q per uscire
        if key == 17: # DC1 / Ctrl+Q
            return True
        # Ctrl+S per salvare
        elif key == 19: # DC3 / Ctrl+S
            self.save_file()
            return False
        
        # Tasti freccia e navigazione
        elif key == curses.KEY_UP:
            if self.cy > 0:
                self.cy -= 1
                self.cx = min(self.cx, len(self.lines[self.cy]))
        elif key == curses.KEY_DOWN:
            if self.cy < len(self.lines) - 1:
                self.cy += 1
                self.cx = min(self.cx, len(self.lines[self.cy]))
        elif key == curses.KEY_LEFT:
            if self.cx > 0:
                self.cx -= 1
            elif self.cy > 0:
                self.cy -= 1
                self.cx = len(self.lines[self.cy])
        elif key == curses.KEY_RIGHT:
            if self.cx < len(self.lines[self.cy]):
                self.cx += 1
            elif self.cy < len(self.lines) - 1:
                self.cy += 1
                self.cx = 0
                
        # Invio (nuova riga)
        elif key in (10, 13, curses.KEY_ENTER):
            line = self.lines[self.cy]
            new_line = line[self.cx:]
            self.lines[self.cy] = line[:self.cx]
            self.lines.insert(self.cy + 1, new_line)
            self.cy += 1
            self.cx = 0
            self.modified = True
            
        # Backspace
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if self.cx > 0:
                line = self.lines[self.cy]
                self.lines[self.cy] = line[:self.cx-1] + line[self.cx:]
                self.cx -= 1
                self.modified = True
            elif self.cy > 0:
                prev_line_len = len(self.lines[self.cy - 1])
                self.lines[self.cy - 1] += self.lines[self.cy]
                del self.lines[self.cy]
                self.cy -= 1
                self.cx = prev_line_len
                self.modified = True
                
        # Caratteri normali
        elif 32 <= key <= 126:
            char = chr(key)
            line = self.lines[self.cy]
            self.lines[self.cy] = line[:self.cx] + char + line[self.cx:]
            self.cx += 1
            self.modified = True
            
        return False

    def save_file(self):
        if not self.filename:
            self.filename = "matrix_output.py" # Nome di default se non specificato
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write("\n".join(self.lines) + "\n")
        self.modified = False

def main(stdscr):
    # Inizializzazione colori terminale
    curses.start_color()
    curses.use_default_colors()
    
    # Palette Matrix
    curses.init_pair(1, curses.COLOR_GREEN, COLOR_BG)      # Verde standard
    curses.init_pair(2, curses.COLOR_YELLOW, COLOR_BG)     # Verde scuro/Giallognolo per dettagli
    curses.init_pair(3, curses.COLOR_WHITE, COLOR_BG)      # Bianco brillante per keyword/numeri
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN) # Barra di stato invertita (verde/nero)

    filename = sys.argv[1] if len(sys.argv) > 1 else "matrix_code.py"
    editor = MatrixEditor(stdscr, filename)
    editor.run()

if __name__ == "__main__":
    curses.wrapper(main)
