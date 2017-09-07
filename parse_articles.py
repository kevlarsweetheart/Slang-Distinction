import raw_data_process as rdp
import jsonlines

with jsonlines.open('articles.jl') as articles:
    with jsonlines.open('norm_articles.jl', mode = 'w') as writer:
        for obj in articles:
            line = rdp.jl_line(item = obj)
            sentences = line.normalize()
            for item in sentences:
                writer.write(item)