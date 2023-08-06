from dataclasses import dataclass
from typing import Union, Any


class TdProgressBase:
    total: int
    current: int

    def __init__(self, total: int):
        self.total = total
        self.current = 0

    def update(self, current: int):
        self.current = current

    def increment(self, amount: int = 1):
        self.current += amount

    def display(self) -> str:
        return f"Progress: {str(self.current).zfill(len(str(self.total)))} / {self.total}"

    def print(self):
        if self.current < self.total:
            print(self.display(), end='\r')
        else:
            print(self.display())


@dataclass
class TdProgressOptions:
    progress_prefix: str = '⏳'
    complete_prefix: str = '✅'
    title_postfix: str = ': '
    title_prefix: str = ' '
    title: str = 'status'

    progress_bar_width: int = 20
    progress_bar_left: str = '['
    progress_bar_right: str = ']'
    progress_bar_complete: str = '█'
    progress_bar_incomplete: str = '░'
    progress_bar_last: Union[str, None] = None

    postfix: str = ' (%d%%)'

    def set_title(self, title: str):
        self.title = title

    def update(self, key: str, value: Any):
        setattr(self, key, value)


class TdProgress(TdProgressBase):
    styles = {
        'default': TdProgressOptions(),
        'arrow': TdProgressOptions(
            progress_bar_last='>',
            progress_bar_incomplete=' ',
            progress_bar_complete='=',
        ),
        'hash': TdProgressOptions(
            progress_bar_complete='#',
            progress_bar_incomplete=' ',
        )
    }

    def __init__(self, total: int, options: TdProgressOptions = None):
        super().__init__(total)

        if options is None:
            options = self.styles['default']

        self.options = options

    def display(self) -> str:
        options = self.options
        progress = self.current / self.total

        prefix = options.progress_prefix if self.current < self.total else options.complete_prefix
        title = options.title

        filled = int(progress * options.progress_bar_width)
        unfilled = options.progress_bar_width - filled

        progress_bar = None
        if options.progress_bar_last is None:
            progress_bar = f"{filled * options.progress_bar_complete}{unfilled * options.progress_bar_incomplete}"
        else:
            if filled == 0:
                fill = ''
            else:
                fill = options.progress_bar_complete * (filled - 1) + options.progress_bar_last
            progress_bar = f"{fill}{unfilled * options.progress_bar_incomplete}"

        postfix = options.postfix % (progress * 100)

        return f"{prefix}{options.title_prefix}{title}{options.title_postfix}{options.progress_bar_left}{progress_bar}{options.progress_bar_right}{postfix}"


# testing
if __name__ == "__main__":
    from time import sleep

    progress = TdProgress(100)
    for i in range(100):
        progress.increment()
        progress.print()
        sleep(1)
