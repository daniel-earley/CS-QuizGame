import cx_Freeze

executables = [cx_Freeze.Executable("Quiz_Game.py")]

cx_Freeze.setup(
    name="Quiz Game",
    options={"build_exe": {"packages":["pygame","os","time","linecache","random"],
                           "include_files":["Master Sheet.png","Neutral Stage.png", "heart.png", "Speech Box.png", "Game Questions.txt"]}},
    executables = executables

    )