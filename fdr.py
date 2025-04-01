def count_fdr_line(data, score_colname, decoy_colname): 
    """Function that counts at what score the fdr should be from a score distribtuion of decoys and hits.
    Work in progress
    
    """ 
    # cleanup
    data[decoy_colname] = data[decoy_colname].fillna(0).replace('+',1)
    
    # sorting data 
    data_sorted = data.sort_values(by=[score_colname], ascending=False)
    
    number_decoys = 0
    count1 = 0
    count5 = 0
    fdr_line_01 = 0
    fdr_line_05 = 0
    decoy_number1 = 0
    decoy_number5 = 0
    
    fdr = []
    for i in range(len(data_sorted)): 
        
        # adds all number together, 0 addition for non decoy and +1 addition for decoys
        number_decoys += data_sorted[decoy_colname].iloc[i]
        
        current_fdr = number_decoys / (i + 1 - number_decoys)
        
        fdr.append(current_fdr)
                                       
        if current_fdr < 0.01:  
            fdr_line_01 = data_sorted[score_colname].iloc[i]
            count1 = i
            decoy_number1 = number_decoys

        elif current_fdr < 0.05 :  
            fdr_line_05 = data_sorted[score_colname].iloc[i] 
            count5 = i
            decoy_number5 = number_decoys
            
        else: 
            continue
    
    fdr_colname = "fdr_" + score_colname 
    data_sorted[fdr_colname] = fdr 
    
    # reset index after fltering to match current order of dataframe, drop removes old index 
    hit_count_colname = "hit_count_" + score_colname 
    data_sorted = data_sorted.reset_index(drop=True)
    data_sorted[hit_count_colname] = data_sorted.index
            
    return data_sorted, fdr_line_01, fdr_line_05, count1, decoy_number1, count5, decoy_number5 