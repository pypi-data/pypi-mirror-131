#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Mon Feb  4 07:45:05 2017

author: Murray

"""


import numpy as np
import scipy.interpolate as intp
import matplotlib.pyplot as plt
import random


PVcolors={'Dark Red':'#680b18','Medium Red':'#aa182c','Bright Red':'#ff3000', \
        'Dark Blue':'#1a1b2f','Cloud':'#f9f4f2','Twilight':'#21213d',
        'Gold':'#ffa943','Blue':'#4297fc','Sea':'#12d6e0'}
colorlist = list(PVcolors.keys())

class pdf():
    """
    Builds probability density functions and cummalative density functions
    from arrays of data. 
    
    Inputs:
        array: data as python array or numpy qarray
        name: String for the name of the object (optional)
        bins: number of bins for the historgram, default is 50. May need turning for small data sets
        
    
    """
    def __init__(self,array,name='',bins=50):
        if len(array) > 10000:
            self.bins = int(len(array)/500)
        else:
            self.bins = bins
            
        self.name=name
        self.array=array
        self.hist = np.histogram(self.array,self.bins,density=True)
        self.x = self.__find_centers() #X-axis
        self.y = self.hist[0] # y axis
        self.cy = self.__cdf()
        self.inv_cdf= self.__inv_cdf_funct()
        self.cdf_func=self.__cdf_funct()
        self.mean= array.mean()
        self.std = array.std()
        self.mode= self.__modef()
        self.title='Distribution of %s' %self.name
        

    def __find_centers(self):
        """
        finds centers of bins for histogram'
        """
        cents = []
        x = self.hist[1]
        for n in range(len(x)-1):
            cents.append((x[n+1]+x[n])/2)
        return cents
    
    def __dist(self):     
        x = self.hist[1]
        cents= []
        for n in range(len(x)-1):
            cents.append((x[n+1]+x[n])/2)
        hist_y = self.hist[0]
        return cents, hist_y
    
    def __cdf(self):
        xa = self.hist[1]
        dx = xa[1]-xa[0]# Find the delta of the x axis intervals
        cum = self.y.cumsum()
        return dx*cum
    
    def pdfunction(self,p):
        tx = np.append(self.hist[1][0],self.x)
        tx = np.append(tx,self.hist[1][-1])
        ty =np.append([0],self.y)
        ty = np.append(ty,[1])
        f=intp.interp1d(tx,ty)
        return f(p)
        
    
    def __cdf_funct(self):
        tx = np.append(self.hist[1][0],self.x)
        tx = np.append(tx,self.hist[1][-1])
        ty =np.append([0],self.cy)
        ty = np.append(ty,[1])
        return intp.interp1d(tx,ty)
        
    
    def __inv_cdf_funct(self):
        tx = np.append(self.hist[1][0],self.x)
        tx = np.append(tx,self.hist[1][-1])
        ty =np.append([0],self.cy)
        ty = np.append(ty,[1])
        return intp.interp1d(ty,tx)
    
    def __plot_range(self,x,y):
        crit = np.max(y)/100
        plot_x= []
        plot_y = []
        for n in range(len(x)):
            if y[n] > crit:
                plot_x.append(x[n])
                plot_y.append(y[n])
        return plot_x, plot_y
                
        
    def samples(self,nsamples=1):
        """
        returns nsamples of the distribution
        """
        samples = []
        for n in range(nsamples):
            t=np.random.uniform()
            samples.append(float(self.inv_cdf(t)))
        return np.array(samples)
    
    def __modef(self):
        x = self.x
        max = -np.inf
        mode = x[0]
        fn = self.pdfunction
        for p in x:
            if fn(p) > max:
                max= fn(p)
                mode= p
        return mode
    
    def median(self):
        return self.percentile(50)
            
    def percentile(self,val):
        """
        returns the valth percentile of the distribution
        val can be between 0 and 100
        """
        return float(self.inv_cdf(val/100))
    
    def cdf(self,p):
        return float(self.cdf_func(p))
    
    def confidence(self,p):
        """
        returns 1 - cdf
        """
        return float(1-self.cdf(p))
    def __oldplot(self,xlabel=''):
        fig = plt.figure(figsize=(11,11))
        title= 'Distribution for %s' %self.name
        fig.suptitle(title, fontsize=20)
        ax=fig.add_subplot(111)
        ax.plot(self.x,self.y)
        ax.set_xlabel(xlabel)   
        return fig
    
    def plot(self,xlab='',ylab= '',title='',xmin=np.inf):
        """
        plots the pdf 
        if minx is omitted, the entire pdf is distrayed
        if minx is given, the pdf is plotted from minx to the upper limit.
        xlab is the x axis label
        """
        if title == '':title=self.title
        else: title = title
        range= max(self.x)-min(self.x)
        gran = range/200
        xa = np.arange(min(self.x),max(self.x),gran)
        ya=self.pdfunction(xa)
     
        fig = plt.figure(figsize=(20,11))
        #title= 'Distribution of %s' %self.name
        fig.suptitle(title, fontsize=30)
        ax=fig.add_subplot(111)
        if xmin < np.inf:
            ax.set_xlim(left=xmin,right=max(xa))
            ax.set_ylim(top=self.__pdfunction()(xmin))
        xa,ya = self.__plot_range(xa,ya)
        ax.plot(xa,ya,lw=8)
        ax.tick_params(axis='x', labelsize= 15)
        ax.set_xlabel(xlab,fontsize = 20)
        ax.set_ylabel(ylab,fontsize = 20)
        return fig
    
    def fillPlot(self,percent, c1=PVcolors['Gold'], c2=PVcolors['Blue'],xlab='Percentile'):
        pct= self.percentile(percent)
        pct = np.round(pct,decimals=0)
        if xlab== 'Percentile':
            fig=self.plot(xlab= f'{percent}th precentile = {pct}')
        else:
            fig=self.plot(xlab= xlab)
        ax = fig.axes[0]
        ax.fill_between(self.x,self.y,color=c2)
        xr = [x for x in self.x if x < pct]
        ax.fill_between(xr,self.y[:len(xr)],color=c1)
        return fig
    
    def plot_cdf(self,xlabel=''):
        fig = plt.figure(figsize=(11,11))
        title= 'Cummulative Distribution for %s' %self.name
        fig.suptitle(title, fontsize=20)
        ax=fig.add_subplot(111)
        ax.plot(self.x,self.cy,lw=8)
        ax.set_xlabel(xlabel)
        ax.tick_params(axis='x', labelsize= 15)
        return fig
    
class pmf():
    """
    creates a probability mass object with 
            
        

        Parameters
        ----------
        xs : numpy array of n values
            The domain
        ps : numpy array of n values
            Dthe masses

    
    """
    def  __init__(self,xs, ps):
        self.xs = xs
        self.ps = ps
        #self.pdict= dict(zip(xs,ps))
        #self.cdict= dict(zip(xs,ps.cumsum()))
    def __make_pdict(self):
        return dict(zip(self.xs,self.ps))
    def __make_cdict(self):
        return  dict(zip(self.xs,self.ps.cumsum()))
      
    def samples(self,num):
        return random.choices(self.xs,weights=self.ps,k=num)
    def prob(self,n):
        if n in self.xs: return self.__make_pdict()[n]
        else: return 0.
    def cum(self,n):
        if n in self.xs: return self.__make_cdict()[n]
        else: return 0.
    def mean(self):
        axs=np.array(self.xs)
        product= axs*self.ps
        return product.sum()
    def plot(self,title = ''):
        """

        Parameters
        ----------
        title : string optional
            DESCRIPTION. The default is ''.

        Returns
        -------
        fig : pyplot figure object
            

        """
        fig = plt.figure()
        ax=fig.add_subplot(111)
        ax.set_axis_on()
        ax.grid(b=False)
        ax.scatter(self.xs,self.ps)
        ax.set_xticks(self.xs)
        ax.set_xlabel('Number of Arrivals in Next Period')
        ax.set_ylabel('likelihood')
        ax.set_title(title)
        return fig

def samples(pdf,nsamps=1):
    x = pdf[0]
    y= pdf[1]
    dx= x[1]-x[0]
    cdf=dx*y.cumsum()
    f =intp.interp1d(cdf,x)
    samples = []
    for n in range(nsamps):
        t = np.random.uniform(cdf[0],cdf[-1])
        samples.append(f(t))
    rsamples = [float(p) for p in samples]
    return np.array(rsamples)
    
   
    