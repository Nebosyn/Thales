import csv, os, json

def loadEclipseCache(fileDirPath,fileName):
    with open(f"{os.path.join(fileDirPath,fileName)}","r") as f:
        dicitonary = json.load(f)
        return dicitonary

def compare_all(filesNames):

    # Читаємо файли за даними від NASA
    nasa_data = list()
    for file_name in filesNames:
        f = open(file_name, "r")
        nasa_data += list(csv.reader(f))[1:]

    # Отримаємо з csv файлу тільки потрібні дані
    for i, data in enumerate(nasa_data):
        nasa_data[i] = data[1:5]
    
    my_data = loadEclipseCache("", "All_eclipses.json")
    # Комбінування затемнень з 19, 20 та 21 століть
    my_data = my_data["19"]+my_data["20"]+my_data["21"]
    
    # Конвертація даних 
    for i in range(len(my_data)):
        my_data[i][0] = my_data[i][0].split(" ")
        my_data[i][1] = my_data[i][1].split(" ")
        my_data[i][0][1] = my_data[i][0][1].lower()
        my_data[i][1][1] = my_data[i][1][1].lower()
        
    counter = 0
    compared_eclipses = str()
    unfound_eclipses = str()
    for i in range(len(my_data)):
        j = i+counter
        # Порівняння дати від NASA з датою початку та кінця затемнення
        if my_data[i][0][2] != nasa_data[j][2] and my_data[i][1][2] != nasa_data[j][2]:
            counter+=1
            unfound_eclipses += f"Не знайдено затемненння: {' '.join(nasa_data[j])}\n\n"
        else:
            to_print = f"Розрахований початок затемнення: {' '.join(my_data[i][0])}\nРозрахований кінець затемнення: {' '.join(my_data[i][1])}\nЗатемнення по даним від NASA: {' '.join(nasa_data[j])}\n"
            print(to_print)
            compared_eclipses += to_print + "\n"

    # Зберігання порвіняних даних у файл
    with open("Перевірка затемненнь.txt", "w", encoding="utf8") as fw:
        fw.write(compared_eclipses)
    
    # Зберігання порвіняних даних у файл
    with open("Не знайденні затемнення.txt", "w", encoding="utf8") as fw:
        fw.write(unfound_eclipses)


if __name__ == "__main__":
    files = ("1901-2000.csv","2001-2100.csv","2101-2200.csv")
    compare_all(files)