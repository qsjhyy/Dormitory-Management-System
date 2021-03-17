"""
学生信息包括
学号（唯一）  姓名  性别  年龄  寝室（一间寝室最多安排4人）
寝室编号 男生（100 101 102） 女生（200 201 202）

功能包括：
1. 可以录入学生信息
2. 录入过程中可以为其分配寝室（可选自动分配或手动分配，手动分配的话如果选择的寝室人员已满，提示重新分配）
3. 可以打印各寝室人员列表（做到表格打印是加分项）
4. 可以用学号索引打印特定学生信息，可以打印所有学生信息（做到表格打印是加分项）
5. 可以为学生调整寝室（一人调整到其他寝室，两人交换寝室等，自由发挥）
6. 可以将所有信息存入文件（json格式）
7. 程序启动时，将文件中的学生信息自动导入系统
"""
import json

RECORD_INFO = 1
DELETE_INFO = 2
FIND_INFO = 3
SHOW_INFO = 4
CHANGE_ROOM = 5
QUIT_SYSTEM = 0

print_info = '''
========================================
学号\t\t姓名\t\t性别\t\t年龄\t\t寝室号
----------------------------------------'''


# 加载json文件中的学生信息
def load_json_file():
    with open("information.json", "r", encoding='utf-8') as file:
        return json.load(file)      # 将导入的学生信息返回到全局变量student_info_dict（字典类型）


# 将学生信息保存在json文件
def save_json_file():
    with open("information.json", "w", encoding='utf-8') as file:
        json.dump(student_info_dict, file, ensure_ascii=False)  # 传入文件描述符，和dumps一样的结果


# 加载寝室基本信息并录入原有的寝室分配方案
def load_existing_room_info():
    for n in ("100", "101", "102", "200", "201", "202"):        # 录入寝室基础信息
        room_info_dict[n] = {'room_id': n, 'count': 0, 'people': []}

    for i in student_info_dict.values():        # 录入原有寝室分配方案
        room_info_dict[i["room"]]["people"].append(i)
        room_info_dict[i["room"]]["count"] += 1


# 录入学生信息
def record_student_info():
    new_student_info = {}       # 新增学生的个人信息集

    # 判断输入学号是否合法
    new_id = input("请输入要录入学生的学号:\n")
    while True:     # 由于学号格式为整型，所以加了异常和格式转换，阻止了输入为1.1和1、1之类的情况
        try:
            if not int(new_id):  # 学号输入为空或者为0
                new_id = input("您并未输入学生学号或者输入学号是0，请输入学生学号:\n")
            elif str(int(new_id)) in student_info_dict:      # 学号是否唯一
                new_id = input("您输入的学号已存在(提示：有效数字之前的零无效)，请重新输入:\n")
            else:
                new_student_info["student_id"] = new_id
                break
        except ValueError:
            new_id = input("您输入学生学号格式有误，请重新输入:\n")

    # 判断输入姓名是否合法
    new_name = input("请输入录入学生的姓名:\n")
    while not new_name:     # 姓名仅做了输入为空判断
        new_name = input("您并未输入学生姓名，请输入:\n")
    new_student_info["name"] = new_name

    # 判断输入性别是否合法
    new_sex = input("请输入录入学生的性别:\n")
    while new_sex not in ("男", "女"):        # 判断性别输入是否为（男/女）
        new_sex = input("您输入的性别不正确，请重新输入（男/女）:\n")
    new_student_info["sex"] = new_sex

    # 判断输年龄是否合法
    new_age = int(input("请输入录入学生的年龄:\n"))
    while int(new_age) not in range(6, 48):     # 判断年龄输入是否合法
        new_age = int(input("您输入的年龄不合法，请重新输入，范围(6-48):\n"))
    new_student_info["age"] = new_age

    student_info_dict[new_id] = new_student_info
    print("录入成功，请为其分配寝室")
    print(student_info_dict)
    return new_id


