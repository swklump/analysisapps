
def parsecomments(fb_file, row_selection):

    import pandas as pd
    from itertools import tee, islice
    import xlrd
    xlrd.xlsx.ensure_elementtree_imported(False, None)
    xlrd.xlsx.Element_has_iter = True
    from collections import Counter

    sheet = xlrd.open_workbook(file_contents=fb_file).sheet_by_index(0)

    # specify folder path, file name, and read in excel file
    num_rows = sheet.nrows

    # Set up dictionary
    dict_comments = {'Commenter':[],'Comment':[],'Likes':[]}

    def check_for_ints_blanks(x, dict_comments, cell_index):
        for loop_index in range(num_rows-x-cell_index-1):
            if sheet.cell_value(x+cell_index+loop_index,0) == '':
                dict_comments['Likes'].append(0)
                break
            else:
                try:
                    test_var = int(sheet.cell_value(x+cell_index+loop_index,0))
                except Exception:
                    if loop_index == 0:
                        dict_comments['Comment'].append(sheet.cell_value(x+cell_index+loop_index,0))
                    else:
                        last_comment_index = len(dict_comments['Comment'])-1
                        dict_comments['Comment'][last_comment_index] = dict_comments['Comment'][last_comment_index] + '. ' + sheet.cell_value(x+cell_index+loop_index,0)
                else:
                    dict_comments['Likes'].append(sheet.cell_value(x+cell_index+loop_index,0))
                    break
        

    # Run main loop
    for x in range(row_selection,num_rows-2):

        #Do the first comment
        if x == row_selection:
            dict_comments['Commenter'].append(sheet.cell_value(x,0))
            for y in range(num_rows-1):
                if sheet.cell_value(y+1,0) == '':
                    break
                else:
                    try:
                        test_num = int(sheet.cell_value(y+1,0))
                    except Exception:
                        dict_comments['Comment'].append(sheet.cell_value(y+1,0))
                    else:
                        dict_comments['Likes'].append(sheet.cell_value(y+1,0))
        
        #Get the rest of the comments in the file    
        else:
            if sheet.cell_value(x,0) == 'Share':
            
                # Situation 1: cell 2 below 'Share' is blank
                if sheet.cell_value(x+2,0) == '':
                    dict_comments['Commenter'].append(sheet.cell_value(x+3,0))
                    check_for_ints_blanks(x, dict_comments, 4)

                       
                # Situation 2: cell 2 below 'Share' is ' · ' 
                elif sheet.cell_value(x+2,0) == ' · ':
                    if sheet.cell_value(x+4,0) == '':
                        dict_comments['Commenter'].append(sheet.cell_value(x+5,0))
                        check_for_ints_blanks(x, dict_comments, 6)
                
                    else:
                        dict_comments['Commenter'].append(sheet.cell_value(x+4,0))
                        check_for_ints_blanks(x, dict_comments, 5)
                
                
                #Situation 3: cell 2 below 'Share' is 'more reply' or 'more replies'
                elif 'more reply' in sheet.cell_value(x+2,0) or 'more replies' in sheet.cell_value(x+2,0) or 'Replies' in sheet.cell_value(x+2,0) or 'Reply' in sheet.cell_value(x+2,0):
                    if sheet.cell_value(x+3,0) == '':
                        dict_comments['Commenter'].append(sheet.cell_value(x+4,0))
                        check_for_ints_blanks(x, dict_comments, 5)

                    else:
                        dict_comments['Commenter'].append(sheet.cell_value(x+3,0))
                        check_for_ints_blanks(x, dict_comments, 4)
                
                
                # Situation 4: cell 2 below 'Share' is commenter name
                else:
                    dict_comments['Commenter'].append(sheet.cell_value(x+2,0))
                    check_for_ints_blanks(x, dict_comments, 3)
                        
          
    #Add comment ID column
    dict_comments['CommentID'] = []
    for x in range(len(dict_comments['Commenter'])):
        dict_comments['CommentID'].append(x+1)
    
    #Create csv
    df_comments = pd.DataFrame(dict_comments,columns=['CommentID','Commenter','Comment','Likes'])


    ###Analyze comments
    #Remove words you don't want to count
    remove_characters = [':', ',', '.', "'", "’", ',', '!', '?', '-']
    df_comments_wrking = df_comments.copy()
    for r in remove_characters:
        df_comments_wrking['Comment'] = df_comments_wrking['Comment'].str.replace(r," ")
        
    stopwords = nltk.corpus.stopwords.words('english')
    RE_stopwords = r'\b(?:{})\b'.format('|'.join(stopwords))
    words = (df_comments_wrking['Comment']
               .str.lower()
               .replace([r'\|', RE_stopwords], [' ', ''], regex=True)
               .str.cat(sep=' ')
               .split())
    
    #Counting words in a row (phrases)
    def ngrams(lst, n):
      tlst = lst
      while True:
        a, b = tee(tlst)
        l = tuple(islice(a, n))
        if len(l) == n:
          yield l
          next(b)
          tlst = b
        else:
          break
   
   #Get two words in a row
    word_combos_wrking_2 = Counter(ngrams(words, 2))
    word_combos_2 = {'Most Common Words: 2 in a row':[], 'Frequency':[]}
    for k,v in word_combos_wrking_2.items():
        temp_var = ''
        for t in k:
            temp_var += t + ' '
        word_combos_2['Most Common Words: 2 in a row'].append(temp_var[:-1])
        word_combos_2['Frequency'].append(int(word_combos_wrking_2[k]))
        
    #Get three words in a row
    word_combos_wrking_3 = Counter(ngrams(words, 3))
    word_combos_3 = {'Most Common Words: 3 in a row':[], 'Frequency':[]}
    for k,v in word_combos_wrking_3.items():
        temp_var = ''
        for t in k:
            temp_var += t + ' '
        word_combos_3['Most Common Words: 3 in a row'].append(temp_var[:-1])
        word_combos_3['Frequency'].append(int(word_combos_wrking_3[k]))
    
    # generate DF out of Counter
    df_mcw_2 = pd.DataFrame(word_combos_2,
                        columns=['Most Common Words: 2 in a row', 'Frequency']).sort_values("Frequency", ascending=False)
    is_2 =  df_mcw_2['Frequency']>=2
    df_mcw_2 = df_mcw_2[is_2]
    df_mcw_3 = pd.DataFrame(word_combos_3,
                        columns=['Most Common Words: 3 in a row', 'Frequency']).sort_values("Frequency", ascending=False)
    is_2 =  df_mcw_3['Frequency']>=2
    df_mcw_3 = df_mcw_3[is_2]
                        
      
    
    #get summary of most liked comments
    df_comments_mostliked = df_comments.copy()
    df_comments_mostliked = df_comments_mostliked.sort_values("Likes", ascending=False)
    df_comments_mostliked = df_comments_mostliked[0:10]

    dfs = [df_comments,df_mcw_2,df_mcw_3,df_comments_mostliked]
    excel_name = 'parsed_comments.xlsx'
    sheetnames = ['Parsed Comments','Analysis','Analysis','Analysis']
    start_cols = [0, 0, (df_mcw_2.shape[1] + 1), (df_mcw_2.shape[1] + df_mcw_3.shape[1] + 2)]

    # Create zipped stream to add spreadsheet to
    import io
    import zipfile
    buf = io.BytesIO()
    zs = zipfile.ZipFile(buf, mode='w')
    zfm1 = zs.open(excel_name, 'w')
    with pd.ExcelWriter(zfm1, engine='xlsxwriter') as writer:
        for d in range(len(dfs)):
            dfs[d].to_excel(writer, sheet_name=sheetnames[d], index=False, startcol = start_cols[d])
    zfm1.close()
    zs.close()

    return buf
