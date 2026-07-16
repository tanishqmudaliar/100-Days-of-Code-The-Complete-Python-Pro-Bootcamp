def format_name(f_name, l_name):
    f_name = f_name.title()
    l_name = l_name.title()
    return f_name + " " + l_name

name = format_name("jOhN", "sMiTh")
print(name)