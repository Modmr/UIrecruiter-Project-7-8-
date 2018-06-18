import fpdf
from fpdf import FPDF



pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial','B',12)
pdf.cell(0,10,"REPORT",0,1,'C')


def AddPage():
    pdf.add_page()

def Write(text):
    pdf.set_font('Arial','',11)
    pdf.cell(40,10,text,0,2,'L')
    
def WriteHeader(text):
    pdf.set_font('Arial','B',12)    
    pdf.cell(40,10,text,0,2,'L')
    

def OutputPDF():
    pdf.output('reports//Report.pdf','F')
    