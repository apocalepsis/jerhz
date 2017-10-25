from lib import users

linux_user = users.model.linux.User("aflores","Passw0rd!","standard",8001,8001)
linux_user_dao = users.dao.linux.DAO()
result = linux_user_dao.find_by_attr("username",linux_user.username)
print(result)
