from .models import Task

def send_sms():
	Task.objects.raw()

send_sms()

crops = [
    {'id': 1, 'title': 'Shudgorlash', 'crop_choice_id': 1, 'task_id': 1, 'year': 2021, 'number': '201', 'farmer_id': 6, 'phone': '+998905567788', 'first_name': 'Sharif', 'last_name': 'Muratov'}, 
    {'id': 1, 'title': 'Yer Tekislash', 'crop_choice_id': 1, 'task_id': 2, 'year': 2021, 'number': '201', 'farmer_id': 6, 'phone': '+998905567788', 'first_name': 'Sharif', 'last_name': 'Muratov'},
    {'id': 1, 'title': 'Pushta olish', 'crop_choice_id': 1, 'task_id': 3, 'year': 2021, 'number': '201', 'farmer_id': 6, 'phone': '+998905567788', 'first_name': 'Sharif', 'last_name': 'Muratov'}, 
    {'id': 14, 'title': 'Shudgorlash', 'crop_choice_id': 1, 'task_id': 1, 'year': 2021, 'number': '205', 'farmer_id': 6, 'phone': '+998905567788', 'first_name': 'Sharif', 'last_name': 'Muratov'}, 
    {'id': 14, 'title': 'Yer Tekislash', 'crop_choice_id': 1, 'task_id': 2, 'year': 2021, 'number': '205', 'farmer_id': 6, 'phone': '+998905567788', 'first_name': 'Sharif', 'last_name': 'Muratov'}, 
    {'id': 14, 'title': 'Pushta olish', 'crop_choice_id': 1, 'task_id': 3, 'year': 2021, 'number': '205', 'farmer_id': 6, 'phone': '+998905567788', 'first_name': 'Sharif', 'last_name': 'Muratov'}, 
    {'id': 12, 'title': 'Shudgorlash', 'crop_choice_id': 1, 'task_id': 1, 'year': 2021, 'number': '203', 'farmer_id': 20, 'phone': '9898989898', 'first_name': 'John', 'last_name': 'Doe'}, 
    {'id': 12, 'title': 'Yer Tekislash', 'crop_choice_id': 1, 'task_id': 2, 'year': 2021, 'number': '203', 'farmer_id': 20, 'phone': '9898989898', 'first_name': 'John', 'last_name': 'Doe'}, 
    {'id': 12, 'title': 'Pushta olish', 'crop_choice_id': 1, 'task_id': 3, 'year': 2021, 'number': '203', 'farmer_id': 20, 'phone': '9898989898', 'first_name': 'John', 'last_name': 'Doe'}
    ]
farmers = set(x['farmer_id'] for x in crops)
print(farmers)
contours = [x for x in crops if x['farmer_id']==farmer]