def transform(pixel, centerra, centerdec, angle, arcsecperpix):
    result = [0,0]
    amatrix = [[cos(angle),sin(angle)], [-sin(angle),cos(angle)]]
    xmatrix = [[pixel[0]],[pixel[1]]]
    bmatrix = amatrix * xmatrix
    if bmatrix[0] < centerra:
        result[0] = centerra + (arcsecperpix * bmatrix[0])
    if bmatrix[0] > centerra:
        result[0] = centerra - (arcsecperpix * bmatrix[0])
    if bmatrix[1] < centerdec:
        result[1] = centerdec - (arcsecperpix * bmatrix[1])
    if bmatrix[1] > centerdec:
        result[1] = centerdec + (arcsecperpix * bmatrix[1])
    return result
