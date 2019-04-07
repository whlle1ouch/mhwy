from fuzzywuzzy import fuzz


def fuzzMatch(response_list, str_question):
    requests = [r[1] for r in response_list]
    responses = [r[2] for r in response_list]
    requests_score = list()
    for request in requests:
        score = fuzz.token_set_ratio(request,str_question)
        requests_score.append(score)
    if max(requests_score)==0:
        return ''
    index = requests_score.index(max(requests_score))
    return responses[index]





