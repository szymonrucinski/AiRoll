def findLocalMaximaMinima(n, arr):  
    mx = []  
    mn = []  
  
    # Checking whether the first point is  
    # local maxima or minima or neither  
    if(arr[0][1] > arr[1][1]):  
        mx.append(arr[0])  
    elif(arr[0][1] < arr[1][1]):  
        mn.append(arr[0])  
  
    # Iterating over all points to check  
    # local maxima and local minima  
    for i in range(1, n-1):  
  
        # Condition for local minima  
        if(arr[i-1][1] > arr[i][1] < arr[i + 1][1]):  
            mn.append(arr[i])  
  
        # Condition for local maxima  
        elif(arr[i-1][1] < arr[i][1] > arr[i + 1][1]):  
            mx.append(arr[i])  
  
    # Checking whether the last point is  
    # local maxima or minima or neither  
    if(arr[-1][1] > arr[-2][1]):  
        mx.append(arr[n-1])  
    elif(arr[-1][1] < arr[-2][1]):  
        mn.append(arr[n-1])  
  
        # Print all the local maxima and  
    print(mn)
    print(mx)
    return mx