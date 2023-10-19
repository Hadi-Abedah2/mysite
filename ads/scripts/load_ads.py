import csv
from ads.models import Ad
from django.contrib.auth.models import User
filename = 'ads/scripts/data/ads.csv' 


def run():
    Ad.objects.filter(id__range=(7, 108)).delete() # I want to delete previously added records but not the ones I manually adeded
    with open(filename, 'r') as f:
        counter = 1
        user_1= User.objects.get(username='hadi')
        user_2= User.objects.get(username='fadi')
        user_3= User.objects.get(username='amjad')
        
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if counter % 3 == 0 and counter % 5 != 0:       # here i am making sure my three users alternate making 100 ads.
                 user = user_1
            elif counter % 5 == 0 and counter % 3 != 0:     # I should have used radndom.choice(iterable), I did this in the load_comment.py
                user = user_2
            else:
                user = user_3
            try:
                ad = Ad(
                    id = row[0],
                    title = row[1],
                    price = row[2],
                    text = row[3], 
                    owner = user,
                    #tags = row[4],
                    created_at = row[5], 
                    updated_at = row[6]
                )
                counter += 1
                ad.save()
                tag_to_add = [tag.strip() for tag in row[4].split(',')]
                ad.tags.add(*tag_to_add)
                
            except Exception as e:
                print(e)
