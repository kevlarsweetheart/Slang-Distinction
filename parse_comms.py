import raw_data_process as rdp
import jsonlines

with jsonlines.open('vk_comms.jl') as comments:
    with jsonlines.open('norm_comms.jl', mode = 'w') as writer:
        for obj in comments:
            line = rdp.jl_line(item = obj)
            sentences = line.normalize()
            for item in sentences:
                writer.write(item)
