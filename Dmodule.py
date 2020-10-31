import requests
import sys
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://api.trello.com/1/members/me/boards"
query = {
   'key': '75c9c0ac0e8822a5906ad489506211ce',
   'token': 'dc73d5f482b5e6cf38d5a81744d2e273b3acfc1f84882bb5aa5692b1fcbcbd9c',
   # 'name': 'Made through API'
}


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




# Данные авторизации в API Trello  
auth_params = query
# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы.  
base_url = "https://api.trello.com/1/{}"  
def read():      
    # Получим данные всех колонок на доске:      
    # column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params,verify=False).json()      
    column_data = requests.request("GET", base_url.format('boards') + '/' + board_id + '/lists', params=auth_params,verify=False).json()      
    # print(column_data) 

    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:      
  
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params,verify=False).json() 
        if len(list(filter(lambda x : x['name']==column['name'], column_data)))>1:
        	print(column['name'],"id:" + column['id'], "tasks: ",len(task_data))
        else:
        	print(column['name'],"tasks: ",len(task_data))

        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'] + ', id: '+task['id'])  




def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params,verify=False).json()      
      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params},verify=False)
            break

def move(name, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params,verify=False).json()    
        

    task_id = None  
    taskss=[]
    repeated_tasks=[]
        
    for column in column_data:  
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params,verify=False).json()    
        for task in column_tasks: 
        	taskss.append((column['name'],column['id'],task['name'],task['id']))
    # print(taskss)
    repeated_tasks=list((filter(lambda x : x[2] == name, taskss)))
    if len(repeated_tasks)>1:
    	i=1
    	for task in repeated_tasks:
     		print(i, name, " Из колонки ", task[0])
     		i=i+1

    	chosen_task = int(input("Конкретизируйте задачу. Введите номер позиции из списка выше: "))-1

    	# print(repeated_tasks[chosen_task][3])
    	task_id = repeated_tasks[chosen_task][3]

    else:
    	task_id = repeated_tasks[0][3]

 
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params},verify=False)    
            break    


def newlist(list_name):
	requests.post(base_url.format('lists'), data={'name': list_name, 'idBoard': board_id, **auth_params},verify=False)

def start():
	mode = input("Выбери режим.\n1 - Вывести текущие списки и задания \n2 - Создать новую задачу\n3 - Переместить задачу\n4 - Создать новый список\n")
	if mode == "1":
		read()
	elif mode == "2":
		create_name = input("Введите наименование задачи: ")
		create_column_name = input("Введите наименование карточки для вставки: ")
		create(create_name, create_column_name)
	elif mode == "3":
		move_name= input("Введите наименование задачи: ")
		move_column_name = input("Введите наименование карточки для вставки: ")
		move(move_name, move_column_name)
	elif mode == "4":
		newlist_name= input("Введите наименование карточки: ")
		newlist(newlist_name)
	elif mode == "5":
		check("Additional Card")
	else:
		start()


if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        start()  
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3])  
    elif sys.argv[1] == 'newlist':    
        newlist(sys.argv[2])
