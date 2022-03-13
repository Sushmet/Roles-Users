from role import ROLES_HIERARCHY

root_name = input("Enter root role name : ")
ROOT = ROLES_HIERARCHY(root_name)
print(ROOT)

option = 0
while True:
    try:
        print("\nOptions :")
        print("\t1. Add Sub Role")
        print("\t2. Display Roles")
        print("\t3. Delete Role")
        print("\t4. Add User")
        print("\t5. Display Users")
        print("\t6. Display Users and Sub Users")
        print("\t7. Delete User")
        print("\t8. Number of users from top")
        print("\t9. Height of role hierarchy")
        print("\t10.Common boss of users")
        print("\t11. Exit")
        option = int(input("Option to be performed : "))
        if option == 11:
            break

        elif option == 1:
            Child_name = input("Enter sub role name : ")
            Parent_name = input("Enter reporting to role name : ")
            ROOT.AddSubRole(Parent_name, Child_name)

        elif option == 2:
            for role in ROOT:
                print(role, end=" ")
            print()

        elif option == 3:
            Child_name = input("Enter the role to be deleted : ")
            Parent_name = input("Enter the role to be transferred : ")
            ROOT.DeleteAndTransferRole(Child_name, Parent_name)

        elif option == 4:
            Username = input("Enter User name : ")
            Rolename = input("Enter Role : ")
            ROOT.AddUser(Username, Rolename)

        elif option == 5:
            for Username in ROOT.userMaps:
                print(Username, "-", ROOT.userMaps[Username])

        elif option == 6:
            for Username in ROOT.userMaps:
                print(Username, "-", end=" ")
                headRole = ROOT.userMaps[Username]
                for subrole in headRole:
                    if subrole == headRole:
                        continue
                    for users in subrole.userlist:
                        print(users, end=" ")
                print()

        elif option == 7:
            Username = input("Enter username to be deleted : ")
            ROOT.DeleteUser(Username)

        elif option == 8:
            Username = input("Enter the user name : ")
            levelRoles = [ROOT]
            height = 0
            found = False
            while len(levelRoles) != 0 and not found:
                newLevel = list()
                for role in levelRoles:
                    if Username in role.userlist:
                        found = True
                        break
                    newLevel.extend(role.child)
                else:
                    height += 1
                    levelRoles = newLevel
            if found:
                print(f"Number of users from top : {height}")
            else:
                print("Username not found")

        elif option == 9:
            levelRoles = [ROOT]
            height = 0
            while len(levelRoles) != 0:
                newLevel = list()
                for role in levelRoles:
                    newLevel.extend(role.child)
                height += 1
                levelRoles = newLevel
            print(f"height - {height}")

        elif option == 10:
            User1 = input("Enter First user  : ")
            User2 = input("Enter Second user  : ")
            boss = ROOT.CommonBoss(User1, User2)
            print("Top most common boss :", " ".join(boss))

    except Exception as e:
        print(f"Error: {e}")
