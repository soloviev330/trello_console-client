import requests
import json
# r =  requests.get('https://api.trello.com/1/members/me/boards?key=75c9c0ac0e8822a5906ad489506211ce&token=dc73d5f482b5e6cf38d5a81744d2e273b3acfc1f84882bb5aa5692b1fcbcbd9c', verify=False)
# print(r)
# new_board =  requests.post('https://api.trello.com/1/members/me/boards?key=75c9c0ac0e8822a5906ad489506211ce&token=dc73d5f482b5e6cf38d5a81744d2e273b3acfc1f84882bb5aa5692b1fcbcbd9c', verify=False)
# 

url = "https://api.trello.com/1/members/me/boards"
query = {
   'key': '75c9c0ac0e8822a5906ad489506211ce',
   'token': 'dc73d5f482b5e6cf38d5a81744d2e273b3acfc1f84882bb5aa5692b1fcbcbd9c',
   'name': 'Made through API'
}
# response = requests.request(
#    "POST",
#    url,
#    params=query,
#    verify=False
# )

headers = {
   "Accept": "application/json"
}
response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query,
   verify=False
)
board_id=json.loads(response.text)[1]["id"]


print(board_id)
print(json.loads(response.text)[1]["id"])






def lists_ids_on_board (id):
	url = "https://api.trello.com/1/boards/"+id+"/lists"
	response = requests.request(
	   "GET",
	   url,
	   params=query,
	   verify=False
	)
	lists={}
	for name in json.loads(response.text):
		lists[name["name"]]=name["id"]

	return (lists)

def lists_names_on_board (board_id):
	lists=[]
	for key,value in lists_ids_on_board(board_id).items():
		lists.append(key)

	return (lists)



# print(json.loads(get_list_on_board (query,board_id))[0]["name"])
# lists=[]
# for name in json.loads(get_list_on_board (query,board_id)):
# 	lists.append(name["name"])
# print(lists)
# print(type(json.loads(get_list_on_board (query,board_id))))

lists_id_on_board=lists_ids_on_board(board_id)

print(lists_names_on_board(board_id))

print(lists_id_on_board["To Do"])

def cards_on_list (name):
	id=lists_ids_on_board (board_id)[name]

	url = "https://api.trello.com/1/lists/"+id+"/cards"
	response = requests.request(
	   "GET",
	   url,
	   params=query,
	   verify=False
	)

	return(response.text)

print(cards_on_list("To Do"))




# print(lists_ids_on_board(board_id).get('To Do'))

# Данные авторизации в API Trello  
auth_params = query
# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}"  
def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params,verify=False).json()      
      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
        print(column['name'])    
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params,verify=False).json()      
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'])  

if __name__ == "__main__":    
    read()  