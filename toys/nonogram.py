import random

random.seed("lel")

class nonogram(object):

    changes= {
        1:"@",
        0:" "
    }

    def __init__(self, lists):
        self.X_hints = self.get_X_hints(lists)
        self.Y_hints = self.get_Y_hints(lists)
        self.data = lists

    @staticmethod
    def get_hints(list):
        "Returns hints for a given list of elements"
        hints = []
        hint  = 0
        for element in list:

            if element: hint += 1

            if not element and hint:
                hints.append(str(hint))
                hint = 0
        else:
            # A else after a for loop will run if the for exits without a break
            if hint: hints.append(str(hint))
        return hints

    @staticmethod
    def get_X_hints(lists):
        """get the hints that go on the top of the puzzle,"""
        hints = []
        for col in range(len(lists)):
            hints.append(nonogram.get_hints(
                [row[col] for row in lists]
            ))
        return hints


    @staticmethod
    def get_Y_hints(lists):
        """get the hints that go on the side of the puzzle,"""
        hints = []

        for row in lists:
            hints.append(nonogram.get_hints(row))
        return hints


    @classmethod
    def gen_matix(cls, x, y):
        return [
        [random.choice(list(cls.changes.keys())) for element in range(y)] for row in range(x)
                ]


    def _str_data(self):
        return "".join(self._get_row_data())

    def _get_row_data(self):
        output = []
        width = len(self.data[0])
        output.append("+" + "-" * width + "+")
        for row in self.data:
            s = ""
            s += "|"
            for e in row:
                s += self.changes[e]
            s += "|"
            output.append(s)
        output.append("+" + "-" * width + "+")
        return output

    def _str_X_hints(self):
        output = []
        height = max(len(hints) for hints in self.X_hints)
        for i in range(1, height+1):
            row_of_hints = [" "] # Border Spacing
            for hints in self.X_hints:
                try:
                    row_of_hints.append(hints[-i])
                except IndexError:
                    row_of_hints.append(" ")
            output.append("".join(row_of_hints))
        output.reverse()
        return output

    def _str_Y_hints(self):
        """generator"""
        output = []
        width = max(len(hints) for hints in self.Y_hints)
        output.append(" "*width)
        for hints in self.Y_hints:
            output.append("".join(hints).rjust(width))
        output.append(" " * width)
        return output

    def __str__(self):
        Y_hints = self._str_Y_hints()
        X_hints = self._str_X_hints()
        data = self._get_row_data()
        rpad = max(len(hints) for hints in Y_hints)
        output = []
        for x in X_hints:
            output.append(" "*rpad + x)
        for i, row in enumerate(data): #Same as calling range(len(mumble...)) exept you get the item and the index
            output.append(Y_hints[i] + row)
        return "\n".join(output)

t = nonogram(
    nonogram.gen_matix(10,10)
    )
print(t._str_X_hints())
print(list(t._str_Y_hints()))
print(t._str_data())
print("X",t.X_hints)
print("Y",t.Y_hints)

print(t)

print(nonogram.get_hints([0,1,1,1,0,0,1,1,0,1]))
# ['3', '2', '1']
