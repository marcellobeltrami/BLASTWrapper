import requests

## Add all parameters from documentation.
BASE_URL = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"

def put_query(sequence, program="blastn", database="core_nt",
              short_query="true",filter="mL",expect=10.0,
              nuc_rew=2,nuc_pen=-3,word_size=11,
              gap_cost="5 2", matrix="BLOSUM62",cbs=2,
              ht_list=100,fmt_type="HTML", description=100, 
              alignment="false", report="false"):
    
    # Submit BLAST search    
    params = {
        "CMD": "Put",
        "PROGRAM": program,
        "DATABASE": database,
        "QUERY": sequence, 
        "SHORT_QUERY_ADJUST": short_query,
        "FILTER": filter,
        "EXPECT": expect,
        "NUCL_REWARD": nuc_rew,
        "NUCL_PENALTY" : nuc_pen,
        "WORD_SIZE" : word_size,
        "GAPCOSTS": gap_cost,
        "MATRIX" : matrix,
        "COMPOSITION_BASED_STATISTICS" : cbs,
        "HITLIST_SIZE":ht_list,
        "FORMAT_TYPE":fmt_type, 
        "DESCRIPTIONS": description,
        "ALIGNMENTS": alignment,
        "NCBI_GI" : report
    }

    response = requests.get(BASE_URL, params=params)
    if "RID" in response.text:
        rid = response.text.split("RID = ")[1].split("\n")[0]
        print("Job submitted. RID:", rid)
        return rid
    else:
        print("Error submitting job.")
        exit(1)

    
# Checks if the query has completed
def check_status(rid, time_elapsed, 
                 fmt_type="Text&amp",fmt_object="SearchInfo", align_view="Tabular",
                 descr=100, align=100, report="false" ):
    
    status_response = requests.get(BASE_URL, params={"CMD": "Get", "RID": rid, 
                                                     "FORMAT_OBJECT": fmt_object , 
                                                     "FORMAT_TYPE":fmt_type, 
                                                     "ALIGNMENT_VIEW":align_view,
                                                     "DESCRIPTIONS" :  descr,
                                                     "ALIGNMENTS" : align,
                                                     "NCBI_GI": report
                                                    })
    
    
    if "Status=READY" in status_response.text:
        print("Job completed!")
        return "READY"
    else:
        print(f"Running... || TIME ELAPSED: {round(time_elapsed/60, 2)} minutes")
        
        return "NOT READY"


# Get results
def get_results(rid,view_res="FromRes",fmt_type="Text",
                descr=100,align=100, report="false"):
    result_response = requests.get(BASE_URL, params={"CMD": "Get", 
                                                     "VIEW_RESULTS":view_res,
                                                     "FORMAT_TYPE": fmt_type,
                                                     "DESCRIPTIONS": descr,
                                                     "ALIGNMENTS" : align,
                                                     "NCBI_GI" : report,
                                                     "RID": rid})

    return result_response