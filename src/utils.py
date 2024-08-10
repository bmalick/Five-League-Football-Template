#! get_keys
#! load headers
#! create
import sys
import yaml, unidecode, requests
from bs4 import BeautifulSoup
from bs4.element import Tag


def read_yaml(filename: str) -> str:
    with open(filename, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_yaml(filename: str, data: dict):
    with open(filename, 'w') as f:
        yaml.safe_dump(data, f, sort_keys=False)


class Parameters:
    def save_parameters(self, ignore: list[str] = None, **kwargs):
        ignore = ignore or []
        for k, v in kwargs.items():
            if k not in ignore: setattr(self, k, v)

class Displayer(Parameters):

    def __init__(self, widths: list[int] = [4, 60], columns: list[str] = ['', "Title"]) -> None:
        assert len(widths) == len(columns), "widths and columns arguments must have the same number of elements."
        self.save_parameters(widths=widths, columns=columns)

    @property
    def line(self) -> str:
        line = "+" + "%s+" * len(self.widths)
        line %= tuple(['-'*w for w in self.widths])
        return line
    
    @property
    def top(self) -> str:
        res = self.line + "\n"
        cols = "|" + " %s|" * len(self.widths)
        cols %= tuple([col.ljust(w-1)
                       for w,col in zip(self.widths, self.columns)])
        res += cols
        res += "\n|%s|\n" % self.line[1:-1]
        return res   
    
    def display(self, to_display: list):
        text = self.top
        for idx, args in enumerate(to_display):
            col = "|" + " %s |" * len(self.widths) + "\n"
            col %= tuple([str(idx+1).ljust(self.widths[0]-2)] + [
                val.ljust(w-2) if isinstance(val, str) else str(val).rjust(w-2)
                for w,val in zip(self.widths[1:], args)
            ])
            text += col
        text += self.line
        return text