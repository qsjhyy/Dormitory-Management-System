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
import hyy


# 显示学生全部信息
def show_all():
    print("-"*50)
    print("显示所有学生信息")
    if s_dict == 0:
        print('没有当前学生信息，请确认输入或者进行添加')
        return
    print("学号\t\t姓名\t\t性别\t\t年龄\t\t寝室号")
    print("="*50)
    for dic in s_dict.values():  # 打印输出这个字典的值
        print("{}\t\t{}\t\t{}\t\t{}\t\t{}" .format(dic["sid"], dic["name"], dic["sex"], dic["age"], dic["room"]))


# 指定目标进行搜索
def search_card():
    print("======================我是可爱的分割线========================")
    print("[搜索学生信息]\n")
    print("1.按学号搜索\n")
    print("0.返回主菜单\n")
    print("======================我是可爱的分割线========================")
    choice = input("请输入你想要进行的操作是")
    print("你选择的操作是{}".format(choice))
    if choice in ["1", "0"]:
        if choice == "1":
            f_id = input("请你输入想要查找的学号:")
            if f_id in s_dict:
                ft = s_dict[f_id]
                print("学号\t\t姓名\t\t性别\t\t年龄\t\t寝室号")
                print("==============================================")
                print("{}\t\t{}\t\t{}\t\t{}\t\t{}" .format(ft["sid"], ft["name"], ft["sex"], ft["age"], ft["room"]))
            else:
                print("抱歉！没有找到该学生")
        elif choice == "0":
            return
    else:
        print("请输入操作向对应的数字0-1")
        return


def show_menu():
    while True:
        print("*"*50)
        print("欢迎使用[寝室管理系统]")
        print()
        print("1.录入学生信息")
        print("2.显示学生信息")
        print("3.搜索学生信息")
        print("4.显示各寝室人员列表")
        print("5.寝室人员调整")
        print("6.删除学生信息")
        print("0.退出管理系统")
        print("*"*50)
        choice = input("请输入你想进行的操作是:")

        if int(choice) == 1:
            m_sid = hyy.record(s_dict)
            if m_sid:
                print("======================我是可爱的分割线========================\n")
                print("========================寝室分配============================")
                print("1.自动分配")
                print("2.手动分配")
                room = input("请选择你需要进行的操作：")
                if room in ["1", "2"]:
                    if room == "1":
                        hyy.manuel_arrange(r_dict, s_dict, m_sid)
                    elif room == "2":
                        m_rid = int(input("请输入你想为其分配的寝室号："))
                        while not hyy.manuel_arrange(r_dict, s_dict, m_sid, m_rid):
                            m_rid = int(input("请重新输入你想为其分配的寝室号："))
            print("按enter键继续：")
            input()
            continue
        elif int(choice) == 2:
            print("======================我是可爱的分割线========================\n")
            print("========================寝室分配============================")
            print("1.按学号显示")
            print("2.按寝室显示")
            room = input("请选择你需要进行的操作：")
            if room in ["1", "2"]:
                if room == "1":
                    show_all()
                elif room == "2":
                    hyy.print_room_list(r_dict)
            print("按enter键继续：")
            input()
            continue
        elif int(choice) == 3:
            search_card()
            print("按enter键继续：")
            input()
            continue
        elif int(choice) == 4:
            hyy.print_room_list(r_dict)
            print("按enter键继续：")
            input()
            continue
        elif int(choice) == 5:
            hyy.allot(s_dict, r_dict)
            print("按enter键继续：")
            input()
            continue
        elif int(choice) == 6:
            hyy.delete(input("请输入你想要删除的学生号："), s_dict)
            print("按enter键继续：")
            input()
            continue
        elif int(choice) == 0:
            print("欢迎再次使用学生管理系统！")
            break

        else:
            print("请您输入操作相对应的数字：")


if __name__ == "__main__":      # 自动导入文件中的学生信息
    s_dict = hyy.load()  # 录入文件中的学生信息
    r_dict = dict()
    hyy.previous_r_dict(s_dict, r_dict)
    s_dict = hyy.dict_sorted(s_dict)
    # print("----------------")
    # print(r_dict)
    # print("----------------")
    # hyy.arrange(s_dict, r_dict)
    # print(r_dict)
    show_menu()

    hyy.save(s_dict)
