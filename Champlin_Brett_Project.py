import sys
import numpy as np
import math

from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox

from mplcanvas import MatplotlibCanvas

class Form(QLabel) :

    def __init__(self, parent=None) :
        super(Form, self).__init__(parent)

        # Define three text boxes, one each for f(x), the value x, and
        # the output.  I've done the first for you.
        

        self.cb1 = QComboBox()
        self.cb1.setEditable(True)
        self.cb1.addItems(["Material", "ANSI 1010", "ANSI 1020", "ANSI 1030", "ANSI 1035", "ANSI 1040", "ANSI 1045", "ANSI 1050", "ANSI 1060", "ANSI 1095"])

        self.cb2 = QComboBox()
        self.cb2.setEditable(True)
        self.cb2.addItems(["Hot Rolled", "Cold Rolled"])
        
        self.cb3 = QComboBox()
        self.cb3.setEditable(True)
        self.cb3.addItems(["Type of Loading", 'Bending', 'Axial', 'Pure Torsion'])
        
        self.cb4 = QComboBox()
        self.cb4.setEditable(True)
        self.cb4.addItems(["Reliability Percentage", '50', '90', '95', '99', '99.9', '99.99', '99.999', '99.9999'])
        
        self.cb5 = QComboBox()
        self.cb5.setEditable(True)
        self.cb5.addItems(["Type of Surface", 'Ground', 'Machined', 'Cold-Rolled', 'Hot-Rolled', 'As-Forged'])
        
        
        
        #        self.cb.currentIndexChanged.connect(self.updateUI) # What does selectAll() do?

        # Step 1. Add box for "x"
        self.value_edit = QLineEdit(" ")
        self.value_edit.selectAll()
        
        self.value_edit1 = QLineEdit(" ")
        self.value_edit.selectAll()
        
        self.value_edit2 = QLineEdit(" ")
        self.value_edit2.selectAll()

        # Step 2. Add box for "output"
        self.output_edit = QLineEdit(" ")
        self.output_edit.selectAll()
        
        self.label1 = QLabel("Material")
        self.label2 = QLabel("Diameter (mm)")
        self.label3 = QLabel("Temperature (C)")
        self.label4 = QLabel("Max Stress (MPa)")
        self.label5 = QLabel("Number of Cycles")
        
        self.plot = MatplotlibCanvas()
        # Step 3. How do we combine these widgets?  Use a *layout*....
        layout = QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.cb1)
        layout.addWidget(self.cb2)
        layout.addWidget(self.cb3)
        layout.addWidget(self.cb4)
        layout.addWidget(self.cb5)
        layout.addWidget(self.label2)
        layout.addWidget(self.value_edit)
        layout.addWidget(self.label3)
        layout.addWidget(self.value_edit1)
        layout.addWidget(self.label4)
        layout.addWidget(self.value_edit2)
        layout.addWidget(self.label5)
        layout.addWidget(self.output_edit)
        self.setLayout(layout)
        

        # Step 4. Make sure the function box is the default one active.
        
        self.cb1.activated

        # Step 5. Connect updateUI to the event that one returns while the 
        #         output box is active
        
        self.output_edit.returnPressed.connect(self.updateUI)

        # Step 6. Implement updateUI.

        # Step 7. Give the GUI a title.
        
        self.setWindowTitle("Number of Cycles Calculator for Steels")
 

    def updateUI(self) :
        """ Method for updating the user interface.

        This is called whenever an event triggers an update.  Specifically,
        this event is when the return key is pressed when the output box
        is active.  The result of this method should be to show the 
        resulting function value (f of x) in the output box."""

        mat = self.cb1.currentText()
        form = self.cb2.currentText()
        load = self.cb3.currentText()
        rel = self.cb4.currentText()
        surf = self.cb5.currentText()
        dia = float(self.value_edit.text())
        temp = float(self.value_edit1.text())
        stress = float(self.value_edit2.text())
        
        if form=="Hot Rolled":
            if mat=='ANSI 1010':
                Sut = 324.0
            elif mat=='ANSI 1020':
                Sut = 379.0
            elif mat=='ANSI 1030':
                Sut = 469.0
            elif mat=='ANSI 1035':
                Sut = 496.0
            elif mat=='ANSI 1040':
                Sut = 524.0
            elif mat=='ANSI 1045':
                Sut = 565.0
            elif mat=='ANSI 1050':
                Sut = 621.0
            elif mat=='ANSI 1060':
                Sut = 676.0
            elif mat=='ANSI 1095':
                Sut = 827.0
        elif form=="Cold Rolled":
            if mat=='ANSI 1010':
                Sut = 365.0
            elif mat=='ANSI 1020':
                Sut = 469.0
            elif mat=='ANSI 1030':
                Sut = 524.0
            elif mat=='ANSI 1035':
                Sut = 552.0
            elif mat=='ANSI 1040':
                Sut = 586.0
            elif mat=='ANSI 1045':
                Sut = 627.0
            elif mat=='ANSI 1050':
                Sut = 689.0
        
        Seprime = (0.5 * Sut)
        
        if load=="Bending":
            Cload = 1.0
            Sm = (0.9 * Sut)
        elif load=="Axial":
            Cload = 0.7
            Sm = (0.75 * Sut)
        elif load=="Pure Torsion":
            Cload = 1.0
            Sm = Sut
            
        if temp <= 450:
            Ctemp = 1.0
        elif temp > 450:
            dT = temp - 450.0
            dC = (0.0058*dT)
            Ctemp = (1.0 - dC)
        
        if rel=="50":
            Crel = 1.0
        elif rel=="90":
            Crel = 0.897
        elif rel=="95":
            Crel = 0.868
        elif rel=="99":
            Crel = 0.814
        elif rel=="99.9":
            Crel = 0.753
        elif rel=="99.99":
            Crel = 0.702
        elif rel=="99.999":
            Crel = 0.659
        elif rel=="99.9999":
            Crel = 0.620
            
        if load == "Bending":
            if dia <= 8:
                Csize = 1.0
            elif dia in range(8,250):
                exp = (dia ** -0.097)
                Csize = (exp * 0.869)
            elif dia > 250:
                Csize = 0.6
        else:
            Csize = 1
            
        if surf == "Ground":
            A = 1.58
            b = -0.085
            exp2 = (Sut ** b)
            Csurf = (A * exp2)
        elif surf == "Machined":
            A = 4.51
            b = -0.265
            exp2 = (Sut ** b)
            Csurf = (A * exp2)
        elif surf == "Cold Rolled":
            A = 4.51
            b = -0.265
            exp2 = (Sut ** b)
            Csurf = (A * exp2)
        elif surf == "Hot Rolled":
            A = 57.7
            b = -0.718
            exp2 = (Sut ** b)
            Csurf = (A * exp2)
        elif surf == "As Forged":
            A = 272.0
            b = -0.995
            exp2 = (Sut ** b)
            Csurf = (A * exp2)
            
        Se = (Cload * Csize * Csurf * Ctemp * Crel * Seprime)
        
        if stress <= Se:
            self.output_edit.setText("Infinite Life")
        elif stress > Sm:
            self.output_edit.setText("Member Does not last 1000 cycles")
        else:
            log1 = math.log10(Sm/Se)
            log2 = math.log10(1000)
            log3 = math.log10(1000000)
            den = (log2 - log3)
            b = (log1/den)
            log4 = math.log10(Sm)
            c = (3.0 * b)
            d = (log4 - c)
            a = (10.0 ** d)
            e = (1.0/b)
            SN = (stress/a)
            N = (SN ** e)
            z = str(int(N))
            self.output_edit.setText(z)
        
        
#        x = float(s)
#        x = np.fromstring(s, dtype=int, sep=',')
#        
#        y = eval(p)
#        z = str(y).strip('[]')
#        self.output_edit.setText(str(z))
#        f = open("data.txt", "w")
#        f.write(str(p) + "" + str(x) + "\n")
#        f.close()

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
