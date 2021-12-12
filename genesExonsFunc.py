import fileSelectFunc as fs
import urlEntryFunc as ue
import regionFunc as rf
import generateGraphFunc as gg
import generateStatFunc as gs
import tkinter as tk
from tkinter import StringVar, filedialog
from tkinter.constants import ANCHOR, CENTER, E, LEFT, NS, NSEW, RAISED, RIGHT, VERTICAL, W, Y
import wget
import validators
from glob import glob
import os
import numpy as np 
import matplotlib.pyplot as plt
import  gffutils
from gffutils.create import create_db
from pathlib import Path
import sqlite3
import pandas as pd
from fileSelectFunc import *
import tkinter.ttk as ttk 
import ttkthemes as themes
from tkinter import messagebox

def getPlus():
     """
     Retrieves number of genes and exons in the + strand inside selected chromosome region from the database.
     Modifies labels geneResult and exonResult text values to show retrieved numbers.
     """

     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()

     numberGenesList = cur.execute("SELECT count(start) FROM features WHERE featuretype='gene' and strand = '+' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberGenes = numberGenesList[0][0]
  
     numberExonsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='exon' and strand = '+' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberExons = numberExonsList[0][0]
         
     numberIntronsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='intron' and strand = '+' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberIntrons = numberIntronsList[0][0]

     con.commit()
     cur.close()
     con.close()
     return numberGenes,numberExons,numberIntrons

def getMinus():
     """
     Retrieves number of genes and exons in the - strand inside selected chromosome region from the database.
     Modifies labels geneResult and exonResult text values to show retrieved numbers.
     """
     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()

     numberGenesList = cur.execute("SELECT count(start) FROM features WHERE featuretype='gene' and strand = '-' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberGenes = numberGenesList[0][0]

     numberExonsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='exon' and strand = '-' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberExons = numberExonsList[0][0]

     numberIntronsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='intron' and strand = '-' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberIntrons = numberIntronsList[0][0]

     con.commit()
     cur.close()
     con.close()
     return numberGenes,numberExons,numberIntrons

def getBoth():
     """
     Retrieves number of genes and exons in both strands inside selected chromosome region from the database.
     Modifies labels geneResult and exonResult text values to show retrieved numbers.
     """

     con = sqlite3.connect(fs.dbName)
     cur = con.cursor()
               
     numberGenesList = cur.execute("SELECT count(start) FROM features WHERE featuretype='gene' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberGenes = numberGenesList[0][0]
    
     numberExonsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='exon' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberExons = numberExonsList[0][0]

     numberIntronsList = cur.execute("SELECT count(start) FROM features WHERE featuretype='intron' and seqid = '%s' and start>=%s and end <=%s"%(rf.chrSelected,rf.startSelected,rf.endSelected)).fetchall()
     numberIntrons = numberIntronsList[0][0]

     con.commit()
     cur.close()
     con.close()     
     return numberGenes,numberExons,numberIntrons

def genesExonsFunc(window,resultsFrame,selectedRegion):
     """
     Verifies if a chromosome region is selected : 
     * Case 1 : no region is selected 
     => Shows messagebox with warning to select a region 
     * Case 2 : a region is selected
     => Creates strand selection buttons inside resultsFrame in main program window
     """
     if selectedRegion.cget("text") == "Aucune région sélectionnée" or selectedRegion.cget("text") == "" : 
          messagebox.showwarning("Selection de région","Veuillez sélectionner une région")
     else :
          for widget in resultsFrame.winfo_children() :
               widget.destroy()
          
          window.geometry("730x450+350+0")

          genesExonsTitle = ttk.Label(resultsFrame,text="Nombre de gènes et d'exons",foreground="black")
          genesExonsTitle.grid(column=0,row=0,pady=15,columnspan=4)
          #Create treeview widget
          numbersTab = ttk.Treeview(resultsFrame,height=3)
          

          plusGenes,plusExons,plusIntrons=getPlus()
          minusGenes,minusExons,minusIntrons=getMinus()
          bothGenes,bothExons,bothIntrons=getBoth()

          #Define columns
          numbersTab["columns"] = ("Genes","Exons","Introns")
          #Format columns
          numbersTab.column("#0",anchor=CENTER,width=120,minwidth=120)
          numbersTab.column("Genes",anchor=CENTER,width=120,minwidth=120)
          numbersTab.column("Exons",anchor=CENTER,width=120,minwidth=120)
          numbersTab.column("Introns",anchor=CENTER,width=120,minwidth=120)
          #Create headings
          numbersTab.heading("#0",text="",anchor=CENTER)
          numbersTab.heading("Genes",text="Genes",anchor=CENTER)
          numbersTab.heading("Exons",text="Exons",anchor=CENTER)
          numbersTab.heading("Introns",text="Introns",anchor=CENTER)
          #Insert values
          numbersTab.insert(parent="",index='end',iid=0,text="Brin +",value=(plusGenes,plusExons,plusIntrons))
          numbersTab.insert(parent="",index='end',iid=1,text="Brin -",value=(minusGenes,minusExons,minusIntrons))
          numbersTab.insert(parent="",index='end',iid=2,text="2 Brins",value=(bothGenes,bothExons,bothIntrons))

          numbersTab.grid(column=0,row=1,rowspan=1,columnspan=4)

     return