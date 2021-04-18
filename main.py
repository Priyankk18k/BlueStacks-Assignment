import time
import json


class Admin:
    def __init__(self, user_name='priyank'):
        self.user_dict = self.read_json_file()
        self.main(user_name)

    def read_json_file(self):
        with open('user_data.txt') as json_file:
            data = json.load(json_file)
            print(data)
            return data

    def create_new_user(self, main_user_name):
        user_name = input("Please Enter the User Name of the New User").lower()
        if self.user_dict.get(user_name):
            out = input("User Already Exists. Do you Want to add a new role to the User Yes/No").lower()
            if out == 'yes':
                new_role = input("Enter the new Role of the User. Ex:- Admin/User").lower()
                if new_role in ['user', 'admin']:
                    self.user_dict[user_name]['role'] = new_role
            else:
                self.main(main_user_name)
        print("\n")
        role = input("Please Enter the Role of the new User").lower()
        resource = input("Please Enter the Resource To be attached with the User").lower()
        print("\n")
        if role == 'user':
            self.user_dict[user_name] = {'role': role, 'resource': [resource], 'action_type': ['read']}
            print("User Added")
            self.main(main_user_name)
        elif role == 'admin':
            self.user_dict[user_name] = {'role': role, 'resource': [resource],
                                         'action_type': ['read', 'update', 'delete', 'write']}
        else:
            print("Enter only user/admin for Role")
            time.sleep(3)
            self.create_new_user(main_user_name)

    def edit_role(self, main_user_name):
        role_list = ['user', 'admin']
        user_name = input("Enter the User name to edit the role").lower()
        if self.user_dict[user_name].get('role'):
            print("Current role is:-", self.user_dict[user_name]['role'])
            new_role = input("Enter the New role. Ex: User/admin").lower()
            if new_role in role_list:
                if self.user_dict.get(new_role + "_user"):
                    print("User Already Exists.")
                    self.main(main_user_name)
                elif new_role != self.user_dict[user_name]['role']:
                    self.user_dict[user_name]['role'] = new_role
                    self.main(main_user_name)

    def login_as_another_user(self, main_user_name):
        user_name = input("Enter the Existing User name:-")
        if self.user_dict.get(user_name):
            user_role = input("Enter the role of the user. Ex: User/Admin:-").lower()
            if user_role == 'user':
                if self.user_dict.get(user_name + "_user") is None:
                    # Here we can Also Log Everyone out and rerun the code Again.
                    print("\n")
                    print("User Does not Exist. Create New User, You are now loggin in as Admin name Priyank")
                    self.user_details(main_user_name)
                else:
                    user_name = user_name + "_user"
                    self.user_details(user_name)
            elif user_role == 'admin':
                self.main(user_name=user_name)
        else:
            print("User Does Not Exists. To Create User Login as an Admin")
            try:
              user = main_user_name.split("_")[-1]
              self.user_details(main_user_name)
            except:
              time.sleep(3)
              self.main(user_name=main_user_name)

    def access_resource(self, user_name):
        resource = self.user_dict[user_name]['resource']
        print("Your resource is:- ", resource)
        if self.user_dict[user_name]['role'] == 'admin':
            next_response = input(
                "Do you want to append Resource or delete the existing Resource? Append/Delete/Nothing") \
                .lower()
            if next_response in ['append', 'delete', 'nothing']:
                if next_response == 'append':
                    data = input("Enter What you want to add")
                    self.user_dict[user_name]['resource'].append(data)
                elif next_response == 'delete':
                    self.user_dict[user_name]['resource'] = []
                    print("Resource Deleted for user", user_name)
                elif next_response == 'nothing':
                    pass
            else:
                print("Please Enter only Append/Delete/Nothing")
                self.access_resource(user_name)
        else:
            print("You are only Authorized to view the resource")

    def outjson(self):
        print("runnnn")
        with open("user_data.txt", 'w') as f:
            json.dump(self.user_dict, f)

    def main(self, user_name):
        print("hi! you are logged in as admin ", user_name)
        print("\n")
        print("press 1 for login as another user:-")
        print("press 2 for create user:-")
        print("press 3 for edit role:-")
        print("press 4 for access resource")
        print("\n")
        try:
            entry = int(input("Enter your input here:-"))
        except ValueError:
            print("Please input integer only...")
            self.main(user_name)
        if entry == 1:
            self.login_as_another_user(user_name)
        elif entry == 2:
            self.create_new_user(user_name)
            self.outjson()
        elif entry == 3:
            self.edit_role(user_name)
            self.outjson()
        elif entry == 4:
            self.access_resource(user_name)
            self.outjson()
            self.main(user_name)
        else:
            print("Please Enter a Valid Input")
            self.main(user_name)



class User(Admin):
    def user_entry(self):
        try:
            entry = int(input("Enter your input here"))
        except ValueError:
            print("Please input integer only...")
            self.user_entry()
        return entry

    def user_option(self, user_input, user_name):
        if user_input == 1:
            self.login_as_another_user(user_name)
        elif user_input == 2:
            roles = self.user_dict[user_name]['role']
            print("Roles are", roles)
        elif user_input == 3:
            resource = self.user_dict[user_name]['resource']
            print("Your Resource is :- ", *resource, sep=",")
        else:
            print("Invalid Input")
        self.user_details(user_name)

    def user_details(self, user_name):
        print("hi! you are logged in as ", user_name)
        print("\n")
        print("press 1 for login as another user")
        print("press 2 for view roles")
        print("press 3 for access resource")
        print("\n")

        user_input = self.user_entry()
        self.user_option(user_input, user_name)


# You can also pass a User Name.


a = User()
