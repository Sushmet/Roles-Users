class MAIN_ROLES:

    def __init__(self, RObj):
        self.lst = [RObj]

    def __next__(self):
        if len(self.lst) == 0:
            raise StopIteration
        next = self.lst[0]
        self.lst.remove(next)
        self.lst.extend(next.child)
        return next


class ROLES_HIERARCHY:

    def __init__(self, name: str):

        self.name = name
        self.parent = None
        self.child = list()
        self.userlist = set()
        self.userMaps = dict()

    def __str__(self) -> str:
        return self.name

    def __iter__(self):
        return MAIN_ROLES(self)

    def findRoles(self, name: str):

        for role in self:
            if role.name == name:
                return role
        return None

    def AddSubRole(self, Parent_name: str, Child_name: str) -> None:

        parent = self.findRoles(Parent_name)
        child = self.findRoles(Child_name)
        if parent is None:
            raise ValueError(f"No role {Parent_name} found")
        if child is not None:
            raise ValueError(f"Role {Child_name} pre-exist")

        child = ROLES_HIERARCHY(Child_name)
        child.parent = parent
        child.userMaps = self.userMaps
        parent.child.append(child)

    def DeleteAndTransferRole(self, delete_name: str, transfer_name: str) -> None:

        if delete_name == transfer_name:
            raise ValueError("Deleting  role and transfer roles are same")

        transfer = self.findRoles(transfer_name)
        delRole = self.findRoles(delete_name)
        if transfer is None:
            raise ValueError(f"No role {transfer_name} found")
        if delRole is None:
            raise ValueError(f"No role {delete_name} found")
        if delRole.parent is None:
            raise ValueError(f"Cannot delete ROOT role {delete_name}")

        for role in delRole:
            if role == transfer:
                transfer = delRole.parent
                break

        delRole.parent.child.remove(delRole)
        transfer.child.extend(delRole.child)

        # update on usernames, transfer to new role
        for username in delRole.userlist:
            self.userMaps[username] = transfer
            transfer.userlist.add(username)

    def AddUser(self, Username: str, rolename: str):

        if Username in self.userMaps:
            raise ValueError(f"user {Username} cannot have more than one role")

        newrole = self.findRoles(rolename)
        if newrole is None:
            raise ValueError(f"No role {rolename} found")

        newrole.userlist.add(Username)
        self.userMaps[Username] = newrole

    def DeleteUser(self, Username: str):

        if Username not in self.userMaps:
            return
        role = self.userMaps[Username]
        if Username in role.userlist:
            role.userlist.remove(Username)
        del self.userMaps[Username]

    def CommonBoss(self, User1: str, User2: str) -> list:

        if User1 not in self.userMaps:
            raise ValueError(f"Username {User1} not found")
        if User2 not in self.userMaps:
            raise ValueError(f"Username {User2} not found")

        # top most common boss of any valid users is the user at root note
        root = self
        while root.parent is not None:
            root = root.parent
        if len(root.userlist) == 0:
            return [f'no users at role {root}']
        return root.userlist

        role1 = self.userMaps[User1]
        role1_route = list()
        while role1 is not None:
            role1_route.add(role1)
            role1 = role1.parent
        role1_route.reverse()

        # map role-2 to top
        role2 = self.userMaps[User2]
        role2_route = list()
        while role2 is not None:
            role2_route.add(role2)
            role2 = role2.parent
        role2_route.reverse()

        # find common points
        common = set(role1_route).intersection(set(role2_route))
        for TopCommon in role1_route:
            if TopCommon in common:
                if len(TopCommon.userlist) == 0:
                    return [f'no users at role {TopCommon}']
                return TopCommon.userlist
        return ['no common boss']
