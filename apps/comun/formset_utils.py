def get_records_formset(request):
    ids_inside_post = []
    for key, val in list(request.POST.items()):
        if key.endswith("id"):
            if val not in ids_inside_post and val != "":
                ids_inside_post.append(val)

    return ids_inside_post


def get_records_formset_by_prefix(request, prefix):
    ids_inside_post = []
    for key, val in list(request.POST.items()):
        if key.startswith(prefix) and key.endswith("id"):
            if val not in ids_inside_post and val != "":
                ids_inside_post.append(val)

    return ids_inside_post
