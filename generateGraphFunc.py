import fileSelectFunc as fs
import urlEntryFunc as ue
import regionFunc as rf
import genesExonsFunc as ge
import generateStatFunc as gs
import tkinter as tk
from tkinter import Label, StringVar, filedialog
from tkinter.constants import ANCHOR, E, LEFT, NS, NSEW, RAISED, RIGHT, VERTICAL, W, Y
import wget
import validators
from glob import glob
import os
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.widgets import Button  
import  gffutils
from gffutils.create import create_db
from pathlib import Path
import sqlite3
import pandas as pd
import tkinter.ttk as ttk 
import ttkthemes as themes
from tkinter import messagebox
import matplotlib as mpl
from matplotlib import pylab
import seaborn as sns



def generateGraphExon (show,save):

     mpl.rcParams['axes.spines.right'] = False
     mpl.rcParams['axes.spines.top'] = False
     fig1 = pylab.gcf()
     fig1.canvas.manager.set_window_title('Graphes des exons')
     plt.bar(exonPositions,exonTInt,label='exon',color='darksalmon')
     plt.xlabel('Position')
     plt.ylabel('Taille (acide nucleique)')
     plt.title('Distribution de taille des exons sur les 2 brins',fontsize=13)
     plt.legend(ncol=3,loc='upper right')
          
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./Figures/barExon.png")
          plt.close()
     


def generateGraphGene(show,save):

     mpl.rcParams['axes.spines.right'] = False
     mpl.rcParams['axes.spines.top'] = False
     fig2 = pylab.gcf()
     fig2.canvas.manager.set_window_title('Graphes des genes')
     plt.bar(genePositions,geneTInt,label='Gene',color='olive')
     plt.xlabel('Position')
     plt.ylabel('Taille (acide nucleique)')
     plt.title('Distribution de taille des genes sur les 2 brins',fontsize=13)
     plt.legend(ncol=3,loc='upper right')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./Figures/barGene.png")
          plt.close()
     


def generateGraphIntron(show,save):

     mpl.rcParams['axes.spines.right'] = False
     mpl.rcParams['axes.spines.top'] = False
     fig3 = pylab.gcf()
     fig3.canvas.manager.set_window_title('Graphes des introns')
     plt.bar(intronPositions,intronTInt,label='Intron',color='firebrick')
     plt.xlabel('Position')
     plt.ylabel('Taille (acide nucleique)')
     plt.title('Distribution de taille des introns sur les 2 brins',fontsize=13)
     plt.legend(ncol=3,loc='upper right')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./Figures/barIntron.png")
          plt.close()



def generateGraphInter(show,save):  

     mpl.rcParams['axes.spines.right'] = False
     mpl.rcParams['axes.spines.top'] = False
     fig1 = pylab.gcf()
     fig1.canvas.manager.set_window_title('Graphes des régions intergéniques')
     plt.bar(interPositionsBoth,interListBoth,label='Régions Intergéniques',color='yellowgreen')

     print(interListBoth)
     plt.xlabel('Position')
     plt.ylabel('Taille (acide nucleique)')
     plt.title('Distribution de taille des régions intergéniques sur les 2 brins',fontsize=11)
     plt.legend(ncol=4,loc='upper right')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./Figures/barInter.png")
          plt.close()

def generatePiechartExonsIntrons (show,save):

     values = [sumIntrons,sumExons]
     Names = ["Introns","Exons"]
     col=['firebrick','darksalmon']
     
     figP = pylab.gcf()
     figP.canvas.manager.set_window_title('Distributions des exons et des intron')
     plt.pie(values,labels=Names,autopct="%.1f%%",wedgeprops={'edgecolor':'white', 'linewidth':2},colors=col)
     plt.title('Pourcentages des exons et introns')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./Figures/pieExonsIntrons.png")
          plt.close()

