def slice_data(data,amount):
    data_=[]
    length=len(data)
    block_length=int(length/amount)
    for i in range(amount-1):
        data_.append(data[i*block_length:(i+1)*block_length])
    data_.append(data[length-length%block_length:])
    return data_

    