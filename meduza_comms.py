import vk
import time
import re
import jsonlines
import sys


session = vk.AuthSession(6114637, 'login', 'password', scope='groups')

vk_api = vk.API(session)
meduza_id = -76982440
post_cnt = 10000


def get_comments(id):
    time.sleep(0.33)
    return vk_api.wall.getComments(owner_id = meduza_id, post_id = id, count = 100, preview_length = 0)




with jsonlines.open('vk_comms.jl', mode = 'w') as writer:
    for _offset in range(0, 20001, 100):
        posts = None
        while True:
            try:
                posts = vk_api.wall.get(owner_id = meduza_id, offset = _offset, count = post_cnt)[1:]
            except KeyboardInterrupt:
                sys.exit()
            except:
                continue
            else:
                break

        post_ids = [post.get('id') for post in posts]
        for id in post_ids:
            post_comms = get_comments(id)
            bound = len(post_comms)
            for i in range(1, bound):
                comment = post_comms[i].get('text')
                check = re.match('\[id\d{1,10}\|.+\]', comment)
                if check:
                    comm_start = check.end() + 2
                    comment = comment[comm_start:]
                comm = {'Comment': [comment]}
                writer.write(comm)