def generatePiechartGenesIntergeniques (show,save):

     values1 = [sumGenes,sumInter]
     Names1 = ["Genes","Intergeniques"]
     col=['olive','yellowgreen']
     
     figP = pylab.gcf()
     figP.canvas.manager.set_window_title('Distributions des genes et des intergenes')
     plt.pie(values1,labels=Names1,autopct="%.1f%%",wedgeprops={'edgecolor':'white', 'linewidth':2},colors=col)
     plt.title('Pourcentage des genes et intergenes')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./Figures/pieGeneInter.png")
          plt.close()


def generateBoxplot1(show,save) :

     figB1 = pylab.gcf()
     figB1.canvas.manager.set_window_title('Boxplot des genes et des intergenes')
     a = pd.DataFrame({ '' : np.repeat('Genes',len(geneTInt)), 'value': geneTInt })
     b = pd.DataFrame({ '' : np.repeat('Intergenes',len(interListBoth)), 'value': interListBoth })
     df=a.append(b)
     my_pal2 = {"Genes": "olive", "Intergenes": "yellowgreen"}
     sns.boxplot(x='', y='value', data=df,showmeans=True,palette=my_pal2)
     plt.title('Comparaison de taille entre genes et intergenes')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./Figures/box1.png")
          plt.close()
     return 

def generateBoxplot2(show,save) : 

     figB2 = pylab.gcf()
     figB2.canvas.manager.set_window_title('Boxplot des exons et des introns')
     c = pd.DataFrame({ '' : np.repeat('Exons',len(exonTInt)), 'value': exonTInt })
     d = pd.DataFrame({ '' : np.repeat('Introns',len(intronTInt)), 'value':intronTInt })
     df=c.append(d)
     
     my_pal1 = {"Exons": "darksalmon", "Introns": "firebrick"}
     sns.boxplot(x='', y='value', data=df,showmeans=True,palette=my_pal1)
     plt.title('Comparaison de taille entre exons et introns')
     if show == 1 :
          plt.show()
     if save == 1 : 
          plt.savefig("./Figures/box2.png")
          plt.close()

