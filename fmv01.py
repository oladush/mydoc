MAX_LINES = 5

class ConsoleFileMenu:
    def __init__(self, files):
        self.files = files
        self.path = []
        self.cursor = 0

        self._set()
        self._render()

    def keyboard_control(self):
        keyboard.add_hotkey('up', lambda: self.cursor_up())
        keyboard.add_hotkey('down', lambda: self.cursor_down())

        keyboard.add_hotkey('enter', lambda: self.enter())
        keyboard.add_hotkey('backspace', lambda: self.back())

        try:
            keyboard.wait("esc")
        except KeyboardInterrupt:
            pass

    def cursor_down(self):
        if self.cursor < len(self.cur_dir) - 1:
            self.cursor += 1
        else:
            self.cursor = 0
        self._render()

    def cursor_up(self):
        if self.cursor > 0:
            self.cursor -= 1
        else:
            self.cursor = len(self.cur_dir) - 1
        self._render()

    def enter(self):
        try:
            self.set_path_forward(self.cur_dir[self.cursor])
            self._render()
        except IndexError:
            try:
                self.open()
                message = f'Open file:{"/".join(self.path)} this real name: {self.files["/".join(self.path)]}'
            except KeyError:
                message = f'Ooops, it seems this file not exist. Sorry.'

            self._render(message)

    def back(self):
        message = None
        try:
            self.set_path_back()
        except IndexError:
            message = 'Do you wanna break it down?'
        self._render(message)

    def set_path_forward(self, dirs):
        for dir in dirs.split('/'):
            self.path.append(dir)
        self._set()

    def set_path_back(self):
        del self.path[-1]
        self._set()

    def set_path(self, path):
        self.path = []
        for dir in path.split('/'):
            self.path.append(dir)
        self._set()

# ****
    def open(self):
        print(f"open {self.path}")
        file = '/'
        file = file.join(self.path)
        print(f'Real file name: {self.files[file]}')

    def _set(self):
        self.cur_dir = []
        for file in self.files:
            if file.split('/')[:len(self.path)] == self.path:

                line = file.split('/')[len(self.path)]

                if line not in self.cur_dir:
                    self.cur_dir.append(line)

    def _render(self, message=None):
        if self.cursor < MAX_LINES:
            beg = 0
            end = MAX_LINES - 1
        else:
            beg = self.cursor - (MAX_LINES - 1)
            end = self.cursor

        os.system('cls')
        print('-------fmV.01-------')
        for i in range(len(self.cur_dir)):
            if i in range(beg, end+1):
                print(self.cur_dir[i], end='')
                if i == self.cursor:
                    print(' <')
                else:
                    print()
        print('--------------------')
        if message:
            print(message)
        else:
            print(f'Path: {self.path}')


cm = ConsoleFileMenu(files_2)
cm.keyboard_control()
