from pybricks.tools import hub_menu

# Choose a letter.
selected = hub_menu("1","2","3","4","5","6")

# Based on the selection, run a program.
if selected == "1":
    import program1
elif selected == "2":
    import program2
elif selected == "3":
    import program3
elif selected == "4":
    import program4
elif selected == "5":
    import program5
elif selected == "6":
    import program6

