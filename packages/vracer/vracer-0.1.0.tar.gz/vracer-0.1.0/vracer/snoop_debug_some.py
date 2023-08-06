
import snoop

snoop.install(columns="", json_file_path="youareawesome.json")


@snoop
def trace():
    for i, x in enumerate(range(18)):
        print(i, x)


trace()
