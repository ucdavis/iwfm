# mysql_create.py
# Create a mysql database
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


def mysql_create(dbname, host, port=3306, user="root", passwd="", debug=0):
    """ mysql_create() Create a mysql database """
    import pymysql

    # establish a database connection on local machine as root database user
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db="mysql")
    # conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='mysql')

    if debug:
        print(" PyMySQL connected to {}".format(dbname))

    # get the database cursor needed to change the database
    cur = conn.cursor()

    # check if database exists, and drop it if it does
    cur.execute("DROP DATABASE IF EXISTS " + dbname)
    cur.execute("CREATE DATABASE " + dbname)

    # Close cursor and connection
    cur.close()
    conn.close()