def generateGraphFunc (window,resultsFrame,selectedRegion):

     if selectedRegion.cget("text") == "Aucune région sélectionnée" or selectedRegion.cget("text") == "" : 
          messagebox.showwarning("Selection de région","Veuillez sélectionner une région")
     else :
          for widget in resultsFrame.winfo_children() :
               widget.destroy()
          
          window.geometry("730x550+350+0")

          mainTitle = ttk.Label(resultsFrame,text="Generation des graphes",foreground="black")
          mainTitle.grid(column=0,row=0,pady=15,columnspan=3)

          barTitle = ttk.Label(resultsFrame,text="Distribution des tailles",foreground="black")
          barTitle.grid(column=0,row=1,padx=20,pady=5)

          pieTitle = ttk.Label(resultsFrame,text="Proportions",foreground="black")
          pieTitle.grid(column=1,row=1,padx=20,pady=5)

          boxTitle = ttk.Label(resultsFrame,text="Comparaison des distributions",foreground="black")
          boxTitle.grid(column=2,row=1,padx=20,pady=5)

          co= sqlite3.connect(fs.dbName)
          c = co.cursor()


          global exonT
          exonT= c.execute("SELECT end-start from features WHERE featuretype = 'exon' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          
          global exonTInt
          exonTInt = []
          for exonLength in exonT :
               exonTInt.append(exonLength[0])


          global exonPositions 
          exonPositions = []
          for position in range(1,len(exonT)+1): 
               exonPositions.append(position)

          global sumExons
          sumExons = 0
          for e in exonTInt :
               sumExons += e
          

          geneT= c.execute("SELECT end-start from features WHERE featuretype = 'gene' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

          global geneTInt
          geneTInt = []
          for geneLength in geneT :
               geneTInt.append(geneLength[0])

          global genePositions
          genePositions = []
          for position in range(1,len(geneT)+1): 
               genePositions.append(position)

          global sumGenes
          sumGenes = 0
          for g in geneTInt :
               sumGenes+= g
          #print(sumGenes)


          global intronT
          intronT= c.execute("SELECT end-start from features WHERE featuretype ='intron' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

          global intronTInt
          intronTInt = []
          for intronLength in intronT :
               intronTInt.append(intronLength[0])
          
          global intronPositions
          intronPositions = []
          for position in range(1,len(intronT)+1): 
               intronPositions.append(position)

          global sumIntrons
          sumIntrons = 0
          for s in intronTInt :
               sumIntrons += s    

          global startGenePlus
          startGenePlus = c.execute("SELECT start from features WHERE featuretype ='gene' and strand = '+' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

          global endGenePlus
          endGenePlus= c.execute("SELECT end from features WHERE featuretype ='gene' and strand = '+' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
          
          interArrayPlus = np.column_stack((startGenePlus,endGenePlus))

          global interListPlus
          interListPlus = []
          for inter in range (1,len(interArrayPlus)) :
               if interArrayPlus[inter,0] - interArrayPlus[inter-1,1] < 0 :
                    continue
               else :
                    interListPlus.append(interArrayPlus[inter,0] - interArrayPlus[inter-1,1])

          
          global interPositionsPlus
          interPositionsPlus = []
          for interStart in range(1,len(interListPlus)+1) : 
               interPositionsPlus.append(interStart)

     
          global startGeneMinus
          startGeneMinus= c.execute("SELECT start from features WHERE featuretype ='gene' and strand = '-' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

          global endGeneMinus 
          endGeneMinus= c.execute("SELECT end from features WHERE featuretype ='gene' and strand = '-' and seqid='%s' and start >=%s and end<=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()

          interArrayMinus = np.column_stack((startGeneMinus,endGeneMinus))

          global interListMinus
          interListMinus = []
          for inter in range (1,len(interArrayMinus)) :
               if interArrayMinus[inter,0] - interArrayMinus[inter-1,1] < 0 :
                    continue
               else : 
                    interListMinus.append(interArrayMinus[inter,0] - interArrayMinus[inter-1,1])
          

          global interListBoth
          interListBoth = interListPlus + interListMinus 


          global sumInter
          sumInter = 0
          for v in interListBoth :
               sumInter+= v
   
          global interPielist
          interPielist = len(interListBoth)
 

          global interPositionsBoth
          interPositionsBoth = []
          for i in range(1,len(interListBoth)+1) : 
               interPositionsBoth.append(i)
  

          co.commit()
          c.close()
          co.close()

          gene_Button = ttk.Button(resultsFrame,text="Genes",command= lambda  : generateGraphGene(1,0))
          gene_Button.grid(column=0,row=2,pady=10,padx=25)

          inter_Button = ttk.Button(resultsFrame,text="Intergenes",command= lambda : generateGraphInter(1,0))
          inter_Button.grid(column=0,row=3,pady=10,padx=25)

          exon_Button = ttk.Button(resultsFrame,text="Exons",command= lambda : generateGraphExon(1,0))
          exon_Button.grid(column=0,row=4,pady=10,padx=25)

          intron_Button = ttk.Button(resultsFrame,text="Introns",command= lambda : generateGraphIntron(1,0))
          intron_Button.grid(column=0,row=5,pady=10,padx=25)

          pie2_Button = ttk.Radiobutton(resultsFrame,text='Genes/Intergenes',command= lambda : generatePiechartGenesIntergeniques(1,0))
          pie2_Button.grid(column=1,row=2,padx=30,ipady= 25,sticky=W,rowspan=2) 

          pie1_Button = ttk.Radiobutton(resultsFrame,text='Exons/Introns',command= lambda :generatePiechartExonsIntrons(1,0))
          pie1_Button.grid(column=1,row=4,padx=30,ipady= 25,sticky=W,rowspan=2) 

          box1_Button = ttk.Button(resultsFrame,text='Boxplot G/I',command= lambda : generateBoxplot1(1,0))
          box1_Button.grid(column=2,row=2,padx=20,pady=5,rowspan=2)

          box2_Button = ttk.Button(resultsFrame,text='Boxplot E/I',command=lambda : generateBoxplot2(1,0))
          box2_Button.grid(column=2,row=4,padx=20,pady=5,rowspan=2)



     return