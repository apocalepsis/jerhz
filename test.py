from lib import users
from lib import utils

linux_user_dao = users.dao.linux.DAO()

linux_user = users.model.linux.User("aflores","Passw0rd!","standard",8001,8001)
print(linux_user)

result = linux_user_dao.save(linux_user)
print(result)

result = linux_user_dao.find_by_attr("username",linux_user.username)
print(result)

result = linux_user_dao.delete_by_attr("username","aflores")
print(result)

result = linux_user_dao.find_by_attr("username",linux_user.username)
print(result)

result = linux_user_dao.all()
print(result)

for user in result["payload"]:
    print(user)
