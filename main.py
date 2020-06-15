# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 13:24:32 2020

@author: Mateo Toquica Arango
"""
import csv
import numpy as np

def readFile(path):
    """
    Read a csv file.
    
    This function read a csv file thanks to the library csv, the library must be already imported

    Parameters
    ----------
    path : string 
        This path should has the path of the csv file.

    Returns
    -------
    tmp : list
        List of list where we can find the information of the csv file.

    """
    tmp = []
    with open(path, encoding="utf-8-sig") as File:  
        reader = csv.reader(File,delimiter=';')
        for row in reader:
            tmp.append(row)                
        return tmp
    
def deleteTitles(array, index, pos):
    """
    Delete rows and columns from an array.
    
    This function is made to delete the rows and columns from an array.

    Parameters
    ----------
    array : ndarray
        Must contain a ndarray.
    index : int
        This must contain 0 if you want to delete rows and columns, 1 if you want delete rows and 2 if you want to delete columns.
    pos : int
        This must contain the position to delete the row, the column or the row and column.

    Returns
    -------
    aux : ndarray
        This contain the same array but without the position that you already deleted.

    """
    if(index == 0):
        aux = np.delete(array, pos, 1)
        aux = np.delete(aux, pos, 0)       
    if(index == 1):
        aux = np.delete(array, pos, 1)
    if(index == 2):
        aux = np.delete(array, pos, 0)
    return aux

def matrixNormalized(array):
    """
    Make a normalization with an array

    Parameters
    ----------
    array : ndarray
        Contain an array.

    Returns
    -------
    divideArray : ndarray
        return an array.

    """
    floatArray = transformIntoFloat(array)
    sumArray = summary(floatArray, 0)
    divideArray = np.divide(floatArray, sumArray)        
    return divideArray

def transformIntoFloat(array):
    """
    Transform a int type to a float type.

    Parameters
    ----------
    array : ndarray
        contain an array.

    Returns
    -------
    ndarray
        return the array of float type.

    """
    return array.astype(np.float)

def summary(array, index):
    """
    make the sum of a rows or columns

    Parameters
    ----------
    array : ndarray
        ndarray that contain float type.
    index : int
        this must contain 0 if you want to sum the column, 1 if you sum the rows and None if you want sum everything.

    Returns
    -------
    ndarray
        sum of values.

    """
    return np.sum(array, axis = index)

def averageRow(array, index):
    """
    Contain the mean of an array

    Parameters
    ----------
    array : ndarray
        this contain the ndarray of float values.
    index : contain 
        this must contain 0 if you want to sum the column, 1 if you sum the rows and None if you want sum everything.

    Returns
    -------
    ndarray
        sum of values.

    """
    return np.mean(array, axis=index)

def multArray(array1, array2):
    """
    make the multiplication betwetn 2 ndarray

    Parameters
    ----------
    array1 : array number 1
        ndarray of floats.
    array2 : array number 2
        ndarray of floats.

    Returns
    -------
    ndarray
        this return the multiplication.

    """
    return array1*array2

def ci(index, lambdaMax):
    """
    Make the ci analysis.

    Parameters
    ----------
    index : int
        the number of applicants.
    lambdaMax : float
        The lambdaMax value.

    Returns
    -------
    float
        Return the abalysis.

    """
    return ((lambdaMax-index)/(index-1))
    
def consistencyRatio(arrayRi, index, ciValue):
    """
    make the analysis to the consistency ratio

    Parameters
    ----------
    arrayRi : array
        Must contain the table of RI.
    index : int
        the number of applicants.
    ciValue : float
        contain the ci value.

    Returns
    -------
    float
        return the value of consistency ratio.

    """
    riValue = arrayRi[index-1]
    return ciValue/riValue[0]

def readCsv3D(M, N):
    """
    Read multiple csv files.

    Parameters
    ----------
    M : int
        the number of matrices that you will load.
    N : int
        the values of the rows and columns of the matrices.

    Returns
    -------
    arrayElements : ndarray
        return a list o matrices.

    """
    arrayElements = np.zeros((M, N, N))
    cont = 0
    while M > cont:
        try:
            pathFulano = input("Enter the file of the variables: \n")
            arrayFulanoTitle = np.array(readFile('resources/'+pathFulano))
            arrayFulano = transformIntoFloat(deleteTitles(arrayFulanoTitle, 0, 0))
            arrayElements[cont] = arrayFulano 
            cont += 1
            
        except:
            print("Ops, little error here.")  
    
    return arrayElements
def normalized3Darray(array3d):
    """
    This function is to analyise the  normalized matrices from a list.

    Parameters
    ----------
    array3d : ndarray
        The list o matrices.

    Returns
    -------
    themeNorm : ndarray
        the list o matrices that contain the values of the normalized.

    """
    cont = 0
    themeNorm = np.copy(array3d)
    while cont < len(array3d):
        
        themeNorm[cont] = matrixNormalized(array3d[cont])
        cont += 1
    
    return themeNorm
def priorityMatrix3D(array3D, col, row):
    """
    calculate the priority value from a list of matrices.

    Parameters
    ----------
    array3D : ndarray
        List of matrices.
    col : int
        the number of variables.
    row : int
        the number of candidates.

    Returns
    -------
    themeMat : array
        return the priority matrix.

    """
    cont = 0
    themeMat = np.zeros((col, row))
    while cont < len(array3D):
        critWeight = averageRow(array3D[cont], 1)
        themeMat[cont] = critWeight
        cont += 1
    return themeMat
def priorityxOriginal(arrayPriority, array3D):
    """
    Multiply the original matrix with the priority matrix

    Parameters
    ----------
    arrayPriority : array
        priority matrix.
    array3D : array
        Original matrix.

    Returns
    -------
    tmp : array
        the values of the multiplication.

    """
    cont = 0
    tmp = np.copy(array3D)
    while cont < len(arrayPriority):
        tmp[cont] = arrayPriority[cont]*array3D[cont]
        cont += 1
    return tmp
def weightedSumValue2d(priorityPerOri, col, row):
    """
    make the weighetd sum value.

    Parameters
    ----------
    priorityPerOri : array
        the matrix of values of the multiplication the original matrix with the priority matrix.
    col : int
        the number of variables.
    row : int
        the number of candidates.

    Returns
    -------
    tmpVal : array
        return a matrix with the values.

    """
    tmpVal = np.zeros((col, row))
    cont = 0
    limit = len(priorityPerOri)
    while cont < limit:
        valor = summary(priorityPerOri[cont], 1)
        tmpVal[cont] = valor
        cont += 1
    return tmpVal
def consistencyRatio2d(array2d, arrayRi, N, M):
    """
    make the analyisis of the consistency ratio with a list of matrices.
    
    this function gonna return 3 lists with the values in the index 0 of the mean, second in the index 1 the ci analysis and in the index 2 the value of the ri.

    Parameters
    ----------
    array2d : array
        array of weighted sum values.
    arrayRi : array
        insert the matrix with the ri values.
    N : int
        the number of candidates.
    M : int
        the number of variables.

    Returns
    -------
    tmp : array
        return a matrix with the values of ci, ri and lambdamax of the matrices.

    """
    tmp = np.zeros((3, M))
    mean = averageRow(array2d, 1)
    contador = 0
    ciquare = []
    rifin = []
    while contador < len(mean):
        ciquare.append(ci(N, mean[contador]))
        rifin.append(consistencyRatio(arrayRi, N, ciquare[contador]))
        contador += 1
    tmp[0] = mean
    tmp[1] = np.array(ciquare)
    tmp[2] = np.array(rifin)
    return tmp
def validationCR(array, cr):
    """
    Make a validation with the list of the final ri.

    Parameters
    ----------
    array : array
        list with the final ri of the candidates.
    cr : float
        float with the value to make the comparison.

    Returns
    -------
    tmp : boolean
        if all the candidates meet the requirements.

    """
    
    tmp = False
    cont = 0
    while cont < len(array[0]):
        
        if(array[2][cont] < cr):
            tmp = True
        
        cont += 1
    
    return tmp
def sensitivity(priorityVariable, priorityFul):
    """
    Give the analyisis made by the sensitivity analysis.

    Parameters
    ----------
    priorityVariable : array
        Priority matrix of the variables.
    priorityFul : array
        priority matrix of the candidates.

    Returns
    -------
    tmp : array
        gives 3 diferent values of the result of the sensitivity analydsis.

    """
    tmp = np.zeros((len(arrayCandidate), 3))
    peso = len(priorityVariable)
    tmpList = oneDiferent_restEqual(peso)
    tmpList1 = equalWeights(peso)
    tmp[0] = summary(np.multiply(priorityVariable, np.transpose(priorityFul)), 1)
    tmp[1] = summary(np.multiply(tmpList1, np.transpose(priorityFul)), 1)
    tmp[2] = summary(np.multiply(tmpList, np.transpose(priorityFul)), 1)
    
    return tmp

def equalWeights (numcols):
    """
    make a list with the same value.

    Parameters
    ----------
    numcols : int
        the number of the variables.

    Returns
    -------
    a : array
        return a list with the same value.

    """
    
    a= np.full(shape=numcols,fill_value=(1/numcols),dtype=np.float)
    return a
def oneDiferent_restEqual (numcols):
    """
    make 1 of the values higher than the others.

    Parameters
    ----------
    numcols : int
        the number of variables.

    Returns
    -------
    w : array
        return a list of the values.

    """
    y = np.full(shape=1,fill_value=0.5,dtype=np.float)
    z= np.full(shape=(numcols-1),fill_value=(0.5/(numcols-1)),dtype=np.float)
    w= np.append(y,z)
    return w
arrayCandidate = np.array([])
arrayComparison =np.array([])
arrayRi = np.array([])
while (arrayCandidate.size == 0) and (arrayComparison.size == 0) and (arrayRi.size == 0):
    try:
        pathCandidate = input("Matrix for candidates: \n")
        pathComparison = input("Matrix for your comparisons: \n")
        pathRi = input("Matrix of the value of RI: \n")
        
        arrayCandidateTitle = np.array(readFile('resources/'+pathCandidate))
        arrayComparisonTitle = np.array(readFile('resources/'+pathComparison))
        arrayRiTitle = np.array(readFile('resources/'+pathRi))
       

        arrayCandidate = transformIntoFloat(deleteTitles(arrayCandidateTitle, 0, 0))
        arrayComparison = transformIntoFloat(deleteTitles(arrayComparisonTitle, 0, 0))
        arrayRi = transformIntoFloat(deleteTitles(arrayRiTitle, 1, 0))        

    except:
        
        print ('Path not found or some problem could be happend, try again.')

matrixNorm = matrixNormalized(arrayComparison)
critWeight = averageRow(matrixNorm, 1)
priorityMatrix = multArray(arrayComparison, critWeight)
weightedSumValue = summary(priorityMatrix, 1)
finalRank = weightedSumValue/critWeight
lambdaMax = averageRow(finalRank, None)
ciValue = ci(len(arrayComparison[0]), lambdaMax)
if(len(arrayComparison) < 2):
    crValue = 0
else:        
    crValue = consistencyRatio(arrayRi, len(arrayComparison[0]), ciValue)
print("Original comparison matrix: \n", arrayComparison, '\n')
print("Original candidate matrix: \n", arrayCandidate, '\n')
print("Matrix normalized: \n", matrixNorm, '\n')
print("Criterial Weight: \n", critWeight, '\n')
print("Priority matrix: \n", priorityMatrix, '\n')
print("Summary of priority matrix: \n", weightedSumValue, '\n')
print("Final rank: \n", finalRank, '\n')
print("LambdaMax: \n", lambdaMax, '\n')
print("The value of ci: \n", ciValue, '\n')
print("The consistency ratio is: \n", crValue, "\n")
while True:
    try:
        userValCr = int(input('Insert the value of Consistency ratio, choose 0 if you want to use the standar one, choose 1 if you want to insert your own value: \n'))
        if(userValCr == 0):
            CR = 0.1
            break
        if(userValCr == 1):
            CR = int(input('Insert your value.'))
            break
    except ValueError:
        print("Choose a number.")
    else:
        print("Please select a number betwen 0 and 1")
    
if(crValue < CR):
    print("\nWe can say that here that under the estándar from concistency ratio which is less than 0.1. We can say that the concistency ratiothe matrix is reasonably consistant \n")
    
    array3DVariables = readCsv3D(len(arrayComparison), len(arrayCandidate))

    normalized3D = normalized3Darray(array3DVariables)
    priority2d = priorityMatrix3D(normalized3D, len(arrayComparison), len(arrayCandidate))
    priorityPerOri = priorityxOriginal(priority2d, array3DVariables)
    wsv2d = weightedSumValue2d(priorityPerOri, len(arrayComparison), len(arrayCandidate))    
    finalRank2d = np.divide(wsv2d, priority2d)
    ri2d = consistencyRatio2d(finalRank2d, arrayRi, len(arrayCandidate), len(arrayComparison))
    print("The lambda max for all the candidates is this: \n", ri2d[0],'\n')
    print("The consinstency index for all the candidates is this: \n", ri2d[1], '\n')
    print("the consistency ratio for all the candidates is this: \n", ri2d[2], '\n')
    if(validationCR(ri2d, CR) or len(arrayComparison) < 2):
        print("The consistency ratio from all your file are Ok. \n")
        
        sens = sensitivity(critWeight, priority2d)
        
        print("The overall priority with the priority founded before is: \n", sens[0], '\n')
        print("The overall priority with the equal priority for all is: \n", sens[1], '\n')
        print("The overall priority with the the first value with the highest value is: \n", sens[2], '\n')
    else:
        print("The Consistency ratio from one of your files isn't less than", CR)
else:
    print("The result is not as expected, therefore the analysis can only go so far.")
