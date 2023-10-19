import csv  
import random 
from datetime import timedelta
from ads.models import Ad, Comment
from django.contrib.auth.models import User 
file_name = 'ads/scripts/data/comments.csv'

def random_ad():
    return random.choice(Ad.objects.all())

def random_user():
    return random.choice(User.objects.all())

def random_timedelta(): 
    return timedelta(days=random.randint(1, 5), hours=random.randint(0, 24), minutes=random.randint(0, 60))

def run():
    with open(file_name, 'r') as f:
        f_handle = csv.reader(f)
        next(f_handle)  # Skip the header row
        try:
            for row in f_handle:
                selected_ad = random_ad()
                selected_user = random_user()
                comment = Comment(
                    text=row[1],
                    ad=selected_ad,
                    created_at=selected_ad.created_at + random_timedelta(),
                    owner = selected_user
                )
                comment.save()
        except Exception as e:
            print(e)
