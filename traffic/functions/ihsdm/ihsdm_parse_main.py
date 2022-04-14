
def ihsdm_parse_func(bs_files, html_dfs, highwaynames, zs):
    import pandas as pd
    from .html_to_excel import html_to_excel

    ### CREATE EMPTY LISTS FOR MODEL TYPES
    freeway_bs_files, freeway_html_dfs, freeway_highwaynames = [], [], []
    ramp_bs_files, ramp_html_dfs, ramp_highwaynames = [], [], []
    art_bs_files, art_html_dfs, art_highwaynames = [], [], []
    rt_bs_files, rt_html_dfs, rt_highwaynames = [], [], []

    ### ASSIGN DATA BY ELEMENT TYPE
    # for each file in uploaded zipped folder
    for h in range(len(bs_files)):
        # find all the text
        bs_text = bs_files[h].find_all('font')
        # for each line in text
        for f in bs_text:
            # format the text to check
            check_text = f.text.replace("\t", "").replace("\r", "").replace("\n", "")

            # assign by freeway segment, ramps, arterials, and intersections
            if 'Model Category' in check_text:
                index = check_text.find(':')
                if check_text[index+2:] == 'Freeway Segment':
                    freeway_bs_files.append(bs_files[h])
                    freeway_html_dfs.append(html_dfs[h])
                    freeway_highwaynames.append(highwaynames[h])
                elif check_text[index+2:] in ['Freeway Service Ramp', 'C-D Road & System Ramp']:
                    ramp_bs_files.append(bs_files[h])
                    ramp_html_dfs.append(html_dfs[h])
                    ramp_highwaynames.append(highwaynames[h])
                elif check_text[index+2:] in ['Urban/Suburban Arterial','Rural, Two Lane']:
                    art_bs_files.append(bs_files[h])
                    art_html_dfs.append(html_dfs[h])
                    art_highwaynames.append(highwaynames[h])
            elif 'Intersection:' in check_text:
                rt_bs_files.append(bs_files[h])
                rt_html_dfs.append(html_dfs[h])
                rt_highwaynames.append(highwaynames[h])

    ### RUN FUNCTIONS BY MODEL TYPE
    html_to_excel(freeway_bs_files,freeway_html_dfs,freeway_highwaynames, zs, 'parsed_freewaysegment.xlsx')
    html_to_excel(ramp_bs_files, ramp_html_dfs, ramp_highwaynames, zs, 'parsed_freewayramp.xlsx')
    html_to_excel(art_bs_files, art_html_dfs, art_highwaynames, zs, 'parsed_arterial.xlsx')
    html_to_excel(rt_bs_files, rt_html_dfs, rt_highwaynames, zs, 'parsed_rampterminal.xlsx')