# 删除学生信息
def delete_student_info():
    delete_id = input("请输入要删除学生的学号:\n")
    while delete_id not in student_info_dict:  # 判断输入的学号是否存在
        delete_id = input("您输入的学生学号不存在，请重新输入:\n")

    delete_room = student_info_dict[delete_id]["room"]      # 提取删除学生的寝室号
    if delete_room:  # 判断该生原来是否有宿舍
        room_info_dict[delete_room]["people"].remove(student_info_dict[delete_id])      # 删除寝室字典里面的该生信息
        room_info_dict[delete_room]["count"] -= 1

    del student_info_dict[delete_id]        # 删除学生字典里面的该生信息
    print("已删除学号{}的学生信息".format(delete_id))


# 显示学生信息
def show_student_info():
    print("按学号显示学生信息:", end="")
    print(print_info)
    for i in student_info_dict.values():  # 打印输出这个字典的值
        print("{}\t\t{}\t\t{}\t\t{}\t\t{}".format(i["student_id"], i["name"], i["sex"], i["age"], i["room"]))


# 显示寝室信息
def show_room_info():
    print("按寝室显示学生信息:", end="")
    print(print_info)
    for i in room_info_dict:
        print("{}号寝室，人员如下:".format(i))
        for j in room_info_dict[i]["people"]:
            print("{}\t\t{}\t\t{}\t\t{}\t\t{}" .format(j["student_id"], j["name"], j["sex"], j["age"], j["room"]))


# 搜索学生信息
def find_student_info():
    find_id = input("请你输入想要查找的学号:\n")
    if find_id in student_info_dict:
        find_info = student_info_dict[find_id]
        print("{}号学生信息如下:".format(find_info), end="")
        print(print_info)
        print("{}\t\t{}\t\t{}\t\t{}\t\t{}"
              .format(find_info["student_id"], find_info["name"], find_info["sex"], find_info["age"], find_info["room"]))
    else:
        print("系统未录入此学号的学生")


# 具体分配步骤
def concreteness_allot_step(room_info, student_info, room_id):
    if room_info["count"] < 4:      # 判断寝室是否未住满
        room_info["people"].append(student_info)        # 将学生信息添加到寝室信息字典中
        room_info["count"] += 1
        student_info["room"] = room_id      # 在学生个人信息中备注其寝室号
        print("分配成功")
        return True
    else:
        return False


# 分配学生宿舍
def allot_student_room(new_id, mode):       # 可将新录入的学生自动分配到空余寝室，或者根据手动分配要求为学生分配寝室
    if mode == "1":     # 自动分配模式
        if student_info_dict[new_id]["sex"] == "男":
            for i in (100, 101, 102):
                if concreteness_allot_step(room_info_dict[i], student_info_dict[new_id], i):
                    break
        else:
            for i in (200, 201, 202):
                if concreteness_allot_step(room_info_dict[i], student_info_dict[new_id], i):
                    break

    elif mode == "2":       # 手动分配模式
        room_id = input("请输入要分配的寝室号:\n")
        if student_info_dict[new_id]["sex"] == "男":
            while int(room_id) not in (100, 101, 102):
                room_id = input("您输入的寝室号不符合规定，请重新输入:\n")
            while not concreteness_allot_step(room_info_dict[room_id], student_info_dict[new_id], room_id):
                room_id = input("您输入的寝室号对应的寝室已住满，请重新输入:\n")

        else:
            while int(room_id) not in (200, 201, 202):
                room_id = input("您输入的寝室号不符合规定，请重新输入:\n")
            while not concreteness_allot_step(room_info_dict[room_id], student_info_dict[new_id], room_id):
                room_id = input("您输入的寝室号对应的寝室已住满，请重新输入:\n")


