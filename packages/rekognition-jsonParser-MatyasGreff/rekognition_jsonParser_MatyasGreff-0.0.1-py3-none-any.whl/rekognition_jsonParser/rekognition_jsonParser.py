def celebrity_jsonParser(response):
    links = []
    return_list = []
    name = []
    for celebrity in response['CelebrityFaces']:
        name.append(celebrity['Name'])
        for url in celebrity['Urls']:
            links.append(url)
        return_list = [name, links]
    return return_list
    
def detectLabel_jsonParser(response):
    name = []
    instances = []
    x = 0
    for label in response['Labels']:
        name.append(label['Name'])
    for i in name:
        for label in response['Labels']:
            if label['Name'] == i:
                x = len(label['Instances'])
                instances.append(x)
        return_list = [name, instances]
    return return_list