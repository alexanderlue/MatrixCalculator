"""This module provides a basic Matrix data type with all associated 
operations (+, -, *, and **). Matrices are represented as 2-dimensional 
lists of floats or integers. Other methods include: construct(),copy(),
edit(), ref(), rref(), transpose()
"""
class Matrix:

    #Matrix Constructor initializes empty 0 matrix
    def __init__(self, rows, cols):
        if(rows<=0 or cols<=0):
            stringErr='Cannot create 0 or negetive matrix'
            print(stringErr)
        else:
            self.matrix = []
            self.rows = rows
            self.cols = cols
            for x in range(rows):
                self.matrix.append([0])
                for y in range(cols-1):
                    self.matrix[x].append(0)

    #Construct with values
    def construct(self):
        for row in range(self.rows):
            while True:
                colVal = input('row '+ str(row+1) + ': ')
                #print(colVal)
                colList = colVal.split()
                if(len(colList)==self.cols):
                    colList = [self.__cast(float(x)) for x in colList]
                    print(colList)
                    for col in range(self.cols):
                        self.__change(row,col,colList[col])
                    break
                else:
                    print('Each row has '+str(self.cols)+' values.')
            
        
    #User method to edit Matrix values
    def edit(self, x, y, newval):
        if(isinstance(newval, str)):
           return('Cannot have string values in matrix')
        self.__change(x-1,y-1,newval)

    #Private method to edit Matrix value
    def __change(self, x, y, newval):
        if((x>=self.rows or x<0) or (y>=self.cols or y<0)):
            stringErr='Cannot find row: ' + str(x) + ' column: '+ str(y)
            print(stringErr)
        else:
            self.matrix[x][y] = self.__cast(newval)

    #private method: cast value as int or float(2 decimals)
    def __cast(self, value):
        if(int(float(value))==value):
            return int(float(value))
        else:
            return round(value, 2)

    #swap two rows
    def __swap(self, rA, rB, g=0):
        if((rA<0 or rA>=self.rows) or (rB<0 or rB>=self.rows)):
            return('Must be a row index')
        if g==1:
            print('R'+str(rA+1)+' <-> R'+str(rB+1)+':')
        for x in range(self.cols):
            rAtemp = self.matrix[rA][x]
            self.__change(rA,x,self.matrix[rB][x])
            self.__change(rB,x,rAtemp)

    #Private Method: Scalar Add rA + rB*c -> rA (rA & rB are indices)
    def __scalarAdd(self, rA, rB, c, g=0):
        if g==1:
            print(str(self.__cast(c))+'*R'+str(rB+1)+' + R'+str(rA+1)+' -> R'+str(rA+1)+':') 
        rowA = self.matrix[rA]
        for x in range(self.cols):
            rowA[x]+=self.matrix[rB][x]*c
            self.__change(rA,x,rowA[x])

    #Private Method: Scalar multiply row rA*c -> rA
    def __scalarRow(self, rA, c, g=0):
        if g==1:
            print(str(self.__cast(c))+'*R'+str(rA+1)+' -> R'+str(rA+1)+':')
        for x in range(self.cols):
            self.__change(rA, x, self.matrix[rA][x]*c)

    #add matrices
    def __add__(self, B):
        if(B.rows!=self.rows or B.cols!=self.cols):
            StringErr='Cannot add matrices of different dimensions'
            return(StringErr)
        else:
            C = Matrix(self.rows, self.cols)
            for x in range(self.rows):
                for y in range(self.cols):
                    sumN = B.matrix[x][y]+self.matrix[x][y]
                    C.__change(x,y,sumN)
            return(C)

    #subtract matrices
    def __sub__(self,B):
        if(B.rows!=self.rows or B.cols!=self.cols):
            StringErr='Cannot subtract matrices of different dimensions'
            return(StringErr)
        A = B*-1
        C = self + A
        return(C)

    #multiply matrices and scalars, return resulting matrix
    def __mul__(self, V):
        #if scalar multiple
        if(isinstance(V, int) or isinstance(V,float)):
            C = Matrix(self.rows, self.cols)
            for x in range(self.rows):
                for y in range(self.cols):
                    scale = V*self.matrix[x][y]
                    C.__change(x,y,scale)
            return(C)
        #if matrix
        if(isinstance(V, Matrix)):
            if(self.cols != V.rows):
                stringErr='Cannot multiply matrices'
                return(stringErr)
            else:
                #return('ADD Matrix Mult Here')
                C = V.copy()
                C.transpose()
                M = Matrix(self.rows, V.cols)
                for row in range(self.rows):
                    for col in range(V.cols):
                        multSum=0
                        for x in range(self.cols):
                            multSum+=(self.matrix[row][x]*C.matrix[col][x])
                        M.__change(row,col,multSum)
                return(M)

    def __pow__(self, intVal):
        if(not isinstance(intVal, int)):
           return('Only positive interger value exponents')
        elif(intVal<=0):
            return('Only positive interger value exponents')
        elif(self.rows!=self.cols):
            return('Only square matrices')
        else:
            Pow = self.copy()
            for x in range(intVal-1):
                Pow*=self
            return(Pow)
    #copies matrix returns new matrix
    def copy(self):
        B = Matrix(self.rows, self.cols)
        for x in range(self.rows):
            for y in range(self.cols):
                B.__change(x,y,self.matrix[x][y])
        return(B)

    #clear matrix
    def __clear(self):
        self.matrix[:]=[]
        for x in range(self.rows):
            self.matrix.append([0])
            for y in range(self.cols-1):
                self.matrix[x].append(0)

    #transpose current matrix
    def transpose(self):
        B = self.copy()
        self.rows = B.cols
        self.cols = B.rows
        self.__clear()
        for x in range(self.rows):
            for y in range(self.cols):
                self.__change(x,y,B.matrix[y][x])

    #Returns Row Echelon Form of Matrix
    def ref(self, g=0):
        A=self.copy()
        if g==1:
            print('Steps for Row Echelon Form: \n(Original)')
            print(A)
        rowcnt,colcnt,cnt = 0,0,1
        while(rowcnt<A.rows and colcnt<A.cols):
            valueIndex=-1
            for row in range(rowcnt, A.rows):
                if A.matrix[row][colcnt]!=0:
                    valueIndex=row
                if valueIndex!=-1:
                    break
            if valueIndex!=-1:
                #Swap to top to make pivot and divide to get 1
                if rowcnt!=valueIndex:
                    if g==1:
                        print(str(cnt)+'. ',end='')
                        cnt+=1
                    A.__swap(rowcnt,valueIndex, g)
                    if g==1: print(A)
                if g==1:
                    print(str(cnt)+'. ',end='')
                    cnt+=1
                A.__scalarRow(rowcnt,(A.matrix[rowcnt][colcnt])**-1, g)
                if g==1:
                    print(A)
                #for loop to make lower triangle matrix zero
                for x in range(rowcnt+1, A.rows):
                    if A.matrix[x][colcnt]!=0:
                        if g==1:
                            print(str(cnt)+'. ',end='')
                            cnt+=1
                        A.__scalarAdd(x, rowcnt,-(A.matrix[x][colcnt]), g)
                        if g==1:
                            print(A)
                rowcnt+=1
            colcnt+=1
        return(A)
    
    #Returns Reduced Row Echelon Form of Matrix
    def rref(self, g=0):
        A=self.copy()
        if g==1:
            print('Steps for Reduced Row Echelon Form: \n(Original)')
            print(A)
        rowcnt,colcnt,cnt = 0,0,1
        while(rowcnt<A.rows and colcnt<A.cols):
            valueIndex=-1
            for row in range(rowcnt, A.rows):
                if A.matrix[row][colcnt]!=0:
                    valueIndex=row
                if valueIndex!=-1:
                    break
            if valueIndex!=-1:
                #Swap to top to make pivot and divide to get 1
                if rowcnt!=valueIndex:
                    if g==1:
                        print(str(cnt)+'. ',end='')
                        cnt+=1
                    A.__swap(rowcnt,valueIndex, g)
                    if g==1: print(A)
                if g==1:
                    print(str(cnt)+'. ',end='')
                    cnt+=1
                A.__scalarRow(rowcnt,(A.matrix[rowcnt][colcnt])**-1, g)
                if g==1:
                    print(A)
                #for loop to make zero values
                for x in range(A.rows):
                    if A.matrix[x][colcnt]!=0 and x!=rowcnt:
                        if g==1:
                            print(str(cnt)+'. ',end='')
                            cnt+=1
                        A.__scalarAdd(x, rowcnt,-(A.matrix[x][colcnt]), g)
                        if g==1:
                            print(A)
                rowcnt+=1
            colcnt+=1
        return(A)
            
    #toString override
    def __str__(self):
        stringv=''
        for x in range(self.rows):
            stringv+='['
            for y in range(self.cols):
                if y==len(self.matrix[x])-1:
                    stringv+=str(self.matrix[x][y])
                else:
                    stringv+=str(self.matrix[x][y])+' '
            stringv+=']\n'
        return(stringv)

    #Matrices representation in python Shell
    def __repr__(self):
        stringv=''
        for x in range(self.rows):
            stringv+='['
            for y in range(self.cols):
                if y==len(self.matrix[x])-1:
                    stringv+=str(self.matrix[x][y])
                else:
                    stringv+=str(self.matrix[x][y])+' '
            stringv+=']\n'
        return(stringv)