# 调整学生宿舍
def change_student_room():      # 可将学生调整到空余寝室，或者和其他学生互换寝室
    change_id = input("请输入要调整学生的学号:\n")     # 输入调整学生的学号
    while change_id not in student_info_dict:  # 判断此学号对应的学生信息是否存在
        change_id = input("您输入学号不存在，请查证后再输:\n")

    change_room = input("请输入要调整的寝室号:\n")
    if student_info_dict[change_id]["sex"] == "男":
        k = 0
    else:
        k = 1
    while int(change_room) not in (100 + 100*k, 101 + 100*k, 102 + 100*k):
        change_room = input("您输入的寝室号不符合规定，请重新输入寝室号:\n")
    if not concreteness_allot_step(room_info_dict[change_room], student_info_dict[change_id], change_room):
        print("{}号寝室已满，人员如下:".format(change_room))
        print(print_info)
        for j in room_info_dict[change_room]["people"]:
            print("{}\t\t{}\t\t{}\t\t{}\t\t{}".format(j["room_id"], j["name"], j["sex"], j["age"], j["room"]))

        if 'y' == input("是否交换宿舍(y/n)"):
            another_change_id = input("请输入与之交换寝室的学生学号")

            # 删除调整生原有宿舍信息
            room_info_dict[student_info_dict[change_id]["room"]]["people"].remove(student_info_dict[change_id])
            room_info_dict[change_room]["people"].remove(student_info_dict[another_change_id])

            # 为被交换生指定宿舍的相应信息
            room_info_dict[change_room]["people"].append(student_info_dict[change_id])
            room_info_dict[student_info_dict[change_id]["room"]]["people"]\
                .append(student_info_dict[another_change_id])
            student_info_dict[another_change_id]["room"] = student_info_dict[another_change_id]["room"]
            student_info_dict[change_id]["room"] = change_room
            print("调整学生寝室成功")


# 系统功能菜单
def show_menu():
    while True:
        info = """
欢迎使用[寝室管理系统]:
            1.录入学生信息
            2.删除学生信息
            3.搜索学生信息
            4.显示学生信息
            5.调整学生宿舍
            0.退出管理系统
               """
        print(info)
        choice = input("请输入你想进行的操作是:\n")

        if int(choice) == RECORD_INFO:        # 1.录入学生信息
            new_student_id = record_student_info()
            if new_student_id:
                while True:
                    info = """========================寝室分配============================
                    1.自动分配
                    2.手动分配
                    """
                    print(info)
                    choice1 = input("请选择你需要进行的操作:\n")
                    if choice1 == "1":
                        allot_student_room(new_student_id, choice1)
                        save_json_file()
                    elif choice1 == "2":
                        allot_student_room(new_student_id, choice1)
                        save_json_file()
                    else:
                        print("请按照提示输入正确的数字:\n")
                    print("按enter键继续...")
                    input()
                    break
        elif int(choice) == DELETE_INFO:      # 2.删除学生信息
            delete_student_info()
            save_json_file()
            print("按enter键继续...")
            input()
            continue
        elif int(choice) == FIND_INFO:      # 3.搜索学生信息
            find_student_info()
            print("按enter键继续...")
            input()
            continue
        elif int(choice) == SHOW_INFO:      # 4.显示学生信息
            while True:
                info = """========================学生信息============================
                1.按学号显示
                2.按寝室显示
                """
                print(info)
                choice1 = input("请选择你需要进行的操作:\n")
                if choice1 == "1":
                    show_student_info()
                    break
                elif choice1 == "2":
                    show_room_info()
                    break
                else:
                    print("请按照提示输入正确的数字:\n")
                    continue
            print("按enter键继续...")
            input()
            continue
        elif int(choice) == CHANGE_ROOM:      # 5.调整学生宿舍
            change_student_room()
            save_json_file()
            print("按enter键继续...")
            input()
            continue
        elif int(choice) == QUIT_SYSTEM:      # 0.退出管理系统
            print("欢迎再次使用学生管理系统！")
            break
        else:
            print("请您输入操作相对应的数字:\n")


if __name__ == "__main__":
    student_info_dict = load_json_file()        # 加载json文件的学生信息到字典中
    room_info_dict = {}
    load_existing_room_info()       # 加载原有的寝室分配方案到字典room_info_dict中

    show_menu()     # 显示系统主菜单，并在其中循环

    save_json_file()        # 将学生信息保存在json文件
