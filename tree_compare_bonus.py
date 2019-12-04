import functions

#function which will create report based on missing simple typed element
def compare_simple_types(content_dst, content_src, *check_types):
    report = ''
    for check_type in list(check_types):
        missing_content_in_dst = [x for x in content_src if type(x) == check_type and x not in content_dst]
        #mark non existent elements as ---
        for element in missing_content_in_dst:
          report += "--- %s (%s) \n" % (element, check_type.__name__)
        existing_content_in_dst = [x for x in content_dst if type(x) == check_type and x in content_dst]
        for element in existing_content_in_dst:
          #mark existing ones with +++
          report += "+++ %s (%s) \n" % (element, check_type.__name__)

    return report

#function which will cimpare lists
def compare_lists(list_dst, list_src):
    if type(list_src) == list and type(list_dst) == list:
        return [x for x in list_src if x not in list_dst]

#function to compare dicts on key level
def compare_dict_keys(content_dst, content_src):
    keys_dst = []
    keys_src = []
    report = ''

    dicts_dst = [x for x in content_dst if type(x) == dict] #list of dict(s)
    dicts_src = [x for x in content_src if type(x) == dict] #list of dict(s)

    #find out all keys in all dicts
    for element_dst in dicts_dst:
        keys_dst += element_dst.keys()
    for element_src in dicts_src:
        keys_src += element_src.keys()

    for element in [x for x in keys_src if x not in keys_dst]:
        report += "--- %s (dict) \n" % element

    for element in [x for x in keys_src ]:
        report += "+++ %s (dict) \n" % element

    return report


def compare_dict_deep(content_dst, content_src):

    dicts_dst = [x for x in content_dst if type(x) == dict]
    dicts_src = [x for x in content_src if type(x) == dict]
    report = ''

    #loop through each dict of tree with which we compare
    for element_src in dicts_src:

        for element_dst in dicts_dst:
            common_keys = []
            common_keys = [x for x in element_dst.keys() if x in element_src.keys()]
            # if there are common keys go deeper
            if common_keys != []:
                for common_key in common_keys:
                    #compare deeper values which differ for common keys
                    if element_dst[common_key] != element_src[common_key]:
                        #in case we reached simple type show diff

                        for element in compare_lists(element_dst[common_key], element_src[common_key]):
                            if type(element) != dict:

                                report += "%s \n  --- %s (%s) \n" % (common_key, element, type(element).__name__)

                            if type(element) == dict:

                                for (k,v) in element.items():
                                    report += "%s \n  %s \n    --- %s (%s) \n" % (common_key, k, v, type(v).__name__)


    return report

def tree_compare(file1, file2):
    #perform factual comparison using functions from above
    content1 = functions.t_read(file1)
    content2 = functions.t_read(file2)
    functions.t_write(compare_simple_types(content1, content2, int, str), "%s_report_bonus" % file1)
    functions.t_write(compare_simple_types(content2, content1, int, str), "%s_report_bonus" % file2)
    functions.t_write(compare_dict_keys(content1, content2), "%s_report_bonus" % file1, openmode='a')
    functions.t_write(compare_dict_keys(content2, content1), "%s_report_bonus" % file2, openmode='a')
    functions.t_write(compare_dict_deep(content1, content2), "%s_report_bonus" % file1, openmode='a')
    functions.t_write(compare_dict_deep(content2, content1), "%s_report_bonus" % file2, openmode='a')



tree_compare("tree1.txt", "tree2.txt")

