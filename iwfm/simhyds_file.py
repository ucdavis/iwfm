# simhyds_file.py
# Class of methods for working with IWFM simulation hydrographs
# Copyright (C) 2020-2021 Hydrolytics LLC
# -----------------------------------------------------------------------------
# This information is free; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This work is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# For a copy of the GNU General Public License, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# -----------------------------------------------------------------------------

# ** Incomplete **


class simhyds_file:
    def __init__(self, filename):
        self.content = []
        with open(filename, 'r') as inputfile:
            lines = inputfile.read().splitlines()
        lines = [word.replace('_24:00', ' ') for word in lines]

        for j in range(9, len(lines)):
            line = lines[j].split()
            for i in range(1, len(line)):
                line[i] = float(line[i])
            self.content.append(line)

    def sim_head(self, date, col):
        # find bracketing dates
        j = 0
        while index_date(date, self.content[j][0]) > 0:
            j += 1
        num = index_date(
            date, self.content[j - 1][0]
        )  # numerator:   days to observed value
        den = index_date(
            self.content[j][0], self.content[j - 1][0]
        )  # denominator: days between simulated values
        return self.content[j - 1][col] + (
            self.content[j][col] - self.content[j - 1][col]
        ) * (num / den)

    def get_head(self, row, col):
        return self.content[row][col]

    def date(self, row):
        return self.content[row][0]

    def start_date(self):
        return self.content[0][0]

    def end_date(self):
        return self.content[len(self.content) - 1][0]

    def nlines(self):
        return len(self.content)

    def ncols(self):
        return len(self.content[0])
