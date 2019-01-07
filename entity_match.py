
with open("data/entity_data/animEntityPrepro","w") as empty_file:
    with open("data/entity_data/animEntity") as entity_file:
        entity_file_content=entity_file.readlines()
        for line in entity_file_content:
            try:
                lindex=line.index("#")
                rindex=line.index(" of")
                empty_file.write(line.strip()+";"+line[lindex+1:rindex].strip()+"\n")
            except:
                pass