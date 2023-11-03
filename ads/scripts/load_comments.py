import csv
import random
from datetime import timedelta
from ads.models import Ad, Comment
from django.contrib.auth import get_user_model
file_name = 'ads/scripts/data/comments.csv'

def random_ad():
    return random.choice(Ad.objects.all())

def random_user():
    return random.choice(get_user_model().objects.all())

def random_timedelta():
    return timedelta(days=random.randint(0,28))
def run():
    count = 0
    Comment.objects.all().delete()
    with open(file_name, 'r') as f:
        f_handle = csv.reader(f)
        next(f_handle)  # Skip the header row
        try:
            for row in f_handle:
                count += 1 
                if count == 60: break
                selected_ad = random_ad()
                selected_user = random_user()
                random_added_time = random_timedelta()
                comment = Comment(
                    text=row[1],
                    ad=selected_ad,
                    created_at=selected_ad.created_at + random_added_time, #this will not work because of the "auto_add_now"
                    owner = selected_user
                )
                comment.save()
                comment.created_at = selected_ad.created_at + random_added_time
                comment.save()
        except Exception as e:
            print(e)
