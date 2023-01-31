# Just adding this here for storage

seen = set()
with open('combined.txt', 'r') as start, open('deduped.txt', 'w') as end:
    for line in start:
        h = hash(line)
        if h not in seen:
            end.write(line)
            seen.add(h)
