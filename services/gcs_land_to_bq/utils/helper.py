def get_entity_name(file_name):

    file_base_name = file_name.split("/")[-1]

    entity_name = file_base_name.split("_")[0]

    return entity_name