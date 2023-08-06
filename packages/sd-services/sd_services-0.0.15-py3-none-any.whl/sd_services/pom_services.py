#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""
This is new
Created on Mon Dec  7 07:43:40 2020

@author: murraycantor
"""

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import pomegranate as pm
from numpy import arange


def build_network(network, states, edges) -> object:
    """
    Populates a raw Pomegranate Bayesian net with states (nodes) and edges

    Parameters
    ----------
    network: A pomegranate raw network
    states: An array of Pomegranate state objects
    edges: An array of ordered pairs of states which specify the net edges

    Returns: The baked populated pomegranate network object
    -------

    """
    network.add_states(*states)
    for edge in edges:
        network.add_edge(*edge)
    network.bake()
    return network


layouts ={0:"circular_layout",1:"kamada_kawai_layout",2:"planar_layout",3:"random_layout",
          4:"shell_layout",5:"spectral_layout",6:"spring_layout",7:"spiral_layout"}


class belief():
    """
    Provides servces for getting data from and plotting belielfs
    """
    def __init__(self,prob, state, pom_states):
        """
        :param prob: a pomegranate belief object
        :param state: the state to compute given the belief
        :param pom_states: all the states in the network
        """
        self.prob = prob
        self.state = state
        self.pom_states= pom_states
        self.index = pom_states.index(state)


    def data(self):
        """
        :return: a dictonary of the state probabilities
        """

        return self.prob[self.index].parameters[0]

    def plot(self, title=''):
        """
        :param title: Title for plots
        :return: pyplot pie chart of state probabilities
        """
        fig, ax = plt.subplots()
        dat = self.data()
        ax.pie(dat.values(), labels=dat.keys(), autopct='%.2f%%')
        ax.set_title(title)
        return fig





def gen_cond_npt_2(frame, causes,effect,npts, printct=False):
    """
    Generates conditional npt of effect with two causes
    Parameters
    ----------
    frame: Pandas data frame with columns for discretized
    causes and effects
    causes: array of column names of cause data
    effect: column name of effects data
    npts; pomegranate cause_npt objects of causes in same order of cause array
    printct: boolean, prints ct for debug purposes
    Returns
    -------
    npt conditional  npt
    """
    table=[]
    ct = pd.crosstab([frame[causes[0]],frame[causes[1]]],frame[effect],normalize='index') #note these are discrete variables (as they should be)
    if printct: print('ct = ',ct)
    levels = ct.index.levels
    for i in levels[0]:
        for j in levels[1]:
            for k in ct.columns:
                table.append([i,j,k,ct[k].loc[(i,j)]])
    if printct: print('table = \n',table)
    return pm.ConditionalProbabilityTable(table, npts)

def gen_cond_npt_1(frame, Cause, Effect, npt):
    """
    Generates conditional npt of effect with one cause
    Parameters
    ----------
    frame: Pandas data frame with columns for discretized
    cause and effects
    cause: column name of cause data
    effect: column name of effects data
    npt: pomegranate cause npt object
    Returns
    -------
    npt conditional  npt
    """
    ct = pd.crosstab(frame[Cause],frame[Effect],normalize='index') #note these are discrete variables (as they should be)
    table = []
    for i in ct.index:
        for c in ct.columns:
            table.append([i,c,ct[c].loc[i]])
    return pm.ConditionalProbabilityTable(table,[npt])

def ind_npt(frame,col):
    """
    generates the node probability table (priors) for an independent node


    Parameters
    ----------
    frame
    col

    Returns pomegranate npt object
    -------

    """
    cause1_dict = frame[col].value_counts(normalize=True).to_dict()
    return  pm.DiscreteDistribution(cause1_dict)

def plot_graph(edges, size=2000, color='w',edge_colors='k',
               ewidth=2,layout = 1,title='',fname='./figs/graph.png'):
    """
    Uses networkx to plot a directed graph specified by the array of edges.
    Parameters
    ----------
    edges:  An array of ordered pairs of states which specify the net edges
    size: A networkx parameter for specify the size of the graph
    color: The face color of the nodes, using the matplotlib color map
    edge_colors: The color of the edges using the matplotlib color map
    ewidth: The width of the edges
    layout:  An index into this dictionary  of networkx layouts
        layouts ={0:"circular_layout",1:"kamada_kawai_layout",2:"planar_layout",3:"random_layout",
              4:"shell_layout",5:"spectral_layout",6:"spring_layout",7:"spiral_layout"}
    title: A string that is the title of the

    Returns
    -------

    """
    graph = nx.DiGraph()
    names = []
    for edge in edges:
        e1 = edge[0].name
        e2 = edge[1].name
        names.append((e1, e2))
    graph.add_edges_from(names)
    plt.tight_layout()
    if layout == 2:
        nx.drawing.layout.planar_layout(graph)
    elif layout == 6:
       nx.drawing.layout.spring_layout(graph)
    elif layout == 7:
       nx.drawing.layout.spiral_layout(graph)
    elif layout == 5:
       nx.drawing.layout.spectral_layout(graph)
    elif layout == 4:
       nx.drawing.layout.shell_layout(graph)
    elif layout == 3:
       nx.drawing.layout.random_layout(graph)
    elif layout == 1:
       nx.drawing.layout.kamada_kawai_layout(graph)
    elif layout == 0:
       nx.drawing.layout.circular_layout(graph)
    else:
       nx.drawing.layout.planar_layout(graph)

    nx.draw_networkx(graph, node_size=size, node_color=color,
                     edgecolors=edge_colors, width=ewidth)
    plt.title(title)
    plt.savefig(fname)
    plt.show()


def build_bars(bels, xticks, subticks, eff_state,rep, network, states):
    """
    Builds the bars for displaying in pyplot bar charts of the probable of the effect
    for two causes

    :param bels: Dictionary of the beliefs for each (xtick, subtick) pair
    :param xticks: string array of the states pf the primary cause
    :param subticks: string array of the states of secondary cause
    :param rep: the state of the effect
    :param network: a pomegranate network
    :param states: array of the states of the network
    :return: array of values for plot_bar services
    """
    bars = []
    if subticks== None:
        arr = []
        for xtick in xticks:
            bef = network.predict_proba(bels[(xtick)])
            beli = belief(bef, eff_state, states)
            data = beli.data()[rep]
            arr.append(data)
        bars.append(arr)
    else:
        for subs in subticks:
            arr = []
            for xtick in xticks:
                bef = network.predict_proba(bels[(xtick, subs)])

                beli = belief(bef, eff_state, states)
                data = beli.data()[rep]
                arr.append(data)
            bars.append(arr)
    return bars


def plot_bar(x,bars,labels=None,ylabel='',title= ''):
    """

    :param x: The xticks, String for each bar
    bars: arrays of floats in order of bar for xticks
    :param labels: labels for the arr bars
    :param ylabel: string
    :return:
    """
    if labels == None:
        withdiv  = 1
    else:
        withdiv = len(labels)
    ind = arange(len(x))
    width = 1/len(x)
    n = 0
    fig, ax = plt.subplots()
    for bar in bars:
        if labels == None:
            ax.bar(ind + n*width,bar , width)
            ax.set_xticks(ind, x)
        else:
            ax.bar(ind + n * width, bar, width, label=labels[n])
            ax.set_xticks(ind +width/2, x)
        n +=1
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    if labels == None:
        pass
    else:
        ax.legend(loc='best')
    return fig