def clean_wiki_extract(data):
    """
        Change the content format of extract returned by wiki api
    """
    # content after See also such as references, further reading, External links can be ignored
    data, ignore = data.split('\n== See also')
    # change wiki tag representation to text equivalent
    data = data.replace('\n== ', '<heading>')
    data = data.replace(' ==\n', '</heading>')
    data = data.replace('\n=== ', '<subheading>')
    data = data.replace(' ===\n', '</subheading>')
    data = data.replace('\n==== ', '<sub_subheading>')
    data = data.replace('====\n', '</sub_subheading>')
    # clean redundent symbols
    data = data.replace('\n', '')
    data = data.replace('\t', '')
    data = data.replace('\\', '')
    return data


def extract_as_dict(data):
    """
    Change extract from string to python dictionary for json conversion
    Keeping the fact extract might have categorisation upto 3 levels i.e.
    1 Category
        1.1 Sub-category
            1.1.1 Sub-sub-category
    """
    city_detail = {}
    data = data.split('<heading>')

    city_detail['Summary'] = data[0]
    for data_part in data[1:]:
        heading, content = data_part.split('</heading>')
        if '<subheading>' not in content:
            # content has no sub-category
            city_detail[heading] = content
        else:
            sub_detail = {}
            sub_data = content.split('<subheading>')
            sub_detail['Summary'] = sub_data[0]
            for sub_data_part in sub_data[1:]:
                sub_heading, sub_content = sub_data_part.split('</subheading>')
                if '<sub_subheading>' not in sub_content:
                    # content has only sub-category
                    sub_detail[sub_heading] = sub_content
                else:
                    # content has sub-sub-category
                    sub_sub_detail = {}
                    sub_sub_data = sub_content.split('<sub_subheading>')
                    sub_sub_detail['Summary'] = sub_sub_data[0]
                    for sub_sub_data_part in sub_sub_data[1:]:
                        sub_sub_heading, sub_sub_content = sub_sub_data_part.split('</sub_subheading>')
                        sub_sub_detail[sub_sub_heading] = sub_sub_content
                    sub_detail[sub_heading] = sub_sub_detail
            city_detail[heading] = sub_detail
    return city_detail
