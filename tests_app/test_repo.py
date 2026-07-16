def __get_score_key(test_id):
    return f'test_{test_id}_score'


def __get_progress_key(test_id):
    return f'test_{test_id}_progress'


def __get_favorites_key():
    return 'favorite_test_ids'

def get_score(request, test_id):
    score_key = __get_score_key(test_id)
    return request.session.get(score_key, 0)

def add_score(request, test_id, value=0):
    score_key = __get_score_key(test_id)
    request.session[score_key] = get_score(request, test_id) + value
    
def set_score(request, test_id, value):
    score_key = __get_score_key(test_id)
    request.session[score_key] = value


def clear_score(request, test_id):
    request.session.pop(__get_score_key(test_id), None)


def get_progress(request, test_id):
    return request.session.get(__get_progress_key(test_id), {})


def set_progress(request, test_id, progress):
    request.session[__get_progress_key(test_id)] = progress


def clear_progress(request, test_id):
    request.session.pop(__get_progress_key(test_id), None)


def get_favorite_ids(request):
    return request.session.get(__get_favorites_key(), [])


def is_favorite(request, test_id):
    return int(test_id) in [int(value) for value in get_favorite_ids(request)]


def toggle_favorite(request, test_id):
    favorite_ids = [int(value) for value in get_favorite_ids(request)]
    test_id = int(test_id)

    if test_id in favorite_ids:
        favorite_ids.remove(test_id)
    else:
        favorite_ids.append(test_id)

    request.session[__get_favorites_key()] = favorite_ids
    request.session.modified = True
    return test_id in favorite_ids