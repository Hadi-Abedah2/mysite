import csv
from ads.models import Ad
from django.contrib.auth import get_user_model
from django.utils import timezone

import random
from datetime import timedelta, datetime

filename = "ads/scripts/data/ads_ad_2.csv"


all_users = list(get_user_model().objects.all())


def random_user():
    return random.choice(all_users)


def run():
    with open(filename, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            user = random_user()
            created_at = datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S")
            try:
                ad = Ad(
                    title=row[0],
                    price=float(row[1]),
                    text=row[2],
                    owner=user,
                    created_at=created_at,
                )
                ad.save()
                tag_to_add = ["movies", "demo"]
                ad.tags.add(*tag_to_add)
                #updating the created_at field here 
                ad.created_at = created_at
                ad.save()

            except Exception as e:
                print(e)
