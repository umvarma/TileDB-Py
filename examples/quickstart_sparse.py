# quickstart_sparse.py
#
# LICENSE
#
# The MIT License
#
# Copyright (c) 2018 TileDB, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# DESCRIPTION
#
# This is a part of the TileDB quickstart tutorial:
#   https://docs.tiledb.io/en/latest/tutorials/quickstart.html
#
# When run, this program will create a simple 2D sparse array, write some data
# to it, and read a slice of the data back.
#


import numpy as np
import sys
import tiledb

# Name of the array to create.
array_name = "quickstart_sparse"


def create_array():
    # Create a TileDB context
    ctx = tiledb.Ctx()

    # The array will be 4x4 with dimensions "rows" and "cols", with domain [1,4].
    dom = tiledb.Domain(ctx,
                        tiledb.Dim(ctx, name="rows", domain=(1, 4), tile=4, dtype=np.int32),
                        tiledb.Dim(ctx, name="cols", domain=(1, 4), tile=4, dtype=np.int32))

    # The array will be sparse with a single attribute "a" so each (i,j) cell can store an integer.
    schema = tiledb.ArraySchema(ctx, domain=dom, sparse=True,
                                attrs=[tiledb.Attr(ctx, name="a", dtype=np.int32)])

    # Create the (empty) array on disk.
    tiledb.SparseArray.create(array_name, schema)


def write_array():
    ctx = tiledb.Ctx()
    # Open the array and write to it.
    with tiledb.SparseArray(ctx, array_name, mode='w') as A:
        # Write some simple data to cells (1, 1), (2, 4) and (2, 3).
        I, J = [1, 2, 2], [1, 4, 3]
        data = np.array(([1, 2, 3]))
        A[I, J] = data


def read_array():
    ctx = tiledb.Ctx()
    # Open the array and read from it.
    with tiledb.SparseArray(ctx, array_name, mode='r') as A:
        # Slice only rows 1, 2 and cols 2, 3, 4.
        data = A[1:3, 2:5]
        a_vals = data["a"]
        for i, coord in enumerate(data["coords"]):
            print("Cell (%d, %d) has data %d" % (coord[0], coord[1], a_vals[i]))


ctx = tiledb.Ctx()
if tiledb.object_type(ctx, array_name) != "array":
    create_array()
    write_array()

read_array()
