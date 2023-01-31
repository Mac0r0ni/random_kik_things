import re

f = open("DEBUG.log", "r", encoding="utf8", errors='ignore')
f2 = open("usernames.txt", "a+", encoding='utf8')

txt_input = f.read()
findall_matches = re.findall("<username>(.*?)</username>", txt_input, flags=re.DOTALL)
joined_output_string = "\n".join(findall_matches)
f2.write(joined_output_string)

f.close()
f2.close()
