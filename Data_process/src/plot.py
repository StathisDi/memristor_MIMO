#!python3

"""
MIT License

Copyright (c) 2023 Dimitrios Stathis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def get_col_names(df):
    '''
    # Get data columns (columns with the error values)
    '''
    names = df.columns
    labels = []
    for x in names:
        if x.isdigit():
            labels.append(x)
    return labels


def add_means(cls, df):
    '''
    # Add means column in a dataframe and remove the rest of the columns
    '''
    print(df)
    df['avg'] = df[cls].abs().mean(axis=1)
    df = df.drop(columns=cls)
    return df


def plot_var_error(df, var='var_abs'):
    '''
    Create 3D-plot for absolute or relative variation avg_error for different rows (0 relative/absolute variations according to var parameter)
    Arguments:
          df: dataframe
          var: takes values of abs or rel. \'abs\' means that it will plot the absolute variations and vis-versa for \'rel\' 
    '''
    if var != 'abs' and var != 'rel':
        raise Exception("Parameter var should only take \'abs\' or \'rel\'")

    remove = 'var_rel' if var == 'abs' else 'var_abs'
    keep = 'var_rel' if var == 'rel' else 'var_abs'
    title = 'Absolute variations' if var == 'abs' else 'Relative variations'
    df_abs = df.loc[df[remove] == 0]
    df_abs = df_abs.drop(columns=[remove])
    df_abs = df_abs.reset_index(drop=True)
    labels = get_col_names(df_abs)
    df_abs = add_means(labels, df_abs)
    print(df_abs)
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # plot the data as a scatter plot
    ax.scatter(df_abs[keep], df_abs['rows'], df_abs['avg'])
    plot = ax.plot_trisurf(df_abs[keep], df_abs['rows'], df_abs['avg'], cmap='coolwarm', linewidth=0, antialiased=True)
    # set the labels for the x, y and z axes
    ax.set_xlabel(title)
    ax.set_ylabel('Crossbar rows')
    ax.set_zlabel('Average error')
    fig.colorbar(plot, shrink=0.5, aspect=5)
    plt.title(title)
    return (fig)


def plot_var_comb_error(rows, df):
    '''
    Create 3D-plot for relative and absolute variation avg error for specific rows
    '''
    return ()


def plot_rows(abs_var, rel_var, df, box=True):
    '''
    Create 2D plot for specific variation point for different rows, either avg error or box plot
    '''
    return ()


def plot_rel_vars(rows, abs_var, df, box=True):
    '''
    Create 2D plot for specific abs variation and row point for different rel var, either avg error or box plot
    '''
    return ()


def plot_abs_vars(rows, rel_var, df, box=True):
    '''
    Create 2D plot for specific rel variation and row point for different abs var, either avg error or box plot
    '''
    return ()
