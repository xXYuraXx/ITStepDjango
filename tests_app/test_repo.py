def __get_score_key(test_id):
    return f'test_{test_id}_score'

def get_score(request, test_id):
    score_key = __get_score_key(test_id)
    return request.session.get(score_key, 0)

def add_score(request, test_id, value=0):
    score_key = __get_score_key(test_id)
    request.session[score_key] = get_score(request, test_id) + value
    
def set_score(request, test_id, value):
    score_key = __get_score_key(test_id)
    request.session[score_key] = value